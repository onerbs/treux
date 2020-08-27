from django.db import models

from base.models import BaseModel
from cards.models import Card
from users.models import User


class Comment(BaseModel):
	text = models.TextField()
	history = models.TextField()
	author = models.ForeignKey(
		User, models.DO_NOTHING, 'authored_comments', editable=False)
	target = models.ForeignKey(
		Card, models.CASCADE, 'comments', editable=False)
	exports = BaseModel.exports + ['text', 'author', 'target']
