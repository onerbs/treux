from datetime import datetime
from uuid import uuid4

from django.db import models

from core.responses import *


def extends(model, *fields):
	return model.exports + [*fields]


class BaseModel(models.Model, WithResponses):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	deleted_at = models.DateTimeField(null=True, default=None)
	uuid = models.UUIDField(default=uuid4())
	exports = ['created_at', 'updated_at', 'deleted_at', 'uuid']

	def kind(self) -> str:
		return self.__class__.__name__

	def delete(self, is_staff=False, hard_delete=False, *args, **kwargs):
		if hard_delete:
			if not is_staff:
				return staff_only()
			super().delete(*args, **kwargs)
			return self.deleted(hard=True)

		if self.deleted_at is None:
			self.deleted_at = datetime.now()
			self.save(using=kwargs.get('using'))
			return self.deleted()
		else:
			self.deleted_at = None
			self.save(using=kwargs.get('using'))
			return self.undeleted()

	def undelete(self, is_staff=False, **kwargs):
		if not is_staff:
			return staff_only()
		self.deleted_at = None
		self.save(using=kwargs.get('using'))
		return self.undeleted()

	def rotate_uuid(self):
		self.uuid = uuid4()

	class Meta:
		abstract = True


class NamedModel(BaseModel):
	name = models.CharField(max_length=150)
	description = models.TextField(blank=True, default='')
	exports = extends(BaseModel, 'name', 'description')

	def __str__(self):
		return self.name

	class Meta:
		abstract = True
