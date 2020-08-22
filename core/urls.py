from django.urls import path, include

urlpatterns = [
	path('auth/', include('core.auth')),
	path('', include('core.docs')),
]
