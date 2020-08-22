from django.db import models

from base.models import BaseModel, extends
from boards.models import Board
from users.models import User


class List(BaseModel):
	index = models.PositiveIntegerField()
	title = models.CharField(max_length=100)
	of_board = models.ForeignKey(Board, models.CASCADE, 'lists')
	exports = extends(BaseModel, 'index', 'title', 'of_board')


class Card(BaseModel):
	index = models.PositiveIntegerField()
	text = models.TextField()
	of_list = models.ForeignKey(List, models.CASCADE, 'cards')
	assigned_to = models.ManyToManyField(User, 'assigned_cards')
	expires_at = models.DateTimeField(null=True, default=None)
	exports = extends(
		BaseModel,
		'index', 'text', 'of_list', 'assigned_to', 'expires_at'
	)
