from rest_framework.serializers import StringRelatedField

from base.serializers import serializer
from cards.models import List, Card


class ListSerializer(serializer(List, [
	'index', 'title', 'uuid:'
])):
	of_board = StringRelatedField()
	cards = StringRelatedField(many=True)


class CardSerializer(serializer(Card, [
	'index', 'text', 'expires_at', 'uuid:'
])):
	of_list = StringRelatedField()
	assigned_to = StringRelatedField(many=True)
