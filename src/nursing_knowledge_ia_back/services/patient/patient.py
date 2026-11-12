

import re
from datetime import date, datetime


def validate_patient(patient):

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
