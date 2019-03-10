from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskproject import db, bcrypt
from flaskproject.models import Game, User
from flaskproject.games.forms import GameForm, EnterGameForm, WinnerForm

from flaskproject.games.utils import save_picture, calculate_elo

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

        game = Game.query.get(form.game_id.data)
        if game is None:
            flash(f'Game does not exist!', 'danger')
            return redirect(url_for('games.enter_game'))

        if current_user not in game.players and len(game.players) == 1:

            if bcrypt.check_password_hash(game.password, form.password.data):
                game.players.append(current_user)
                db.session.commit()
            else:
                flash(f'Wrong password!', 'danger')
                return redirect(url_for('games.enter_game'))
        flash(f"Game already full", "warning")

        return redirect(url_for('games.view_game', game_id=game.id))

    return render_template('join_game.html', title='Join game', form=form, legend='Create' )


@games.route("/game/<int:game_id>/view", methods=['GET', 'POST'])
def view_game(game_id):
    """

    ToDo: add ability to keep the games going after the winner as been decided

    :param game_id:
    :return:
    """

    game = Game.query.get_or_404(game_id)

    form = WinnerForm()
    choices = [(0, 'TBD')]

    players = [i for i in game.players]

    for j in range(len(players)):
        choices.append((j+1, players[j].username))

    form.group_id.choices = choices

    if form.validate_on_submit() and form.group_id.data != -1:
        flash('Your game has been updated 1!', 'success')
        p1_elo, p2_elo = calculate_elo(game.players[0].elo, players[1].elo, form.group_id.data)

        players[0].elo = p1_elo
        players[1].elo = p2_elo
        game.winner = players[form.group_id.data - 1].id

        db.session.commit()

        flash('The winner has been decided !', 'success')

        return redirect(url_for('main.home'))

    return render_template('game.html', title='View game', game=game, creator = players[0], form = form, players = players)


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


@games.route("/game/<int:game_id>/update/", methods=['GET', 'POST'])
@login_required
def update_game(game_id):
    '''

    Update game name and password

                To be implemented
    :param game_id:
    :return:
    '''

    abort(404)


@games.route("/game/<int:game_id>/<int:user_id>/exit", methods=['GET', 'POST'])
@login_required
def exit_game(game_id, user_id):
    """
    Exits the game. If there is only one player then the game is deleted.

    :param game_id:
    :param user_id:
    :return:
    """

    game = Game.query.get_or_404(game_id)
    players = [i for i in game.players]
    if current_user not in game.players:
        abort(405)

    else:
        if len(players) == 1:
            delete_game(game.id)
            return redirect(url_for('main.home'))

        if players[0].id == user_id:
            game.players.remove(game.players[0])
        else:
            game.players.remove(game.players[1])

    db.session.commit()
    flash('You exited the game!', 'success')

    return redirect(url_for('main.home'))


@games.route("/game/match_history/<string:which>/<int:user_id>", methods=['GET'])
@login_required
def match_history(which,user_id):
    """
    See all games in which a user is in
    :return:
    """
    page = request.args.get('page', 1, type = int)
    user = User.query.filter_by(id = user_id).first_or_404()
    if which == 'all':
        games = user.games.order_by(Game.date_created.desc())
    elif which == 'active':
        games = user.games.filter_by(winner = None).order_by(Game.date_created.desc())
    elif which == 'closed':
        games = user.games.filter(Game.winner != None).order_by(Game.date_created.desc())

    tots = 0
    wins = 0

    game_info = {}
    for j in games:
        if j.winner:
            tots += 1
            if j.winner == user_id:
                wins += 1

    game_info['total_number'] = tots
    try:
        game_info['wins'] = wins * 100 / tots
    except ZeroDivisionError:
        game_info['wins'] = 100
    games_in = games.paginate(page = page, per_page = 5)
    return render_template('all_games.html', games=games_in, title = ' All Games', user = user, game_info = game_info)

