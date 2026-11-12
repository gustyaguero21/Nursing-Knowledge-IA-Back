
# Import the regular expression module to validate email addresses.

import re
from datetime import date, datetime

def validate_nurse(nurse):

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
