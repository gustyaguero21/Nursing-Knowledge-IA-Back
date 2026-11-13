

import re
from datetime import date, datetime
class PatientService:
    def __init__(self, patient_repo):
        try:
            self.patient_repo = patient_repo
        except Exception as error:
            raise RuntimeError(f"Failed to initialize patient service: {error}") from error

    def validate_patient(self, patient):
        try:
            # Validate patient's first name
            if not isinstance(patient.name, str) or not patient.name.strip():
                return False
            elif any(character.isdigit() for character in patient.name):
                return False

            # Validate patient's last name
            if not isinstance(patient.lastname, str) or not patient.lastname.strip():
                return False
            elif any(character.isdigit() for character in patient.lastname):
                return False

            # Validate email address
            if not isinstance(patient.email, str) or not patient.email.strip():
                return False
            elif not re.fullmatch(
                r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                patient.email.strip()
            ):
                return False

            # Validate patient's age
            if type(patient.age) is not int or patient.age < 0:
                return False

            # Validate patient's gender
            if not isinstance(patient.sex, str) or not patient.sex.strip():
                return False

            # Validate current diagnosis
            if not isinstance(patient.currentDiagnosis, str):
                return False

            # Validate date of entry
            if not isinstance(patient.dateOfEntry, (date, datetime)):
                return False

            # Return True if all validations pass
            return True
        except Exception as error:
            raise RuntimeError(f"Failed to validate patient: {error}") from error

    def create_patient(self, patient_data: dict) -> str:
        import hashlib
        import secrets
        from types import SimpleNamespace

        try:
            if not isinstance(patient_data, dict):
                return "Invalid patient data"

            password = patient_data.get('password')
            if not isinstance(password, str) or not password:
                return "Invalid patient data"

            if not self.validate_patient(SimpleNamespace(**patient_data)):
                return "Invalid patient data"

            if self.patient_repo.chekExist(patient_data['email']):
                return "Patient already exists"

            else:
                salt = secrets.token_bytes(16)
                iterations = 600_000
                password_hash = hashlib.pbkdf2_hmac(
                    'sha256', password.encode('utf-8'), salt, iterations
                )
                data_to_save = patient_data.copy()
                data_to_save['password'] = (
                    f"pbkdf2_sha256${iterations}${salt.hex()}${password_hash.hex()}"
                )
                self.patient_repo.create(data_to_save)
                return "Patient created successfully"
        except Exception as error:
            raise RuntimeError(f"Failed to create patient: {error}") from error


    def get_patients(self) -> list | str:
        try:
            patients = self.patient_repo.get()
            if patients == []:
                return "No patient records found"
            return patients
        except Exception as error:
            raise RuntimeError(f"Failed to retrieve patients: {error}") from error

    def get_patient_by_pid(self, pid: str):
        try:
            return self.patient_repo.get_by_pid(pid)
        except Exception as error:
            raise RuntimeError(f"Failed to retrieve patient by PID: {error}") from error

    def update_patient(self, pid: str, update_data: dict) -> bool:
        try:
            if not self.validate_patient(update_data):
                return False
            return self.patient_repo.update(pid, update_data)
        except Exception as error:
            raise RuntimeError(f"Failed to update patient: {error}") from error

    def delete_patient(self, pid: str) -> bool:
        try:
            return self.patient_repo.delete(pid)
        except Exception as error:
            raise RuntimeError(f"Failed to delete patient: {error}") from error
