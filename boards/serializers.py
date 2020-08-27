from rest_framework.serializers import StringRelatedField

from base.serializers import serializer
from boards.models import Board


class BoardSerializer(
	serializer(Board, ['name', 'description', 'is_public'])
):
	owner = StringRelatedField()
	favorite_of = StringRelatedField(many=True)
	lists = StringRelatedField(many=True)
