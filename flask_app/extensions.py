from re import T
from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_admin import Admin, AdminIndexView
from turbo_flask import Turbo
from flask_bootstrap import Bootstrap


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.admin:
            return True
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))


db = SQLAlchemy()
cors = CORS()
bcrypt = Bcrypt()
login_manager = LoginManager()
admin = Admin(index_view=MyAdminIndexView())
turbo = Turbo()
boostrap = Bootstrap()
