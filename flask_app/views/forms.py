# project/user/forms.py
# originally taken from https://github.com/mjhea0/flask-basic-registration/blob/master/project/user/forms.py
from pathlib import Path
import pytz
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Email, Length, EqualTo

from ..models import User
from ..extensions import bcrypt


class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user is None:
            self.email.errors.append("This email is not found in our records")
            return False
        else:
            if user and bcrypt.check_password_hash(user.password, self.password.data):
                return True
            else:
                self.password.errors.append("This password does not match email.")
                return False


with open(Path(__file__).parent.parent / "states.txt", "r") as f:
    STATES = [i.strip("\n") for i in f.readlines()]


class RegisterUserForm(FlaskForm):
    role = SelectField(
        "Your Role (Group Leader or Scientist)", choices=["group_leader", "scientist"]
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    confirm_email = StringField(
        "Confirm Email",
        validators=[
            DataRequired(),
            Email(message=None),
            Length(min=6, max=40),
            EqualTo("email", message="Make sure your email entries match"),
        ],
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm_password = PasswordField(
        "Repeat Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )

    def validate(self):
        initial_validation = super(RegisterUserForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True


class ForgotPasswordForm(FlaskForm):
    email = StringField(
        "Email", validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )


class RegisterGroup(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=40)])
    school_district = StringField("School District", validators=[])
    city = StringField("City", validators=[])
    state = SelectField("State", choices=STATES, validators=[])
    country = SelectField("Country", choices=["US", "CA"], validators=[])
    time_zone = SelectField("Timezone", choices=pytz.all_timezones_set, validators=[])
    monday_start_time = DateTimeField("Monday Start Time", format="%H:%M")
    scientist_preferred_type = SelectField(
        "Preferred Scientist Type",
        choices=[
            "cool ones"
        ],  # TODO: Query the db to pull out all available types of scientsists from those that have signed up
    )


class ChangePasswordForm(FlaskForm):
    password = PasswordField(
        "password", validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        "Repeat password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
