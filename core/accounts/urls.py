from django.urls import path

from core.accounts import actions

urlpatterns = [
	path('join/', actions.create_account, name='join'),
]
