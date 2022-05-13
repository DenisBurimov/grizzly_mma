import pytest
from sqlalchemy import desc
from app import db, create_app
from app.controllers import init_db
from app.models import User
from .utils import login


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


def test_users_page(client):
    response = client.get("/users")
    assert response.status_code == 302
    login(client)
    response = client.get("/users")
    assert response.status_code == 200
    assert b"Users" in response.data
    assert b"Role" in response.data
    assert b"Spent" in response.data
    assert b"Balance" in response.data
    assert b"Credit" in response.data
    assert b"Action" in response.data


def test_add_user(client):
    login(client)
    TEST_USERNAME = "TEST_USERNAME"
    TEST_PASSWORD = "TEST_PASS"
    TEST_ROLE = 1

    res = client.post(
        "/user_add",
        data=dict(
            username=TEST_USERNAME,
            password=TEST_PASSWORD,
            password_confirm=TEST_PASSWORD,
            role=TEST_ROLE,
        ),
        follow_redirects=True,
    )
    assert res.status_code == 200

    user: User = User.query.order_by(desc(User.id)).first()

    assert user.username == TEST_USERNAME
    assert user.credits_available == 0
    assert user.credit_alowed is False


# def test_user_delete(client):
#     response = client.get("/user_delete/10")
#     assert response.status_code == 302
#     user: User = User.query.get(10)
#     assert user.deleted is True
