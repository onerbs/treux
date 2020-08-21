from base import serializer
from comments.models import Comment


class CommentSerializer(serializer(Comment, [
	'text', 'author', 'target'
])):
	pass
