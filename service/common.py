"""
Common utilities for the Customer Accounts Microservice.
Contains HTTP status codes and error handling helpers.
"""

######################################################################
# HTTP STATUS CODES
######################################################################

HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_401_UNAUTHORIZED = 401
HTTP_403_FORBIDDEN = 403
HTTP_404_NOT_FOUND = 404
HTTP_405_METHOD_NOT_ALLOWED = 405
HTTP_409_CONFLICT = 409
HTTP_415_UNSUPPORTED_MEDIA_TYPE = 415
HTTP_500_INTERNAL_SERVER_ERROR = 500
HTTP_501_NOT_IMPLEMENTED = 501


class status:
    """Status code constants."""
    HTTP_200_OK = 200
    HTTP_201_CREATED = 201
    HTTP_204_NO_CONTENT = 204
    HTTP_400_BAD_REQUEST = 400
    HTTP_401_UNAUTHORIZED = 401
    HTTP_403_FORBIDDEN = 403
    HTTP_404_NOT_FOUND = 404
    HTTP_405_METHOD_NOT_ALLOWED = 405
    HTTP_409_CONFLICT = 409
    HTTP_415_UNSUPPORTED_MEDIA_TYPE = 415
    HTTP_500_INTERNAL_SERVER_ERROR = 500
    HTTP_501_NOT_IMPLEMENTED = 501


######################################################################
# ERROR HANDLING HELPERS
######################################################################


def error_handler(app):
    """Register error handlers on the app. (Optional - can also be inline.)"""
    @app.errorhandler(404)
    def not_found(error):
        return {"status": 404, "error": "Not Found"}, 404

    @app.errorhandler(400)
    def bad_request(error):
        return {"status": 400, "error": "Bad Request"}, 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return {"status": 405, "error": "Method Not Allowed"}, 405

    @app.errorhandler(500)
    def server_error(error):
        return {"status": 500, "error": "Internal Server Error"}, 500
