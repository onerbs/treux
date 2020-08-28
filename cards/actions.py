from cards.models import List, Card
from core.util import create_item


def create_list(item=None, **kwargs):
	if item is None:
		item = create_item(**kwargs)
	return List.objects.create(
		index=item.index,
		title=item.title,
		of_board=item.board,
	)


def create_card(item=None, **kwargs):
	if item is None:
		item = create_item(**kwargs)
	return Card.objects.create(
		index=item.index,
		text=item.text,
		expires_at=item.expires_at,
		of_list=item.list,
	)
