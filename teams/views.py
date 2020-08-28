from base.views import viewset
from core.decorators import with_fields
from teams.actions import create_team
from teams.models import Team
from teams.serializers import TeamSerializer


class TeamViewSet(viewset(Team, TeamSerializer)):
	@with_fields(['name'], ['description'])
	def create(self, request):
		if team := create_team(request):
			team.members.add(request.user)
			team.save()
		return self.created(team)
