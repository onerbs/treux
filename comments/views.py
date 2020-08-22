from base import viewset
from cards.models import Card
from comments.models import Comment
from comments.serializers import CommentSerializer
from core import error, created, not_found


class CommentViewSet(viewset(Comment, CommentSerializer)):
	@staticmethod
	def create(request, *args, **kwargs):
		if not (uuid := request.data.get('uuid')):
			return error('Bad request.')
		try:
			card = Card.objects.get_queryset().get(uuid=uuid)
		except Card.DoesNotExist:
			return not_found('Card')
		Comment.objects.create(
			text=request.data.get('text'),
			author=request.user,
			target=card,
		)
		return created('Comment')
