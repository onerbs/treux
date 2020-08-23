from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet


def _meta(_model, _fields):
	class _Meta:
		model = _model
		fields = _fields
		ref_name = _model.__name__
	return _Meta


def serializer(_model, _post_fields: list, _put_fields: list = None):
	"""
	Create a serializer for the specified model.

	:param _model: The model to be serialized.
	:param _post_fields: The fields for the POST method.
	:param _put_fields: The fields for the PUT method. This extends POST.
	"""
	class BaseSerializer(ModelSerializer):
		Meta = _meta(_model, _model.exports)

		class POST(ModelSerializer):
			Meta = _meta(_model, _post_fields)

		class PUT(ModelSerializer):
			Meta = _meta(_model, _put_fields)

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
		queryset = _model.objects.all()
		serializer_class = _serializer
		permission_classes = _permissions

		def get_serializer_class(self):
			if self.request.method == 'POST':
				return _serializer.POST
			if self.request.method == 'PUT':
				return _serializer.PUT
			return _serializer

		def get_queryset(self):
			queryset = super().get_queryset()
			return queryset.filter(deleted_at=None)

	return BaseViewSet
