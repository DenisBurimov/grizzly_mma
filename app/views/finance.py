from flask import (
    render_template,
    Blueprint,
    request,
    current_app,
)
from flask_login import login_required, current_user
from sqlalchemy import desc
from app.models import User, Transaction


finance_blueprint = Blueprint("finance", __name__)


@finance_blueprint.route("/finance")
@login_required
def finance_page():
    page_data = Transaction.query.order_by(desc(Transaction.id))
    if current_user.role != User.Role.admin:
        page_data = page_data.filter(Transaction.reseller_id == current_user.id)
    page = request.args.get("page", 1, type=int)
    page_data = page_data.paginate(page=page, per_page=current_app.config["PAGE_SIZE"])
    return render_template("finance.html", transactions=page_data)
