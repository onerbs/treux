from unittest import TestCase

from core.util import peek


class TestCommentPeek(TestCase):
	def setUp(self) -> None:
		self.text_1 = 'Lorem ipsum dolor site, consectetur adipiscing elit.'
		self.text_2 = 'NullaInEstVehiculaPosuereNisiSitAmetUltricesAnte.'

	def test_peek(self):
		self.assertEqual(peek(self.text_1, 20), 'Lorem ipsum dolor site,...')
		self.assertEqual(peek(self.text_2, 20), 'NullaInEstVehiculaPo...')
