from .reset_db import reset_db


def register_commands(app):
    app.cli.add_command(reset_db)
