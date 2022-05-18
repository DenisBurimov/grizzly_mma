import datetime
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


@finance_blueprint.route("/finance_search/<query>")
@login_required
def finance_search(query):
    finance_data = Transaction.query.order_by(desc(Transaction.id))
    if current_user.role != User.Role.admin:
        flash("Access denied", "danger")
        return redirect(url_for("main.index"))
    page = request.args.get("page", 1, type=int)

    if query.isdigit():
        finance_data = Transaction.query.filter(Transaction.transaction_amount == query)

    if finance_data.count() == 0 or not query.isdigit():
        try:
            # Dates
            search_date = datetime.datetime.strptime(query, "%Y-%m-%d")
            next_day = search_date + datetime.timedelta(1)
            finance_data = finance_data.filter(
                search_date <= Transaction.created_at,
                Transaction.created_at <= next_day,
            )
        except Exception:
            users = User.query.filter(User.username.like(f"%{query}%")).all()
            users_id_list = [user.id for user in users]
            finance_data = Transaction.query.filter(
                (Transaction.reseller_id.in_(users_id_list))
                | (Transaction.admin_id.in_(users_id_list))
                | (Transaction.comment.like(f"%{query}%"))
            )

    finance_data = finance_data.paginate(
        page=page, per_page=current_app.config["PAGE_SIZE"]
    )

    (debt,) = (
        db.session.query(func.sum(User.credits_available).label("dept"))
        .filter(User.credits_available < 0)
        .first()
    )

    return render_template("finance.html", transactions=finance_data, debt=debt)
