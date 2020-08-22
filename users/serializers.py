from base import serializer
from users.models import User

UserSerializer = serializer(User, [
	'first_name', 'last_name', 'email', 'password'
])
