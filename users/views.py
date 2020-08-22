from django.contrib.auth import get_user_model

from base import viewset
from core.generics import create_resource
from core.postman import send_confirmation_email
from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewset(User, UserSerializer)):
	def create(self, request, *args, **kwargs):
		user_model = get_user_model()
		user = user_model.objects.create_user(
			request.data.get('email').split('@')[0],
			request.data.get('email'),
			request.data.get('password'),
			first_name=request.data.get('first_name'),
			last_name=request.data.get('last_name'),
		)
		response = create_resource(self, UserSerializer(user))
		if response.status_code == 200:
			send_confirmation_email(user)
		return response

	def get_serializer_class(self):
		if self.request.method == 'POST':
			return UserSerializer.POST
		return UserSerializer
