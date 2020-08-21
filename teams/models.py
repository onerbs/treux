from django.db import models

from base import serializer
from base.models import NamedModel
from users.models import User


class Team(NamedModel):
	owner = models.ForeignKey(User, models.CASCADE, 'owned_teams')
	members = models.ManyToManyField(User, 'member_of')


TeamSerializer = serializer(Team, [
	'name', 'description', 'owners', 'members'
])
