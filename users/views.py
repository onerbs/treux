from django.contrib.auth import get_user_model
from xu import string

from base import viewset
from core.decorators import check_fields
from core.postman import send_confirmation_email
from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewset(User, UserSerializer, [])):
	@check_fields(['email', 'password', 'first_name'], ['last_name'])
	def create(self, request):
		user_model = get_user_model()
		user = user_model.objects.create_user(
			string(6, prefix='user_0x').digit.extend('abcdef'),
			request.email,
			request.password,
			first_name=request.first_name,
			last_name=request.last_name,
		)
		send_confirmation_email(user)
		return self.created()
