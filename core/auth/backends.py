from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailOrUsernameModelBackend(ModelBackend):
	def authenticate(self, request, identifier=None, password=None, **kwargs):
		if '@' in identifier:
			user_model = get_user_model()
			try:
				identifier = user_model.objects.get(email=identifier).username
			except user_model.DoesNotExist:
				pass
		return super().authenticate(request, identifier, password, **kwargs)
