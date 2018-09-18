from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskproject import db, bcrypt
from flaskproject.models import Game
from flaskproject.games.forms import GameForm, EnterGameForm

from flaskproject.games.utils import save_picture
games = Blueprint('games', __name__)


@games.route("/game/new", methods=['GET', 'POST'])
@login_required
def create_game():
    form = GameForm()

    if form.validate_on_submit():

        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        game = Game(name=form.name.data, password=hashed_pw)

        if form.picture.data:
            picture_fn = save_picture(form.picture.data)
            game.image_file = picture_fn

        game.players.append(current_user)

        db.session.add(game)
        db.session.commit()

        flash('Your game has been created!', 'success')

        return redirect(url_for('games.view_game', game_id=game.id))

    return render_template('create_game.html', title='Create game', form=form)


@games.route("/game/enter", methods=['GET', 'POST'])
@login_required
def enter_game():

    form = EnterGameForm()
    if form.validate_on_submit():

        game = Game.query.get_or_404(form.game_id.data)
        if current_user not in game.players and len(game.players) == 1:

            if bcrypt.check_password_hash(game.password, form.password.data):
                game.players.append(current_user)
                db.session.commit()

                return redirect(url_for('games.view_game', game_id=game.id))

    return render_template('join_game.html', title='Join game', form=form, legend='Create' )


@games.route("/game/<int:game_id>/view", methods=['GET', 'POST'])
@login_required
def view_game(game_id):

    game = Game.query.get_or_404(game_id)
    if current_user not in game.players:
        abort(403)

    return render_template('game.html', title='View game', game=game, creator = game.players[0])




@games.route("/game/<int:game_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_game(game_id):
    '''
    :param game_id:
    :return:
    '''

    # TODO: implement notification system to notify the users that the game has been deleted
    game = Game.query.get_or_404(game_id)

    if current_user != game.players[0]:
        abort(403)

    db.session.delete(game)
    db.session.commit()
    flash('Your game has been deleted!', 'success')

    return redirect(url_for('main.home'))



@games.route("/game/<int:game_id>/update", methods=['GET', 'POST'])
@login_required
def update_game(game_id):
    '''
    :param game_id:
    :return:
    '''

    # TODO: implement notification system to notify the users that the game has been deleted
    game = Game.query.get_or_404(game_id)

    if current_user != game.players[0]:
        abort(403)

    flash('Your game has been updated (Not yet implemented)!', 'success')

    return redirect(url_for('main.home'))


@games.route("/game/<int:game_id>/<int:user_id>/exit", methods=['GET', 'POST'])
@login_required
def exit_game(game_id, user_id):
    game = Game.query.get_or_404(game_id)

    if current_user not in game.players:
        abort(405)

    else:
        if len(game.players) == 1:
            delete_game(game.id)
            return redirect(url_for('main.home'))

        if game.players[0].id == user_id:
            game.players.remove(game.players[0])
        else:
            game.players.remove(game.players[1])

    db.session.commit()
    flash('You exited the game!', 'success')

    return redirect(url_for('main.home'))
