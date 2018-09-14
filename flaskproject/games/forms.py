from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,BooleanField
from wtforms.validators import DataRequired, Length


class GameForm(FlaskForm):
	title = StringField('Title',
		default='Default Name',
		validators=[DataRequired()])

	password = PasswordField('Password', validators=[Length(min=0, max=8)])
	enable_pw = BooleanField('Private Game')
	submit = SubmitField('Create Game')

	def validate_game_form(self, username):
		if self.enable_pw:
			if self.password == '':
				raise DataRequired('Please specify a password.')


class EnterGameForm(FlaskForm):
	game_id = StringField('Game ID:',
		default='Insert Number',
		validators=[DataRequired()])

	password = PasswordField('Password')
	submit = SubmitField('Enter Game')