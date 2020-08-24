from treux.api import TestCase, api_post, api_get
from faker import Faker
from xu import string


class TestLoginLogout(TestCase):
	def setUp(self) -> None:
		fake = Faker('es_MX')
		self.email = f'0x{string(6).digit.extend("abcdef")}@example.com'
		self.password = string(16).alpha.next()
		self.first_name = fake.first_name()
		self.last_name = fake.last_name()

	def test_auth(self):
		self.should_pass(api_post(self, 'users/', {
			'email': self.email,
			'password': self.password,
			'first_name': self.first_name,
			'last_name': self.last_name,
		}), 201, 'Create user')

		self.should_pass(api_post(self, 'auth/login/', {
			'identifier': self.email,
			'password': self.password,
		}), 200, 'Log in with email')

		self.should_pass(api_get(self, 'auth/logout/'), 200, 'Log out')

	def test_bad_auth(self):
		self.should_fail(api_post(self, 'users/', {
			'email': self.email,
			'password': self.password,
		}), 400, 'Create user')

		self.should_fail(api_post(self, 'auth/login/', {
			'identifier': self.email,
			'password': self.password[::-1],
		}), 400, 'Log in with email')
