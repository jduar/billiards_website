from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,BooleanField
from wtforms.validators import DataRequired, Length


class GameForm(FlaskForm):
	title = StringField('Title',
		default='Default Name',
		validators=[DataRequired()])

	password = PasswordField('Password', validators=[Length(min=0, max=8)])
	submit = SubmitField('Create Game')


class EnterGameForm(FlaskForm):
	game_id = StringField('Game ID:',
		default='Insert Number',
		validators=[DataRequired()])

	password = PasswordField('Password')
	submit = SubmitField('Enter Game')
