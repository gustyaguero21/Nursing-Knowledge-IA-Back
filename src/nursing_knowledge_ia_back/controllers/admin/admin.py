from functools import wraps

from flask import current_app, jsonify
from werkzeug.exceptions import BadRequest, Conflict, HTTPException, NotFound


def json_response_errors(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except HTTPException as error:
            return jsonify(error=error.description), error.code
        except Exception:
            current_app.logger.exception("Error in AdminController")
            return jsonify(error="Internal server error"), 500

    return wrapper


class AdminController:
    """Controladores sin rutas. Requieren un contexto de aplicación Flask."""

    def __init__(self, admin_service):
        self.admin_service = admin_service

    def _validate_data(self, data):
        if not isinstance(data, dict):
            raise BadRequest("Expected a JSON object")

        fields = {"name", "lastname", "email", "password", "createdAt", "active", "accessLevel"}
        missing = fields - data.keys()
        if missing:
            raise BadRequest(f"Missing fields: {', '.join(sorted(missing))}")
        if data.keys() - fields:
            raise BadRequest("The object contains fields that are not allowed")

        data = data.copy()
        for field in ("name", "lastname", "email", "password"):
            if not isinstance(data[field], str) or not data[field].strip():
                raise BadRequest(f"The {field} field must be a non-empty string")
            if field != "password":
                data[field] = data[field].strip()

        if type(data["active"]) is not bool:
            raise BadRequest("The active field must be a boolean")

        if type(data["accessLevel"]) is not int:
            raise BadRequest("The accessLevel field must be an integer")

        if isinstance(data["createdAt"], str):
            try:
                data["createdAt"] = datetime.fromisoformat(data["createdAt"])
            except ValueError:
                raise BadRequest("createdAt must be an ISO 8601 date") from None
        if not isinstance(data["createdAt"], (date, datetime)):
            raise BadRequest("createdAt must be an ISO 8601 date")

        if not self.admin_service.validate_admin(data):
            raise BadRequest(
                "Invalid data: names must not contain digits, email must be valid, and password "
                "must be at least 8 characters long"
            )
        return data

    @staticmethod
    def _validate_name(name):
        if not isinstance(name, str) or not name.strip():
            raise BadRequest("The name must be a non-empty string")
        return name.strip()

    @json_response_errors
    def create_admin(self, admin_data):
        data = self._validate_data(admin_data)
        result = self.admin_service.create_admin(data)
        if result == "Invalid administrator data":
            raise BadRequest("Invalid administrator data")
        if result == "Administrator already exists":
            raise Conflict("Administrator already exists")
        if result != "Administrator created successfully":
            raise RuntimeError("Unexpected response from the administrator service")
        return jsonify(message="Administrador creado correctamente"), 201

    @json_response_errors
    def update_admin(self, name, update_data):
        """Actualización completa: el servicio requiere todos los campos."""
        name = self._validate_name(name)
        data = self._validate_data(update_data)
        if not self.admin_service.update_admin(name, data):
            raise NotFound("Administrator not found or not updated")
        return jsonify(message="Administrador actualizado correctamente"), 200

    @json_response_errors
    def delete_admin(self, name):
        name = self._validate_name(name)
        if not self.admin_service.delete_admin(name):
            raise NotFound("Administrator not found or not deleted")
        return jsonify(message="Administrador eliminado correctamente"), 200
