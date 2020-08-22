from django.urls import path, include

from core import views

urlpatterns = [
	path('auth/', include('core.auth')),
	path('confirm/', views.user_confirm),
	path('reset/', views.user_reset_password),
	path('', include('core.docs')),
]
