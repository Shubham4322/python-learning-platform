from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import logout


def home(request):
    return JsonResponse({
        'message': 'Python Learning Platform API',
        'endpoints': {
            'admin': '/admin/',
            'api': '/api/',
        }
    })


def admin_logout_view(request):
    """Log out and redirect to admin login (for admin panel logout button)."""
    logout(request)
    # Redirect to admin login page
    from django.urls import reverse
    return redirect(reverse('admin:login'))


# Handler for Django admin redirect after login
def admin_login_redirect(request):
    """Redirect to admin after login."""
    from django.shortcuts import redirect
    return redirect('/admin/')

urlpatterns = [
    path('', home, name='home'),
    path('accounts/profile/', admin_login_redirect),  # Fix admin redirect
    path('admin-logout/', admin_logout_view, name='admin_logout'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('summernote/', include('django_summernote.urls')),
]
