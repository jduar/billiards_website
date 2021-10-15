from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from itsdangerous import BadSignature
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flaskproject import bcrypt, db, login_manager

game_players = db.Table(
    "game-players",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("game_id", db.Integer, db.ForeignKey("game.id")),
)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)

    elo = db.Column(db.Float, default=1200, nullable=False)

    games = db.relationship(
        "Game",
        secondary=game_players,
        lazy="dynamic",
        backref=db.backref("players", lazy="dynamic"),
    )

    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def set_password(self, raw_password: str):
        self.password = bcrypt.generate_password_hash(raw_password).decode("utf-8")

    def get_reset_token(self, expires_sec=18000):
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])

        try:
            user_id = s.loads(token)["user_id"]
        except BadSignature:
            return None

        return User.query.get(user_id)

    def __repr__(self):
        return f"User({self.username}, {self.email} , {self.image_file})"


class Game(db.Model):
    """Base class for a Game between two players.
    Player1 will be the one that creates the game and player2 will be the
    challenged player. The second player id can be null since it can take
    some time for the second user to accept the game. If that is the case then
    the state of the game will be pending.
    It's also possible to add a password to the game if the creator wishes to make
    it a private game.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    image_file = db.Column(db.String(20), nullable=False, default="default.png")

    winner = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"Game({self.name}, {self.date_created})"
