import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, flash
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from .extensions import db, cors, bcrypt, login_manager, admin, turbo
from .models import User, Group

BASE_DIR = Path(__file__).parent.parent


## Do flask login setup: https://flask-login.readthedocs.io/en/latest/#how-it-works
login_manager.login_view = "auth.login"
login_manager.login_message_category = "danger"


@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter(User.id == int(user_id)).first()
    return user


class MyModelView(ModelView):
    def is_accessible(self):
        # default is to return True
        return current_user.admin

    def inaccessible_callback(self, name, **kwargs):
        flash(f"You must log in to get access to {name}")
        return redirect(url_for("auth.login"))  # TODO flash something more useful...


def create_app(deploy_mode="Development", settings_override={}):
    load_dotenv()
    deploy_mode = (
        deploy_mode
        if deploy_mode is not None
        else os.environ.get("DEPLOY_MODE", "Development")
    )
    app = Flask(__name__, static_folder="../frontend/build", static_url_path="/static/")

    config_module = f"config.{deploy_mode}Config"
    print(f"running with {config_module} config")
    app.config.from_object(config_module)
    app.config["CORS_HEADERS"] = "Content-Type"
    app.config["Access-Control-Allow-Origin"] = "*"
    app.config.update(
        {
            "WEBPACK_LOADER": {
                "MANIFEST_FILE": os.path.join(BASE_DIR, "frontend/build/manifest.json"),
            }
        }
    )
    app.config.update(settings_override)

    cors.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)
    turbo.init_app(app)

    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Group, db.session))

    from webpack_boilerplate.config import setup_jinja2_ext

    setup_jinja2_ext(app)
    from .views import main_blueprint, auth_blueprint, matches_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(matches_blueprint)

    @app.cli.command("webpack_init")
    def webpack_init():
        from cookiecutter.main import cookiecutter
        import webpack_boilerplate

        pkg_path = os.path.dirname(webpack_boilerplate.__file__)
        cookiecutter(pkg_path, directory="frontend_template")

    return app
