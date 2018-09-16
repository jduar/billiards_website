from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length

from flask_wtf.file import FileField, FileAllowed


class GameForm(FlaskForm):
	name = StringField('Title',
		default='Default Name',
		validators=[DataRequired()])

	password = PasswordField('Password', validators=[Length(min=3, max=8)])
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Create Game')


class EnterGameForm(FlaskForm):
	game_id = StringField('Game ID:',
		default='Insert Number',
		validators=[DataRequired()])

	password = PasswordField('Password')
	submit = SubmitField('Enter Game')
