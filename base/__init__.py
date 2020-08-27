from rest_framework.serializers import ModelSerializer



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
