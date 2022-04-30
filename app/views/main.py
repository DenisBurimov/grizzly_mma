import ast
from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import current_user, login_required
from app.models import User, Account, Billing
from app.controllers import get_paid_qrcode

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
@login_required
def index():
    if current_user.role == User.Role.admin:
        return redirect(url_for("users.users_page"))
    return redirect(url_for("accounts.accounts_page"))


@main_blueprint.route("/qrscanner", methods=["GET", "POST"])
@login_required
def qrscanner():
    qr_data = None
    INITIAL_BILLING_CREDITS = 1000
    if request.method == "POST":
        qr_string_data = request.form["qr_data"]
        qr_data = ast.literal_eval(qr_string_data)
        public_key = qr_data.get("itemText")
        account_id = qr_data.get("account_id")
        account: Account = Account.query.get(account_id)
        if public_key and account_id:
            account.public_key = public_key
            account.save()
            billing = Billing(
                user_id=current_user.id,
                credits=INITIAL_BILLING_CREDITS,
                qrcode=get_paid_qrcode(INITIAL_BILLING_CREDITS),
            )
            billing.save()

    return render_template("qrscanner.html", info=qr_data)
