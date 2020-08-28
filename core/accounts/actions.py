from rest_framework.decorators import api_view

from core.decorators import without_login, with_fields
from users.actions import create_user_to_response


@api_view(['post'])
@without_login
@with_fields(['email', 'password', 'first_name'], ['last_name'])
def create_account(request):
	return create_user_to_response(request)
