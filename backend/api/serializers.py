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

    class Meta:
        model = Question
        fields = ('id', 'title', 'description', 'order', 'is_completed')

    def get_is_completed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserProgress.objects.filter(
                user=request.user,
                question=obj,
                completed=True
            ).exists()
        return False


class QuestionDetailSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()
    topic_title = serializers.CharField(source='topic.title', read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'title', 'description', 'expected_output', 'order', 'is_completed', 'topic_title', 'topic')

    def get_is_completed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserProgress.objects.filter(
                user=request.user,
                question=obj,
                completed=True
            ).exists()
        return False


class TopicSerializer(serializers.ModelSerializer):
    is_unlocked = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()
    questions_count = serializers.SerializerMethodField()
    completed_count = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ('id', 'title', 'description', 'order', 'is_unlocked', 'is_completed', 'questions_count', 'completed_count')

    def get_is_unlocked(self, obj):
        # All topics are always unlocked
        return True

    def get_is_completed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Check if all questions are completed
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
        # All topics are always unlocked
        return True

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