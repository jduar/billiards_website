from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class GameForm(FlaskForm):
    name = StringField("Title", default="Default Name", validators=[DataRequired()])

    password = PasswordField("Password", validators=[Length(min=3, max=8)])
    picture = FileField(
        "Update Profile Picture", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Create Game")


class EnterGameForm(FlaskForm):
    game_id = StringField(
        "Game ID:", default="Insert Number", validators=[DataRequired()]
    )

    password = PasswordField("Password")
    submit = SubmitField("Enter Game")


class WinnerForm(FlaskForm):
    group_id = SelectField(
        u"group_id", choices=[], validators=[DataRequired()], coerce=int
    )
    submit = SubmitField("Add result")
