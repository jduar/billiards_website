'''

from flaskproject import create_app
from flaskproject.__init__ import db
from flaskproject.models import current_app, User, Post, Game
app = create_app()
app.app_context().push()

user = User( username = 'aaa' , email = 'aaa@gmail.com')
user1 = User( username = 'aaa1' , email = 'aaa1@gmail.com')

game = Game(title = 'test')

game.players.append(user)
game.players.append(user1)


'''


from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskproject import db, login_manager
from datetime import datetime
from flask_login import UserMixin


game_players = db.Table('game-players',
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                        db.Column('game_id', db.Integer, db.ForeignKey('game.id'))
                        )


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20), unique = True, nullable = False)
	email = db.Column(db.String(120), unique = True, nullable = False)

	image_file = db.Column(db.String(20), nullable = False, default='default.jpg')
	password = db.Column(db.String(60), nullable = False)

	posts = db.relationship('Post', backref='author', lazy = True)

	elo = db.Column(db.Float, nullable = True)
	games = db.relationship('Game', secondary=game_players, backref = db.backref('players', lazy = True))

	def get_reset_token(self, expires_sec = 18000):
		s = Serializer(current_app.config['SECRET_KEY'],expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])

		try:
			user_id = s.loads(token)['user_id']
		except:
			return None

		return User.query.get(user_id)

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
	id = db.Column(db.Integer, primary_key=True)

	title = db.Column(db.String(100), unique=True, nullable=False)

	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	winner_id = db.Column(db.Integer, nullable=True)

	password = db.Column(db.String(60), nullable=True)

	def __repr__(self):
		return f"Game({self.title}, {self.date_created})"
