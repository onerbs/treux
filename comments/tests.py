from datetime import datetime
from unittest import TestCase

from comments.models import peek
from comments.encoder import encode, decode


class TestCommentPeek(TestCase):
	def setUp(self) -> None:
		self.text_1 = 'Lorem ipsum dolor site, consectetur adipiscing elit.'
		self.text_2 = 'NullaInEstVehiculaPosuereNisiSitAmetUltricesAnte.'

	def test_peek(self):
		self.assertEqual(peek(self.text_1, 20), 'Lorem ipsum dolor site,...')
		self.assertEqual(peek(self.text_2, 20), 'NullaInEstVehiculaPo...')


class TestCommentEncoder(TestCase):
	def setUp(self) -> None:
		timestamp = datetime.now().timestamp()
		self.comment = ('Lorem Ipsum', timestamp)

	def test_encoder(self):
		self.assertEqual(self.comment, decode(encode(*self.comment)))
