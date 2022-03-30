from app.models import User


def register(username, password="password"):
    user = User(username=username, password=password)
    user.save()
    return user.id


def login(client, username, password="password"):
    return client.post(
        "/login", data=dict(username=username, password=password), follow_redirects=True
    )


def logout(client):
    return client.get("/logout", follow_redirects=True)
