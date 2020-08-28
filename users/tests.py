from boards.actions import create_board
from cards.actions import create_list, create_card
from core.api.status import SUCCESS
from core.api.test_cases import WithUser


class TestUser(WithUser):
	def test_assign(self) -> None:
		self.board = create_board(
			name=self.fake.first_name(),
			user=self.user,
		)
		self.list = create_list(
			index=0,
			title=self.fake.first_name(),
			board=self.board,
		)
		self.card = create_card(
			index=0,
			text=self.fake.first_name(),
			list=self.list,
		)
		self.jwt_auth(
			username=self.user.username,
			password=self.password,
		)
		path = f'users/{self.user.username}/assign/'
		self.assertEqual(self.api_post(path, {
			'uuid': self.card.uuid
		}).status_code, SUCCESS, 'Should assign a card to a user')

		self.assertNotEqual(self.api_post(path, {
			'uuid': self.card.uuid
		}).status_code, SUCCESS, 'Should not double assign a card to a user')
