from base import serializer
from boards.models import Board

BoardSerializer = serializer(Board, [
	'name', 'description', 'owner', 'is_public', 'favorite_of', 'lists'
])
