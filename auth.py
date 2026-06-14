import os
from datetime import datetime, timedelta, timezone

import jwt

JWT_SECRET = os.environ.get("JWT_SECRET", "dev-only-default")
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = 1


def generate_token(username: str) -> str:
    payload = {
        "sub": username,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRY_HOURS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> str:
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    return payload["sub"]
