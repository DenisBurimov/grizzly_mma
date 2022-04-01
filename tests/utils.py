from app.models import User

from app.controllers.database import TEST_PASS


def register(username, password=TEST_PASS):
    user = User(username=username, password=password)
    user.save()
    return user.id


def login(client, username, password=TEST_PASS):
    return client.post(
        "/login", data=dict(username=username, password=password), follow_redirects=True
    )


def logout(client):
    return client.get("/logout", follow_redirects=True)
