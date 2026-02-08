from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django_summernote.admin import SummernoteModelAdmin
from .models import Topic, Question, UserProgress, TopicProgress


admin.site.site_header = "PyLearn Administration"
admin.site.site_title = "PyLearn Admin"
admin.site.index_title = "Welcome to PyLearn Admin Panel"


@admin.register(Topic)
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


@admin.register(Question)
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
            'classes': ('collapse',),
            'description': 'Set required keywords to prevent direct print cheating'
        }),
    )
    
    def has_keywords(self, obj):
        return bool(obj.required_keywords)
    has_keywords.short_description = 'Has Keywords'
    has_keywords.boolean = True


@admin.register(UserProgress)
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
            'classes': ('collapse',),
        }),
    )


@admin.register(TopicProgress)
class TopicProgressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'topic', 'is_unlocked', 'is_completed')
    list_filter = ('is_unlocked', 'is_completed', 'user')


class CustomUserAdmin(UserAdmin):
    search_fields = ('username', 'email')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)