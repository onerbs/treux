from base import serializer
from teams.models import Team

TeamSerializer = serializer(Team, [
	'name', 'description', 'owners', 'members'
])
