from datetime import datetime

from comments import encoder
from comments.models import Comment
from core.util import create_item


def create_comment(item=None, **kwargs):
	if item is None:
		item = create_item(**kwargs)
	return Comment.objects.create(
		text=item.text,
		history=encoder.encode(
			item.text, datetime.now().timestamp()
		),
		author=item.user,
		target=item.card,
	)
