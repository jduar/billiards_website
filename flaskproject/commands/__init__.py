from .create_db import create_db


def register_commands(app):
    app.cli.add_command(create_db)
