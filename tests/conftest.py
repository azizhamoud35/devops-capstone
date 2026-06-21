"""
Test fixtures and configuration for pytest.
"""
import pytest
from service import create_app
from service.models import db, Account


@pytest.fixture(scope="session")
def app():
    """Create the Flask application configured for testing."""
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "testing",
        "DEBUG": False,
    })
    with app.app_context():
        db.create_all()
    return app


@pytest.fixture(autouse=True)
def clean_db(app):
    """Clear all data from the database before each test."""
    with app.app_context():
        db.session.query(Account).delete()
        db.session.commit()
    yield
    with app.app_context():
        db.session.query(Account).delete()
        db.session.commit()


@pytest.fixture()
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture()
def account_data():
    """Sample account data for tests."""
    return {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "555-1234",
        "balance": 100.50,
        "locked": False,
    }


@pytest.fixture()
def account(app, account_data):
    """Create and return a sample Account object."""
    with app.app_context():
        account = Account(**account_data)
        account.create()
        return account
