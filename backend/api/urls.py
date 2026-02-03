from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # Auth endpoints
    path('auth/register/', views.register, name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/user/', views.get_user, name='get_user'),
    
    # Dashboard
    path('dashboard/', views.get_dashboard, name='dashboard'),
    
    # Topics
    path('topics/', views.get_topics, name='topics'),
    path('topics/<int:topic_id>/', views.get_topic, name='topic_detail'),
    
    # Questions
    path('questions/<int:question_id>/', views.get_question, name='question_detail'),
    
    # Code execution
    path('run-code/', views.run_code, name='run_code'),
    path('submit/<int:question_id>/', views.submit_code, name='submit_code'),
]