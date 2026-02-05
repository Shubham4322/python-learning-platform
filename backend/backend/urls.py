from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def home(request):
    return JsonResponse({
        'message': 'Python Learning Platform API',
        'endpoints': {
            'admin': '/admin/',
            'api': '/api/',
        }
    })


urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('summernote/', include('django_summernote.urls')),
]