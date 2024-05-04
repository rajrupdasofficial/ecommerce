import os
from pathlib import Path
from decouple import config
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if config('DEBUG') == "True" else False
PRODUCTION = True if config('PRODUCTION') == "True" else False
IS_REDIS = True if config('IS_REDIS') == "True" else False
IS_MEMCACHED = True if config('IS_MEMCACHED') == "True" else False

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'app.apps.AppConfig',
    'customuser.apps.CustomuserConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'taggit',
]

if PRODUCTION:
    MIDDLEWARE = [
        # 'corsheaders.middleware.CorsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.cache.UpdateCacheMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.cache.FetchFromCacheMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        # 'analyticsapp.middlewares.TrackIPAddressMiddleware'
    ]
    CACHE_MIDDLEWARE_ALIAS = "default"
    CACHE_MIDDLEWARE_SECONDS = 600
    CACHE_MIDDLEWARE_KEY_PREFIX = "default"
else:
    MIDDLEWARE = [
        # 'corsheaders.middleware.CorsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        # 'analyticsapp.middlewares.TrackIPAddressMiddleware'

    ]
ROOT_URLCONF = 'ecomm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'ecomm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if PRODUCTION:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('SUPABASE_DB_NAME'),
            'HOST': config('SUPABASE_HOST'),
            'USER': config('DB_USER'),
            'PASSWORD': config('SUPABASE_PASSWORD'),
            'PORT': config('PORT'),
            'OPTIONS': {
                'sslmode': 'require',
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

if IS_REDIS:
    CACHE_TTL = 50 * 15
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": config("REDIS_LOCATION"),
            "OPTIONS": {
                "DB": 1,
                "PASSWORD": config("REDIS_PASSWORD"),
                'parser_class': config("PARSER_CLASS"),
                'pool_class': config('POOL_CLASS'),
                "CLIENT_CLASS": config('CLIENT_CLASS'),
            }
        }
    }
    SESSION_ENGINE = config("SESSION_ENGINE")
    SESSION_CACHE_ALIAS = config("SESSION_CACHE_ALIAS")
elif IS_MEMCACHED:
    CACHE_TTL = 3600
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }
    SESSION_ENGINE = config("SESSION_ENGINE")
    SESSION_CACHE_ALIAS = config("SESSION_CACHE_ALIAS")
else:
    CACHE_TTL = 0 * 0


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# secure user

AUTH_USER_MODEL = 'customuser.User'

# login redirect url

LOGIN_REDIRECT_URL = '/users/profile/'


CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js'
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 900,
        'width': 900,
    },
}
"""Stripe payment setup"""
STRIPE_PUBLIC_KEY = config('STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')
"""paypal payment gateway"""
# PAYPAL_CLIENT_ID = config('PAYPAL_CLIENT_ID')
# PAYPAL_SECRET_KEY = config('PAYPAL_SECRET_KEY')
