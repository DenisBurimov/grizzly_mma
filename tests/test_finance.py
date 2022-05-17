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


def test_user_finance(client: FlaskClient):
    TEST_USER_ID = 5
    TEST_URL = f"/user_finance/{TEST_USER_ID}"
    # try w/o login
    res = client.get(TEST_URL)
    assert res.status_code == 302

    login(client, "user_2", "pass")
    res = client.get(TEST_URL)
    assert res.status_code == 302
    res = client.get(res.location, follow_redirects=True)
    assert res.status_code == 200
    assert b"Access denied" in res.data
    logout(client)

    login(client)
    res = client.get(TEST_URL)
    assert res.status_code == 200

    TEST_TRANS_TYPE = Transaction.Action.deposit.name
    TRANSACTION_AMOUNT = 1000
    PACKAGE_500_COST = 50
    PACKAGE_1000_COST = 100
    PACKAGE_1500_COST = 150
    PACKAGE_2500_COST = 250

    user: User = User.query.get(TEST_USER_ID)
    credits_before = user.credits_available

    res = client.post(
        TEST_URL,
        data=dict(
            transaction_type=TEST_TRANS_TYPE,
            transaction_amount=TRANSACTION_AMOUNT,
            package_500_cost=PACKAGE_500_COST,
            package_1000_cost=PACKAGE_1000_COST,
            package_1500_cost=PACKAGE_1500_COST,
            package_2500_cost=PACKAGE_2500_COST,
        ),
        follow_redirects=True,
    )
    assert res.status_code == 200

    user: User = User.query.get(TEST_USER_ID)

    assert user.credits_available == credits_before + TRANSACTION_AMOUNT

    transaction: Transaction = Transaction.query.order_by(desc(Transaction.id)).first()

    assert transaction.transaction_amount == TRANSACTION_AMOUNT
    assert transaction.admin.id == 1
    assert transaction.reseller.id == TEST_USER_ID
