"""
URL configuration for backend project.
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static


def home(request):
    return JsonResponse({
        'message': 'Python Learning Platform API',
        'endpoints': {
            'admin': '/admin/',
            'api': '/api/',
            'ckeditor': '/ckeditor/',
        }
    })


urlpatterns = [
    path('', home, name='home'),            # Root URL
    path('admin/', admin.site.urls),        # Admin
    path('api/', include('api.urls')),      # API
    path('ckeditor/', include('ckeditor_uploader.urls')),  # ✅ CKEditor
]

# ✅ Media serving (needed for CKEditor uploads)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
