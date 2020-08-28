from django.conf.urls import url
from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

from treux.settings import SITE_EMAIL, base

schema_view = get_schema_view(
	openapi.Info(
		title="Treux API",
		default_version='v1',
		description=open(base('docs', 'README.md')).read(),
		contact=openapi.Contact(email=SITE_EMAIL),
	),
	permission_classes=(AllowAny,),
	public=True,
)

urlpatterns = [
	path('docs/', schema_view.with_ui('redoc'), name='docs'),
	url(r'^schema(?P<format>\.json|\.yaml)$', schema_view.without_ui()),
]
