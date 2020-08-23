from django.contrib.auth import get_user_model, authenticate, login, logout
from django.urls import path
from rest_framework.decorators import api_view

from core.decorators import check_fields, with_reference
from core.postman import send_reset_pass_email
from core.responses import *


@api_view(['POST'])
@check_fields(['identifier', 'password'])
def default_login(request):
	if request.user.is_authenticated:
		return respond('Already logged in.', HTTP_202_ACCEPTED)
	try:
		if not (user := authenticate(
			request,
			identifier=request.identifier,
			password=request.password,
		)):
			return respond('Invalid credentials', HTTP_403_FORBIDDEN)
		login(request, user)
		return success('Logged in.')
	except get_user_model().DoesNotExist:
		return error('User does not exist.')


@api_view(['GET'])
def default_logout(request):
	if not request.user.is_authenticated:
		return error('Invalid session.')
	logout(request)
	return success('Logged out.')


@api_view(['POST'])
@check_fields(['email'])
def reset_pass(request):
	user_model = get_user_model()
	if user := user_model.objects.get(email=request.email):
		send_reset_pass_email(user)
		return success('Email sent.')
	return user.not_found()


@api_view(['POST'])
@with_reference(get_user_model(), 'user')
@check_fields(['password', 'confirmation'])
def change_pass(request):
	if request.password == request.confirmation:
		request.user.set_password(request.password)
		return success('The password has changed.')


urlpatterns = [
	path('login/', default_login),
	path('logout/', default_logout),
	path('reset/', reset_pass),
]
