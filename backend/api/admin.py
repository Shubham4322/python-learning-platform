from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django_summernote.admin import SummernoteModelAdmin
from .models import Topic, Question, UserProgress, TopicProgress
from .admin_site import pylearn_admin_site

# Use custom admin site (fixes login redirect 404)
site = pylearn_admin_site
site.site_header = "PyLearn Administration"
site.site_title = "PyLearn Admin"
site.index_title = "Welcome to PyLearn Admin Panel"


@site.register(Topic)
class TopicAdmin(SummernoteModelAdmin):
    summernote_fields = ('theory',)
    list_display = ('id', 'title', 'order', 'questions_count', 'created_at')
    list_display_links = ('id', 'title')
    list_editable = ('order',)
    search_fields = ('title', 'description')
    ordering = ('order',)
    
    def questions_count(self, obj):
        return obj.questions.count()
    questions_count.short_description = 'Questions'


@site.register(Question)
class QuestionAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_display = ('id', 'title', 'topic', 'order', 'has_keywords', 'created_at')
    list_display_links = ('id', 'title')
    list_editable = ('order',)
    list_filter = ('topic',)
    search_fields = ('title', 'description')
    ordering = ('topic', 'order')
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('topic', 'title', 'order')
        }),
        ('Question Content', {
            'fields': ('description', 'expected_output')
        }),
        ('Anti-Cheating (Optional)', {
            'fields': ('required_keywords', 'hint'),
            'description': 'Set required keywords to prevent direct print cheating'
        }),
    )
    
    def has_keywords(self, obj):
        return bool(obj.required_keywords)
    has_keywords.short_description = 'Has Keywords'
    has_keywords.boolean = True


@site.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question', 'completed', 'attempts', 'completed_at')
    list_filter = ('completed', 'user')
    search_fields = ('user__username', 'question__title')
    readonly_fields = ('submitted_code',)
    
    fieldsets = (
        ('Progress Info', {
            'fields': ('user', 'question', 'completed', 'attempts', 'completed_at')
        }),
        ('Submitted Code', {
            'fields': ('submitted_code',),
        }),
    )


@site.register(TopicProgress)
class TopicProgressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'topic', 'is_unlocked', 'is_completed')
    list_filter = ('is_unlocked', 'is_completed', 'user')


class CustomUserAdmin(UserAdmin):
    search_fields = ('username', 'email')


# User model is registered on default admin by auth; register on our site
from django.contrib.auth import get_user_model
UserModel = get_user_model()
if admin.site.is_registered(UserModel):
    admin.site.unregister(UserModel)
site.register(UserModel, CustomUserAdmin)