from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key-here-change-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = ["*"]  # ok for fresher project

# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'ckeditor',  # Add this
    # Our apps
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Must be at top
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# Database - Using SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# CORS Settings - Allow React frontend
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CORS_ALLOW_CREDENTIALS = True

# ==================== JAZZMIN ADMIN SETTINGS ====================

JAZZMIN_SETTINGS = {
    # Title on the login screen
    "site_title": "PyLearn Admin",
    
    # Title on the brand (top left)
    "site_header": "PyLearn",
    
    # Title in the browser tab
    "site_brand": "PyLearn Admin",
    
    # Logo (you can add a logo image later)
    "site_logo": None,
    
    # Welcome text on the login screen
    "welcome_sign": "Welcome to PyLearn Admin Panel",
    
    # Copyright text at the bottom
    "copyright": "PyLearn - Python Learning Platform",
    
    # The model admin to search from the search bar
    "search_model": ["auth.User", "api.Topic", "api.Question"],
    
    # User avatar (uses Gravatar by default)
    "user_avatar": None,

    #############
    # Side Menu #
    #############
    
    # Whether to display the side menu
    "show_sidebar": True,
    
    # Whether to auto-expand the menu
    "navigation_expanded": True,
    
    # Icons for apps/models
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "api.Topic": "fas fa-book",
        "api.Question": "fas fa-question-circle",
        "api.UserProgress": "fas fa-chart-line",
        "api.TopicProgress": "fas fa-tasks",
    },
    
    # Default icon for models
    "default_icon_parents": "fas fa-folder",
    "default_icon_children": "fas fa-file",

    #############
    # UI Tweaks #
    #############
    
    # Relative paths to custom CSS/JS files
    "custom_css": None,
    "custom_js": None,
    
    # Show UI customizer on the sidebar
    "show_ui_builder": False,

    ###############
    # Change view #
    ###############
    
    # Render out the change view as a single form, or in tabs
    "changeform_format": "horizontal_tabs",
    
    # Override change forms on a per model basis
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
}

JAZZMIN_UI_TWEAKS = {
    # Theme color
    "theme": "cosmo",
    
    # Dark mode sidebar
    "theme": "darkly", 
    
    # Navbar settings
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}

# ==================== CKEDITOR SETTINGS ====================

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Strike'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent'],
            ['Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source'],
            ['Maximize'],
        ],
        'height': 300,
        'width': '100%',
        'removePlugins': 'elementspath',
        'resize_enabled': True,
    },
    'theory': {
        'toolbar': 'Full',
        'toolbar_Full': [
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript'],
            ['TextColor', 'BGColor'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source'],
            ['Maximize', 'Preview'],
            '/',
            ['Table', 'HorizontalRule', 'SpecialChar'],
            ['Undo', 'Redo'],
        ],
        'height': 400,
        'width': '100%',
        'removePlugins': 'elementspath',
        'resize_enabled': True,
        'extraAllowedContent': 'pre code span(*)',
    },
}


