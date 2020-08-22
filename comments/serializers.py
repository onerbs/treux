from base import serializer
from comments.models import Comment

CommentSerializer = serializer(Comment, ['text', 'uuid'])
