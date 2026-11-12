
import re
from datetime import date, datetime


def validate_patient(patient):
    errors = {}

    # Validar nombre
    if not isinstance(patient.name, str) or not patient.name.strip():
        errors["name"] = "Name is required."
    elif any(character.isdigit() for character in patient.name):
        errors["name"] = "Name cannot contain numbers."

    # Validar apellido
    if not isinstance(patient.lastname, str) or not patient.lastname.strip():
        errors["lastname"] = "Last name is required."
    elif any(character.isdigit() for character in patient.lastname):
        errors["lastname"] = "Last name cannot contain numbers."

    # Validar email
    if not isinstance(patient.email, str) or not patient.email.strip():
        errors["email"] = "Email is required."
    elif not re.fullmatch(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        patient.email.strip()
    ):
        errors["email"] = "Email format is invalid."

    # Validar edad
    if type(patient.age) is not int or patient.age < 0:
        errors["age"] = "Age must be a non-negative integer."

    # Validar género
    if not isinstance(patient.sex, str) or not patient.sex.strip():
        errors["sex"] = "Sex is required."

    # Validar diágnostico actual
    if not isinstance(patient.currentDiagnosis, str):
        errors["currentDiagnosis"] = (
            "Current diagnosis must be a string."
        )

    # Validar fecha ingreso
    if not isinstance(patient.dateOfEntry, (date, datetime)):
        errors["dateOfEntry"] = (
            "Date of entry must be a valid date."
        )

    if errors:
        return {
            "valid": False,
            "errors": errors
        }

    return {
        "valid": True,
        "data": {
            "name": patient.name.strip(),
            "lastname": patient.lastname.strip(),
            "email": patient.email.strip(),
            "age": patient.age,
            "sex": patient.sex.strip(),
            "currentDiagnosis": patient.currentDiagnosis.strip(),
            "dateOfEntry": patient.dateOfEntry.isoformat()
        }
    }
