from base import serializer
from teams.models import Team


class TeamSerializer(serializer(Team, [
	'name', 'description', 'owner', 'members'
])):
	pass
