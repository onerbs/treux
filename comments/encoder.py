from base64 import b64encode as _e, b64decode as _d


def encode(text: str, timestamp: float) -> str:
	"""Encode comment into base64 string.

	:param text: The text of the comment.
	:param timestamp: The timestamp of the comment.

	:return: The base64-encoded comment.
	"""
	return '%s:%s' % (_encode(text), _encode(timestamp))


def decode(comment: str) -> tuple:
	"""Decode base64 string into comment.

	:param comment: The base64-encoded comment.

	:return: The decoded comment (text, timestamp).
	"""
	text, timestamp = comment.split(':', 1)
	return _decode(text), _decode(timestamp)


def encode_many(comments: list) -> str:
	"""Encode many comments into base64 string.

	:param comments: The source list of comments.

	:return: The base64-encoded list of comments.
	"""
	return ';'.join(encode(text, timestamp) for text, timestamp in comments)


def decode_many(comments: str) -> list:
	"""Decode base64 string into many comments.

	:param comments: The base64-encoded list of comments.

	:return: The decoded list o comments [(text, timestamp)].
	"""
	return [decode(comment) for comment in comments.split(';')]


def _encode(src: str or float) -> str:
	return _e(str(src).encode()).decode()


def _decode(src: str) -> str or float:
	decoded = _d(src).decode()
	try:
		return float(decoded)
	except ValueError:
		return decoded
