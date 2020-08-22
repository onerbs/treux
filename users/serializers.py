from base import serializer
from users.models import User


class UserSerializer(serializer(User)):
	POST = serializer(User)
	POST.Meta.fields = [
		'first_name', 'last_name', 'email', 'password'
	]
