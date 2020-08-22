from base import serializer
from cards.models import List, Card

ListSerializer = serializer(List, [
	'index', 'title', 'uuid'
])
CardSerializer = serializer(Card, [
	'index', 'text', 'expires_at', 'uuid'
])
