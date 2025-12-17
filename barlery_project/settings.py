from pathlib import Path
import os
from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv
import sys
import dj_database_url
from datetime import datetime

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# This should only do anything if a .env file exists at the root of the workspace directory
# it will return false if not .env file exists
load_dotenv()

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "False") == "True"

# SECURITY WARNING: keep the keys used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
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
if DEVELOPMENT_MODE == True:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic' and sys.argv[1] != 'compilescss':
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
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

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
        EMAIL_PORT = os.getenv("EMAIL_PORT")
        EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")
        EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL")
    except:
        raise Exception("Email backend configuration not properly defined.")

# Hardcoded redirects after login/logout
LOGIN_REDIRECT_URL = 'barlery:index'
LOGOUT_REDIRECT_URL = 'barlery:successful_logout'
