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

from .models import Topic, Question, UserProgress, TopicProgress
from .serializers import (
    UserRegisterSerializer,
    UserSerializer,
    TopicSerializer,
    TopicDetailSerializer,
    QuestionDetailSerializer,
)


# ==================== AUTH VIEWS ====================

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Register a new user.
    """
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Create tokens for immediate login
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
    """
    Get current logged in user details.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard(request):
    """
    Get dashboard data for logged in user.
    """
    user = request.user
    
    # Get total topics and completed topics
    total_topics = Topic.objects.count()
    completed_topics = TopicProgress.objects.filter(
        user=user,
        is_completed=True
    ).count()
    
    # Get total questions and completed questions
    total_questions = Question.objects.count()
    completed_questions = UserProgress.objects.filter(
        user=user,
        completed=True
    ).count()
    
    # Get all topics with progress
    topics = Topic.objects.all()
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


# ==================== TOPIC VIEWS ====================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_topics(request):
    """
    Get all topics with progress info.
    """
    topics = Topic.objects.all()
    serializer = TopicSerializer(topics, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_topic(request, topic_id):
    """
    Get single topic with questions.
    """
    try:
        topic = Topic.objects.get(id=topic_id)
    except Topic.DoesNotExist:
        return Response(
            {'error': 'Topic not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Check if topic is unlocked
    if topic.order != 1:
        progress = TopicProgress.objects.filter(
            user=request.user,
            topic=topic
        ).first()
        if not progress or not progress.is_unlocked:
            return Response(
                {'error': 'Topic is locked'},
                status=status.HTTP_403_FORBIDDEN
            )
    
    serializer = TopicDetailSerializer(topic, context={'request': request})
    return Response(serializer.data)


# ==================== QUESTION VIEWS ====================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_question(request, question_id):
    """
    Get single question details.
    """
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return Response(
            {'error': 'Question not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Check if topic is unlocked
    topic = question.topic
    if topic.order != 1:
        progress = TopicProgress.objects.filter(
            user=request.user,
            topic=topic
        ).first()
        if not progress or not progress.is_unlocked:
            return Response(
                {'error': 'Topic is locked'},
                status=status.HTTP_403_FORBIDDEN
            )
    
    serializer = QuestionDetailSerializer(question, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def run_code(request):
    """
    Run Python code and return output.
    """
    code = request.data.get('code', '')
    
    if not code.strip():
        return Response(
            {'error': 'No code provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Create temporary file to run code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        # Run the code with timeout
        result = subprocess.run(
            ['python', temp_file],
            capture_output=True,
            text=True,
            timeout=5  # 5 second timeout
        )
        
        # Clean up temp file
        os.unlink(temp_file)
        
        if result.returncode == 0:
            return Response({
                'output': result.stdout,
                'error': None
            })
        else:
            return Response({
                'output': None,
                'error': result.stderr
            })
            
    except subprocess.TimeoutExpired:
        os.unlink(temp_file)
        return Response({
            'output': None,
            'error': 'Code execution timed out (max 5 seconds)'
        })
    except Exception as e:
        return Response({
            'output': None,
            'error': str(e)
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_code(request, question_id):
    """
    Submit code for a question and check if output matches.
    """
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return Response(
            {'error': 'Question not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    code = request.data.get('code', '')
    
    if not code.strip():
        return Response(
            {'error': 'No code provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Create temporary file to run code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        # Run the code
        result = subprocess.run(
            ['python', temp_file],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        # Clean up
        os.unlink(temp_file)
        
        if result.returncode != 0:
            return Response({
                'passed': False,
                'output': result.stderr,
                'expected': question.expected_output,
                'message': 'Code has errors'
            })
        
        # Compare output with expected
        actual_output = result.stdout.strip()
        expected_output = question.expected_output.strip()
        
        passed = actual_output == expected_output
        
        if passed:
            # Mark question as completed
            user_progress, created = UserProgress.objects.get_or_create(
                user=request.user,
                question=question
            )
            user_progress.completed = True
            user_progress.completed_at = timezone.now()
            user_progress.save()
            
            # Check if all questions in topic are completed
            topic = question.topic
            total_questions = topic.questions.count()
            completed_questions = UserProgress.objects.filter(
                user=request.user,
                question__topic=topic,
                completed=True
            ).count()
            
            if completed_questions >= total_questions:
                # Mark topic as completed
                topic_progress, created = TopicProgress.objects.get_or_create(
                    user=request.user,
                    topic=topic
                )
                topic_progress.is_completed = True
                topic_progress.is_unlocked = True
                topic_progress.save()
                
                # Unlock next topic
                next_topic = Topic.objects.filter(order=topic.order + 1).first()
                if next_topic:
                    next_progress, created = TopicProgress.objects.get_or_create(
                        user=request.user,
                        topic=next_topic
                    )
                    next_progress.is_unlocked = True
                    next_progress.save()
        
        return Response({
            'passed': passed,
            'output': actual_output,
            'expected': expected_output,
            'message': 'Correct! Well done!' if passed else 'Output does not match expected result'
        })
        
    except subprocess.TimeoutExpired:
        os.unlink(temp_file)
        return Response({
            'passed': False,
            'output': None,
            'expected': question.expected_output,
            'message': 'Code execution timed out'
        })
    except Exception as e:
        return Response({
            'passed': False,
            'output': None,
            'expected': question.expected_output,
            'message': str(e)
        })