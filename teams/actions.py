from core.util import create_item
from teams.models import Team


def create_team(item=None, **kwargs):
	if item is None:
		item = create_item(**kwargs)
	return Team.objects.create(
		name=item.name,
		description=item.description,
		owner=item.user,
	)
