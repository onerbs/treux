from base import viewset
from boards.models import Board
from boards.serializers import BoardSerializer
from core import created


class BoardViewSet(viewset(Board, BoardSerializer)):
	@staticmethod
	def create(request):
		Board.objects.create(
			name=request.data.get('name'),
			description=request.data.get('description'),
			is_public=request.data.get('is_public') in ['on', 'true'],
			owner=request.user,
		)
		return created('Board')
