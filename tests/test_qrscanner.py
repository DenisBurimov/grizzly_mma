import pytest
from flask.testing import FlaskClient
from app import db, create_app
from app.controllers import init_db
from app.models import Account
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


def test_get_qrcode_data(client: FlaskClient, monkeypatch):
    import app.controllers

    login(client)

    TEST_PUBLIC_KEY = """{'public_key': 'MIICIjANBgkqhkiG9w0BAQEFAAOCAgKCAgEAxbwddmSg0tVAr3t9ZdaPUQ==' """
    TEST_QRCODE = b"test"

    def mock_get_qrcode_public_key(input_string):
        itemText = TEST_PUBLIC_KEY
        return itemText

    monkeypatch.setattr(
        app.controllers, "get_qrcode_public_key", mock_get_qrcode_public_key
    )

    def mock_get_paid_qrcode(credits: int) -> bytes:
        return TEST_QRCODE

    monkeypatch.setattr(app.controllers, "get_paid_qrcode", mock_get_paid_qrcode)

    response = client.post(
        "/account_info/3",
        data=dict(qr_data="no_matter_what"),
    )

    assert response.status_code == 200

    # account: Account = Account.query.order_by(desc(Account.id)).first()
    account: Account = Account.query.get(3)
    assert account.public_key == TEST_PUBLIC_KEY
