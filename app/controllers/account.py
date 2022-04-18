import secrets
from config import BaseConfig as conf
from app.models import Account

LOGIN_LEN = 6


def gen_login() -> str:
    """Generation of a account login

    Returns:
        str: login value
    """
    ALPHABET = conf.ALPHABET_UP_DIGITS
    while True:
        login = "".join(secrets.choice(ALPHABET) for i in range(LOGIN_LEN))
        if (
            login[0].isdigit()
            and sum(c.isalpha() for c in login) >= 3
            and sum(c.isdigit() for c in login) >= 3
        ):
            if not Account.query.filter(Account.login == login).first():
                return login


def gen_password(pass_length=7) -> str:
    """Generation of a password for account

    Returns:
        str: password value
    """
    alphabet = conf.ALPHABET_FULL
    while True:
        password = "".join(secrets.choice(alphabet) for i in range(pass_length))
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password) >= 1
        ):
            return password
