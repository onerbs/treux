from datetime import datetime

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action

from base.views import viewset
from cards.models import Card
from comments import encoder
from comments.actions import create_comment
from comments.models import Comment
from comments.serializers import CommentSerializer
from core.decorators import with_fields, with_dependency

raw = openapi.Parameter(
	'raw', openapi.IN_QUERY,
	'Display raw data',
	type=openapi.TYPE_BOOLEAN
)


class CommentViewSet(viewset(Comment, CommentSerializer)):
	@with_fields(['text'])
	@with_dependency(Card)
	def create(self, request, **kwargs):
		return self.created(create_comment(request))

	@with_fields(['text'])
	def update(self, request, **kwargs):
		comment = self.get_object()
		text = request.text.strip()
		timestamp = datetime.now().timestamp()
		history = encoder.decode_many(comment.history)
		kwargs.pop(self.lookup_field)
		if text != history[-1][0]:
			history.append((text, timestamp))
			comment.text = text
			comment.history = encoder.encode_many(history)
			comment.save(**kwargs)
			return self.updated()
		return self.accept('No changes performed.')

	@action(['get'], True)
	@swagger_auto_schema(manual_parameters=[raw])
	def history(self, request, **kwargs):
		this = self.get_object()
		if request.query_params.get('raw') == 'true':
			return self.send(this.history)
		else:
			return self.send(encoder.decode_many(this.history))
