"""
SQLAlchemy Account model for the Customer Accounts Microservice.
"""
import logging
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DataValidationError(Exception):
    """Raised when data validation fails for an Account."""

    pass


class Account(db.Model):
    """Account model representing a customer account.

    Attributes:
        id (int): Primary key.
        name (str): Customer name.
        email (str): Email address (unique).
        phone (str): Phone number.
        balance (float): Account balance (>= 0).
        locked (bool): Whether the account is locked.
    """

    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    locked = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<Account id={self.id} name='{self.name}' email='{self.email}'>"

    def to_dict(self):
        """Serialize the Account to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "balance": self.balance,
            "locked": self.locked,
        }

    def from_dict(self, data):
        """Populate the Account from a dictionary."""
        for key in ("name", "email", "phone", "balance", "locked"):
            if key in data:
                setattr(self, key, data[key])

    def create(self):
        """Create a new account in the database."""
        logging.info("Creating account %s", self.name)
        if self.balance is None:
            self.balance = 0.0
        if self.locked is None:
            self.locked = False
        if self.balance < 0:
            raise DataValidationError("balance must be non-negative")
        if not self.name:
            raise DataValidationError("name is required")
        if not self.email:
            raise DataValidationError("email is required")
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Update an existing account in the database."""
        logging.info("Updating account id=%s", self.id)
        if self.id is None:
            raise DataValidationError("cannot update an account without an id")
        if self.balance is not None and self.balance < 0:
            raise DataValidationError("balance must be non-negative")
        db.session.commit()

    def delete(self):
        """Delete the account from the database."""
        logging.info("Deleting account id=%s", self.id)
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def all(cls):
        """Return all accounts."""
        logging.info("Retrieving all accounts")
        return cls.query.all()

    @classmethod
    def find(cls, account_id):
        """Find an account by id. Returns None if not found."""
        logging.info("Finding account id=%s", account_id)
        return db.session.get(cls, account_id)

    @classmethod
    def find_by_email(cls, email):
        """Find an account by email. Returns None if not found."""
        logging.info("Finding account by email %s", email)
        return cls.query.filter(cls.email == email).first()

    @classmethod
    def find_by_name(cls, name):
        """Find accounts by name (may return multiple)."""
        logging.info("Finding accounts by name %s", name)
        return cls.query.filter(cls.name == name).all()


def init_db():
    """Create all database tables."""
    db.create_all()
