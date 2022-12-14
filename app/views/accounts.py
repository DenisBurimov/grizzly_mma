import datetime
from flask import (
    current_app,
    render_template,
    redirect,
    request,
    url_for,
    Blueprint,
    flash,
)
from flask_login import current_user, login_required
from sqlalchemy import desc
from app.logger import log
from app.models import User, Account, Billing
from app.forms import AccountForm
from app import db
from app.controllers import gen_login, gen_password, LDAP, MDM

accounts_blueprint = Blueprint("accounts", __name__)

INITIAL_BILLING_CREDITS = 1000


@accounts_blueprint.route("/accounts")
@login_required
def accounts_page():
    page_data = Account.query
    if current_user.role != User.Role.admin:
        page_data = page_data.filter(Account.user_id == current_user.id)
    page = request.args.get("page", 1, type=int)
    page_data = page_data.order_by(desc(Account.id)).paginate(
        page=page, per_page=current_app.config["PAGE_SIZE"]
    )

    return render_template("accounts.html", accounts=page_data)


@accounts_blueprint.route("/account_add", methods=["GET", "POST"])
@login_required
def account_add():
    form = AccountForm()
    mdm_connection = MDM()

    if form.validate_on_submit():
        # if LDAP server configured
        if current_app.config["LDAP_SERVER"]:
            log(log.INFO, "Add AD User")
            ldap_connection = LDAP()

            if not ldap_connection.add_user(form.login.data):
                flash("Something went wrong. Cannot create AD user", "danger")
                log(log.ERROR, "Cannot create AD user: [%s]", form.login.data)
                return render_template("account/add_account.html", form=form)

            if not ldap_connection.change_password(form.login.data, form.password.data):
                flash("Something went wrong. Cannot set the password", "danger")
                log(log.ERROR, "Cannot set the password")
                return render_template("account/add_account.html", form=form)

            mdm_connection.sync()
        else:
            log(log.WARNING, "LDAP server not configured!!")

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


@accounts_blueprint.route("/account_info/<int:account_id>", methods=["GET", "POST"])
@login_required
def account_info(account_id: int):
    account: Account = Account.query.get(account_id)

    # Balance
    billings = Billing.query.filter(Billing.account_id == account_id)
    balance = sum((x.credits for x in billings))

    return render_template(
        "account/info_account.html",
        account=account,
        balance=balance,
    )


@accounts_blueprint.route("/account_billings/<int:account_id>", methods=["GET", "POST"])
@login_required
def account_billings(account_id: int):
    page = request.args.get("page", 1, type=int)
    billings = Billing.query.filter(Billing.account_id == account_id)
    billings = billings.paginate(page=page, per_page=current_app.config["PAGE_SIZE"])

    return render_template("billings.html", billings=billings)


@accounts_blueprint.route("/account_search/<query>")
@login_required
def account_search(query):
    page = request.args.get("page", 1, type=int)
    splitted_queries = query.split(",")
    search_result = Account.query.filter_by(id=0)
    for raw_single_query in splitted_queries:
        single_query = raw_single_query.strip()
        accounts = Account.query

        try:
            # Dates
            search_date = datetime.datetime.strptime(single_query, "%Y-%m-%d")
            next_day = search_date + datetime.timedelta(1)
            accounts = accounts.filter(
                search_date <= Account.created_at, Account.created_at <= next_day
            )
        except ValueError:
            accounts = (
                db.session.query(
                    Account,
                )
                .join(User)
                .filter(
                    User.username.like(f"%{single_query}%")
                    | Account.login.like(f"%{single_query}%")
                )
            )
        search_result = search_result.union(accounts)

    accounts = search_result.paginate(
        page=page, per_page=current_app.config["PAGE_SIZE"]
    )

    if current_user.role != User.Role.admin:
        accounts = accounts.filter(Account.user_id == current_user.id).paginate(
            page=page, per_page=current_app.config["PAGE_SIZE"]
        )

    return render_template("accounts.html", accounts=accounts, query=query)


@accounts_blueprint.route("/account_enroll/<int:account_id>")
@login_required
def account_enroll(account_id):
    account = Account.query.get(account_id)

    return render_template("account/enroll.html", account=account)
