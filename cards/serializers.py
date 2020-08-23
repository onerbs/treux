from base import serializer
from cards.models import List, Card

ListSerializer = serializer(
	List, ['index', 'title', 'uuid'], ['!uuid'])

CardSerializer = serializer(
	Card, ['index', 'text', 'expires_at', 'uuid'], ['!uuid'])
