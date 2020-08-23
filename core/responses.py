from rest_framework.response import Response
from rest_framework.status import *


def respond(message: str, status_code: int, headers=None, exception=False):
	return Response({
		'message': message
	}, status_code, headers=headers, exception=exception)


def success(message='Ok', code=HTTP_200_OK, headers=None):
	return respond(message, code, headers)


def error(message='Error', code=HTTP_400_BAD_REQUEST, headers=None):
	return respond(message, code, headers, True)


def staff_only():
	return error(f'Must be staff to perform this action.', HTTP_403_FORBIDDEN)


class WithResponses:
	@staticmethod
	def kind() -> str:
		return 'Item'

	def created(self):
		return success(f'{self.kind()} created.', HTTP_201_CREATED)

	def updated(self):
		return success(f'{self.kind()} updated.', HTTP_200_OK)

	def deleted(self, *, hard=False):
		message = f'{self.kind()} {"destroyed" if hard else "deleted"}.'
		return success(message, HTTP_204_NO_CONTENT)

	def undeleted(self):
		return success(f'{self.kind()} undeleted.', HTTP_200_OK)

	def not_found(self):
		return error(f'{self.kind()} not found.', HTTP_404_NOT_FOUND)

	@staticmethod
	def broken_reference(item: str):
		return error(f'Broken reference to {item}.')
