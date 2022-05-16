import pytest
import datetime
from sqlalchemy import desc
from app import db, create_app
from app.controllers import init_db
from app.models import Billing
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


def test_billings_page(client):
    response = client.get("/billings")
    assert response.status_code == 302
    login(client)
    response = client.get("/billings")
    assert response.status_code == 200
    assert b"Package" in response.data
    assert b"Cost" in response.data
    assert b"Target" in response.data
    assert b"user_10" in response.data


def test_billings_add_page(client):
    response = client.get("/billing_add")
    assert response.status_code == 302
    login(client)
    response = client.get("/billing_add")
    assert response.status_code == 200
    response = client.get("/billing_add")
    assert b"Get credits" in response.data


def test_create_billing(client, monkeypatch):
    import app.controllers

    TEST_ACCOUNT_ID = 1
    TEST_PUBLIC_KEY = "abrashwabracadabra=="
    TEST_CREDITS = 1000
    login(client, "user_2", "pass")
    TEST_QRCODE = b"test"
    TEST_PACKAGE_COST = 100

    def mock_get_paid_qrcode(users_public_key: str, credits: int) -> bytes:
        return TEST_QRCODE

    monkeypatch.setattr(app.controllers, "get_paid_qrcode", mock_get_paid_qrcode)
    response = client.post(
        "/billing_add",
        data=dict(
            account=TEST_ACCOUNT_ID,
            users_public_key=TEST_PUBLIC_KEY,
            credits=TEST_CREDITS,
        ),
        follow_redirects=True,
    )
    assert response.status_code == 200
    billing: Billing = Billing.query.order_by(desc(Billing.id)).first()
    assert billing.credits == TEST_CREDITS
    assert billing.qrcode == TEST_QRCODE
    assert billing.account_id == TEST_ACCOUNT_ID
    assert billing.cost == TEST_PACKAGE_COST


def test_billing_search(client):
    login(client)
    response = client.get("/billing_search/1000")
    assert b"1000" in response.data

    today = datetime.datetime.today().strftime("%Y-%m-%d")
    response = client.get(f"/billing_search/{today}")
    assert f"{today}" in response.data.decode()
    response = client.get("/billing_search/r_2")
    assert b"r_2" in response.data
