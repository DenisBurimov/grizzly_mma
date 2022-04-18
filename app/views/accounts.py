from flask import render_template, redirect, request, url_for, Blueprint, flash
from flask_login import current_user, login_required
from sqlalchemy import desc
from app.logger import log
from app.models import User, Account
from app.forms import AccountForm
from app.controllers import gen_login, gen_password, LDAP, MDM

accounts_blueprint = Blueprint("accounts", __name__)


@accounts_blueprint.route("/accounts")
@login_required
def accounts_page():
    page_data = Account.query
    if current_user.role != User.Role.admin:
        page_data = page_data.filter(Account.user_id == current_user.id)
    page = request.args.get("page", 1, type=int)
    page_data = page_data.order_by(desc(Account.id)).paginate(page=page, per_page=20)

    return render_template("accounts.html", accounts=page_data)


@accounts_blueprint.route("/account_add", methods=["GET", "POST"])
@login_required
def account_add():
    form = AccountForm()
    ldap_connection = LDAP()
    mdm_connection = MDM()

    if form.validate_on_submit():
        if not ldap_connection.add_user(form.login.data):
            flash("Something went wrong. Cannot create AD user", "danger")
            log(log.ERROR, "Cannot create AD user: [%s]", form.login.data)
            return render_template("account/add_account.html", form=form)

        if not ldap_connection.change_password(form.login.data, form.password.data):
            flash("Something went wrong. Cannot set the password", "danger")
            log(log.ERROR, "Cannot set the password")
            return render_template("account/add_account.html", form=form)

        mdm_connection.sync()

        Account(
            user_id=current_user.id,
            login=form.login.data,
            password=form.password.data,
        ).save()

        return redirect(url_for("accounts.accounts_page"))

    if request.method == "GET":
        form.login.data = gen_login()
        form.password.data = gen_password()

    return render_template("account/add_account.html", form=form)


@accounts_blueprint.route("/account_info/<int:account_id>")
@login_required
def account_info(account_id: int):
    account: Account = Account.query.get(account_id)

    return render_template("account/info_account.html", account=account)


@accounts_blueprint.route("/account_search/<query>")
@login_required
def account_search(query):
    page = request.args.get("page", 1, type=int)
    accounts = (
        Account.query.order_by(desc(Account.id))
        .filter(Account.login.like(f"%{query}%"))
        .paginate(page=page, per_page=20)
    )

    return render_template(
        "accounts.html",
        accounts=accounts,
        query=query,
    )


@accounts_blueprint.route("/account_enroll/<int:account_id>")
@login_required
def account_enroll(account_id):
    account = Account.query.get(account_id)

    return render_template("account/enroll.html", account=account)
