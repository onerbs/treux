from datetime import datetime
from uuid import uuid4

from django.db import models


def extends(model, *fields):
	return model.exports + [*fields]


class BaseModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	deleted_at = models.DateTimeField(null=True, default=None)
	uuid = models.UUIDField(default=uuid4())
	exports = ['created_at', 'updated_at', 'deleted_at', 'uuid']

	def delete(self, using=None, keep_parents=False):
		# todo: respect {keep_parents}.
		self.deleted_at = datetime.now()
		self.save(using=using)

	def recover(self, using=None):
		self.deleted_at = None
		self.save(using=using)

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
