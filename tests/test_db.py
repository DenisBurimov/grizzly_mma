import pytest

from app import db, create_app
from app.controllers import init_db
from app.controllers.database import TEST_USERS_NUMBER
from app.models import User


@pytest.fixture
def client():
    app = create_app(environment="testing")
    app.config["TESTING"] = True

    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()
        db.drop_all()
        db.create_all()
        yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


def test_db_init(client):
    init_db(True)
    assert User.query.count() == TEST_USERS_NUMBER + 1
