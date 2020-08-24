from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import GenericViewSet

from core.decorators import check_fields
from core.responses import *


def serializer(_model, _post_fields: list, _put_fields: list = None):
	"""
	Create a serializer for the specified model.

	:param _model: The model to be serialized.
	:param _post_fields: The fields for the POST method.
	:param _put_fields: The fields for the PUT method. This extends POST.
	"""
	if _put_fields := (_post_fields + (_put_fields or [])):
		_put_fields.sort()
		for field in _put_fields:
			if field.startswith('!'):
				_put_fields.remove(field)
				_put_fields.remove(field[1:])

	_Serializer = _serializer(_model, _model.exports)
	_Serializer.POST = _serializer(_model, _post_fields)
	_Serializer.PUT = _serializer(_model, _put_fields)

	return _Serializer


def _meta(_model, _fields):
	class _Meta:
		model = _model
		fields = _fields
		ref_name = _model.__name__
	return _Meta


def _serializer(_model, _fields):
	class _Serializer(ModelSerializer):
		Meta = _meta(_model, _fields)
	return _Serializer


# ----------------------------------------------------------------------


def viewset(_model, _serializer, _permissions=None):
	"""
	Create a set of views for the specified model.

	:param _model: The model.
	:param _serializer: The model serializer.
	:param _permissions: The list of permission classes.
	"""
	if _permissions is None:
		_permissions = [IsAuthenticated]

	class _ViewSet(
		mixins.RetrieveModelMixin,
		mixins.UpdateModelMixin,
		mixins.ListModelMixin,
		GenericViewSet,
		WithResponses,
	):
		queryset = _model.objects.all()
		serializer_class = _serializer
		permission_classes = _permissions

		@staticmethod
		def kind() -> str:
			return _model.__name__

		def create(self):
			return error(self.name + ' not created.', HTTP_501_NOT_IMPLEMENTED)

		@check_fields([], ['force'])
		def destroy(self, request, **kwargs):
			item = self.get_object()
			is_staff = request.user.is_staff
			kwargs.pop('pk')
			return item.delete(is_staff, force=request.force, **kwargs)

		def get_serializer_class(self):
			if self.request.method == 'POST':
				return self.serializer_class.POST
			if self.request.method == 'PUT':
				return self.serializer_class.PUT
			return self.serializer_class

		def get_queryset(self):
			if self.request.user.is_staff:
				return super().get_queryset()
			else:
				return self.queryset.filter(deleted_at=None)

	return _ViewSet
