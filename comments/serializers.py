from rest_framework.serializers import StringRelatedField

from base.serializers import serializer
from comments.models import Comment


class CommentSerializer(serializer(Comment, ['text', 'uuid:'])):
	author = StringRelatedField()
	target = StringRelatedField()
