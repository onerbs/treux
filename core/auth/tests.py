from core.api.status import *
from core.api.testing import WithShortcuts, WithUser
from faker import Faker
fake = Faker(['es_MX'])


class TestLoginLogout(WithShortcuts):
	def test_best_case(self):
		email = fake.email()
		password = fake.md5()
		response = self.register(
			email=email,
			password=password,
			first_name=fake.first_name(),
			last_name=fake.last_name(),
		)
		self.assertEqual(
			response.status_code, CREATED, 'Should register a user')

		self.assertEqual(self.auth(
			username=email,
			password=password
		).status_code, SUCCESS, 'Should log in with email')

		self.assertEqual(
			self.logout().status_code, SUCCESS, 'Should log out')

		self.assertEqual(self.auth(
			username=response.data.get('username'),
			password=password
		).status_code, SUCCESS, 'Should log in with username')

		self.assertEqual(
			self.logout().status_code, SUCCESS, 'Should log out again')

	def test_bad_password(self):
		email = fake.email()
		first_name = fake.first_name()
		self.assertNotEqual(self.register(
			email=email,
			password='12345678',
			first_name=first_name
		).status_code, CREATED, 'Should fail by weak password 12341234')

		self.assertNotEqual(self.register(
			email=email,
			password='qwerqwer',
			first_name=first_name
		).status_code, CREATED, 'Should fail by weak password qwerqwer')

		self.assertNotEqual(self.register(
			email=email,
			password='qwer1234',
			first_name=first_name
		).status_code, CREATED, 'Should fail by weak password qwer1234')

		self.assertNotEqual(self.register(
			email=email,
			password='1234',
			first_name=first_name
		).status_code, CREATED, 'Should fail by short password')

	def test_worst_case(self):
		self.assertNotEqual(self.register(
			email=fake.email(),
			password=fake.md5(),
		).status_code, CREATED, 'Should not create an account without first name')

		self.assertNotEqual(self.auth(
			username=fake.email(),
			password=fake.md5()
		).status_code, SUCCESS, 'Should not log in with nonexistent credentials')

		self.assertNotEqual(
			self.logout().status_code,
			SUCCESS, 'Should not log out without being logged in')


class TestJWT(WithUser):
	def test_jwt(self):
		response = self.jwt_auth(
			username=self.user.username,
			password=self.password,
		)
		self.assertIsNotNone(
			access := response.data.get('access'),
			'Should have an access token.'
		)
		self.assertIsNotNone(
			refresh := response.data.get('refresh'),
			'Should have an access token.'
		)
		self.assertEqual(self.post('verify', {
			'token': access
		}).status_code, 200, 'Should verify the access token')

		self.assertEqual(self.post('verify', {
			'token': refresh
		}).status_code, 200, 'Should verify the refresh token')

		self.assertEqual(self.post('refresh', {
			'refresh': refresh
		}).status_code, 200, 'Should refresh the token')
