from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailOrUsernameModelBackend(ModelBackend):
	def authenticate(self, request, username=None, password=None, **kwargs):
		if '@' in username:
			user_model = get_user_model()
			try:
				username = user_model.objects.get(email=username).username
			except user_model.DoesNotExist as ex:
				raise ex
		return super().authenticate(request, username, password, **kwargs)
