from flask_app.models import User
from flask_app.views.forms import RegisterUserForm


def test_index(client):
    res = client.get("/")
    assert res.status_code == 200, "index not available, something big is wrong"


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
    # if not form.validate_on_submit():
    #     raise Exception("form constructed incorrectly in test")
    response = client.post(
        "/register",
        data=form.data,
    )
    assert (
        "http://localhost/home" == response.headers["Location"]
    ), "registration response header did not redictrt ot /home as expected"

    # test that the user was inserted into the database
    user = User.query.filter(User.email == email).first()
    assert user.email == email
    # with app.app_context():
    #     assert (
    #         get_db().execute("SELECT * FROM user WHERE username = 'a'").fetchone()
    #         is not None
    #     )


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
