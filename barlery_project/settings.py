from pathlib import Path
import os
from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv
import sys
import dj_database_url
from datetime import datetime
from environs import Env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# This should only do anything if a .env file exists at the root of the workspace directory
# it will return false if not .env file exists
load_dotenv()

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "False") == "True"

# SECURITY WARNING: keep the keys used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"
if DEVELOPMENT_MODE is True: DEBUG = "True"

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")


# Application definition

INSTALLED_APPS = [
    'storages',
    'barlery.apps.BarleryConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'barlery_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'barlery_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# Check to see if DEVELOPMENT_MODE is true:
#  If true, use SQLite 3 bindings
#  If false, use the production environemnt's DB info
#  The comparison at the end of the first line is evaluated to convert a string to a boolean
if DEVELOPMENT_MODE is True:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
    if os.getenv("DATABASE_URL", None) is None:
        raise Exception("DATABASE_URL environment variable not defined")
    DATABASES = {
        "default": dj_database_url.parse(os.environ.get("DATABASE_URL")),
    }

#AUTH_USER_MODEL = "barlery.User" ----- uncomment when custom user model is implemented

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

# Enforce cache busting on every reload in dev environment:
# STATIC_VERSION defines this loads version iteration of all static files
# This is NOT changed when running collectstatic. It is only changed when the new server code is loaded.
if DEVELOPMENT_MODE:
    STATIC_VERSION = datetime.now().strftime("%Y%m%d%H%M%S")  # cache-bust on every reload
else:
    STATIC_VERSION = ""  # no cache-busting in production

# Uncomment the line below if you have extra static files and a directory in your GitHub repo.
# If you don't have this directory and have this uncommented your build will fail
# STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Mailer Settings:
    # Mail is sent using the SMTP host and port specified in the EMAIL_HOST and EMAIL_PORT settings.
    # The EMAIL_HOST_USER and EMAIL_HOST_PASSWORD settings, if set, are used to authenticate to the SMTP server,
    # and the EMAIL_USE_TLS and EMAIL_USE_SSL settings control whether a secure connection is used.
    # The character set of email sent with django.core.mail will be set to the value of your DEFAULT_CHARSET setting.
if DEVELOPMENT_MODE == True: # set all Vars to the env or to None, and don't throw any errors if None
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend" # use console output in development
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic': # this prevents the static site from throwing errors at build-phase
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend" # use SMTP backend in production
    try:
        EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
        EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
        EMAIL_HOST = os.getenv("EMAIL_HOST")
        EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
        EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "False").lower() in ("true", "1", "yes")
        EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False").lower() in ("true", "1", "yes")
    except:
        raise Exception("Email backend configuration not properly defined.")

CONTACT_RECIPIENT_EMAIL = os.getenv("CONTACT_RECIPIENT_EMAIL", "info@barlery.com")
# Site URL for email links
SITE_URL = os.getenv('SITE_URL', 'http://localhost:8000')

DEFAULT_FROM_EMAIL = "Barlery Info <info@barlery.com>"

# Hardcoded redirects after login/logout
LOGIN_REDIRECT_URL = 'barlery:index'

# Points authentication to accounts app User model
AUTH_USER_MODEL = "barlery.User"




#### Storage Settings (Local in Dev, R2 in Production):

if DEVELOPMENT_MODE:
    # Development: Use local file storage
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
    
    # Local media files
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"
    
else:
    # Production: Use R2 Storage
    env = Env()
    env.read_env()
    
    # Pull credentials & bucket from env
    R2_BUCKET   = env.str("R2_BUCKET_NAME")
    R2_ENDPOINT = env.str("R2_ENDPOINT_URL").rstrip("/")  # e.g. https://<ACCOUNT_ID>.r2.cloudflarestorage.com
    
    # Common OPTIONS for both storage backends
    R2_OPTIONS = {
        "access_key": env.str("R2_ACCESS_KEY_ID"),
        "secret_key": env.str("R2_SECRET_ACCESS_KEY"),
        "bucket_name": R2_BUCKET,
        "endpoint_url": R2_ENDPOINT,
        "region_name": "auto",
        "signature_version": "s3v4",
        "addressing_style": "path",     # <endpoint>/<bucket>/<key>
        "default_acl": "public-read",
    }
    
    # Tell Django 5.1+ about your storages
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": R2_OPTIONS,
            "LOCATION": "media",     # objects under /media/
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": R2_OPTIONS,
            "LOCATION": "static",    # objects under /static/
        },
    }
    
    # URLs your templates will use
    STATIC_URL = f"https://{R2_ENDPOINT.replace('https://','')}/{R2_BUCKET}/static/"
    MEDIA_URL  = f"https://{R2_ENDPOINT.replace('https://','')}/{R2_BUCKET}/media/"

# End of settings