import time
import timecop
from onetimepass import get_hotp, get_totp
from app.models import User
from config import BaseConfig as conf

from app.controllers.database import TEST_PASS


def register(username, password=TEST_PASS):
    user = User(username=username, password=password)
    user.save()
    return user.id


def login(client, user_name=conf.ADMIN_USER, password=conf.ADMIN_PASS):
    if conf.AUTH_OTP_ENABLED:
        secret = b"MFRGGZDFMZTWQ2LK"
        with timecop.freeze(time.time()):
            user = User.query.filter(User.username == user_name).first()
            assert user
            user.otp_secret = secret
            user.otp_active = True
            user.save()
            hotp = get_hotp(
                secret=secret,
                intervals_no=int(time.time()) // 30,
            )
            totp = get_totp(secret=secret)
            assert hotp == totp
            res = client.post(
                "/login",
                data=dict(username=user_name, password=password),
                follow_redirects=True,
            )
            assert res.status_code == 200
            if b"Wrong username or password." in res.data:
                return res
            res = client.post(
                "/otp_verify",
                data=dict(token=f"{totp:06d}"),
                follow_redirects=True,
            )
            assert b"You are successfully logged in" in res.data
            return res
    else:
        res = client.post(
            "/login",
            data=dict(username=user_name, password=password),
            follow_redirects=True,
        )
        assert res.status_code == 200
        return res


def logout(client):
    return client.get("/logout", follow_redirects=True)
