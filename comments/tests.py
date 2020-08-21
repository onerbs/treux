from datetime import datetime
from unittest import TestCase

from comments import peek
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
		text_1 = 'Hello World'
		text_2 = 'Lorem Ipsum'
		timestamp = datetime.now().timestamp()
		self.tuple_1 = (text_1, timestamp)
		self.tuple_2 = (text_2, timestamp)

	def test_encoder(self):
		self.assertEqual(self.tuple_1, decode(encode(*self.tuple_1)))
		self.assertEqual(self.tuple_2, decode(encode(*self.tuple_2)))
