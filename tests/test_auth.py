import pytest

from app import db, create_app
from app.controllers import init_db
from tests.utils import login, logout


@pytest.fixture
def client():
    app = create_app(environment="testing")
    app.config["TESTING"] = True

    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()
        db.drop_all()
        db.create_all()
        init_db()
        yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


def test_auth_pages(client):
    response = client.get("/login")
    assert response.status_code == 200
    response = client.get("/logout")
    assert response.status_code == 302


def test_login_and_logout(client):
    # Access to logout view before login should fail.
    response = logout(client)
    assert b"Please log in to access this page." in response.data
    response = login(client)
    assert b"Billings" in response.data
    # Should successfully logout the currently logged in user.
    response = logout(client)
    assert b"Please log in to access this page." in response.data
    # Correct credentials should login
    response = login(client)
    assert b"You are successfully logged in!" in response.data
