from django.db import models

from base.models import BaseModel, extends
from cards.models import Card
from comments import encoder, peek
from users.models import User


class Comment(BaseModel):
	text = models.TextField()
	history = models.TextField()
	author = models.ForeignKey(
		User, models.DO_NOTHING, 'authored_comments', editable=False)
	target = models.ForeignKey(
		Card, models.CASCADE, 'comments', editable=False)
	exports = extends(BaseModel, 'text', 'author', 'target')

	def get_preview(self, max_length=20):
		text, timestamp = encoder.decode_many(self.history)[-1]
		return '"%s", %s' % (peek(text, max_length), timestamp)

	def __str__(self):
		return self.text
