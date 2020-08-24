from django.db import models

from base.models import BaseModel, extends
from cards.models import Card
from users.models import User


class Comment(BaseModel):
	text = models.TextField()
	history = models.TextField()
	author = models.ForeignKey(
		User, models.DO_NOTHING, 'authored_comments', editable=False)
	target = models.ForeignKey(
		Card, models.CASCADE, 'comments', editable=False)
	exports = extends(BaseModel, 'text', 'author', 'history')

	def __str__(self):
		return '"%s"' % peek(self.text, 50)


def peek(text: str, length: int) -> str:
	if len(text) < length:
		return text
	words = text.split(' ')
	result = words.pop(0)
	if len(result) > length:
		result = result[:length]
	while len(result) < length:
		result += f' {words.pop(0)}'
	return result + '...'
