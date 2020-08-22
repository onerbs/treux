from django.urls import path, include

urlpatterns = [
	path('token/', include('core.auth.token')),
	path('default/', include('core.auth.default')),
]
