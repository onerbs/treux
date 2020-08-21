from base import serializer
from cards.models import List, Card

ListSerializer = serializer(List, [
	'index', 'name', 'description', 'of_board'
])

CardSerializer = serializer(Card, [
	'index', 'name', 'description', 'of_list', 'assigned_to', 'expires_at'
])
