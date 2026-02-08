from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    theory = models.TextField(help_text="Theory content for this topic")
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Question(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=200)
    description = models.TextField()
    expected_output = models.TextField()
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # NEW: Required keywords to prevent cheating
    required_keywords = models.CharField(
        max_length=500, 
        blank=True,
        help_text="Comma-separated keywords required in code (e.g., for,range,print)"
    )
    
    # NEW: Hint for required keywords
    hint = models.CharField(
        max_length=500,
        blank=True,
        help_text="Hint to show user about what to use (e.g., 'Use a for loop')"
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.topic.title} - {self.title}"


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # NEW: Save user's submitted code
    submitted_code = models.TextField(blank=True, default='')
    
    # NEW: Track attempts
    attempts = models.IntegerField(default=0)

    class Meta:
        unique_together = ['user', 'question']

    def __str__(self):
        return f"{self.user.username} - {self.question.title}"


class TopicProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topic_progress')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    is_unlocked = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'topic']

    def __str__(self):
        return f"{self.user.username} - {self.topic.title}"