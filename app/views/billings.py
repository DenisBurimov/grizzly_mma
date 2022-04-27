import base64
from flask import render_template, Blueprint, flash, redirect, url_for, request
from flask_login import login_required, current_user
from sqlalchemy import desc
from app.logger import log
from app.models import User, Billing
from app.forms import BillingForm


billings_blueprint = Blueprint("billings", __name__)


@billings_blueprint.route("/billings")
@login_required
def billings_page():
    query = Billing.query.order_by(desc(Billing.id))
    if current_user.role != User.Role.admin:
        query = query.filter(Billing.user_id == current_user.id)
    return render_template("billings.html", billings=query.all())


@billings_blueprint.route("/billing_add", methods=["GET", "POST"])
@login_required
def billing_add():
    form = BillingForm()

    if form.validate_on_submit():
        from app.controllers import get_paid_qrcode

        billing = Billing(
            user_id=current_user.id,
            credits=form.credits.data,
            qrcode=get_paid_qrcode(form.credits.data),
        )
        billing.save()

        return redirect(url_for("billings.billings_details", billing_id=billing.id))

    elif form.is_submitted():
        flash("Something went wrong. Cannot create a billing!", "danger")
        log(log.WARNING, "Cannot create a billing! Please check your credentials.")

    if request.method == "GET" and current_user.role == User.Role.admin:
        form.credits.choices = [(25, 25)]
        form.credits.data = 25
    elif request.method == "GET" and current_user.role != User.Role.admin:
        form.credits.choices.remove(25, 25)
        form.credits.data = 1000

    return render_template("billing/add_billing.html", form=form)


@billings_blueprint.route("/billings_details/<int:billing_id>", methods=["GET", "POST"])
@login_required
def billings_details(billing_id):
    billing: Billing = Billing.query.get(billing_id)
    image_64 = base64.b64encode(billing.qrcode)
    image = image_64.decode()

    return render_template("billing/billing_details.html", billing=billing, image=image)
