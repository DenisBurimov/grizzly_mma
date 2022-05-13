from flask import (
    current_app,
    render_template,
    Blueprint,
    redirect,
    request,
    url_for,
    flash,
)
from flask_login import login_required, current_user
from sqlalchemy import desc
from app.models import User
from app.forms import UserForm, UserUpdateForm, UserFinanceForm

users_blueprint = Blueprint("users", __name__)


@users_blueprint.route("/users")
@login_required
def users_page():
    if current_user.role != User.Role.admin:
        return redirect(url_for("users.users_page"))
    page = request.args.get("page", 1, type=int)
    users = User.query.order_by(desc(User.id)).paginate(
        page=page, per_page=current_app.config["PAGE_SIZE"]
    )

    return render_template("users.html", users=users)


@users_blueprint.route("/user_delete/<int:user_id>", methods=["GET"])
@login_required
def user_delete(user_id: int):
    user: User = User.query.get(user_id)
    user.deleted = True
    user.save()

    return redirect(url_for("users.users_page"))


@users_blueprint.route("/user_add", methods=["GET", "POST"])
@login_required
def user_add():
    form = UserForm()

    if form.validate_on_submit():
        User(
            username=form.username.data,
            password=form.password.data,
            role=User.Role(form.role.data),
            credits_available=0,
        ).save()

        return redirect(url_for("users.users_page"))
    return render_template("user/add.html", form=form)


@users_blueprint.route("/user_update/<int:user_id>", methods=["GET", "POST"])
@login_required
def user_update(user_id: int):
    form = UserUpdateForm()
    user: User = User.query.get(user_id)

    if form.validate_on_submit():
        user.username = form.username.data
        user.password = form.password.data
        user.role = User.Role(form.role.data)
        user.save()

        return redirect(url_for("users.users_page"))

    elif request.method == "GET":
        form.username.data = user.username
        form.role.data = user.role.name

    return render_template("user/update.html", form=form, user=user)


@users_blueprint.route("/user_search/<query>")
@login_required
def user_search(query):
    page = request.args.get("page", 1, type=int)
    users = (
        User.query.order_by(desc(User.id))
        .filter(User.username.like(f"%{query}%"))
        .paginate(page=page, per_page=current_app.config["PAGE_SIZE"])
    )

    return render_template("users.html", users=users, query=query)


@users_blueprint.route("/user_finance/<int:user_id>", methods=["GET", "POST"])
@login_required
def user_finance(user_id: int):
    form = UserFinanceForm()
    user: User = User.query.get(user_id)

    if user.credits_available is None:
        user.credits_available = 0
        user.save()

    if form.validate_on_submit():
        if form.transaction_type.data == "Deposit":
            user.credits_available += form.transaction_amount.data
        else:
            user.credits_available -= form.transaction_amount.data
        user.package_500_cost = form.package_500_cost.data
        user.package_1000_cost = form.package_1000_cost.data
        user.package_1500_cost = form.package_1500_cost.data
        user.package_2500_cost = form.package_2500_cost.data
        user.save()
        flash("Users finance details have been successfully updated", "info")

        return redirect(url_for("users.user_finance", user_id=user.id))

    elif request.method == "GET":
        form.username.data = user.username
        form.credits.data = user.credits_available
        form.package_500_cost.data = user.package_500_cost
        form.package_1000_cost.data = user.package_1000_cost
        form.package_1500_cost.data = user.package_1500_cost
        form.package_2500_cost.data = user.package_2500_cost

    return render_template("user/finance.html", form=form, user=user)
