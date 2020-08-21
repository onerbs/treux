from base import viewset
from boards.models import Board
from boards.serializers import BoardSerializer
from core.generics import create_resource


class BoardViewSet(viewset(Board, BoardSerializer)):
	def create(self, request, *args, **kwargs):
		is_public = request.data.get('is_public')
		is_public = True if is_public == 'on' else False
		board = Board.objects.create(
			name=request.data.get('name'),
			description=request.data.get('description'),
			is_public=is_public,
			owner=request.user,
		)
		return create_resource(self, BoardSerializer(board))
