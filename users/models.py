from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models
from identy import random as avatar

from base.models import BaseModel
from users.validators import UsernameValidator


class User(AbstractUser, BaseModel):
	first_name = models.CharField(max_length=80)
	username = models.CharField(max_length=24, unique=True, error_messages={
		'unique': 'A user with that username already exists.',
	}, validators=[UsernameValidator()])
	email = models.EmailField(unique=True, error_messages={
		'unique': 'A user with that email already exists.',
	}, validators=[EmailValidator()])
	avatar = models.TextField(default=avatar().png(64).base64str())
	is_confirmed = models.BooleanField(default=False)
	exports = BaseModel.exports + [
		'first_name', 'last_name', 'email', 'username', 'is_confirmed',
		'avatar', 'owned_teams', 'member_of', 'owned_boards',
		'favorite_boards', 'assigned_cards', 'authored_comments'
	]

	REQUIRED_FIELDS = ['email', 'password']

	def get_short_name(self):
		return self.first_name or self.username

	def __str__(self):
		return self.username
