from flask_login import current_user
from flask_app.views.forms import RegisterMatchForm
from flask_app.models import User, Group
from utils import add_user, login, logout

def add_match():
    pass

def test_create_match(client, session, test_with_authenticated_user):
    assert client.get("/login").status_code == 200

    role = "scientist"
    email = "create_match@create_match.com"
    password = "fake_password"

    add_user(role, email, password)
    login_res = login(client, email, password)

    form = RegisterMatchForm(
        name="testgroup1",
        school_district="Philadelphia district",
        city="Philadelphia",
        state="Pennsylvania",
        country="US",
        time_zone="EST",
        monday_start_time="09:00",
        scientist_preferred_type="cool ones",
    )
    create_group_res = client.post("/matches/register", data=form.data)
    assert (
        create_group_res.status_code == 201
    ), f"expected status_code 201 for creating group, but got {create_group_res.status_code}. Available errors: {create_group_res.get_data(as_text=True)}"

    g = Group.query.filter(Group.name == form.name.data).first()
    user = User.query.filter(User.email == email).first()
    assert g.id > 0
    assert g.user_id == user.id
    logout_res = logout(client)
