
# Import the regular expression module to validate email addresses.
import re

# Import date types to validate the nurse's creation date.
from datetime import date, datetime


# Validate the nurse's data before preparing the JSON response.
def validate_nurse(nurse):

    # Create a dictionary to store validation errors.
    errors = {}

    # Validate the nurse's name.
    if not isinstance(nurse.name, str) or not nurse.name.strip():
        errors["name"] = "Name is required."
    elif any(character.isdigit() for character in nurse.name):
        errors["name"] = "Name cannot contain numbers."

    # Validate the nurse's last name.
    if not isinstance(nurse.lastname, str) or not nurse.lastname.strip():
        errors["lastname"] = "Last name is required."
    elif any(character.isdigit() for character in nurse.lastname):
        errors["lastname"] = "Last name cannot contain numbers."

    # Validate the email address.
    if not isinstance(nurse.email, str) or not nurse.email.strip():
        errors["email"] = "Email is required."
    elif not re.fullmatch(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        nurse.email.strip()
    ):
        errors["email"] = "Email format is invalid."

    # Validate the password.
    if not isinstance(nurse.password, str) or not nurse.password.strip():
        errors["password"] = "Password is required."
    elif len(nurse.password) < 8:
        errors["password"] = "Password must contain at least 8 characters."

    # Validate the creation date.
    if not isinstance(nurse.createdAt, (date, datetime)):
        errors["createdAt"] = "Creation date must be a valid date."

    # Validate the nurse's active status.
    if type(nurse.active) is not bool:
        errors["active"] = "Active status must be a boolean."

    # Validate the institution.
    if not isinstance(nurse.institution, str) or not nurse.institution.strip():
        errors["institution"] = "Institution is required."

    # Validate the ageCourse field.
    if not isinstance(nurse.ageCourse, str) or not nurse.ageCourse.strip():
        errors["ageCourse"] = "Age course is required."

    # Validate the file field.
    if not isinstance(nurse.file, str) or not nurse.file.strip():
        errors["file"] = "File is required."

    # Return the validation errors if any field is invalid.
    if errors:
        return {
            "valid": False,
            "errors": errors
        }

    # Prepare the validated data for the JSON response.
    # Do not include the password in the response.
    return {
        "valid": True,
        "data": {
            "name": nurse.name.strip(),
            "lastname": nurse.lastname.strip(),
            "email": nurse.email.strip(),
            "createdAt": nurse.createdAt.isoformat(),
            "active": nurse.active,
            "institution": nurse.institution.strip(),
            "ageCourse": nurse.ageCourse.strip(),
            "file": nurse.file.strip()
        }
    }
