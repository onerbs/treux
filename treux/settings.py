"""Django settings for treux project."""
from datetime import timedelta
from os import listdir, path, getenv
from pathlib import Path
from treux import cache, Cache

__root__ = Path(__file__).parents[1]
assert ('manage.py' in listdir(__root__))


def base(*args):
	return path.join(BASE_DIR, *args).replace('\\', '/')


BASE_DIR = str(__root__)
SECRET_KEY = getenv('SECRET_KEY')

DEBUG = False
ALLOWED_HOSTS = ['*']
AUTH_USER_MODEL = 'users.User'

SITE_URL = getenv('SITE_URL')
SITE_EMAIL = getenv('SITE_EMAIL')
DEFAULT_FROM_EMAIL = SITE_EMAIL

EMAIL_HOST = getenv('EMAIL_HOST')
EMAIL_HOST_USER = getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = getenv('EMAIL_PASS')
EMAIL_PORT = getenv('EMAIL_PORT')
EMAIL_USE_TLS = not DEBUG

CSRF_COOKIE_AGE = None
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = not DEBUG
CSRF_USE_SESSIONS = True

SESSION_COOKIE_AGE = 604800
SESSION_COOKIE_SECURE = not DEBUG
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

SHORT_DATE_FORMAT = 'd/m/Y'
SHORT_DATETIME_FORMAT = SHORT_DATE_FORMAT + ' H:i'

AUTHENTICATION_BACKENDS = [
	'core.auth.backends.EmailOrUsernameModelBackend'
]

CACHE_MIDDLEWARE_SECONDS = 0 if DEBUG else 1200
CACHES = {
	'default': {
		'BACKEND': cache(Cache.DUMMY)
	},
	'celery': {
		'BACKEND': cache(Cache.FILE_BASED),
		'LOCATION': base('_cache')
	},
}

REST_FRAMEWORK = {
	'DEFAULT_PAGINATION_CLASS': 'base.pagination.DefaultPagination',
	'DEFAULT_AUTHENTICATION_CLASSES': [
		'rest_framework.authentication.SessionAuthentication',
		'rest_framework_simplejwt.authentication.JWTAuthentication'
	]
}

SIMPLE_JWT = {
	'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
	'SIGNING_KEY': SECRET_KEY,
}

CELERY_CACHE_BACKEND = 'celery'
CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672'
CELERY_TASK_PUBLISH_RETRY = False
CELERY_TASK_PUBLISH_RETRY_POLICY = {
	'interval_step': 0.5
}

INSTALLED_APPS = [
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.staticfiles',
	'core.apps.CoreConfig',
	'teams.apps.TeamsConfig',
	'users.apps.UsersConfig',
	'boards.apps.BoardsConfig',
	'cards.apps.CardsConfig',
	'comments.apps.CommentsConfig',
	'rest_framework',
	'drf_yasg',
]

MIDDLEWARE = [
	'django.middleware.cache.UpdateCacheMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.middleware.cache.FetchFromCacheMiddleware',
]

TEMPLATES = [{
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
}]

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': getenv('DB_NAME'),
		'USER': getenv('DB_USER'),
		'PASSWORD': getenv('DB_PASS'),
		'HOST': getenv('DB_HOST'),
		'PORT': getenv('DB_PORT'),
		'CONN_MAX_AGE': 10,
	}
}

_v = 'django.contrib.auth.password_validation'
AUTH_PASSWORD_VALIDATORS = [
	{'NAME': f'{_v}.UserAttributeSimilarityValidator'},
	{'NAME': f'{_v}.MinimumLengthValidator'},
	{'NAME': f'{_v}.CommonPasswordValidator'},
	{'NAME': f'{_v}.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

WSGI_APPLICATION = 'treux.wsgi.application'
ROOT_URLCONF = 'treux.urls'
STATIC_URL = '/x/'
STATIC_ROOT = None if DEBUG else base('_static', '')
