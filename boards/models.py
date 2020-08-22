from django.db import models

from base.models import NamedModel, extends
from users.models import User


class Board(NamedModel):
	owner = models.ForeignKey(User, models.CASCADE, 'owned_boards')
	is_public = models.BooleanField(default=False)
	favorite_of = models.ManyToManyField(User, 'favorite_boards')
	exports = extends(NamedModel, 'owner', 'is_public', 'favorite_of', 'lists')
