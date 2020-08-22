from celery import Celery


def load_environment():
	from core import dotenv
	from os import getenv
	dotenv.source(getenv('ENV'))

	from os import environ
	environ['DJANGO_SETTINGS_MODULE'] = 'treux.settings'


load_environment()
future = Celery('treux')
future.config_from_object('django.conf:settings', namespace='CELERY')
future.autodiscover_tasks()


# ----------------------------------------------------------------------


_CacheType = [
	'db.DatabaseCache',
	'dummy.DummyCache',
	'filebased.FileBasedCache',
	'locmem.LocMemCache',
	'memcached.MemcachedCache',
	'memcached.PyLibMCCache',
]


class Cache:
	DATABASE = 0
	DUMMY = 1
	FILE_BASED = 2
	LOCAL_MEMORY = 3
	MEMORY = 4
	PY_LIB_MEMORY = 5


def cache(index: int) -> str:
	return 'django.core.cache.backends.' + _CacheType[index]
