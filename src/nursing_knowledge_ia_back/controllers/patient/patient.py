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
            current_app.logger.exception("Error in PatientController")
            return jsonify(error="Internal server error"), 500

    return wrapper


class PatientController:
    """Controladores sin rutas. Requieren un contexto de aplicación Flask."""

    FIELDS = (
        "name", "lastname", "pid", "email", "password", "createdAt",
        "active", "age", "sex", "currentDiagnosis", "dateOfEntry",
    )

    def __init__(self, patient_service):
        self.patient_service = patient_service

    def _validate_data(self, data):
        if not isinstance(data, dict):
            raise BadRequest("Expected a JSON object")

        fields = set(self.FIELDS)
        missing = fields - data.keys()
        if missing:
            raise BadRequest(f"Missing fields: {', '.join(sorted(missing))}")
        if data.keys() - fields:
            raise BadRequest("The object contains fields that are not allowed")

        data = data.copy()
        for field in ("name", "lastname", "pid", "email", "password", "sex"):
            if not isinstance(data[field], str) or not data[field].strip():
                raise BadRequest(f"The {field} field must be a non-empty string")
            if field != "password":
                data[field] = data[field].strip()

        if type(data["active"]) is not bool:
            raise BadRequest("The active field must be a boolean")
        if type(data["age"]) is not int or data["age"] < 0:
            raise BadRequest("The age field must be a non-negative integer")
        if not isinstance(data["currentDiagnosis"], str):
            raise BadRequest("The currentDiagnosis field must be a string")

        for field in ("createdAt", "dateOfEntry"):
            if isinstance(data[field], str):
                try:
                    data[field] = datetime.fromisoformat(data[field])
                except ValueError:
                    raise BadRequest(f"{field} must be an ISO 8601 date") from None
            if not isinstance(data[field], (date, datetime)):
                raise BadRequest(f"{field} must be an ISO 8601 date")

        if not self.patient_service.validate_patient(data):
            raise BadRequest(
                "Invalid patient data: names must not contain digits and email must be valid"
            )
        return data

    @staticmethod
    def _validate_pid(pid):
        if not isinstance(pid, str) or not pid.strip():
            raise BadRequest("The pid must be a non-empty string")
        return pid.strip()

    @classmethod
    def _serialize_patient(cls, patient):
        """Expone los campos del paciente sin incluir su contraseña."""
        result = {}
        for field in cls.FIELDS:
            if field == "password":
                continue
            value = patient.get(field) if isinstance(patient, dict) else getattr(patient, field, None)
            result[field] = value.isoformat() if isinstance(value, (date, datetime)) else value
        return result

    @json_response_errors
    def create_patient(self, patient_data):
        data = self._validate_data(patient_data)
        result = self.patient_service.create_patient(data)
        if result == "Invalid patient data":
            raise BadRequest("Invalid patient data")
        if result == "Patient already exists":
            raise Conflict("Patient already exists")
        if result != "Patient created successfully":
            raise RuntimeError("Unexpected response from the patient service")
        return jsonify(message="Paciente creado correctamente"), 201

    @json_response_errors
    def get_patients(self):
        patients = self.patient_service.get_patients()
        if isinstance(patients, str):
            if patients == "No patient records found":
                return jsonify([]), 200
            raise RuntimeError("Unexpected response from the patient service")
        return jsonify([self._serialize_patient(patient) for patient in patients]), 200

    @json_response_errors
    def get_patient_by_pid(self, pid):
        pid = self._validate_pid(pid)
        patient = self.patient_service.get_patient_by_pid(pid)
        if not patient:
            raise NotFound("Patient not found")
        return jsonify(self._serialize_patient(patient)), 200

    @json_response_errors
    def update_patient(self, pid, update_data):
        """Actualización completa: el servicio requiere todos los campos."""
        pid = self._validate_pid(pid)
        data = self._validate_data(update_data)
        if not self.patient_service.update_patient(pid, data):
            raise NotFound("Patient not found or not updated")
        return jsonify(message="Paciente actualizado correctamente"), 200

    @json_response_errors
    def delete_patient(self, pid):
        pid = self._validate_pid(pid)
        if not self.patient_service.delete_patient(pid):
            raise NotFound("Patient not found or not deleted")
        return jsonify(message="Paciente eliminado correctamente"), 200
