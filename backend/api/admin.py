from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import Topic, Question, UserProgress, TopicProgress


# Customize the admin site header
admin.site.site_header = "PyLearn Administration"
admin.site.site_title = "PyLearn Admin"
admin.site.index_title = "Welcome to PyLearn Admin Panel"


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'order', 'questions_count', 'created_at')
    list_display_links = ('id', 'title')
    list_editable = ('order',)
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    ordering = ('order',)
    readonly_fields = ('created_at', 'theory_preview')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'order')
        }),
        ('Theory Content', {
            'fields': ('theory',),
            'classes': ('wide',),
            'description': 'Use the editor to format your theory content with headings, lists, bold text, etc.'
        }),
        ('Preview', {
            'fields': ('theory_preview',),
            'classes': ('collapse',),
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def questions_count(self, obj):
        count = obj.questions.count()
        return format_html('<b>{}</b>', count)
    questions_count.short_description = 'Questions'
    
    def theory_preview(self, obj):
        if obj.theory:
            return format_html('<div style="background:#f5f5f5; padding:15px; border-radius:5px;">{}</div>', obj.theory)
        return "No content"
    theory_preview.short_description = 'Theory Preview'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'topic', 'order', 'created_at')
    list_display_links = ('id', 'title')
    list_editable = ('order',)
    list_filter = ('topic', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('topic', 'order')
    readonly_fields = ('created_at', 'description_preview')
    autocomplete_fields = ('topic',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('topic', 'title', 'order')
        }),
        ('Question Description', {
            'fields': ('description',),
            'classes': ('wide',),
            'description': 'Use the editor to format the question with examples, code snippets, etc.'
        }),
        ('Expected Output', {
            'fields': ('expected_output',),
            'classes': ('wide',),
            'description': 'Enter the exact output the user\'s code should produce. No formatting - plain text only.'
        }),
        ('Preview', {
            'fields': ('description_preview',),
            'classes': ('collapse',),
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def description_preview(self, obj):
        if obj.description:
            return format_html('<div style="background:#f5f5f5; padding:15px; border-radius:5px;">{}</div>', obj.description)
        return "No content"
    description_preview.short_description = 'Description Preview'


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question', 'completed_status', 'completed_at')
    list_display_links = ('id', 'user')
    list_filter = ('completed', 'completed_at', 'user')
    search_fields = ('user__username', 'question__title')
    ordering = ('-completed_at',)
    readonly_fields = ('completed_at',)
    autocomplete_fields = ('user', 'question')
    
    def completed_status(self, obj):
        if obj.completed:
            return format_html('<span style="color:green; font-weight:bold;">✓ Completed</span>')
        return format_html('<span style="color:orange;">Pending</span>')
    completed_status.short_description = 'Status'


@admin.register(TopicProgress)
class TopicProgressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'topic', 'unlocked_status', 'completed_status')
    list_display_links = ('id', 'user')
    list_filter = ('is_unlocked', 'is_completed', 'user', 'topic')
    search_fields = ('user__username', 'topic__title')
    ordering = ('user', 'topic__order')
    autocomplete_fields = ('user', 'topic')
    
    def unlocked_status(self, obj):
        if obj.is_unlocked:
            return format_html('<span style="color:green;">🔓 Unlocked</span>')
        return format_html('<span style="color:red;">🔒 Locked</span>')
    unlocked_status.short_description = 'Unlocked'
    
    def completed_status(self, obj):
        if obj.is_completed:
            return format_html('<span style="color:green; font-weight:bold;">✓ Completed</span>')
        return format_html('<span style="color:orange;">In Progress</span>')
    completed_status.short_description = 'Completed'


# Customize User Admin for autocomplete
class CustomUserAdmin(UserAdmin):
    search_fields = ('username', 'email', 'first_name', 'last_name')


# Re-register User with custom admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)