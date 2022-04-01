from flask import render_template, Blueprint
from flask_login import current_user
from app.models import Account, User

accounts_blueprint = Blueprint("accounts", __name__)


@accounts_blueprint.route("/accounts")
def accounts_page():
    if current_user != User.Role.admin:
        accounts = Account.query.filter_by(user_id=current_user.id)
    else:
        accounts = Account.query.all()
    return render_template("accounts.html", accounts=accounts)
