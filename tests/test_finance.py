import pytest
from app import db, create_app
from app.controllers import init_db
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
    TEST_FINANCE_SEARCH_INT = "/finance_search/100"
    TEST_FINANCE_SEARCH_STR = "/finance_search/user"
    response = client.get(TEST_FINANCE_SEARCH_INT)
    assert response.status_code == 302
    login(client)
    response = client.get(TEST_FINANCE_SEARCH_INT)
    assert response.status_code == 200
    assert b"Payrolled" in response.data
    assert b"100" in response.data
    response = client.get(TEST_FINANCE_SEARCH_STR)
    assert b"Finance" in response.data
    assert b"admin" in response.data
    assert b"user_2" in response.data
    assert b"Standart transaction" in response.data
    assert b"100" in response.data
    response = client.get("/finance_search/100, admin")
    assert response.status_code == 200

    # import datetime

    # TODAY = datetime.datetime.today().strftime("%Y-%m-%d")
    # TEST_FINANCE_SEARCH_DATE = f"/finance_search/{TODAY}"
    # response = client.get(TEST_FINANCE_SEARCH_DATE)
    # assert f"{TODAY}" in response.data.decode()
