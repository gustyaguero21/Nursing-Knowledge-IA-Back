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
            current_app.logger.exception("Error in DoctorController")
            return jsonify(error="Internal server error"), 500

    return wrapper


class _DoctorData(dict):
    """Permite al servicio consultar los datos como diccionario y como atributos."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name) from None


class DoctorController:
    """Controladores sin rutas. Requieren un contexto de aplicación Flask."""

    def __init__(self, doctor_service):
        self.doctor_service = doctor_service

    def _validate_data(self, data):
        if not isinstance(data, dict):
            raise BadRequest("Expected a JSON object")

        fields = {
            "name", "lastname", "email", "password", "createdAt", "active",
            "register", "enrollment", "especialitation",
        }
        missing = fields - data.keys()
        if missing:
            raise BadRequest(f"Missing fields: {', '.join(sorted(missing))}")
        if data.keys() - fields:
            raise BadRequest("The object contains fields that are not allowed")

        data = _DoctorData(data)
        for field in (
            "name", "lastname", "email", "password", "register", "enrollment",
            "especialitation",
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

        if not self.doctor_service.validate_doctor(data):
            raise BadRequest(
                "Invalid data: names must not contain digits, email must be valid, and password "
                "must be at least 8 characters long"
            )
        return data

    @staticmethod
    def _validate_register(register):
        if not isinstance(register, str) or not register.strip():
            raise BadRequest("The register must be a non-empty string")
        return register.strip()

    @json_response_errors
    def create_doctor(self, doctor_data):
        data = self._validate_data(doctor_data)
        result = self.doctor_service.create_doctor(data)
        if result == "Doctor with this register already exists.":
            raise Conflict("Doctor with this register already exists.")
        if result != "Doctor created successfully.":
            raise RuntimeError("Unexpected response from the doctor service")
        return jsonify(message="Doctor creado correctamente"), 201

    @json_response_errors
    def get_doctors(self):
        doctors = self.doctor_service.get_doctors()
        if doctors == "No records found.":
            doctors = []
        return jsonify(doctors), 200

    @json_response_errors
    def get_doctor_by_register(self, register):
        register = self._validate_register(register)
        doctor = self.doctor_service.get_doctor_by_register(register)
        if not doctor:
            raise NotFound("Doctor not found")
        return jsonify(doctor), 200

    @json_response_errors
    def update_doctor(self, register, update_data):
        """Actualización completa: el servicio requiere todos los campos."""
        register = self._validate_register(register)
        data = self._validate_data(update_data)
        if not self.doctor_service.update_doctor(register, data):
            raise NotFound("Doctor not found or not updated")
        return jsonify(message="Doctor actualizado correctamente"), 200

    @json_response_errors
    def delete_doctor(self, register):
        register = self._validate_register(register)
        if not self.doctor_service.delete_doctor(register):
            raise NotFound("Doctor not found or not deleted")
        return jsonify(message="Doctor eliminado correctamente"), 200
