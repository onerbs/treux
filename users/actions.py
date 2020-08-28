from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from xu import string

from core.postman import send_confirmation_email
from core.responses import WithResponses, Response
from core.util import create_item

self = WithResponses()


def create_user(item=None, **kwargs):
	user_model = get_user_model()
	if item is None:
		item = create_item(**kwargs)
	return user_model.objects.create_user(
		next_username(),
		item.email, item.password,
		first_name=item.first_name,
		last_name=item.last_name,
	)


def create_user_to_response(request) -> Response:
	try:
		validate_email(request.email)
		validate_password(request.password)
		if user := create_user(item=request):
			send_confirmation_email(user)
		return self.created(user, ['username'])
	except Exception as ex:
		return self.fail(str(ex))


def next_username() -> str:
	return ('u%sx%s' % (
		string(4).hex.next(),
		string(2).hex.next(),
	)).lower()
