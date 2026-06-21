# Customer Accounts Microservice

![Build Status](https://github.com/azizhamoud35/devops-capstone/actions/workflows/ci-build.yaml/badge.svg)
[![Python](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Overview

The **Customer Accounts Microservice** is a RESTful Flask microservice that
manages customer account data with full **CRUD** (Create, Read, Update, Delete)
operations. It is part of the IBM DevOps Capstone project and demonstrates a
production-ready, containerized, CI/CD-enabled microservice built with Flask,
SQLAlchemy, Flask-Talisman (security headers), and Flask-CORS.

## Features

- Create, read, update, and delete customer accounts
- Account fields: `id`, `name`, `email`, `phone`, `balance`, `locked`
- Security headers via [Flask-Talisman](https://github.com/GoogleCloudPlatform/flask-talisman)
- Cross-Origin Resource Sharing via [Flask-CORS](https://flask-cors.readthedocs.io/)
- Health check endpoint for container orchestration probes
- Pytest test suite with coverage reporting
- Flake8 linting in CI
- Dockerized deployment on port 8080 with Gunicorn
- GitHub Actions CI/CD pipeline

## API Endpoints

| Method   | Endpoint              | Description           |
| -------- | --------------------- | --------------------- |
| `POST`   | `/api/accounts`       | Create an account    |
| `GET`    | `/api/accounts`       | List all accounts     |
| `GET`    | `/api/accounts/<id>`  | Get an account by id |
| `PUT`    | `/api/accounts/<id>`  | Update an account     |
| `DELETE` | `/api/accounts/<id>`  | Delete an account     |
| `GET`    | `/api/accounts/health`| Health check          |

## Project Structure

```
devops-capstone/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── user-story.md
│   └── workflows/
│       └── ci-build.yaml
├── service/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── common.py
├── tests/
│   ├── test_models.py
│   └── test_routes.py
├── Dockerfile
├── README.md
├── requirements.txt
└── setup.cfg
```

## Getting Started

### Run locally (development)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask development server (port 5000)
FLASK_APP=service flask run --port 5000
```

### Run with Docker (production)

```bash
docker build -t accounts-service .
docker run -p 8080:8080 accounts-service
```

The service is then available at `http://localhost:8080`.

### Run tests

```bash
pytest --cov=service tests
```

## CI/CD

Continuous integration is defined in
[`.github/workflows/ci-build.yaml`](.github/workflows/ci-build.yaml).
The pipeline runs on every push or pull request to `main`/`master` and:

1. Checks out the repository
2. Sets up Python 3.9
3. Installs dependencies
4. Lints with Flake8
5. Runs pytest with coverage
6. Uploads the coverage report as a build artifact

## Repository

https://github.com/azizhamoud35/devops-capstone

## License

MIT License
