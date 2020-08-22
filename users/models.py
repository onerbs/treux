from django.contrib.auth.models import AbstractUser
from django.db import models
from identy import random as avatar

from base.models import BaseModel, extends
from users.validators import UsernameValidator


class User(AbstractUser, BaseModel):
	first_name = models.CharField(max_length=50)
	username = models.CharField(max_length=32, unique=True, error_messages={
		'unique': 'A user with that username already exists.',
	}, validators=[UsernameValidator()])
	email = models.EmailField(unique=True, error_messages={
		'unique': 'A user with that email already exists.',
	})
	avatar = models.TextField(default=avatar().png(64).base64str())
	is_confirmed = models.BooleanField(default=False)
	exports = extends(
		BaseModel, 'first_name', 'last_name', 'username', 'email', 'avatar',
		'is_confirmed', 'owned_teams', 'member_of', 'owned_boards',
		'favorite_boards', 'assigned_cards', 'authored_comments'
	)

	REQUIRED_FIELDS = ['email', 'password']

	def get_short_name(self):
		return self.first_name or self.username

	def __str__(self):
		return self.get_full_name() or self.username
