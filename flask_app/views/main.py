from flask import render_template, request, redirect, Blueprint, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from ..models import User, Group
from ..extensions import bcrypt, db
from .forms import (
    LoginForm,
    ChangePasswordForm,
    RegisterClassroom,
    RegisterUserForm,
    ForgotPasswordForm,
)

main_blueprint = Blueprint("main", __name__, template_folder="templates")


@main_blueprint.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    return render_template("index.html")


@main_blueprint.route("/about/")
def about():
    return render_template("about.html")


@main_blueprint.route("/home")
@login_required
def home():
    classrooms = None
    events = []
    if current_user.role == "Teacher":
        classrooms = Group.query.filter(Group.user_id == current_user.id).all()
    return render_template("home.html", classrooms=classrooms, events=events)


@main_blueprint.route("/register", methods=["GET", "POST"])
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
        return render_template(
            "register.html", form=form, role=request.form.get("role")
        )


@main_blueprint.route("/register/<role>")
def register_form(role):
    form = RegisterUserForm(request.form)
    return render_template(
        "register-form.html",
        form=form,
        role=role,
    )


@main_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, request.form["password"]):
            login_user(user)
            flash("Welcome.", "success")
            return redirect(url_for("main.home"))
        else:
            flash("Invalid email and/or password.", "danger")
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)


@main_blueprint.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    # TODO: Actually send emails by Follow https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-x-email-support
    form = ForgotPasswordForm(request.form)
    return render_template("forgot_password.html", form=form)


@main_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")
    return redirect(url_for("main.login"))


@main_blueprint.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@main_blueprint.route("/register-classroom", methods=["GET", "POST"])
@login_required
def register_classroom():
    form = RegisterClassroom(request.form)
    last_class = Group.query.first()
    if form.validate_on_submit():
        ## TODO: Think of check for repeat classrooms
        user = User.query.filter_by(email=current_user.email).first()
        classroom = Group(user_id=user.id, **form.data)
        db.session.add(classroom)
        db.session.commit()
        flash(f"Successfully added classroom {form.name.data}!", "success")
        return redirect(url_for("main.profile"))
    return render_template("register-classroom.html", form=form)


@main_blueprint.route("/classroom/<classroomid>", methods=["GET", "POST"])
@login_required
def classroom(classroomid):
    return "fuuuuck"


@main_blueprint.route("/profile_update", methods=["GET", "POST"])
@login_required
def profile_update():
    form = ChangePasswordForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=current_user.email).first()
        if user:
            user.password = bcrypt.generate_password_hash(form.password.data)
            db.session.commit()
            flash("Password successfully changed.", "success")
            return redirect(url_for("user.profile"))
        else:
            flash("Password change was unsuccessful.", "danger")
            return redirect(url_for("user.profile"))
    return render_template("profile-update.html", form=form)
