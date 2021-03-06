from django.db import models

from base.models import NamedModel
from users.models import User


class Team(NamedModel):
	owner = models.ForeignKey(User, models.CASCADE, 'owned_teams')
	members = models.ManyToManyField(User, 'member_of')
	exports = NamedModel.exports + ['members']
