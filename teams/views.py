from base import viewset
from core.decorators import check_fields
from teams.models import Team
from teams.serializers import TeamSerializer


class TeamViewSet(viewset(Team, TeamSerializer)):
	@check_fields(['name'], ['description'])
	def create(self, request):
		team = Team.objects.create(
			name=request.name,
			description=request.description,
			owner=request.user,
		)
		team.members.add(request.user)
		team.save()
		return self.created()
