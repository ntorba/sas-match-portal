import re

from flask_app.models import User, Group
from flask_app.views.forms import RegisterUserForm, LoginForm
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


def test_index(client):
    res = client.get("/")
    assert res.status_code == 200, "index not available, something big is wrong"


def test_registered_user_login(client, session):
    assert client.get("/login").status_code == 200, "Retrieving login page failed"

    role = "scientist"
    email = "test_scientist@science.com"
    password = "fake_password"
    scientist = add_user(role, email, password)

    login_res = login(client, email, password)
    assert (
        login_res.status_code == 200
    ), "expected 200 status code for login response"  # TODO: I Guess it changes this from 302 to 200 internally, not sure why?

    home_res = client.get("/home")
    assert (
        home_res.status_code == 200
    ), f"expected status_code 200 for logged in users accessing /home, but got {home_res.status_code}"

    logout_res = logout(client)
    assert logout_res.status_code == 200, "Logout status code should have returned 200"


def test_login_nonexistent_email(client, session):
    role = "scientist"
    email = "test_scientist@science.com"
    password = "fake_password"
    scientist = add_user(role, email, password)

    scientist_form = LoginForm(**{"email": "qqqq@qqqq.com", "password": password})

    response = client.post("/login", data=scientist_form.data)
    assert re.search(  # TODO: Do a more robust check by giving flashed messages an idea in html, make beautiful soup object and find those messages specifically
        "This email is not found in our records", response.get_data(as_text=True)
    ), "did not find 'This email is not found in our records' in response body"
    assert (
        response.status_code == 200
    ), f"Expected status_code 200 with error message embedded, but got {response.status_code} instead."
    assert (
        "Location" not in response.headers
    ), "Location should not be response.headers, this request should not have redirected"


def test_login_bad_password(client, session):
    role = "scientist"
    email = "test_scientist@science.com"
    password = "fake_password"

    scientist = add_user(role, email, password)

    scientist_form = LoginForm(
        **{"email": scientist.email, "password": "notrealpassword"}
    )

    response = client.post("/login", data=scientist_form.data)
    # TODO: Do a more robust check by giving flashed messages an idea in html, make beautiful soup object and find those messages specifically
    assert (
        response.get_data(as_text=True) == "This password does not match email."
    ), "did not find 'This password does not match email.' in response body"
    assert (
        response.status_code == 200
    ), f"Expected status_code 200 with error message embedded, but got {response.status_code} instead."
    assert (
        "Location" not in response.headers
    ), "Location should not be response.headers, this request should not have redirected"


def test_register_group_leader(client, app, session):
    # test that viewing the page renders without template errors
    assert client.get("/register").status_code == 200

    role = "group_leader"
    email = "test_user@test.com"
    confirm_email = "test_user@test.com"
    password = "password"
    # test that successful registration redirects to the login page
    form = RegisterUserForm(
        **{
            "role": role,
            "email": email,
            "confirm_email": confirm_email,
            "password": password,
            "confirm_password": password,
        },
    )
    response = client.post(
        "/register",
        data=form.data,
    )
    assert (
        "http://localhost/home" == response.headers["Location"]
    ), "registration response header did not redictrt to /home as expected"
    assert (
        response.status_code == 302
    ), f"Expected 302 status code for redirect, but go {response.status_code}"
    # test that the user was inserted into the database
    user = User.query.filter(User.email == email).first()
    assert user.email == email


def test_register_scientist(client, session):
    # test that viewing the page renders without template errors
    assert client.get("/register").status_code == 200

    role = "scientist"
    email = "test_scientist@science.com"
    password = "password"
    # test that successful registration redirects to the login page
    form = RegisterUserForm(
        **{
            "role": role,
            "email": email,
            "confirm_email": email,
            "password": password,
            "confirm_password": password,
        },
    )
    response = client.post(
        "/register",
        data=form.data,
    )
    assert (
        "http://localhost/home" == response.headers["Location"]
    ), "registration response header did not redirect to /home as expected"
    assert (
        response.status_code == 302
    ), f"Expected 302 status code for redirect, but go {response.status_code}"

    # test that the user was inserted into the database
    user = User.query.filter(User.email == email).first()
    assert user.email == email
    assert user.role.name == role


def test_register_scientist_mismatched_emails(client, session, app):
    # test that viewing the page renders without template errors
    assert client.get("/register").status_code == 200
    role = "scientist"
    email = "test_scientist@science.com"
    wrong_email = "no@no.com"
    password = "password"
    # test that successful registration redirects to the login page
    form = RegisterUserForm(
        **{
            "role": role,
            "email": email,
            "confirm_email": wrong_email,
            "password": password,
            "confirm_password": password,
        },
    )
    response = client.post(
        "/register",
        data=form.data,
    )
    # TODO: do more research to see if I can access to the active view of the html despirte using turbo streams
    # with this strategy, I can be sure that turbo.push ran in the view file, but it would be better to access the actual html
    assert (
        response.get_data(as_text=True) == "Make sure your email entries match"
    ), "Received an unexpected response error for mismatched emails"

    assert (
        response.status_code == 200
    ), "expected reponse code 200 for mismatched password, success sending back turbo-stream"
    assert (
        "Location" not in response.headers
    ), "registration response tried to redirect when it should have failed"

    # test that the user was inserted into the database
    user = User.query.filter(User.email == email).first()
    assert (
        user is None
    ), f"found user for email {user.email} although no user should exist"


