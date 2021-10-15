from flask import Blueprint, render_template, request

from flaskproject.models import User

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get("page", 1, type=int)
    users = User.query.order_by(User.elo.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", users=users)


@main.route("/about")
def about():
    return render_template("about.html", title="About")
