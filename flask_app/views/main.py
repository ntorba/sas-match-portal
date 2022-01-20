from flask import render_template, request, redirect, Blueprint, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from markupsafe import Markup

from ..models import User, ClassRoom
from ..extensions import bcrypt, db
from .forms import LoginForm, ChangePasswordForm, RegisterTeacherForm, RegisterClassroom

main_blueprint = Blueprint('main', __name__, template_folder="templates")

class Component:
    def __init__(self, placeholder, attribute):
        self.placeholder = placeholder
        self. attribute = attribute

    def create_input_component(self):
        # html = [f"<p><b>{placeholder}</b></p>"]
        # html.append(f'{{{{ form.{attribute}(class="teacher-register-input", placeholder="{placeholder}") }}}}')
        html = f'{{{{ form.{self.attribute}(class="teacher-register-input", placeholder="{self.placeholder}") }}}}'
        return Markup("".join(html))

def create_error_component(placeholder, attribute):
    component = '<span class="error text-red-500">{{% if form.{attribute}.errors %}}{{% for error in form.{attribute}.errors %}}{{{{ error }}}}{{% endfor %}}{{% endif %\}}</span>'
    return Markup(component)

@main_blueprint.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    return render_template("index.html")

@main_blueprint.route("/home")
@login_required
def home():
    return render_template("home.html")

@main_blueprint.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@main_blueprint.route('/register-role/<role>', methods=['GET'])
def register_role(role):
    form = RegisterTeacherForm(request.form)
    return render_template("register-turbo-frame.html", role=role, form=form)

@main_blueprint.route('/register-teacher', methods=['GET', 'POST'])
def register_teacher():
    form = RegisterTeacherForm(request.form)
    if form.validate_on_submit():
        user = User(
            role=form.role.data,
            name=form.name.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash('You registered and are now logged in. Welcome!', 'success')

        return redirect(url_for('main.home'))

    return render_template(
        'register-teacher.html', 
        form=form, 
        Component=Component, 
        create_error_component=create_error_component
    )

@main_blueprint.route("/login",methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                user.password, request.form['password']):
            login_user(user)
            flash('Welcome.', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('login.html', form=form)
    
    return render_template('login.html', form=form)

@main_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.', 'success')
    return redirect(url_for('main.login'))

@main_blueprint.route('/profile')
@login_required
def profile():
    if current_user.role == "Teacher":
        classrooms = ClassRoom.query.filter(ClassRoom.user_id == current_user.id).all()
        return render_template("teacher-profile.html", classrooms=classrooms)
    else:
        return render_template("main.home")

@main_blueprint.route('/register-classroom', methods=["GET", "POST"])
@login_required
def register_classroom():
    form = RegisterClassroom(request.form)
    last_class = ClassRoom.query.first()
    if form.validate_on_submit():
        ## TODO: Think of check for repeat classrooms
        user = User.query.filter_by(email=current_user.email).first()
        classroom = ClassRoom(
            user_id = user.id, 
            **form.data
        )
        db.session.add(classroom)
        db.session.commit()
        flash(f'Successfully added classroom {form.name.data}!', 'success')
        return redirect(url_for('main.profile'))
    return render_template('register-classroom.html', form=form)

@main_blueprint.route('/classroom/<classroomid>', methods=["GET", "POST"])
@login_required
def classroom(classroomid):
    return "fuuuuck"

@main_blueprint.route('/profile_update', methods=['GET', 'POST'])
@login_required
def profile_update():
    form = ChangePasswordForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=current_user.email).first()
        if user:
            user.password = bcrypt.generate_password_hash(form.password.data)
            db.session.commit()
            flash('Password successfully changed.', 'success')
            return redirect(url_for('user.profile'))
        else:
            flash('Password change was unsuccessful.', 'danger')
            return redirect(url_for('user.profile'))
    return render_template('profile-update.html', form=form)
