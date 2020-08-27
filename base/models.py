from uuid import uuid4

from django.db import models

from core.responses import WithResponses


class BaseModel(models.Model, WithResponses):
	uuid = models.UUIDField(default=uuid4(), unique=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	deleted_at = models.DateTimeField(null=True, default=None)
	exports = ['uuid', 'created_at', 'updated_at']

	@property
	def kind(self) -> str:
		"""The readable name of the resource."""
		return self.__class__.__name__

	def rotate_uuid(self):
		"""Assign a new uuid to this resource."""
		self.uuid = uuid4()

	@classmethod
	def get(cls, **kwargs):
		"""Get a resource by identifier key."""
		return cls.objects.filter(deleted_at=None).get(**kwargs)

	@classmethod
	def alive(cls, **kwargs):
		"""Filter the alive resources by the provided criteria."""
		return cls.objects.filter(deleted_at=None, **kwargs)

	def __str__(self):
		return str(self.uuid)

	class Meta:
		abstract = True


class NamedModel(BaseModel):
	name = models.CharField(max_length=150)
	description = models.TextField(blank=True, default='')
	exports = BaseModel.exports + ['name', 'description']

	class Meta:
		abstract = True
