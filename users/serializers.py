from base import serializer
from users.models import User


class UserSerializer(serializer(User, [
	'first_name', 'last_name', 'username', 'email', 'avatar', 'is_confirmed',
	'owned_teams', 'member_of', 'owned_boards', 'favorite_boards',
	'assigned_cards', 'authored_comments'
])):
	POST = serializer(User, [
		'first_name', 'last_name', 'email', 'password'
	])
