from datetime import datetime

from rest_framework.viewsets import GenericViewSet, mixins

from core.decorators import with_fields
from core.responses import WithResponses
from users.permissions import Default


def viewset(_model, serializer, permissions: list = None):
	if permissions is None:
		permissions = [Default]

	class _ViewSet(BaseViewSet):
		queryset = _model.objects.all()
		serializer_class = serializer
		permission_classes = permissions
		kind = _model.__name__

	return _ViewSet


class BaseViewSet(
	mixins.RetrieveModelMixin,
	mixins.UpdateModelMixin,
	mixins.ListModelMixin,
	GenericViewSet,
	WithResponses
):
	lookup_field = 'uuid'

	def create(self, *args, **kwargs):
		"""Not implemented."""
		return self.fail(status=501)

	@with_fields([], ['is_forever'])
	def destroy(self, request, **kwargs):
		"""Soft delete/undelete or destroy completely a resource.

		**Note**:
			Only superusers are granted to destroy elements
			from the database.
		"""
		item = self.get_object()
		kwargs.pop(self.lookup_field)
		if request.is_forever is True:
			if not request.user.is_superuser:
				return self.forbidden(True)
			item.delete(**kwargs)
			return self.deleted(hard=True)

		using = kwargs.pop('using')
		if item.deleted_at is None:
			item.deleted_at = datetime.now()
			item.save(using=using)
			return self.deleted()
		else:
			item.deleted_at = None
			item.save(using=using)
			return self.undeleted()

	def get_serializer_class(self):
		method = self.request.method
		if hasattr(self.serializer_class, method):
			return getattr(self.serializer_class, method)
		return self.serializer_class

	def get_queryset(self):
		if self.request.user.is_staff:
			return self.queryset
		else:
			return self.queryset.filter(deleted_at=None)
