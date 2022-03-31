from flask import render_template, Blueprint
from app.models.user import User

accounts_blueprint = Blueprint("accounts", __name__)


@accounts_blueprint.route("/users")
def users_page():
    users = User.query.all()

    return render_template("users.html", users=users)
