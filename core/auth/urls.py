from django.urls import path, include

urlpatterns = [
	path('', include('core.auth.default')),
	path('token/', include('core.auth.token')),
]
