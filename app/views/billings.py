import base64
import datetime
from flask import (
    render_template,
    Blueprint,
    flash,
    redirect,
    url_for,
    request,
    current_app,
)
from flask_login import login_required, current_user
from sqlalchemy import desc
from app.logger import log
from app.models import User, Account, Billing
from app.forms import BillingForm
from app import db


billings_blueprint = Blueprint("billings", __name__)


@billings_blueprint.route("/billings")
@login_required
def billings_page():
    page_data = Billing.query.order_by(desc(Billing.id))
    if current_user.role != User.Role.admin:
        page_data = page_data.filter(Billing.user_id == current_user.id)
    page = request.args.get("page", 1, type=int)
    page_data = page_data.paginate(page=page, per_page=current_app.config["PAGE_SIZE"])
    return render_template("billings.html", billings=page_data)


@billings_blueprint.route("/billing_add", methods=["GET", "POST"])
@login_required
def billing_add():
    form = BillingForm()
    user: User = User.query.filter_by(id=current_user.id).first()
    if current_user.role == User.Role.admin:
        form.account.choices = [
            (account.id, account.login)
            for account in Account.query.filter(
                Account.deleted == False  # noqa E712
            ).all()
        ]
    else:
        form.account.choices = [
            (account.id, account.login) for account in current_user.accounts
        ]

    if form.validate_on_submit():
        from app.controllers import get_paid_qrcode

        cost: int
        if form.credits.data == 500:
            cost = user.package_500_cost
        elif form.credits.data == 1000:
            cost = user.package_1000_cost
        elif form.credits.data == 1500:
            cost = user.package_1500_cost
        elif form.credits.data == 2500:
            cost = user.package_2500_cost

        billing = Billing(
            user_id=current_user.id,
            account_id=form.account.data,
            credits=form.credits.data,
            cost=cost,
            qrcode=get_paid_qrcode(form.users_public_key.data, form.credits.data),
        )
        billing.save()

        user.credits_available -= cost
        user.save()

        return redirect(url_for("billings.billings_details", billing_id=billing.id))

    elif form.is_submitted():
        flash("Something went wrong. Cannot create a billing!", "danger")
        log(log.WARNING, "Cannot create a billing! Please check your credentials.")

    form.credits.data = 1000
    if current_user.role != User.Role.admin:
        form.credits.choices.remove((25, 25))

    return render_template("billing/add_billing.html", form=form)


@billings_blueprint.route("/billings_details/<int:billing_id>", methods=["GET", "POST"])
@login_required
def billings_details(billing_id):
    billing: Billing = Billing.query.get(billing_id)
    image_64 = base64.b64encode(billing.qrcode)
    image = image_64.decode()

    return render_template(
        "billing/billing_details.html",
        billing=billing,
        image=image,
    )


@billings_blueprint.route("/billing_search/<query>")
@login_required
def billing_search(query):
    page = request.args.get("page", 1, type=int)
    billings = Billing.query

    if query.isdigit():
        billings = billings.filter(Billing.credits == int(query))
    else:
        try:
            # Dates
            search_date = datetime.datetime.strptime(query, "%Y-%m-%d")
            next_day = search_date + datetime.timedelta(1)
            billings = billings.filter(
                search_date <= Billing.created_at, Billing.created_at <= next_day
            )
        except Exception:
            # Username
            billings = (
                db.session.query(
                    Billing,
                )
                .join(User)
                .filter(User.username.like(f"%{query}%"))
            )
    billings = billings.paginate(page=page, per_page=current_app.config["PAGE_SIZE"])

    if current_user.role != User.Role.admin:
        billings = billings.filter(Billing.user_id == current_user.id).paginate(
            page=page, per_page=current_app.config["PAGE_SIZE"]
        )

    return render_template("billings.html", billings=billings, query=query)
