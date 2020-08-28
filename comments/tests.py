from datetime import datetime
from unittest import TestCase

from comments.encoder import encode, decode


class TestCommentEncoder(TestCase):
	def setUp(self) -> None:
		timestamp = datetime.now().timestamp()
		self.comment = ('Lorem Ipsum', timestamp)

	def test_encoder(self):
		self.assertEqual(self.comment, decode(encode(*self.comment)))
