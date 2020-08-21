from django.db import models

from base.models import NamedModel
from boards.models import Board
from users.models import User


class List(NamedModel):
	index = models.PositiveIntegerField()
	of_board = models.ForeignKey(Board, models.CASCADE, 'lists')


class Card(NamedModel):
	index = models.PositiveIntegerField()
	of_list = models.ForeignKey(List, models.CASCADE, 'cards')
	assigned_to = models.ManyToManyField(User, 'assigned_cards')
	expires_at = models.DateTimeField(null=True, default=None)
