from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskproject import db, bcrypt
from flaskproject.models import Game
from flaskproject.games.forms import GameForm, EnterGameForm

games = Blueprint('games', __name__)


@games.route("/game/new", methods=['GET', 'POST'])
@login_required
def create_game():
    form = GameForm()

    if form.validate_on_submit():
        if form.password.data == '':
            game = Game(title=form.title.data, password=None)
        else:
            hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            game = Game(title=form.title.data, password=hashed_pw)

        game.players.append(current_user)

        db.session.add(game)
        db.session.commit()

        return redirect(url_for('games.view_game'))

    return render_template('create_game.html', title='New game', form=form, legend='Create' )


@games.route("/game/<int:game_id>/enter", methods=['GET', 'POST'])
@login_required
def enter_game(game_id):
    game = Game.query.get_or_404(game_id)

    form = EnterGameForm()
    if form.validate_on_submit():
        if current_user != game.players[0] and len(game.players) == 1:
            if game.password is None or bcrypt.check_password_hash(game.password, form.password.data):
                game.players.append(current_user)
                db.session.commit()

    return render_template('enter_game.html', title='New game', form=form, legend='Create', pw = False )


@games.route("/game/<int:game_id>/view", methods=['GET', 'POST'])
@login_required
def view_game(game_id):
    game = Game.query.get_or_404(game_id)


@games.route("/game/<int:game_id>/delete", methods=['POST'])
@login_required
def delete(game_id):
    game = Game.query.get_or_404(game_id)

    if current_user != game.players[0]:
        abort(403)

    db.session.delete(game)
    db.session.commit()
    flash('Your game has been deleted!', 'success')
