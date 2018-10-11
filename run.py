from flaskproject import create_app

# PYTHONUNBUFFERED=1;SECRET_KEY=12312321;SQLALCHEMY_DATABASE_URI=sqlite:///site.db
app = create_app()


if __name__ == "__main__":

	app.run( debug = True)