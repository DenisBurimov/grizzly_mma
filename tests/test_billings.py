import pytest

from app import db, create_app
from app.controllers import init_db
from app.models.billing import Billing
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

    TEST_CREDITS = 1001
    login(client)
    TEST_QRCODE = b"test"

    def mock_get_paid_qrcode(credits: int) -> bytes:
        return TEST_QRCODE

    monkeypatch.setattr(app.controllers, "get_paid_qrcode", mock_get_paid_qrcode)

    response = client.post(
        "/billing_add",
        data=dict(credits=TEST_CREDITS),
    )
    assert response.status_code == 302
    billing: Billing = Billing.query.filter(Billing.credits == TEST_CREDITS).first()
    assert billing.credits == TEST_CREDITS
    assert billing.qrcode == TEST_QRCODE
