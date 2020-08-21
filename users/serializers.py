from base import serializer
from users.models import User


class UserSerializer(serializer(User, [
	'first_name', 'last_name', 'username', 'email', 'avatar', 'is_confirmed',
	'owned_teams', 'teams', 'boards', 'favorite_boards', 'assigned_cards',
	'authored_comments'
])):
	POST = serializer(User, [
		'first_name', 'last_name', 'email', 'password'
	])
