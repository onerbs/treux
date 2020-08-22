from django.contrib.auth import get_user_model, authenticate, login, logout
from django.urls import path
from rest_framework.decorators import api_view

from core import success, resource_not_found
from core.postman import send_reset_pass_email


@api_view(['POST'])
def default_login(request):
	if not request.user.is_authenticated:
		user = authenticate(
			request,
			username=request.data['username'],
			password=request.data['password'],
		)
		if user is None:
			return resource_not_found('User')
		login(request, user)
	return success('You\'ve logged in.')


@api_view(['GET'])
def default_logout(request):
	logout(request)
	return success('You\'ve logged out.')


@api_view(['POST'])
def reset_pass(request):
	user_model = get_user_model()
	if email := request.data.get('email'):
		if user := user_model.objects.get(email=email):
			if send_reset_pass_email(user) > 0:
				return success('Email sent.')
		return resource_not_found('User')
	#
	uuid = request.data.get('uuid')
	password = request.data.get('password')
	confirmation = request.data.get('confirmation')
	if password and confirmation and password == confirmation:
		if not (user := user_model.objects.get(uuid=uuid)):
			return resource_not_found('User')
		user.set_password(password)
		return success('The password has changed.')


urlpatterns = [
	path('login/', default_login),
	path('logout/', default_logout),
	path('reset/', reset_pass),
]
