from base import viewset
from core import created
from teams.models import Team
from teams.serializers import TeamSerializer


class TeamViewSet(viewset(Team, TeamSerializer)):
	@staticmethod
	def create(request, *args, **kwargs):
		team = Team.objects.create(
			name=request.data.get('name'),
			description=request.data.get('description'),
			owner=request.user,
		)
		team.members.add(request.user)
		team.save()
		return created('Team')
