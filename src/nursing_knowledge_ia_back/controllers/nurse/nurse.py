from datetime import date, datetime
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
            current_app.logger.exception("Error in NurseController")
            return jsonify(error="Internal server error"), 500

    return wrapper


class NurseController:
    """Controladores sin rutas. Requieren un contexto de aplicación Flask."""

    def __init__(self, nurse_service):
        self.nurse_service = nurse_service

    def _validate_data(self, data):
        if not isinstance(data, dict):
            raise BadRequest("Expected a JSON object")

        fields = {
            "name", "lastname", "email", "password", "createdAt", "active",
            "institution", "ageCourse", "file",
        }
        missing = fields - data.keys()
        if missing:
            raise BadRequest(f"Missing fields: {', '.join(sorted(missing))}")
        if data.keys() - fields:
            raise BadRequest("The object contains fields that are not allowed")

        data = data.copy()
        for field in (
            "name", "lastname", "email", "password", "institution", "ageCourse", "file",
        ):
            if not isinstance(data[field], str) or not data[field].strip():
                raise BadRequest(f"The {field} field must be a non-empty string")
            if field != "password":
                data[field] = data[field].strip()

        if type(data["active"]) is not bool:
            raise BadRequest("The active field must be a boolean")

        if isinstance(data["createdAt"], str):
            try:
                data["createdAt"] = datetime.fromisoformat(data["createdAt"])
            except ValueError:
                raise BadRequest("createdAt must be an ISO 8601 date") from None
        if not isinstance(data["createdAt"], (date, datetime)):
            raise BadRequest("createdAt must be an ISO 8601 date")

        validation = self.nurse_service.validate_nurse(data)
        if isinstance(validation, str):
            raise RuntimeError("Unexpected response while validating nurse data")
        if validation is not True:
            raise BadRequest(
                "Invalid data: names must not contain digits, email must be valid, and password "
                "must be at least 8 characters long"
            )
        return data

    @staticmethod
    def _validate_file(file):
        if not isinstance(file, str) or not file.strip():
            raise BadRequest("The file must be a non-empty string")
        return file.strip()

    @staticmethod
    def _public_nurse(nurse):
        """No exponer contraseñas ni hashes en las respuestas."""
        return {key: value for key, value in nurse.items() if key != "password"}

    @json_response_errors
    def create_nurse(self, nurse_data):
        data = self._validate_data(nurse_data)
        result = self.nurse_service.create_nurse(data)
        if result == "Invalid nurse data":
            raise BadRequest("Invalid nurse data")
        if result == "Error creating nurse: Nurse already exists":
            raise Conflict("Nurse already exists")
        if result != "Nurse created successfully":
            raise RuntimeError("Unexpected response from the nurse service")
        return jsonify(message="Enfermero creado correctamente"), 201

    @json_response_errors
    def get_nurses(self):
        result = self.nurse_service.get_nurses()
        if isinstance(result, str):
            if result == "No records found":
                return jsonify([]), 200
            raise RuntimeError("Unexpected response from the nurse service")
        if not isinstance(result, list):
            raise RuntimeError("Unexpected response from the nurse service")
        return jsonify([self._public_nurse(nurse) for nurse in result]), 200

    @json_response_errors
    def get_nurse_by_file(self, file):
        file = self._validate_file(file)
        result = self.nurse_service.get_nurse_by_file(file)
        if result is None or result is False or result == {}:
            raise NotFound("Nurse not found")
        if not isinstance(result, dict):
            raise RuntimeError("Unexpected response from the nurse service")
        return jsonify(self._public_nurse(result)), 200

    @json_response_errors
    def update_nurse(self, file, update_data):
        """Actualización completa: el servicio requiere todos los campos."""
        file = self._validate_file(file)
        data = self._validate_data(update_data)
        result = self.nurse_service.update_nurse(file, data)
        if result == "Invalid nurse data":
            raise BadRequest("Invalid nurse data")
        if isinstance(result, str):
            raise RuntimeError("Unexpected response from the nurse service")
        if not result:
            raise NotFound("Nurse not found or not updated")
        return jsonify(message="Enfermero actualizado correctamente"), 200

    @json_response_errors
    def delete_nurse(self, file):
        file = self._validate_file(file)
        result = self.nurse_service.delete_nurse(file)
        if isinstance(result, str):
            raise RuntimeError("Unexpected response from the nurse service")
        if not result:
            raise NotFound("Nurse not found or not deleted")
        return jsonify(message="Enfermero eliminado correctamente"), 200
