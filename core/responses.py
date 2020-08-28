from rest_framework.response import Response

from core.api.status import *


class WithResponses:
	@staticmethod
	def send(*args, **kwargs) -> Response:
		return Response(*args, **kwargs)

	def respond(
		self, msg: str = 'Empty', tag: str = 'detail',
		*args, status=None, **kwargs
	):
		return self.send({tag: msg}, *args, status=status, **kwargs)

	def item(self, action: str, ref=True, status=None, strict=False) -> Response:
		stat = _boolean(ref)
		msg = f'{self.__class__.__name__} {stat + action}'
		if not strict and 'not' in stat:
			status = FAILURE
		return self.respond(msg, status=status)

	def succeed(self, msg: str = None, status: int = SUCCESS) -> Response:
		return self.respond(msg, status=status)

	def fail(self, msg: str = None, status: int = FAILURE) -> Response:
		return self.respond(msg, 'error', status=status)

	def accept(self, msg: str = None) -> Response:
		return self.succeed(msg, ACCEPTED)

	def reject(self, msg: str = None) -> Response:
		return self.fail(msg, REJECTED)

	def forbidden(self, superuser=False) -> Response:
		level = 'manager' if superuser else 'staff'
		msg = f"Must be {level} to perform this action."
		return self.fail(msg, FORBIDDEN)

	def created(self, ref=True, fields=None) -> Response:
		if not ref:
			return self.item('created', False)
		if not fields:
			fields = ['uuid']  # !! uuid.
		data = {f: getattr(ref, f) for f in fields}
		return self.send(data, status=CREATED)

	def updated(self, ref=True) -> Response:
		return self.item('updated', ref, UPDATED)

	def deleted(self, ref=True, /, hard=False) -> Response:
		action = 'destroyed' if hard else 'deleted'
		return self.item(action, ref, DELETED)

	def undeleted(self, ref=True) -> Response:
		return self.item('undeleted', ref, UNDELETED)

	def not_found(self) -> Response:
		return self.item('found', False, NOT_FOUND, True)


def _boolean(ref) -> str:
	return 'not ' if ref in [None, False] else ''
