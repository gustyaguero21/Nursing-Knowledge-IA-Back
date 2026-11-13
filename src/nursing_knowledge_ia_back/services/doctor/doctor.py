# Import the regular expression module to validate email addresses.
import re

# Import date types to validate the doctor's creation date.
from datetime import date, datetime
from xmlrpc import client
import hashlib
import secrets

class DoctorService:
    def __init__(self, doctor_repo):
        try:
            self.doctor_repo = doctor_repo
        except Exception as error:
            raise RuntimeError(f"Failed to initialize the doctor service: {error}") from error

    # Validate the doctor's data.
    def validate_doctor(self, doctor):
        try:
            # Validate the doctor's name.
            if not isinstance(doctor.name, str) or not doctor.name.strip():
                return False

            if any(character.isdigit() for character in doctor.name):
                return False

            # Validate the doctor's last name.
            if not isinstance(doctor.lastname, str) or not doctor.lastname.strip():
                return False

            if any(character.isdigit() for character in doctor.lastname):
                return False

            # Validate the email address.
            if not isinstance(doctor.email, str) or not doctor.email.strip():
                return False

            if not re.fullmatch(
                r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                doctor.email.strip()
            ):
                return False

            # Validate the password.
            if not isinstance(doctor.password, str) or not doctor.password.strip():
                return False

            if len(doctor.password) < 8:
                return False

            # Validate the creation date.
            if not isinstance(doctor.createdAt, (date, datetime)):
                return False

            # Validate the doctor's active status.
            if type(doctor.active) is not bool:
                return False

            # Validate the enrollment number.
            if not isinstance(doctor.enrollment, str) or not doctor.enrollment.strip():
                return False

            # Validate the medical specialization.
            if (
                not isinstance(doctor.especialitation, str)
                or not doctor.especialitation.strip()
            ):
                return False

            # Return True when all validations are successful.
            return True
        except Exception as error:
            raise RuntimeError(f"Failed to validate doctor data: {error}") from error

    def create_doctor(self, doctor):
        try:
            if self.doctor_repo.checkExist(doctor["register"])==True:
                return "Doctor with this register already exists."
            else:


                salt = secrets.token_bytes(16)
                iterations = 600_000
                password_hash = hashlib.pbkdf2_hmac(
                    "sha256", doctor["password"].encode("utf-8"), salt, iterations
                )
                doctor = doctor.copy()
                doctor["password"] = (
                    f"pbkdf2_sha256${iterations}${salt.hex()}${password_hash.hex()}"
                )
                self.doctor_repo.create(doctor)
                return "Doctor created successfully."
        except Exception as error:
            raise RuntimeError(f"Failed to create doctor: {error}") from error

    def get_doctors(self) -> list | str:
        try:
            doctors = self.doctor_repo.get()
            if not doctors:
                return "No records found."
            return doctors
        except Exception as error:
            raise RuntimeError(f"Failed to retrieve doctors: {error}") from error

    def get_doctor_by_register(self, register: str) -> dict:
        try:
            return self.doctor_repo.get_by_register(register)
        except Exception as error:
            raise RuntimeError(f"Failed to retrieve doctor by register: {error}") from error

    def update_doctor(self, register: str, update_data: dict) -> bool:
        try:
            if self.validate_doctor(update_data):
                return self.doctor_repo.update(register, update_data)
            else:
                raise ValueError("Invalid doctor data")
        except Exception as error:
            raise RuntimeError(f"Failed to update doctor: {error}") from error

    def delete_doctor(self, register: str) -> bool:
        try:
            return self.doctor_repo.delete(register)
        except Exception as error:
            raise RuntimeError(f"Failed to delete doctor: {error}") from error
