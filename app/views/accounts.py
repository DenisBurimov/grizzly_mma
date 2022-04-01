from flask import render_template, redirect, request, url_for, Blueprint
from flask_login import current_user, login_required
from app.models import Account, User
from app.forms import AccountForm
from app.controllers import gen_login, gen_password

accounts_blueprint = Blueprint("accounts", __name__)


@accounts_blueprint.route("/accounts")
@login_required
def accounts_page():
    query = Account.query
    if current_user.role != User.Role.admin:
        query = query.filter(Account.user_id == current_user.id)
    return render_template("accounts.html", accounts=query.all())


@accounts_blueprint.route("/account_add", methods=["GET", "POST"])
def account_add():
    form = AccountForm()

    if form.validate_on_submit():
        Account(
            user_id=current_user.id,
            login=form.login.data,
            password=form.password.data,
        ).save()

        return redirect(url_for("accounts.accounts_page"))

    elif request.method == "GET":
        form.login.data = gen_login()
        form.password.data = gen_password()

    return render_template("account/add_account.html", form=form)
