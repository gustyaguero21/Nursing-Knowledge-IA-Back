
# Import the regular expression module to validate email addresses.

import re
from datetime import date, datetime
class Nurseservice:
    def __init__(self, nurse_repo):
        self.nurse_repo = nurse_repo

    def validate_nurse(self, nurse):
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


    def create_nurse(self, nurse_data: dict) -> str:
        if not self.validate_nurse(nurse_data):
            return "Invalid nurse data"

        if self.nurse_repo.checkExist(nurse_data['password'], nurse_data['email']):
            raise ValueError("Nurse already exists")

        else:
            self.nurse_repo.create(nurse_data)
            return "Nurse created successfully"


    def get_nurse_by_email(self, email: str) -> dict:
        return self.nurse_repo.get_by_email(email)


    def update_nurse(self, email: str, update_data: dict) -> bool:
        if not self.validate_nurse(update_data):
            return "Invalid nurse data"

        return self.nurse_repo.update(email, update_data)

    def delete_nurse(self, email: str) -> bool:
        return self.nurse_repo.delete(email)
    