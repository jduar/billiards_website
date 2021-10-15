import unittest

from flask import url_for

from flaskproject import create_app, db, mail
from flaskproject.models import Game, User

app = create_app()
app.app_context().push()

TEST_DB = "site.db"


class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["DEBUG"] = False
        app.config["SECRET_KEY"] = "213123asd"
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + TEST_DB
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        # Disable sending emails during unit testing
        mail.init_app(app)
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    def register(self, user, email, password, confirm):
        return self.app.post(
            "/register",
            data=dict(
                username=user, email=email, password=password, confirm_password=confirm
            ),
            follow_redirects=True,
        )

    def login(self, email, password):
        return self.app.post(
            "/login", data=dict(email=email, password=password), follow_redirects=True
        )

    def logout_user(self):
        return self.app.get("/logout", follow_redirects=True)

    def test_create_game(self):

        response = self.register(
            "patKen", "patkennedy79@gmail.com", "FlaskIsAwesome", "FlaskIsAwesome"
        )
        response = self.login("patkennedy79@gmail.com", "FlaskIsAwesome")

        game_pw = "1234"
        response = self.app.post(
            "/game/new", data=dict(password=game_pw), follow_redirects=True
        )

        self.assertIn(b"Your game has been created!", response.data)
        self.assertFalse(Game.query.all() == [])

    def test_delete_game(self):

        response = self.register(
            "patKen", "patkennedy79@gmail.com", "FlaskIsAwesome", "FlaskIsAwesome"
        )
        response = self.login("patkennedy79@gmail.com", "FlaskIsAwesome")

        game_pw = "1234"
        response = self.app.post(
            "/game/new", data=dict(password=game_pw), follow_redirects=True
        )

        response = self.app.post(
            url_for("game.game_delete", game_id=Game.query.first().id),
            data=dict(password=game_pw),
            follow_redirects=True,
        )

        self.assertIn(b"Your game has been created!", response.data)
        self.assertTrue(Game.query.all() == [])

    def test_add_game(self):
        user = User(username="aaa", email="aaa@gmail.com")
        user.set_password("aaaa")
        user1 = User(username="aaa1", email="aaa1@gmail.com")
        user1.set_password("bbbb")
        game = Game(title="test", password="1")  # noqa: S106

        db.session.add(user)
        db.session.add(user1)
        db.session.add(game)

        game.players.append(user)
        game.players.append(user1)

        db.session.commit()

        self.assertEqual(game, user.games[0])
        self.assertEqual(game, user1.games[0])

        game.players.remove(user)
        result = []
        for player in game.players:
            result.append(player)

        self.assertEqual([user1], result)

    def test_del(self):
        user = User(username="aaa", email="aaa@gmail.com")
        user.set_password("aaaa")
        user1 = User(username="aaa1", email="aaa1@gmail.com")
        user1.set_password("bbbb")
        game = Game(title="test", password="1")  # noqa: S106

        db.session.add(user)
        db.session.add(user1)
        db.session.add(game)

        game.players.append(user)
        game.players.append(user1)

        db.session.commit()

        self.assertEqual(game, user.games[0])
        self.assertEqual(game, user1.games[0])

        game.players.remove(user)

        self.assertEqual([player for player in game.players], [user1])
        self.assertEqual([game for game in user.games], [])

        game.players.append(user)

        db.session.commit()

        db.session.delete(game)

        self.assertEqual([game for game in user.games], [])


if __name__ == "__main__":
    unittest.main()
