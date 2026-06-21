"""
Customer Accounts Microservice
Flask application factory with Talisman security headers and CORS support.
"""
import os
from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS

# Import after app is created in some cases, but for factory pattern we
# import models and routes inside create_app to avoid circular imports.


def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=False)

    # Default configuration
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev"),
        SQLALCHEMY_DATABASE_URI=os.getenv(
            "DATABASE_URI", "sqlite:///accounts.db"
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        DEBUG=os.getenv("DEBUG", "False").lower() in ("true", "1", "yes"),
        TESTING=False,
    )

    # Override config for testing
    if test_config is None:
        if app.config.get("TESTING"):
            app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    else:
        app.config.from_mapping(test_config)

    # Initialize security headers with Talisman
    Talisman(
        app,
        force_https=False,
        strict_transport_security=False,
        content_security_policy=None,
    )

    # Initialize CORS
    CORS(app)

    # Initialize SQLAlchemy
    from service.models import db, init_db

    db.init_app(app)

    # Register error handlers
    from service.common import status

    @app.errorhandler(status.HTTP_404_NOT_FOUND)
    def not_found(error):
        """Handle 404 errors."""
        from flask import jsonify
        msg = {"status": status.HTTP_404_NOT_FOUND, "error": "Not Found"}
        return jsonify(msg), status.HTTP_404_NOT_FOUND

    @app.errorhandler(status.HTTP_400_BAD_REQUEST)
    def bad_request(error):
        """Handle 400 errors."""
        from flask import jsonify
        msg = {"status": status.HTTP_400_BAD_REQUEST, "error": "Bad Request"}
        return jsonify(msg), status.HTTP_400_BAD_REQUEST

    @app.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
    def method_not_allowed(error):
        """Handle 405 errors."""
        from flask import jsonify
        msg = {"status": status.HTTP_405_METHOD_NOT_ALLOWED,
               "error": "Method Not Allowed"}
        return jsonify(msg), status.HTTP_405_METHOD_NOT_ALLOWED

    @app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
    def server_error(error):
        """Handle 500 errors."""
        from flask import jsonify
        msg = {"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
               "error": "Internal Server Error"}
        return jsonify(msg), status.HTTP_500_INTERNAL_SERVER_ERROR

    # Register routes
    from service import routes

    app.register_blueprint(routes.api_bp)

    # Initialize the database tables if running locally (not on Heroku)
    if not app.config["TESTING"] and os.getenv("FLASK_ENV") != "production":
        with app.app_context():
            init_db()

    return app
