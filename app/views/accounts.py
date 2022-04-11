from flask import render_template, redirect, request, session, url_for, Blueprint
from flask_login import current_user, login_required
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker
from app.models import User, Account
from app.forms import AccountForm
from app.controllers import gen_login, gen_password
from app import db

accounts_blueprint = Blueprint("accounts", __name__)

Session = sessionmaker()
sess = Session()


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

    if form.validate_on_submit():
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

    # testing_query = db.session.execute(
    #     f"select login, username from users join accounts on users.id = accounts.user_id where username like '%{query}%'"
    # )

    #  where username like '%{query}%'
    testing_query = (
        db.session.query(
            Account,
        )
        .join(User)
        .filter(Account.login.like(f"%{query}%"))
        .filter(User.username.like(f"%{query}%"))
        .paginate(page=page, per_page=10)
    )

    return render_template(
        "accounts.html",
        accounts=accounts,
        query=query,
        testing_query=testing_query,
    )
