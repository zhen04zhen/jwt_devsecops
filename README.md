# JWT DevSecOps Demo

A simple JWT login authentication REST API built with Python and Flask, demonstrating a DevSecOps CI/CD pipeline using GitHub Actions.

## Language & Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.12 |
| Framework | Flask 3.1.3 |
| Authentication | JWT (PyJWT 2.13.0) |
| Password Hashing | bcrypt 4.1.3 |
| Testing | pytest 9.0.3 + pytest-flask 1.3.0 |
| Containerization | Docker |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/login` | Login and receive JWT token |
| GET | `/protected` | Protected route (requires JWT token) |

### Login Example

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "pass123"}'
```

Response:
```json
{"token": "<JWT_TOKEN>"}
```

### Access Protected Route

```bash
curl http://localhost:5000/protected \
  -H "Authorization: Bearer <your_token>"
```

Response:
```json
{"message": "Hello alice", "status": "authorized"}
```

## Running Locally

```bash
docker build -t jwt-api .
docker run -e JWT_SECRET=your-secret-key-at-least-32-characters -p 5000:5000 jwt-api
```

## Running Tests

```bash
docker run --rm -e JWT_SECRET=test-secret-key-at-least-32-characters jwt-api pytest tests/ -v
```

## DevSecOps Pipeline

This project uses GitHub Actions to automatically run the following security checks on every push:

| Step | Tool | Purpose |
|------|------|---------|
| Test | pytest | Automated unit tests |
| Secret Scan | Gitleaks | Detect hardcoded secrets in code |
| SAST | ShiftLeft Scan | Static application security testing |
| Dependency Scan | pip-audit | Scan for known CVEs in dependencies |
| Container Scan | Trivy | Scan Docker image for vulnerabilities |
| Dockerfile Scan | Dockle | Check Dockerfile security best practices |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `JWT_SECRET` | Secret key for signing JWT tokens (min. 32 characters) |

Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```

## Test Accounts

| Username | Password |
|----------|----------|
| alice | pass123 |
| bob | pass456 |
