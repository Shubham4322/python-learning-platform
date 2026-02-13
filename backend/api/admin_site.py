"""
Custom AdminSite that fixes admin login redirect (avoid 404 after login)
by always redirecting to /admin/ after login.
"""
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _


class PyLearnAdminSite(AdminSite):
    """Admin site that forces a safe redirect after login to avoid 404."""

    def login(self, request, extra_context=None):
        # Force redirect to admin index after login so we never get 404
        extra_context = extra_context or {}
        extra_context.setdefault('next', '/admin/')
        return super().login(request, extra_context=extra_context)


# Single instance used by urls and model registration
pylearn_admin_site = PyLearnAdminSite(name='admin')
