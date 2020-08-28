from boards.models import Board
from core.util import create_item


def create_board(item=None, **kwargs):
	if item is None:
		item = create_item(**kwargs)
	return Board.objects.create(
		name=item.name,
		description=item.description,
		is_public=item.is_public,
		owner=item.user,
	)
