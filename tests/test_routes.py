"""
Test the CRUD routes of the Customer Accounts Microservice.
"""
from service.models import Account
from service.common import status


######################################################################
#  HEALTH CHECK TESTS
######################################################################

class TestHealthCheck:
    """Test the health check endpoint."""

    def test_health_check(self, client):
        """Health check should return 200 and OK status."""
        resp = client.get("/api/accounts/health")
        assert resp.status_code == status.HTTP_200_OK
        payload = resp.get_json()
        assert payload["status"] == "OK"


######################################################################
#  CREATE ACCOUNT TESTS (POST)
######################################################################

class TestCreateRoutes:
    """Test the Create (POST) routes."""

    def test_create_account(self, client, account_data):
        """Create a new account."""
        resp = client.post(
            "/api/accounts",
            json=account_data,
            content_type="application/json",
        )
        assert resp.status_code == status.HTTP_201_CREATED
        payload = resp.get_json()
        assert payload["id"] is not None
        assert payload["name"] == account_data["name"]
        assert payload["email"] == account_data["email"]
        assert payload["balance"] == account_data["balance"]

    def test_create_account_no_data(self, client):
        """Creating an account without data should return 400."""
        resp = client.post("/api/accounts", content_type="application/json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_account_no_content_type(self, client):
        """Creating an account without content type should return 400."""
        resp = client.post("/api/accounts", data="no json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_account_missing_name(self, client):
        """Creating an account with missing name should return 400."""
        data = {"email": "noname@example.com"}
        resp = client.post(
            "/api/accounts",
            json=data,
            content_type="application/json",
        )
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_account_missing_email(self, client):
        """Creating an account with missing email should return 400."""
        data = {"name": "No Email"}
        resp = client.post(
            "/api/accounts",
            json=data,
            content_type="application/json",
        )
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_account_negative_balance(self, client):
        """Creating an account with negative balance should return 400."""
        data = {"name": "Neg", "email": "neg@example.com", "balance": -5.0}
        resp = client.post(
            "/api/accounts",
            json=data,
            content_type="application/json",
        )
        assert resp.status_code == status.HTTP_400_BAD_REQUEST


######################################################################
#  LIST ACCOUNTS TESTS (GET)
######################################################################

class TestListRoutes:
    """Test the List (GET all) routes."""

    def test_list_accounts_empty(self, client):
        """List accounts when database is empty."""
        resp = client.get("/api/accounts")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.get_json() == []

    def test_list_accounts_with_data(self, client, app):
        """List accounts with data."""
        with app.app_context():
            Account(name="User1", email="user1@example.com").create()
            Account(name="User2", email="user2@example.com").create()
        resp = client.get("/api/accounts")
        assert resp.status_code == status.HTTP_200_OK
        payload = resp.get_json()
        assert len(payload) == 2

    def test_list_accounts_root_path(self, client):
        """List accounts at root path with trailing slash."""
        resp = client.get("/api/accounts/")
        assert resp.status_code == status.HTTP_200_OK


######################################################################
#  GET SINGLE ACCOUNT TESTS (GET /:id)
######################################################################

class TestGetRoutes:
    """Test the Get single account (GET /:id) routes."""

    def test_get_account(self, client, app, account_data):
        """Get an existing account by id."""
        with app.app_context():
            account = Account(**account_data)
            account.create()
            account_id = account.id
        resp = client.get(f"/api/accounts/{account_id}")
        assert resp.status_code == status.HTTP_200_OK
        payload = resp.get_json()
        assert payload["id"] == account_id
        assert payload["name"] == account_data["name"]

    def test_get_account_not_found(self, client):
        """Getting a non-existent account should return 404."""
        resp = client.get("/api/accounts/999")
        assert resp.status_code == status.HTTP_404_NOT_FOUND


######################################################################
#  UPDATE ACCOUNT TESTS (PUT /:id)
######################################################################

class TestUpdateRoutes:
    """Test the Update (PUT /:id) routes."""

    def test_update_account(self, client, app, account_data):
        """Update an existing account."""
        with app.app_context():
            account = Account(**account_data)
            account.create()
            account_id = account.id
        update_data = {"name": "Updated Name", "email": "updated@example.com"}
        resp = client.put(
            f"/api/accounts/{account_id}",
            json=update_data,
            content_type="application/json",
        )
        assert resp.status_code == status.HTTP_200_OK
        payload = resp.get_json()
        assert payload["name"] == "Updated Name"
        assert payload["email"] == "updated@example.com"

    def test_update_account_not_found(self, client):
        """Updating a non-existent account should return 404."""
        resp = client.put(
            "/api/accounts/999",
            json={"name": "Updated"},
            content_type="application/json",
        )
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_update_account_no_data(self, client, app, account_data):
        """Updating an account without data should return 400."""
        with app.app_context():
            account = Account(**account_data)
            account.create()
            account_id = account.id
        resp = client.put(f"/api/accounts/{account_id}")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_account_negative_balance(self, client, app, account_data):
        """Updating an account with negative balance should return 400."""
        with app.app_context():
            account = Account(**account_data)
            account.create()
            account_id = account.id
        update_data = {"balance": -50.0}
        resp = client.put(
            f"/api/accounts/{account_id}",
            json=update_data,
            content_type="application/json",
        )
        assert resp.status_code == status.HTTP_400_BAD_REQUEST


######################################################################
#  DELETE ACCOUNT TESTS (DELETE /:id)
######################################################################

class TestDeleteRoutes:
    """Test the Delete (DELETE /:id) routes."""

    def test_delete_account(self, client, app, account_data):
        """Delete an existing account."""
        with app.app_context():
            account = Account(**account_data)
            account.create()
            account_id = account.id
        resp = client.delete(f"/api/accounts/{account_id}")
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        # Verify it's gone
        resp2 = client.get(f"/api/accounts/{account_id}")
        assert resp2.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_account_not_found(self, client):
        """Deleting a non-existent account should return 404."""
        resp = client.delete("/api/accounts/999")
        assert resp.status_code == status.HTTP_404_NOT_FOUND


######################################################################
#  SECURITY HEADER TESTS
######################################################################

class TestSecurityHeaders:
    """Test that security headers are present in responses."""

    def test_security_headers_present(self, client):
        """Verify that Talisman security headers are in the response."""
        resp = client.get("/api/accounts/health")
        assert resp.status_code == status.HTTP_200_OK
        # Talisman should set X-Content-Type-Options
        assert resp.headers.get("X-Content-Type-Options") == "nosniff"
        # X-Frame-Options should be set by Talisman
        assert resp.headers.get("X-Frame-Options") is not None
        # Referrer-Policy should be set by Talisman
        assert resp.headers.get("Referrer-Policy") is not None

    def test_cors_header_present(self, client):
        """Verify that CORS does not block requests."""
        resp = client.get("/api/accounts/health")
        assert resp.status_code == status.HTTP_200_OK
        # CORS should allow the response through
        assert resp.headers.get("Access-Control-Allow-Origin") is not None

    def test_method_not_allowed(self, client):
        """Unsupported method should return 405."""
        resp = client.patch("/api/accounts/1")
        # PATCH on specific account id is not defined
        assert resp.status_code in (
            status.HTTP_404_NOT_FOUND,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )


######################################################################
#  INTEGRATION / FULL CRUD TESTS
######################################################################

class TestFullCrudFlow:
    """Test a full CRUD lifecycle."""

    def test_full_crud_lifecycle(self, client, account_data):
        """Create, read, update, and delete an account."""
        # CREATE
        resp = client.post(
            "/api/accounts",
            json=account_data,
            content_type="application/json",
        )
        assert resp.status_code == status.HTTP_201_CREATED
        account_id = resp.get_json()["id"]

        # READ
        resp = client.get(f"/api/accounts/{account_id}")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.get_json()["name"] == account_data["name"]

        # UPDATE
        update_data = {"name": "New Name", "balance": 500.0}
        resp = client.put(
            f"/api/accounts/{account_id}",
            json=update_data,
            content_type="application/json",
        )
        assert resp.status_code == status.HTTP_200_OK
        assert resp.get_json()["name"] == "New Name"
        assert resp.get_json()["balance"] == 500.0

        # DELETE
        resp = client.delete(f"/api/accounts/{account_id}")
        assert resp.status_code == status.HTTP_204_NO_CONTENT

        # VERIFY DELETE
        resp = client.get(f"/api/accounts/{account_id}")
        assert resp.status_code == status.HTTP_404_NOT_FOUND
