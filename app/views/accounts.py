from flask import render_template, Blueprint
from app.models import User
from app.models.account import Account

accounts_blueprint = Blueprint("accounts", __name__)


@accounts_blueprint.route("/accounts")
def accounts():
    accounts = Account.query.all()
    return render_template("accounts.html", accounts=accounts)
