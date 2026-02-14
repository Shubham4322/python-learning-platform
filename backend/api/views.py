from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.utils import timezone
import subprocess
import tempfile
import os
import re

from .models import Topic, Question, UserProgress, TopicProgress
from .serializers import (
    UserRegisterSerializer,
    UserSerializer,
    TopicSerializer,
    TopicDetailSerializer,
    QuestionDetailSerializer,
)


def normalize_output(text):
    """Normalize output for comparison"""
    if text is None:
        return ""
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def check_required_keywords(code, required_keywords):
    """
    Check if code contains required keywords.
    Returns (is_valid, missing_keywords)
    """
    if not required_keywords or required_keywords.strip() == '':
        return True, []
    
    keywords = [k.strip().lower() for k in required_keywords.split(',') if k.strip()]
    code_lower = code.lower()
    
    missing = []
    for keyword in keywords:
        if keyword not in code_lower:
            missing.append(keyword)
    
    return len(missing) == 0, missing


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        first_topic = Topic.objects.order_by('order').first()
        if first_topic:
            TopicProgress.objects.get_or_create(
                user=user,
                topic=first_topic,
                defaults={'is_unlocked': True, 'is_completed': False}
            )
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Registration successful',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard(request):
    user = request.user
    
    first_topic = Topic.objects.order_by('order').first()
    if first_topic:
        progress, created = TopicProgress.objects.get_or_create(
            user=user,
            topic=first_topic,
            defaults={'is_unlocked': True, 'is_completed': False}
        )
        if not progress.is_unlocked:
            progress.is_unlocked = True
            progress.save()
    
    total_topics = Topic.objects.count()
    completed_topics = 0
    
    for topic in Topic.objects.all():
        total_q = topic.questions.count()
        if total_q > 0:
            completed_q = UserProgress.objects.filter(
                user=user,
                question__topic=topic,
                completed=True
            ).count()
            if completed_q >= total_q:
                completed_topics += 1
    
    total_questions = Question.objects.count()
    completed_questions = UserProgress.objects.filter(
        user=user,
        completed=True
    ).count()
    
    topics = Topic.objects.all().order_by('order')
    topics_serializer = TopicSerializer(topics, many=True, context={'request': request})
    
    return Response({
        'user': UserSerializer(user).data,
        'progress': {
            'total_topics': total_topics,
            'completed_topics': completed_topics,
            'total_questions': total_questions,
            'completed_questions': completed_questions,
        },
        'topics': topics_serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_topics(request):
    first_topic = Topic.objects.order_by('order').first()
    if first_topic:
        progress, created = TopicProgress.objects.get_or_create(
            user=request.user,
            topic=first_topic,
            defaults={'is_unlocked': True, 'is_completed': False}
        )
        if not progress.is_unlocked:
            progress.is_unlocked = True
            progress.save()
    
    topics = Topic.objects.all().order_by('order')
    serializer = TopicSerializer(topics, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_topic(request, topic_id):
    try:
        topic = Topic.objects.get(id=topic_id)
    except Topic.DoesNotExist:
        return Response({'error': 'Topic not found'}, status=status.HTTP_404_NOT_FOUND)
    
    first_topic = Topic.objects.order_by('order').first()
    
    if first_topic and topic.id != first_topic.id:
        is_unlocked = TopicProgress.objects.filter(
            user=request.user,
            topic=topic,
            is_unlocked=True
        ).exists()
        
        if not is_unlocked:
            return Response(
                {'error': 'Topic is locked. Complete previous topics first.'},
                status=status.HTTP_403_FORBIDDEN
            )
    
    serializer = TopicDetailSerializer(topic, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_question(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)
    
    topic = question.topic
    first_topic = Topic.objects.order_by('order').first()
    
    if first_topic and topic.id != first_topic.id:
        is_unlocked = TopicProgress.objects.filter(
            user=request.user,
            topic=topic,
            is_unlocked=True
        ).exists()
        
        if not is_unlocked:
            return Response(
                {'error': 'Topic is locked. Complete previous topics first.'},
                status=status.HTTP_403_FORBIDDEN
            )
    
    serializer = QuestionDetailSerializer(question, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def run_code(request):
    code = request.data.get('code', '')
    
    if not code.strip():
        return Response({'error': 'No code provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(code)
            temp_file = f.name
        
        result = subprocess.run(
            ['python', temp_file],
            capture_output=True,
            text=True,
            timeout=5,
            encoding='utf-8'
        )
        
        os.unlink(temp_file)
        
        if result.returncode == 0:
            return Response({'output': result.stdout, 'error': None})
        else:
            return Response({'output': None, 'error': result.stderr})
            
    except subprocess.TimeoutExpired:
        os.unlink(temp_file)
        return Response({'output': None, 'error': 'Code execution timed out (max 5 seconds)'})
    except Exception as e:
        return Response({'output': None, 'error': str(e)})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_code(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)
    
    code = request.data.get('code', '')
    
    if not code.strip():
        return Response({'error': 'No code provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Get or create user progress to track attempts
    user_progress, created = UserProgress.objects.get_or_create(
        user=request.user,
        question=question
    )
    
    # Increment attempts
    user_progress.attempts += 1
    user_progress.submitted_code = code  # Save code regardless of result
    user_progress.save()
    
    # Check required keywords (anti-cheating)
    is_valid, missing_keywords = check_required_keywords(code, question.required_keywords)
    
    if not is_valid:
        return Response({
            'passed': False,
            'output': None,
            'expected': question.expected_output,
            'message': f'Your code must use: {", ".join(missing_keywords)}',
            'missing_keywords': missing_keywords,
            'attempts': user_progress.attempts
        })
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(code)
            temp_file = f.name
        
        result = subprocess.run(
            ['python', temp_file],
            capture_output=True,
            text=True,
            timeout=5,
            encoding='utf-8'
        )
        
        os.unlink(temp_file)
        
        if result.returncode != 0:
            return Response({
                'passed': False,
                'output': result.stderr,
                'expected': question.expected_output,
                'message': 'Code has errors',
                'attempts': user_progress.attempts
            })
        
        actual_output = normalize_output(result.stdout)
        expected_output = normalize_output(question.expected_output)
        passed = actual_output == expected_output
        
        topic_completed = False
        next_topic_unlocked = False
        next_topic_name = None
        
        if passed:
            user_progress.completed = True
            user_progress.completed_at = timezone.now()
            user_progress.save()
            
            topic = question.topic
            total_questions = topic.questions.count()
            completed_questions = UserProgress.objects.filter(
                user=request.user,
                question__topic=topic,
                completed=True
            ).count()
            
            if completed_questions >= total_questions:
                topic_progress, created = TopicProgress.objects.get_or_create(
                    user=request.user,
                    topic=topic
                )
                topic_progress.is_completed = True
                topic_progress.is_unlocked = True
                topic_progress.save()
                topic_completed = True
                
                next_topic = Topic.objects.filter(order__gt=topic.order).order_by('order').first()
                if next_topic:
                    next_progress, created = TopicProgress.objects.get_or_create(
                        user=request.user,
                        topic=next_topic
                    )
                    next_progress.is_unlocked = True
                    next_progress.save()
                    next_topic_unlocked = True
                    next_topic_name = next_topic.title
        
        return Response({
            'passed': passed,
            'output': actual_output,
            'expected': expected_output,
            'message': 'Correct! Well done!' if passed else 'Output does not match expected result',
            'topic_completed': topic_completed,
            'next_topic_unlocked': next_topic_unlocked,
            'next_topic_name': next_topic_name,
            'attempts': user_progress.attempts
        })
        
    except subprocess.TimeoutExpired:
        os.unlink(temp_file)
        return Response({
            'passed': False,
            'output': None,
            'expected': question.expected_output,
            'message': 'Code execution timed out',
            'attempts': user_progress.attempts
        })
    except Exception as e:
        return Response({
            'passed': False,
            'output': None,
            'expected': question.expected_output,
            'message': str(e),
            'attempts': user_progress.attempts
        })