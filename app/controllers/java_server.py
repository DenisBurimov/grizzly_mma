import requests
from urllib.parse import urljoin
from flask import current_app as app


def get_paid_qrcode(users_public_key: str, credits: int) -> bytes:
    base_url = app.config["URL_JAVA_SRV"]
    assert base_url
    url = urljoin(base_url, "/credit")
    data = {
        "key": users_public_key,
        "amount": credits,
    }

    request = requests.post(url=url, json=data)
    request.raise_for_status()

    return request.content
