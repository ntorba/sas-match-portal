from flask_app.models import User
from flask_app.extensions import db


def login(client, email, password):
    return client.post(
        "/login", data=dict(email=email, password=password), follow_redirects=True
    )


def logout(client):
    return client.get("/logout", follow_redirects=True)


def add_user(role, email, password):
    user = User(role=role, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user


def add_group():
    pass
