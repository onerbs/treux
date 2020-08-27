from rest_framework.serializers import StringRelatedField

from base.serializers import serializer
from teams.models import Team


class TeamSerializer(serializer(Team, ['name', 'description'])):
	members = StringRelatedField(many=True)
