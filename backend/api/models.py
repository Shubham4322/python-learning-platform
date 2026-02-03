from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Topic(models.Model):
    """
    Represents a learning topic like 'Variables', 'Loops', etc.
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    theory = RichTextField(config_name='theory', help_text="Theory content for this topic")
    order = models.IntegerField(default=0, help_text="Order in which topics appear")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Question(models.Model):
    """
    Represents a coding question under a topic.
    """
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=200)
    description = RichTextField(config_name='default', help_text="Question description")
    expected_output = models.TextField(help_text="Expected output to check against")
    order = models.IntegerField(default=0, help_text="Order of question in topic")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.topic.title} - {self.title}"


class UserProgress(models.Model):
    """
    Tracks which questions a user has completed.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'question']

    def __str__(self):
        return f"{self.user.username} - {self.question.title}"


class TopicProgress(models.Model):
    """
    Tracks which topics a user has unlocked/completed.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topic_progress')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    is_unlocked = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'topic']

    def __str__(self):
        return f"{self.user.username} - {self.topic.title}"