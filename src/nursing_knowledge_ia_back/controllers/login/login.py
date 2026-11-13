from functools import wraps

from flask import current_app, jsonify
from werkzeug.exceptions import BadRequest, HTTPException, Unauthorized

from nursing_knowledge_ia_back.services.login.login import LoginService


def json_response_errors(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except HTTPException as error:
            return jsonify(error=error.description), error.code
        except Exception:
            current_app.logger.exception("Error in LoginController")
            return jsonify(error="Internal server error"), 500

    return wrapper


class LoginController:
    """Controlador sin rutas. Requiere un contexto de aplicación Flask."""

    def __init__(self, login_service: LoginService) -> None:
        self.login_service = login_service

    @json_response_errors
    def login(self, login_data):
        if not isinstance(login_data, dict):
            raise BadRequest("Expected a JSON object")

        missing = {"email", "password"} - login_data.keys()
        if missing:
            raise BadRequest(f"Missing fields: {', '.join(sorted(missing))}")

        try:
            result = self.login_service.login(
                login_data["email"], login_data["password"]
            )
        except ValueError as error:
            raise BadRequest(str(error)) from None

        if result is None:
            raise Unauthorized("Invalid email or password")

        return jsonify(result), 200
