from base import viewset
from boards.models import Board
from cards.models import List, Card
from cards.serializers import ListSerializer, CardSerializer
from core.decorators import check_fields, with_reference


class ListViewSet(viewset(List, ListSerializer)):
	@with_reference(Board)
	@check_fields(['index', 'title'])
	def create(self, request):
		List.objects.create(
			index=request.index,
			title=request.title,
			of_board=request.board,
		)
		return self.created()


class CardViewSet(viewset(Card, CardSerializer)):
	@with_reference(List)
	@check_fields(['index', 'text'], ['expires_at'])
	def create(self, request):
		Card.objects.create(
			index=request.index,
			text=request.text,
			expires_at=request.expires_at,
			of_list=request.list,
		)
		return self.created()
