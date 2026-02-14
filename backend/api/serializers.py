from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Topic, Question, UserProgress, TopicProgress


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class QuestionSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()
    submitted_code = serializers.SerializerMethodField()
    attempts = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ('id', 'title', 'description', 'order', 'is_completed', 'submitted_code', 'attempts', 'hint')

    def get_is_completed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserProgress.objects.filter(
                user=request.user,
                question=obj,
                completed=True
            ).exists()
        return False

    def get_submitted_code(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            progress = UserProgress.objects.filter(
                user=request.user,
                question=obj
            ).first()
            return progress.submitted_code if progress else ''
        return ''

    def get_attempts(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            progress = UserProgress.objects.filter(
                user=request.user,
                question=obj
            ).first()
            return progress.attempts if progress else 0
        return 0


class QuestionDetailSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()
    topic_title = serializers.CharField(source='topic.title', read_only=True)
    submitted_code = serializers.SerializerMethodField()
    attempts = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ('id', 'title', 'description', 'expected_output', 'order', 
                  'is_completed', 'topic_title', 'topic', 'submitted_code', 
                  'attempts', 'hint', 'required_keywords')

    def get_is_completed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserProgress.objects.filter(
                user=request.user,
                question=obj,
                completed=True
            ).exists()
        return False

    def get_submitted_code(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            progress = UserProgress.objects.filter(
                user=request.user,
                question=obj
            ).first()
            return progress.submitted_code if progress else ''
        return ''

    def get_attempts(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            progress = UserProgress.objects.filter(
                user=request.user,
                question=obj
            ).first()
            return progress.attempts if progress else 0
        return 0


class TopicSerializer(serializers.ModelSerializer):
    is_unlocked = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()
    questions_count = serializers.SerializerMethodField()
    completed_count = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ('id', 'title', 'description', 'order', 'is_unlocked', 'is_completed', 'questions_count', 'completed_count')

    def get_is_unlocked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            first_topic = Topic.objects.order_by('order').first()
            if first_topic and obj.id == first_topic.id:
                return True
            
            progress = TopicProgress.objects.filter(
                user=request.user,
                topic=obj,
                is_unlocked=True
            ).exists()
            return progress
        
        first_topic = Topic.objects.order_by('order').first()
        return obj.id == first_topic.id if first_topic else False

    def get_is_completed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            total = obj.questions.count()
            if total == 0:
                return False
            completed = UserProgress.objects.filter(
                user=request.user,
                question__topic=obj,
                completed=True
            ).count()
            return completed >= total
        return False

    def get_questions_count(self, obj):
        return obj.questions.count()

    def get_completed_count(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserProgress.objects.filter(
                user=request.user,
                question__topic=obj,
                completed=True
            ).count()
        return 0


class TopicDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    is_unlocked = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ('id', 'title', 'description', 'theory', 'order', 'questions', 'is_unlocked', 'is_completed')

    def get_is_unlocked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            first_topic = Topic.objects.order_by('order').first()
            if first_topic and obj.id == first_topic.id:
                return True
            
            progress = TopicProgress.objects.filter(
                user=request.user,
                topic=obj,
                is_unlocked=True
            ).exists()
            return progress
        return False

    def get_is_completed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            total = obj.questions.count()
            if total == 0:
                return False
            completed = UserProgress.objects.filter(
                user=request.user,
                question__topic=obj,
                completed=True
            ).count()
            return completed >= total
        return False