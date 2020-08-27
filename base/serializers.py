from rest_framework.serializers import ModelSerializer


def serializer(model, fields: list):
	"""Create a serializer for the specified model.

	:param model: The model to be serialized.
	:param fields: The serialized fields.
	"""
	post, put = [], []
	for f in fields:
		if '!' in f:
			post.append(f[1:])
		else:
			post.append(f)
			put.append(f)

	_Serializer = _factory(model, model.exports)
	setattr(_Serializer, 'POST', _factory(model, post))
	setattr(_Serializer, 'PUT', _factory(model, put))

	return _Serializer


def _factory(_model, _fields):
	class _Serializer(ModelSerializer):
		class Meta:
			model = _model
			fields = _fields
	return _Serializer
