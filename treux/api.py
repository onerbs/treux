from rest_framework.response import Response
from rest_framework.test import APITestCase

from treux.settings import SITE_URL

api_root = 'api/v1/'


def api_path(path: str) -> str:
	return '/' + api_root + path


def api_url(path: str) -> str:
	return SITE_URL + api_path(path)


class TestCase(APITestCase):
	def should_pass(self, res: Response, expected: int, what: str):
		return self.assertEqual(
			res.status_code, expected, f'Should pass: {what}')

	def should_fail(self, res: Response, expected: int, what: str):
		return self.assertEqual(
			res.status_code, expected, f'Should fail: {what}')


def api_urls(items: list) -> list:
	f"""
	Register the urls under '{api_root}'.

	:param items: The items to register.

	:return: The api url patterns.
	"""
	from django.urls import path, include
	return [path(api_root, include(item)) for item in items]


def api_get(api, path: str) -> Response:
	f"""
	Prepend '{api_root}' to every request.

	:param api: The api client.
	:param path: The request url.

	:return: The Response.
	"""
	return api.client.get(api_path(path))


def api_post(api, path: str, data: dict = None) -> Response:
	f"""
	Prepend '{api_root}' to every request.

	:param api: The api client.
	:param path: The request url.
	:param data: The POST data.

	:return: The Response.
	"""
	return api.client.post(api_path(path), data)
