import click
from flask.cli import with_appcontext

from flaskproject import db
from flaskproject.models import Game, User


@click.command()
@with_appcontext
def reset_db():
    """Initializes the database."""
    if click.confirm("Do you want to continue?"):
        db.drop_all()
        db.create_all()
        load_data()


def load_data():
    """Load base data into the database."""

    user = User(  # noqa: S106
        username="teste", email="teste@gmail.com", password="aaaa"
    )
    user1 = User(  # noqa: S106
        username="teste1", email="teste1@gmail.com", password="bbbb"
    )
    for j in range(2):
        game = Game(name="test" + str(j), password="1")  # noqa: S106

        db.session.add(user)
        db.session.add(user1)
        db.session.add(game)

        game.players.append(user)
        game.players.append(user1)

    db.session.commit()
