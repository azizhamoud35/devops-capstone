"""
Test the Account model methods.
"""
import pytest
from service.models import Account, DataValidationError


######################################################################
#  MODEL TEST CASES
######################################################################

class TestAccountModel:
    """Test the Account model."""

    def test_create_account(self, app, account_data):
        """Create an account and add it to the database."""
        with app.app_context():
            account = Account(**account_data)
            account.create()
            assert account.id is not None
            assert account.name == account_data["name"]
            assert account.email == account_data["email"]
            assert account.phone == account_data["phone"]
            assert account.balance == account_data["balance"]
            assert account.locked == account_data["locked"]

    def test_create_account_defaults(self, app):
        """Test that balance and locked have defaults."""
        with app.app_context():
            account = Account(name="Jane", email="jane@example.com")
            account.create()
            assert account.balance == 0.0
            assert account.locked is False

    def test_create_account_missing_name(self, app):
        """Account with missing name should raise DataValidationError."""
        with app.app_context():
            account = Account(email="noname@example.com")
            with pytest.raises(DataValidationError):
                account.create()

    def test_create_account_missing_email(self, app):
        """Account with missing email should raise DataValidationError."""
        with app.app_context():
            account = Account(name="No Email")
            with pytest.raises(DataValidationError):
                account.create()

    def test_create_account_negative_balance(self, app):
        """Account with negative balance should raise DataValidationError."""
        with app.app_context():
            account = Account(name="Negative", email="neg@example.com", balance=-10.0)
            with pytest.raises(DataValidationError):
                account.create()

    def test_read_account(self, app, account_data):
        """Read an account back from the database."""
        with app.app_context():
            account = Account(**account_data)
            account.create()
            found = Account.find(account.id)
            assert found is not None
            assert found.name == account_data["name"]
            assert found.email == account_data["email"]

    def test_update_account(self, app, account_data):
        """Update an account."""
        with app.app_context():
            account = Account(**account_data)
            account.create()
            original_id = account.id
            account.name = "Updated Name"
            account.update()
            updated = Account.find(original_id)
            assert updated.name == "Updated Name"
            assert updated.id == original_id

    def test_update_account_without_id(self, app):
        """Updating an account without an id should raise DataValidationError."""
        with app.app_context():
            account = Account(name="No Id", email="noid@example.com")
            with pytest.raises(DataValidationError):
                account.update()

    def test_update_account_negative_balance(self, app):
        """Updating an account with negative balance should raise DataValidationError."""
        with app.app_context():
            account = Account(name="Update", email="update@example.com", balance=50.0)
            account.create()
            account.balance = -20.0
            with pytest.raises(DataValidationError):
                account.update()

    def test_delete_account(self, app, account_data):
        """Delete an account from the database."""
        with app.app_context():
            account = Account(**account_data)
            account.create()
            account_id = account.id
            account.delete()
            assert Account.find(account_id) is None

    def test_list_all_accounts(self, app):
        """List all accounts."""
        with app.app_context():
            for i in range(5):
                Account(
                    name=f"User {i}",
                    email=f"user{i}@example.com",
                ).create()
            accounts = Account.all()
            assert len(accounts) == 5

    def test_find_account(self, app, account_data):
        """Find an account by id."""
        with app.app_context():
            account = Account(**account_data)
            account.create()
            found = Account.find(account.id)
            assert found is not None
            assert found.email == account_data["email"]

    def test_find_account_not_found(self, app):
        """Finding a non-existent account returns None."""
        with app.app_context():
            assert Account.find(999) is None

    def test_find_by_email(self, app, account_data):
        """Find an account by email."""
        with app.app_context():
            account = Account(**account_data)
            account.create()
            found = Account.find_by_email(account_data["email"])
            assert found is not None
            assert found.name == account_data["name"]

    def test_find_by_email_not_found(self, app):
        """Finding by non-existent email returns None."""
        with app.app_context():
            assert Account.find_by_email("nobody@example.com") is None

    def test_find_by_name(self, app):
        """Find accounts by name."""
        with app.app_context():
            Account(name="Alice", email="alice1@example.com").create()
            Account(name="Alice", email="alice2@example.com").create()
            Account(name="Bob", email="bob@example.com").create()
            found = Account.find_by_name("Alice")
            assert len(found) == 2

    def test_find_by_name_not_found(self, app):
        """Finding by non-existent name returns empty list."""
        with app.app_context():
            assert Account.find_by_name("Nobody") == []

    def test_to_dict_serialization(self, app, account_data):
        """Test serialization to dictionary."""
        with app.app_context():
            account = Account(**account_data)
            account.create()
            data = account.to_dict()
            assert data["id"] == account.id
            assert data["name"] == account_data["name"]
            assert data["email"] == account_data["email"]
            assert data["phone"] == account_data["phone"]
            assert data["balance"] == account_data["balance"]
            assert data["locked"] == account_data["locked"]

    def test_from_dict_deserialization(self, app):
        """Test deserialization from dictionary."""
        with app.app_context():
            account = Account()
            data = {
                "name": "From Dict",
                "email": "fromdict@example.com",
                "phone": "555-0000",
                "balance": 250.0,
                "locked": True,
            }
            account.from_dict(data)
            assert account.name == "From Dict"
            assert account.email == "fromdict@example.com"
            assert account.phone == "555-0000"
            assert account.balance == 250.0
            assert account.locked is True

    def test_from_dict_partial_data(self, app):
        """Test deserialization with partial data."""
        with app.app_context():
            account = Account(name="Partial", email="partial@example.com")
            account.from_dict({"phone": "555-1111"})
            assert account.phone == "555-1111"
            assert account.name == "Partial"

    def test_repr(self, app, account_data):
        """Test the string representation of an Account."""
        with app.app_context():
            account = Account(**account_data)
            account.create()
            repr_str = repr(account)
            assert "Account" in repr_str
            assert account.name in repr_str
            assert account.email in repr_str

    def test_duplicate_email_raises(self, app):
        """Creating an account with a duplicate email should fail."""
        with app.app_context():
            Account(name="First", email="dup@example.com").create()
            with pytest.raises(Exception):
                Account(name="Second", email="dup@example.com").create()
