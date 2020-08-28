from rest_framework.decorators import action

from base.views import viewset
from boards.models import Board
from cards.actions import create_list, create_card
from cards.models import List, Card
from cards.serializers import ListSerializer, CardSerializer
from comments.models import Comment
from comments.serializers import CommentSerializer
from core.decorators import with_fields, with_dependency


class ListViewSet(viewset(List, ListSerializer)):
	@with_fields(['title'], ['index'])
	@with_dependency(Board)
	def create(self, request):
		return self.created(create_list(request))


class CardViewSet(viewset(Card, CardSerializer)):
	@with_fields(['text'], ['index', 'expires_at'])
	@with_dependency(List)
	def create(self, request):
		return self.created(create_card(request))

	@action(['get'], True)
	def comments(self, request, **kwargs):
		item = self.get_object()
		comments = Comment.alive(target=item)
		data = CommentSerializer(comments, many=True).data
		return self.send(data)
