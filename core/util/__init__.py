from datetime import datetime


class Item:
	"""Placeholder item."""

	def __init__(self):
		object.__setattr__(self, '_items', [])

	@property
	def data(self) -> dict:
		return {it: self[it] for it in self._items}

	def __getattr__(self, key):
		return parse_value(key, '')

	def __getitem__(self, key):
		return getattr(self, key)

	def __setattr__(self, key, value):
		if key not in self._items:
			self._items.append(key)
		object.__setattr__(self, key, value)

	def __setitem__(self, key, value):
		setattr(self, key, value)

	def __str__(self):
		items = '\n\t'.join(f'{k}: {self[k]}' for k in self._items)
		return f'[\n\t{items}\n]'


def create_item(**kwargs) -> Item:
	"""Create a item."""
	_item = Item()
	for k, v in kwargs.items():
		_item[k] = v
	return _item


def parse_value(field: str, value: str):
	if field.startswith('is_'):
		return value.lower() in ['true', 'yes', 'on', '1']
	if field.endswith('_at'):
		if not value:
			return None
		if value.endswith('Z'):
			value = value.replace('Z', '+00:00')
		elif 'Z' in value:
			value = value.replace('Z', '')
		return datetime.fromisoformat(value)
	elif field in ['index']:
		if value == '':
			return 0
		return int(value)
	return value


def peek(text: str, length: int) -> str:
	if len(text) < length:
		return text
	words = text.split(' ')
	result = words.pop(0)
	if len(result) > length:
		result = result[:length]
	while len(result) < length:
		result += f' {words.pop(0)}'
	return result + '...'
