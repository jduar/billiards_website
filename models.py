from flaskproject import db
from datetime import datetime

game_players = db.Table('game-player',
						db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
						db.Column('game_id', db.Integer, db.ForeignKey('game.id')))

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20), unique = True, nullable = False)
	email = db.Column(db.String(120), unique = True, nullable = False)

	image_file = db.Column(db.String(20), nullable = False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)

	posts = db.relationship('Post', backref='author', lazy=True)

	games = db.relationship('Game', secondary=game_players, backref=db.backref('players', lazy='dynamic'))

	def __repr__(self):
		return f"User({self.username}, {self.email} , {self.image_file})"


class Post(db.Model):

	id = db.Column(db.Integer, primary_key = True)

	title = db.Column(db.String(100), unique = True, nullable = False)

	date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
	content = db.Column(db.Text, nullable = False)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

	def __repr__(self):
		return f"Post({self.title}, {self.date_posted})"


class Game(db.Model):
	''' Base class for a Game between two players.
		Player1 will be the one that creates the game and player2 will be the challenged player. The second player id
	can be null since it can take some time for the second user to accept the game. If that is the case then the state
	of the game will be pending.
		It's also possible to add a password to the game if the creator wishes to make it a private game.
	'''

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), unique=False, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	def __repr__(self):
		return f"Post({self.title}, {self.date_posted})"


