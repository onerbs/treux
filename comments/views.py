from datetime import datetime

from base import viewset
from cards.models import Card
from comments import encoder
from comments.models import Comment
from comments.serializers import CommentSerializer
from core.decorators import check_fields, with_reference
from core.responses import success


def now():
	return datetime.now().timestamp()


class CommentViewSet(viewset(Comment, CommentSerializer)):
	@with_reference(Card)
	@check_fields(['text'])
	def create(self, request):
		Comment.objects.create(
			text=request.text,
			history=encoder.encode(request.text, now()),
			author=request.user,
			target=request.card,
		)
		return self.created()

	@check_fields(['text'])
	def update(self, request, **kwargs):
		comment = self.get_object()
		text = request.text.strip()
		timestamp = now()
		history = encoder.decode_many(comment.history)
		kwargs.pop('pk')
		if text != history[-1][0]:
			history.append((text, timestamp))
			comment.text = text
			comment.history = encoder.encode_many(history)
			comment.save(**kwargs)
			return self.updated()
		print(comment)
		return success('No changes performed.')
