import functools
from datetime import datetime

from core.responses import error


def with_reference(model, name: str = None):
	"""Error if the provided uuid isn't related to an existing object."""
	def bridge(function):
		@functools.wraps(function)
		def decorated(*args):
			request = args[-1]
			model_name = model.__name__
			if not (uuid := request.data.get('uuid')):
				return error(f'Missing UUID')
			try:
				instance = model.objects.get(uuid=uuid)
			except:
				return error(f'Broken {model_name} reference.')
			setattr(request, name or model_name.lower(), instance)
			return function(*args[:-1], request)

		return decorated

	return bridge


def check_fields(required: list, optional: list = None):
	"""Error if missing required fields.
	Also injects the named fields into request."""

	def wrapper(function):
		@functools.wraps(function)
		def decorated(*args, **kwargs):
			request, missing_field = _inject(args[-1], required)
			if missing_field:
				return error(f'Missing {missing_field}')
			request, _ = _inject(request, optional)
			return function(*args[:-1], request, **kwargs)

		return decorated

	return wrapper


def _inject(request, fields: list) -> tuple:
	if not fields:
		return request, None
	missing_field = None
	for field in fields:
		if not (value := request.data.get(field)):
			missing_field = field
		if hasattr(request, field):
			return error(f'PollutionError: {field}')
		setattr(request, field, _parse(field, value))
	return request, missing_field


def _parse(name: str, value: str):
	if not value:
		return None
	if name.startswith('is_'):
		return value.lower() in ['on', 'true', '1']
	if name.endswith('_at'):
		if value.endswith('Z'):
			value = value.replace('Z', '+00:00')
		elif 'Z' in value:
			value = value.replace('Z', '')
		return datetime.fromisoformat(value)
	elif name in ['index', 'id'] or name.endswith('_id'):
		return int(value)
	return value
