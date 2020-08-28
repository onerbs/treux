from django.urls import path, include

from core.auth import basic

urlpatterns = [
	path('', basic.AuthView.as_view(), name='auth'),
	path('jwt/', include('core.auth.jwt')),
]
