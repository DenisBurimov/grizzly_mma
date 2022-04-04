import pytest

from app import db, create_app
from app.controllers import init_db
from .utils import login

from app.models import Account


@pytest.fixture
def client():
    app = create_app(environment="testing")
    app.config["TESTING"] = True

    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()
        db.drop_all()
        db.create_all()
        init_db(True)
        yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


def test_accounts_pages(client):
    response = client.get("/accounts")
    assert response.status_code == 302
    login(client, "user_2")
    response = client.get("/accounts")
    assert response.status_code == 200


def test_add_account(client):
    TEST_LOGIN = "TEST_LOGIN"
    TEST_PASSWORD = "TEST_PASS"

    res = client.post(
        "/account_add", data=dict(login=TEST_LOGIN, password=TEST_PASSWORD)
    )
    assert res.status_code == 302

    login(client, "user_2")
    res = client.post(
        "/account_add",
        data=dict(login=TEST_LOGIN, password=TEST_PASSWORD),
        follow_redirects=True,
    )
    assert res.status_code == 200

    account: Account = Account.query.all()[-1]

    assert account.login == TEST_LOGIN
    assert account.password == TEST_PASSWORD

    assert f"{TEST_LOGIN}" in res.data.decode()


# def test_login_and_logout(client):
#     # Access to logout view before login should fail.
#     response = logout(client)
#     assert b"Please log in to access this page." in response.data
#     register("sam")
#     response = login(client, "sam")
#     assert b"Login successful." in response.data
#     # Should successfully logout the currently logged in user.
#     response = logout(client)
#     assert b"You were logged out." in response.data
#     # Incorrect login credentials should fail.
#     response = login(client, "sam", "wrongpassword")
#     assert b"Wrong user ID or password." in response.data
#     # Correct credentials should login
#     response = login(client, "sam")
#     assert b"Login successful." in response.data
