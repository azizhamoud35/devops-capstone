"""
CRUD routes for the Customer Accounts Microservice.
Uses Flask RESTful style with jsonify responses.
"""
from flask import Blueprint, request, jsonify, abort
from service.models import Account, DataValidationError
from service.common import status
api_bp = Blueprint("api", __name__, url_prefix="/accounts")


######################################################################
# HEALTH CHECK
######################################################################

@api_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify(status="OK", message="Account service is running"), status.HTTP_200_OK


######################################################################
# CREATE AN ACCOUNT
# POST /api/accounts
######################################################################

@api_bp.route("", methods=["POST"])
@api_bp.route("/", methods=["POST"])
def create_accounts():
    """Create a new account."""
    data = request.get_json(silent=True)
    if data is None:
        abort(status.HTTP_400_BAD_REQUEST, "No JSON data provided")
    account = Account()
    try:
        account.from_dict(data)
        account.create()
    except DataValidationError as error:
        abort(status.HTTP_400_BAD_REQUEST, str(error))
    except Exception as error:  # pragma: no cover
        abort(status.HTTP_409_CONFLICT, str(error))
    return jsonify(account.to_dict()), status.HTTP_201_CREATED


######################################################################
# LIST ALL ACCOUNTS
# GET /api/accounts
######################################################################

@api_bp.route("", methods=["GET"])
@api_bp.route("/", methods=["GET"])
def list_accounts():
    """List all accounts."""
    accounts = Account.all()
    results = [account.to_dict() for account in accounts]
    return jsonify(results), status.HTTP_200_OK


######################################################################
# GET A SINGLE ACCOUNT
# GET /api/accounts/:id
######################################################################

@api_bp.route("/<int:account_id>", methods=["GET"])
def get_account(account_id):
    """Get a single account by id."""
    account = Account.find(account_id)
    if account is None:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id '{account_id}' was not found.")
    return jsonify(account.to_dict()), status.HTTP_200_OK


######################################################################
# UPDATE AN ACCOUNT
# PUT /api/accounts/:id
######################################################################

@api_bp.route("/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    """Update an existing account by id."""
    account = Account.find(account_id)
    if account is None:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id '{account_id}' was not found.")
    data = request.get_json(silent=True)
    if data is None:
        abort(status.HTTP_400_BAD_REQUEST, "No JSON data provided")
    try:
        account.from_dict(data)
        account.update()
    except DataValidationError as error:
        abort(status.HTTP_400_BAD_REQUEST, str(error))
    return jsonify(account.to_dict()), status.HTTP_200_OK


######################################################################
# DELETE AN ACCOUNT
# DELETE /api/accounts/:id
######################################################################

@api_bp.route("/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    """Delete an account by id."""
    account = Account.find(account_id)
    if account is None:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id '{account_id}' was not found.")
    account.delete()
    return "", status.HTTP_204_NO_CONTENT
