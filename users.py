import bcrypt

_raw_users = {
    "alice": "pass123",
    "bob": "pass456",
}

users = {
    username: bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    for username, password in _raw_users.items()
}


def get_user(username: str):
    return users.get(username)
