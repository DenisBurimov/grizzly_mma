from flask import render_template, Blueprint
from app.models import User
from app.models.account import Account
from app.models.billing import Billing

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def index():
    users = User.query.all()
    accounts = Account.query.all()
    billings = Billing.query.all()
    return render_template("index.html", users=users, accounts=accounts, billings=billings)
