# Import the regular expression module to validate email addresses.

import re
from datetime import date, datetime
class Nurseservice:
    def __init__(self, nurse_repo):
        self.nurse_repo = nurse_repo

    def validate_nurse(self, nurse) -> bool | str:
        try:
            # Validate the nurse's name.
            if not isinstance(nurse.name, str) or not nurse.name.strip():
                return False
            elif any(character.isdigit() for character in nurse.name):
                return False

            # Validate the nurse's last name.
            if not isinstance(nurse.lastname, str) or not nurse.lastname.strip():
                return False
            elif any(character.isdigit() for character in nurse.lastname):
                return False

            # Validate the email address.
            if not isinstance(nurse.email, str) or not nurse.email.strip():
                return False
            elif not re.fullmatch(
                r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                nurse.email.strip()
            ):
                return False

            # Validate the password.
            if not isinstance(nurse.password, str) or not nurse.password.strip():
                return False
            elif len(nurse.password) < 8:
                return False

            # Validate the creation date.
            if not isinstance(nurse.createdAt, (date, datetime)):
                return False

            # Validate the active status.
            if type(nurse.active) is not bool:
                return False

            # Validate the institution.
            if not isinstance(nurse.institution, str) or not nurse.institution.strip():
                return False

            # Validate the ageCourse field.
            if not isinstance(nurse.ageCourse, str) or not nurse.ageCourse.strip():
                return False

            # Validate the file field.
            if not isinstance(nurse.file, str) or not nurse.file.strip():
                return False

            return True
        except Exception as error:
            return "Error validating nurse: " + str(error)

    def create_nurse(self, nurse_data: dict) -> str:
        import hashlib
        import secrets

        try:
            validation = self.validate_nurse(nurse_data)
            if isinstance(validation, str):
                return validation
            if not validation:
                return "Invalid nurse data"

            if self.nurse_repo.checkExists(nurse_data['file']):
                raise ValueError("Nurse already exists")

            else:
                # Guardar únicamente un hash con sal aleatoria, nunca el password.
                salt = secrets.token_bytes(16)
                iterations = 600_000
                password_hash = hashlib.pbkdf2_hmac(
                    "sha256",
                    nurse_data['password'].encode('utf-8'),
                    salt,
                    iterations,
                )
                nurse_to_save = nurse_data.copy()
                nurse_to_save['password'] = (
                    f"pbkdf2_sha256${iterations}${salt.hex()}${password_hash.hex()}"
                )
                self.nurse_repo.create(nurse_to_save)
                return "Nurse created successfully"
        except Exception as error:
            return "Error creating nurse: " + str(error)



    def get_nurses(self) -> list | str:
        try:
            nurses = list(self.nurse_repo.get())
            if not nurses:
                return "No records found"
            return nurses
        except Exception as error:
            return "Error retrieving nurses: " + str(error)


    def get_nurse_by_file(self, file: str) -> dict | str:
        try:
            return self.nurse_repo.get_by_file(file)
        except Exception as error:
            return "Error retrieving nurse: " + str(error)


    def update_nurse(self, file: str, update_data: dict) -> bool | str:
        try:
            validation = self.validate_nurse(update_data)
            if isinstance(validation, str):
                return validation
            if not validation:
                return "Invalid nurse data"

            return self.nurse_repo.update(file, update_data)
        except Exception as error:
            return "Error updating nurse: " + str(error)

    def delete_nurse(self, file: str) -> bool | str:
        try:
            return self.nurse_repo.delete(file)
        except Exception as error:
            return "Error deleting nurse: " + str(error)
