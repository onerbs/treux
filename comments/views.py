from base import viewset
from cards.models import Card
from comments.models import Comment
from comments.serializers import CommentSerializer
from core.generics import create_resource


class CommentViewSet(viewset(Comment, CommentSerializer)):
	def create(self, request, *args, **kwargs):
		card = Card.objects.get_queryset().get(uuid=request.data.get('uuid'))
		comment = Comment.objects.create(
			text=request.data.get('text'),
			author=request.user,
			target=card,
		)
		return create_resource(self, CommentSerializer(comment))
