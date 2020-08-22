from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet


def serializer(_model):
	"""
	Create a serializer for the specified model.

	:param _model: The model to be serialized.
	"""
	class BaseSerializer(ModelSerializer):
		class Meta:
			model = _model
			fields = _model.exports
			ref_name = _model.__name__

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
