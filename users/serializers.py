from rest_framework.serializers import StringRelatedField

from base.serializers import serializer
from users.models import User


class UserSerializer(serializer(User, [
	'first_name', 'last_name', 'email', 'password:', ':username'
])):
	owned_teams = StringRelatedField(many=True)
	member_of = StringRelatedField(many=True)
	owned_boards = StringRelatedField(many=True)
	favorite_boards = StringRelatedField(many=True)
	assigned_cards = StringRelatedField(many=True)
	authored_comments = StringRelatedField(many=True)
