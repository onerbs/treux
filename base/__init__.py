from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet


def serializer(m, f: list):
	"""
	Create a serializer for the specified model.

	:param m: The model to be serialized.
	:param f: The list of fields to serialize.
	"""
	class BaseSerializer(ModelSerializer):
		class Meta:
			model = m
			fields = f + ['uuid', 'created_at', 'updated_at', 'deleted_at']

	return BaseSerializer


def viewset(m, s, p=None):
	"""
	Create a set of views for the specified model.

	:param m: The model.
	:param s: The model serializer.
	:param p: The list of permission classes.
	"""
	if p is None:
		p = [IsAuthenticated]

	class BaseViewSet(ModelViewSet):
		queryset = m.objects.filter(deleted_at=None)
		serializer_class = s
		permission_classes = p

	return BaseViewSet
