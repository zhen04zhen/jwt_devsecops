import bcrypt
import jwt
from flask import Flask, jsonify, request

from auth import generate_token, verify_token
from users import get_user

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Missing username or password"}), 400

    username = data["username"]
    password = data["password"]

    hashed = get_user(username)
    if hashed is None:
        return jsonify({"error": "Invalid credentials"}), 401

    if not bcrypt.checkpw(password.encode(), hashed):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(username)
    return jsonify({"token": token})


@app.route("/protected")
def protected():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Token missing"}), 401

    token = auth_header.split(" ")[1]

    try:
        username = verify_token(token)
        return jsonify({"message": f"Hello {username}", "status": "authorized"})
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired, please login again"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
