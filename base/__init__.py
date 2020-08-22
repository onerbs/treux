from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet


def serializer(_model, _post_fields: list = None):
	"""
	Create a serializer for the specified model.

	:param _model: The model to be serialized.
	:param _post_fields: The fields for the POST method.
	"""
	class BaseSerializer(ModelSerializer):
		class Meta:
			model = _model
			fields = _model.exports
			ref_name = _model.__name__

		class POST(ModelSerializer):
			class Meta:
				model = _model
				fields = _post_fields
				ref_name = _model.__name__

	return BaseSerializer


def viewset(_model, _serializer, _permissions=None):
	"""
	Create a set of views for the specified model.

	:param _model: The model.
	:param _serializer: The model serializer.
	:param _permissions: The list of permission classes.
	"""
	if _permissions is None:
		_permissions = [IsAuthenticated]

	class BaseViewSet(ModelViewSet):
		queryset = _model.objects.filter(deleted_at=None)
		serializer_class = _serializer
		permission_classes = _permissions

		def get_serializer_class(self):
			if self.request.method == 'POST':
				return _serializer.POST
			return _serializer

	return BaseViewSet
