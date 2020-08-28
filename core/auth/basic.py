from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView

from core.decorators import with_fields, without_login
from core.responses import WithResponses


class AuthView(APIView, WithResponses):
	@without_login
	@with_fields(['username', 'password'])
	def post(self, request, **kwargs):
		try:
			if not (user := authenticate(
				request,
				username=request.username,
				password=request.password,
			)):
				return self.reject('Invalid credentials')
			login(request, user)
			return self.succeed('Logged in.')
		except:
			return self.fail('User does not exist.')

	def delete(self, request):
		if not request.user.is_authenticated:
			return self.fail('Invalid session.')
		logout(request)
		return self.succeed('Logged out.')
