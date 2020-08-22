from django.urls import path, include

urlpatterns = [
	path('token/', include('.token')),
]
