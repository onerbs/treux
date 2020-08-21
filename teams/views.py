from base import viewset
from core.generics import create_resource
from teams.models import Team
from teams.serializers import TeamSerializer


class TeamViewSet(viewset(Team, TeamSerializer)):
	def create(self, request, *args, **kwargs):
		print(request.user)
		team = Team.objects.create(
			name=request.data.get('name'),
			description=request.data.get('description'),
			owner=request.user,
		)
		team.members.add(request.user)
		return create_resource(self, TeamSerializer(team))
