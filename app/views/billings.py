from flask import render_template, Blueprint
from flask_login import login_required, current_user
from sqlalchemy import desc
from app.models import User, Billing

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
    form = "Here Will Be A Form"

    return render_template("billing/add_billing.html", form=form)


@billings_blueprint.route("/billings_details/<int:billing_id>", methods=["GET", "POST"])
@login_required
def billings_details(billing_id):
    billing: Billing = Billing.query.get(billing_id)

    return render_template("billing/billing_details.html", billing=billing)
