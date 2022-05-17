from flask import (
    render_template,
    Blueprint,
    request,
    current_app,
    flash,
    redirect,
    url_for,
)
from flask_login import login_required, current_user
from sqlalchemy import desc, func
from app.models import User, Transaction
from app import db


finance_blueprint = Blueprint("finance", __name__)


@finance_blueprint.route("/finance")
@login_required
def finance_page():
    page_data = Transaction.query.order_by(desc(Transaction.id))
    if current_user.role != User.Role.admin:
        flash("Access denied", "danger")
        return redirect(url_for("main.index"))
    page = request.args.get("page", 1, type=int)
    page_data = page_data.paginate(page=page, per_page=current_app.config["PAGE_SIZE"])

    (debt,) = (
        db.session.query(func.sum(User.credits_available).label("dept"))
        .filter(User.credits_available < 0)
        .first()
    )

    return render_template("finance.html", transactions=page_data, debt=debt)
