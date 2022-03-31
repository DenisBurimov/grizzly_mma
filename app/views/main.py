from flask import render_template, Blueprint
from app.models import User, Account, Billing

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def index():
    # users = User.query.filter_by(role="admin").first()
    users = User.query.all()
    accounts = Account.query.all()
    billings = Billing.query.all()
    return render_template(
        "index.html", users=users, accounts=accounts, billings=billings
    )
