from rest_framework.decorators import action

from base.views import viewset
from boards.actions import create_board
from boards.models import Board
from boards.serializers import BoardSerializer
from cards.models import List
from cards.serializers import ListSerializer
from core.decorators import with_fields


class BoardViewSet(viewset(Board, BoardSerializer)):
	@with_fields(['name'], ['description', 'is_public'])
	def create(self, request):
		return self.created(create_board(request))

	@action(['get'], True)
	def lists(self, request, **kwargs):
		board = self.get_object()
		lists = List.alive(of_board=board)
		data = ListSerializer(lists, many=True).data
		return self.send(data)
