import functools

from core.responses import WithResponses, Response
from core.util import parse_value

self = WithResponses()


def missing(field: str) -> Response:
	return self.fail(f'Missing {field}')


def without_login(fn):
	@functools.wraps(fn)
	def enhanced(*args):
		if args[-1].user.is_authenticated:
			return self.accept('Already logged in')
		return fn(*args)

	return enhanced


def with_dependency(model):
	"""Error if the provided uuid isn't related to an existing object."""

	def bridge(fn):
		@functools.wraps(fn)
		def enhanced(*args, **kwargs) -> Response:
			request = args[-1]
			field = 'uuid'  # !! uuid.
			kind = model.__name__.lower()
			if not (_value := request.data.get(field)):
				return missing(field)
			try:
				item = model.find(**{field: _value})
			except:
				return self.fail(f'Wrong {kind} {field}')
			setattr(request, kind, item)
			return fn(*args[:-1], request, **kwargs)

		return enhanced

	return bridge


def with_fields(required: list, optional: list = None):
	"""Error if missing required fields.
	Also injects the named fields into request."""

	def bridge(fn):
		@functools.wraps(fn)
		def enhanced(*args, **kwargs) -> Response:
			request, field = _inject(args[-1], 'data', required)
			if field is not None:
				return missing(field)
			request, _ = _inject(request, 'data', optional)
			return fn(*args[:-1], request, **kwargs)

		return enhanced

	return bridge


def with_params(params: list = None):
	"""Inject the named query params into request."""

	def bridge(fn):
		@functools.wraps(fn)
		def enhanced(*args, **kwargs) -> Response:
			request, field = _inject(args[-1], 'query_params', params)
			if field is not None:
				return missing(field)
			return fn(*args[:-1], request, **kwargs)

		return enhanced

	return bridge


def _inject(request, store_name: str, fields: list) -> tuple:
	if not fields:
		return request, None
	missing_field = None
	store = getattr(request, store_name)
	for field in fields:
		if not (value := store.get(field, '')):
			missing_field = field
		setattr(request, field, parse_value(field, value))
	return request, missing_field
