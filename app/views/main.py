from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user, login_required
from app.models import User, Account, Billing

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
@login_required
def index():
    if current_user.role == User.Role.admin:
        return redirect(url_for("users.users_page"))
    return redirect(url_for("accounts.accounts_page"))


@main_blueprint.route("/search/<query>")
@login_required
def search(query):
    # if query.isalnum():
    users = User.query.filter(User.username.like(f"%{query}%"))
    # accounts = Account.query.all()
    accounts = Account.query.filter(Account.login.like(f"%{query}%"))
    accounts += Account.query.filter(
        Account.user.username == User.username.like(f"%{query}%")
    )
    billings = Billing.query.all()
    # billings = Billing.query.filter(Billing.reseller.like(f"%{query}%"))

    return render_template(
        "search.html",
        users=users,
        accounts=accounts,
        billings=billings,
    )
