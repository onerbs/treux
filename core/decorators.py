import functools

from core.responses import error


def with_required_fields(*required_fields):
	"""Return an error if unfulfilled fields."""
	def wrapper(function):
		@functools.wraps(function)
		def decorated(*args):
			request = args[-1]
			for field in required_fields:
				if not (value := request.data.get(field)):
					return error(f'Missing {field}.')
				setattr(request, field, value)
			return function(*(*args[:-1], request))
		return decorated
	return wrapper
