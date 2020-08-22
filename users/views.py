from django.contrib.auth import get_user_model
from xu import string

from base import viewset
from core import created
from core.postman import send_confirmation_email
from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewset(User, UserSerializer, [])):
	@staticmethod
	def create(request, *args, **kwargs):
		user_model = get_user_model()
		user = user_model.objects.create_user(
			f'user_0x{string(6).using("0123456789abcdef")}',
			request.data.get('email'),
			request.data.get('password'),
			first_name=request.data.get('first_name'),
			last_name=request.data.get('last_name'),
		)
		send_confirmation_email(user)
		return created('User')
