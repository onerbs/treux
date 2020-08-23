from base import viewset
from boards.models import Board
from boards.serializers import BoardSerializer
from core.decorators import check_fields


class BoardViewSet(viewset(Board, BoardSerializer)):
	@check_fields(['name'], ['description', 'is_public'])
	def create(self, request):
		Board.objects.create(
			name=request.name,
			description=request.description,
			is_public=request.is_public,
			owner=request.user,
		)
		return self.created()
