from flask import render_template, Blueprint
from app.models import User

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def index():
    users = User.query.all()
    return render_template("index.html", users=users)
