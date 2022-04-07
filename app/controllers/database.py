from flask import current_app as app
from app.models import User, Account, Billing
from app import db
from app.logger import log
from .account import gen_login, gen_password

TEST_USERS_NUMBER = 120
TEST_ACCOUNTS_PER_USER = 2
TEST_BILLINGS_PER_USER = 2
TEST_PASS = "pass"


def init_db(add_test_data: bool = False):
    """fill database by initial data

    Args:
        add_test_data (bool, optional): will add test data if set True. Defaults to False.
    """
    log(log.INFO, "Add admin account: %s", app.config["ADMIN_USER"])
    User(
        username=app.config["ADMIN_USER"],
        password=app.config["ADMIN_PASS"],
        role="admin",
    ).save(False)
    if add_test_data:
        log(log.INFO, "Generate test data")
        for i in range(TEST_USERS_NUMBER):
            user = User(username=f"user_{i+2}", password=TEST_PASS).save()
            for _ in range(TEST_ACCOUNTS_PER_USER):
                Account(
                    user_id=user.id, login=gen_login(), password=gen_password()
                ).save()
            for _ in range(TEST_BILLINGS_PER_USER):
                Billing(user_id=user.id, credits=1000).save(False)

    db.session.commit()
