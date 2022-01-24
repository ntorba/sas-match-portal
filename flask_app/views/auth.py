from flask import render_template, request, redirect, Blueprint, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from ..models import User
from ..extensions import bcrypt, db, turbo
from .forms import (
    LoginForm,
    ChangePasswordForm,
    RegisterUserForm,
    ForgotPasswordForm,
)

auth_blueprint = Blueprint("auth", __name__, template_folder="templates")


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterUserForm(request.form)
    if request.method == "GET":
        return render_template("register.html", form=form)
    if form.validate_on_submit():
        user = User(
            role=form.role.data,
            email=form.email.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("You registered and are now logged in. Welcome!", "success")

        return redirect(url_for("main.home"))
    else:
        all_errors = []
        for field, errors in form.errors.items():
            # errors = getattr(form, field).errors
            all_errors.extend(errors)
            turbo.push(
                turbo.update(
                    render_template("form-errors.html", errors=errors),
                    f"register-{field}-errors",
                )
            )
        return ", ".join(all_errors), 200


@auth_blueprint.route("/register/<role>")
def register_form(role):
    form = RegisterUserForm(request.form)
    return render_template(
        "register-form.html",
        form=form,
        role=role,
    )


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "GET":
        return render_template("login.html", form=form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user)
        flash("You've successfully logged in.")
        return redirect(url_for("main.home"))
    elif request.method == "POST":
        # flash("Invalid email and/or password.", "danger")
        all_errors = []
        for field, errors in form.errors.items():
            # errors = getattr(form, field).errors
            all_errors.extend(errors)
            turbo.push(
                turbo.update(
                    render_template("form-errors.html", errors=errors),
                    f"login-{field}-errors",
                )
            )
        return ", ".join(errors), 200


@auth_blueprint.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    # TODO: Actually send emails by Follow https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-x-email-support
    form = ForgotPasswordForm(request.form)
    return render_template("forgot_password.html", form=form)


@auth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")
    return redirect(url_for("auth.login"))
