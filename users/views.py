from rest_framework.decorators import action

from base.views import viewset
from cards.models import Card
from core.decorators import with_params, with_dependency
from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewset(User, UserSerializer)):
	lookup_field = 'username'

	@action(['get'], True)
	@with_params(['uuid'])
	def confirm(self, request, **kwargs):
		try:
			user = User.objects.get(uuid=request.uuid)
			if not user.is_confirmed:
				user.is_confirmed = True
				user.rotate_uuid()
				user.save()
				return self.item('confirmed')
			return self.accept('Already confirmed')
		except User.DoesNotExist:
			return self.not_found()

	@action(['post'], True)
	@with_dependency(Card)
	def assign(self, request, **kwargs):
		user, card = request.user, request.card
		if user.assigned_cards.filter(uuid=card.uuid).exists():
			return self.fail('The card is already assigned')
		user.assigned_cards.add(card)
		user.save()
		return card.item('assigned to user')
