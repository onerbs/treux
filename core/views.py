from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view

from core import error, success, resource_not_found


@api_view(['GET'])
def user_confirm(request):
	if not (uuid := request.query_params.get('u')):
		return resource_not_found()
	user_model = get_user_model()
	try:
		user = user_model.objects.get(uuid=uuid)
		user.is_confirmed = True
		user.rotate_uuid()
		user.save()
		return success('User confirmed.')
	except user_model.DoesNotExist:
		return error('User does not exist.')


@api_view(['POST'])
def user_reset_password(request):
	password = request.data.get('password')
	confirmation = request.data.get('confirmation')
	if not (password and confirmation and password == confirmation):
		return error('Passwords does not match or empty.')
	uuid = request.data.get('uuid')
	user_model = get_user_model()
	try:
		user = user_model.objects.get(uuid=uuid)
		user.set_password(password)
		user.save()
		return success('The password has changed.')
	except user_model.DoesNotExist:
		return error('User does not exist.')
