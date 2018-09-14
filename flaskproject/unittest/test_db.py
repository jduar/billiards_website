from flaskproject.models import User, Game
from flaskproject.games.routes import delete
import unittest

class TestDb(unittest.TestCase):
	def test_add_game(self):
		user = User(username='aaa', email='aaa@gmail.com',password='aaaa')
		user1 = User(username='aaa1', email='aaa1@gmail.com',password='aaaa')
		game = Game(title='test')

		db.session.add(user)
		db.session.add(user1)
		db.session.add(game)

		game.players.append(user)
		game.players.append(user1)

		db.session.commit()

		self.assertEqual(game, user.games[0])
		self.assertEqual(game, user1.games[0])

		result = []
		for player in game.players:
			result.append(player)
		self.assertEqual([user, user1], result)


	def test_del_game(self):
		game = Game.query.first()
		delete(game)