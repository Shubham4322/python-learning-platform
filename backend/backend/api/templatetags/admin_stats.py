from django import template
from api.models import Topic, Question, UserProgress
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag
def get_total_topics():
    return Topic.objects.count()

@register.simple_tag
def get_total_questions():
    return Question.objects.count()

@register.simple_tag
def get_total_users():
    return User.objects.count()

@register.simple_tag
def get_completed_progress():
    return UserProgress.objects.filter(completed=True).count()