def test_register_group_leader_mismatched_password(client, session):
    # test that viewing the page renders without template errors
    assert client.get("/register").status_code == 200

    role = "group_leader"
    email = "test_scientist@science.com"
    password = "password"
    wrong_password = "noooooooo"
    # test that successful registration redirects to the login page
    form = RegisterUserForm(
        **{
            "role": role,
            "email": email,
            "confirm_email": email,
            "password": password,
            "confirm_password": wrong_password,
        },
    )
    response = client.post(
        "/register",
        data=form.data,
    )
    # TODO: do more research to see if I can access to the active view of the html despirte using turbo streams
    # with this strategy, I can be sure that turbo.push ran in the view file, but it would be better to access the actual html
    assert (
        response.get_data(as_text=True) == "Passwords must match."
    ), "Received an unexpected response error for mismatched passwords"

    assert (
        response.status_code == 200
    ), "expected reponse code 200 for mismatched password, success sending back turbo-stream"
    assert (
        "Location" not in response.headers
    ), "registration response tried to redirect when it should have failed"
    # test that the user was inserted into the database
    user = User.query.filter(User.email == email).first()
    assert (
        user is None
    ), f"found user for email {user.email} although no user should exist"


def test_register_group_leader_mismatched_password_and_mismatched_email(
    client, session
):
    # test that viewing the page renders without template errors
    assert client.get("/register").status_code == 200

    role = "group_leader"
    email = "test_scientist@science.com"
    wrong_email = "no@no.com"
    password = "password"
    wrong_password = "no"
    # test that successful registration redirects to the login page
    form = RegisterUserForm(
        **{
            "role": role,
            "email": email,
            "confirm_email": wrong_email,
            "password": password,
            "confirm_password": wrong_password,
        },
    )
    response = client.post(
        "/register",
        data=form.data,
    )
    assert (
        response.get_data(as_text=True)
        == "Make sure your email entries match, Passwords must match."
    )
    # assert re.search(  # TODO: Do a more robust check by giving flashed messages an idea in html, make beautiful soup object and find those messages specifically
    #     "Make sure your email entries match", response.get_data(as_text=True)
    # ), "did not find wrong email flashed message in response body"
    # assert re.search(  # TODO: Do a more robust check by giving flashed messages an idea in html, make beautiful soup object and find those messages specifically
    #     "Passwords must match.", response.get_data(as_text=True)
    # ), "did not find wrong email flashed message in response body"
    assert (
        "Location" not in response.headers
    ), "registration response tried to redirect when it should have failed"

    # test that the user was inserted into the database
    user = User.query.filter(User.email == email).first()
    assert (
        user is None
    ), f"found user for email {user.email} although no user should exist"


def test_register_scientist_duplicate_email(client, session):
    # test that viewing the page renders without template errors
    role = "scientist"
    email = "test_scientist@science.com"
    password = "password"
    add_user(role, email, password)

    assert client.get("/register").status_code == 200

    form = RegisterUserForm(
        **{
            "role": role,
            "email": email,
            "confirm_email": email,
            "password": password,
            "confirm_password": password,
        },
    )
    response = client.post(
        "/register",
        data=form.data,
    )

    assert re.search(  # TODO: Do a more robust check by giving flashed messages an idea in html, make beautiful soup object and find those messages specifically
        "Email already registered", response.get_data(as_text=True)
    ), "did not find 'Email already registered' in response body although using duplicate email.."
    assert (
        "Location" not in response.headers
    ), "registration response tried to redirect when it should have failed"
    assert (
        response.status_code == 200
    ), f"expected status_code 200 because of failed registration, but got {response.status_code}"


# def test_registered_logout(client, app, session):
#     user = add_user("scientist", "test_scientist@science.com", "fake_password")

#     rv = login(client, "test_scientist@science.com", "fake_password")
#     assert (
#         b"You've successfully logged in." in rv.data
#     ), "success flash message isn't shown"

#     response = client.get("/home")
#     assert (
#         response.status_code == 302
#     ), f"Expected redirect status_code 302, but got {response.status_code} instead."
#     assert (
#         "http://localhost/home" == response.headers["Location"]
#     ), "login response header did not redirect to /home as expected"


# def test_add_category_post(app, session):
#     """Does add category post a new category?"""
#     TESTEMAIL = "test@test.org"
#     TESTUSER = "Joe Test"
#     user = Users.query.filter(Users.email==TESTEMAIL).first()
#     category = Category(name="Added Category", users_id=user.id)
#     form = CategoryForm(formdata=None, obj=category)
#     with app.test_client() as c:
#         with c.session_transaction() as sess:
#             sess['email'] = TESTEMAIL
#             sess['username'] = TESTUSER
#             sess['users_id'] = user.id
#             response = c.post(
#                 '/category/add', data=form.data, follow_redirects=True)
#     assert response.status_code == 200
#     added_category = Category.query.filter(
#         Category.name=="Added Category").first()
#     assert added_category
#     session.delete(added_category)
#     session.commit()
