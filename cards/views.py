from datetime import datetime

from base import viewset
from boards.models import Board
from cards.models import List, Card
from cards.serializers import ListSerializer, CardSerializer
from core import error, created, not_found


class ListViewSet(viewset(List, ListSerializer)):
	@staticmethod
	def create(request):
		if not (uuid := request.data.get('uuid')):
			return error()
		try:
			of_board = Board.objects.get(uuid=uuid)
		except Board.DoesNotExist:
			return not_found('Board')
		List.objects.create(
			index=int(request.data.get('index')),
			title=request.data.get('title'),
			of_board=of_board,
		)
		return created('List')


class CardViewSet(viewset(Card, CardSerializer)):
	@staticmethod
	def create(request):
		if not (uuid := request.data.get('uuid')):
			return error()
		try:
			of_list = List.objects.get(uuid=uuid)
		except List.DoesNotExist:
			return not_found('List')
		if expires_at := request.data.get('expires_at'):
			expires_at = datetime.fromisoformat(expires_at.replace('Z', ''))
		Card.objects.create(
			index=int(request.data.get('index')),
			text=request.data.get('text'),
			expires_at=expires_at or None,
			of_list=of_list
		)
		return created('Card')
