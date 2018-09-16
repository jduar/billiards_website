from flask import render_template, request, Blueprint
from flaskproject.models import Game

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():    
    page = request.args.get('page', 1, type = int)
    games = Game.query.order_by(Game.date_created.desc()).paginate(page = page, per_page = 5)
    return render_template('home.html', games=games)


@main.route("/about")
def about():
    return render_template('about.html', title = "About")
