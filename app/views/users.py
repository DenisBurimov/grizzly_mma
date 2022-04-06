from flask import render_template, Blueprint, redirect, request, url_for
from flask_login import login_required, current_user
from sqlalchemy import desc
from app.models import User
from app.forms import UserForm

users_blueprint = Blueprint("users", __name__)


@users_blueprint.route("/users")
@login_required
def users_page():
    if current_user.role != User.Role.admin:
        return redirect(url_for("users.users_page"))
    page = request.args.get("page", 1, type=int)
    users = User.query.order_by(desc(User.id)).paginate(page=page, per_page=20)

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
        ).save()

        return redirect(url_for("users.users_page"))
    return render_template("user/add.html", form=form)


@users_blueprint.route("/user_update/<int:user_id>", methods=["GET", "POST"])
@login_required
def user_update(user_id: int):
    form = UserForm()
    user: User = User.query.get(user_id)

    if form.validate_on_submit():
        user.username = form.username.data
        user.password = form.password.data
        user.role = form.role.data
        user.save()

        return redirect(url_for("users.users_page"))

    elif request.method == "GET":
        form.username.data = user.username
        form.role.data = user.role

    return render_template("user/update.html", form=form)


@users_blueprint.route("/user_search/<query>")
@login_required
def user_search(query):
    page = request.args.get("page", 1, type=int)
    users = User.query.order_by(desc(User.id)).filter(User.username.like(f"%{query}%")).paginate(page=page, per_page=20)

    return render_template(
        "users.html",
        users=users,
        query=query,
    )
