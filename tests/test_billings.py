import pytest

from app import db, create_app
from app.controllers import init_db
from .utils import login

from app.models import Billing


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


def test_billings_page(client):
    response = client.get("/billings")
    assert response.status_code == 302
    login(client)
    response = client.get("/billings")
    assert response.status_code == 200


def test_billings_add_page(client):
    response = client.get("/billing_add")
    assert response.status_code == 302
    login(client)
    response = client.get("/billing_add")
    assert response.status_code == 200
    response = client.get("/billing_add")
    assert b"Get credits" in response.data


def test_billings_details_page(client):
    response = client.get("/billings_details/1")
    assert response.status_code == 302
    login(client)
    response = client.get("/billings_details/1")
    assert response.status_code == 200
    response = client.get("/billings_details/1")
    assert b"1000" in response.data
    response = client.get("/billings_details/3")
    assert b"user_3" in response.data
