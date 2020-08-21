from base import serializer
from boards.models import Board


class BoardSerializer(serializer(Board, [
	'name', 'description', 'owner', 'is_public', 'favorite_of', 'lists'
])):
	pass
