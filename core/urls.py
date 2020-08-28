from django.urls import path, include

urlpatterns = [
	path('auth/', include('core.auth.urls')),
	path('', include('core.accounts.urls')),
	path('', include('core.docs')),
]
