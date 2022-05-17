import pytest
from sqlalchemy import desc
from flask.testing import FlaskClient
from app import db, create_app
from app.controllers import init_db
from app.models import User, Transaction
from .utils import login, logout


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


def test_finance_page(client):
    response = client.get("/finance")
    assert response.status_code == 302
    login(client)
    response = client.get("/finance")
    assert response.status_code == 200
    assert b"Action" in response.data
    assert b"Payrolled" in response.data
    assert b"Package" in response.data
    assert b"Recipient" in response.data


def test_finance_search(client):
    TEST_FINANCE_SEARCH_URL = "/finance_search/100"
    response = client.get(TEST_FINANCE_SEARCH_URL)
    assert response.status_code == 302
    login(client)
    response = client.get(TEST_FINANCE_SEARCH_URL)
    assert response.status_code == 200
    assert b"Payrolled" in response.data
    assert b"100" in response.data
