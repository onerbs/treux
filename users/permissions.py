from rest_framework.permissions import BasePermission


class DefaultPermission(BasePermission):
	def has_permission(self, request, view):
		if request.user.is_staff:
			return True
		if view.kind == 'User':
			if request.method in ['DELETE']:
				return False
		if request.user.is_authenticated:
			return True
		return False

	def has_object_permission(self, request, view, obj):
		if request.user.is_staff or obj == request.user:
			return True
		if view.kind == 'User':
			return False
		if request.user.is_authenticated:
			return True
