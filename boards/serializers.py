from base import serializer
from boards.models import Board

BoardSerializer = serializer(Board, [
	'name', 'description', 'is_public'
])
