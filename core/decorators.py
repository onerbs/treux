import functools
from datetime import datetime

from rest_framework.request import Request

from core.responses import error


def check_fields(required_fields: list, fields: list = None):
	"""Error if missing required fields.
	Also injects the named fields into request."""

	def wrapper(function):
		@functools.wraps(function)
		def decorated(*args):
			request, missing_field = _inject(args[-1], required_fields)
			if missing_field:
				return error(f'Missing {missing_field}')
			if fields is not None:
				request, _ = _inject(request, fields)
			return function(*args[:-1], request)

		return decorated

	return wrapper


def _inject(request: Request, fields: list) -> tuple:
	missing_field = None
	for field in fields:
		if not (value := request.data.get(field)):
			missing_field = field
			return request, missing_field
		setattr(request, field, _parse(field, value))
	return request, missing_field


def _parse(name: str, value: str):
	if value is None:
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
