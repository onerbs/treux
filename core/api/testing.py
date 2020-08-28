from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.test import APITestCase

from core.api import api_path
from core.api.status import SUCCESS
from core.util import create_item
from users.actions import create_user


class WithVerbs(APITestCase):
	fake = Faker(['es_MX'])

	def get(self, path: str) -> Response:
		"""Make a GET request to the specified path.

		:param path: The request url.
		"""
		return self.client.get(reverse(path))

	def post(self, path: str, data: dict = None) -> Response:
		"""Make a POST request to the specified path.

		:param path: The request url.
		:param data: The POST data.
		"""
		return self.client.post(reverse(path), data)

	def delete(self, path: str, data: dict = None) -> Response:
		"""Make a DELETE request to the specified path.

		:param path: The request url.
		:param data: The DELETE data.
		"""
		return self.client.delete(reverse(path), data)

	def api_post(self, path: str, data: dict = None) -> Response:
		"""Make a POST request to the specified path.

		:param path: The request url.
		:param data: The POST data.
		"""
		return self.client.post(api_path(path), data)


class WithShortcuts(WithVerbs):
	def register(self, **kwargs) -> Response:
		"""Shortcut to register an user."""
		return self.post('join', create_item(**kwargs).data)

	def jwt_auth(self, **kwargs) -> Response:
		"""Shortcut to JWT authentication."""
		response = self.post('jwt', create_item(**kwargs).data)
		self.assertEqual(
			response.status_code, SUCCESS,
			'Should authenticate (JWT)'
		)
		token = 'Bearer ' + response.data.get('access')
		self.client.credentials(HTTP_AUTHORIZATION=token)
		return response

	def auth(self, **kwargs) -> Response:
		"""Shortcut to basic authentication."""
		return self.post('auth', create_item(**kwargs).data)

	def logout(self) -> Response:
		"""Shortcut to basic log out."""
		return self.delete('auth')


class WithUser(WithShortcuts):
	"""This case provides a user on setup."""
	def setUp(self) -> None:
		self.password = self.fake.md5()
		self.user = create_user(
			email=self.fake.email(),
			password=self.password,
			first_name=self.fake.first_name(),
			last_name=self.fake.last_name(),
		)
