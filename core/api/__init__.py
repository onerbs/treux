from treux.settings import SITE_URL

api_root = 'api/v1/'


def api_path(path: str) -> str:
	"""Create a /api_root/path path."""
	url = '/' + api_root + path
	return url


def api_url(path: str) -> str:
	"""Create a SITE_URL/api_root/path url."""
	url = SITE_URL + api_path(path)
	return url


def api_patterns(items: list) -> list:
	"""Register the urls under {api_root}.

	:param items: The items to register.

	:return: The api url patterns.
	"""
	from django.urls import path, include
	return [path(api_root, include(item)) for item in items]
