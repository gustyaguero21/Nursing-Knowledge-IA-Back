
# Import the regular expression module to validate email addresses.
import re

# Import date types to validate the doctor's creation date.
from datetime import date, datetime


# Validate the doctor's data before preparing the JSON response.
def validate_doctor(doctor):

    # Create a dictionary to store validation errors.
    errors = {}

    # Validate the doctor's name.
    if not isinstance(doctor.name, str) or not doctor.name.strip():
        errors["name"] = "Name is required."
    elif any(character.isdigit() for character in doctor.name):
        errors["name"] = "Name cannot contain numbers."

    # Validate the doctor's last name.
    if not isinstance(doctor.lastname, str) or not doctor.lastname.strip():
        errors["lastname"] = "Last name is required."
    elif any(character.isdigit() for character in doctor.lastname):
        errors["lastname"] = "Last name cannot contain numbers."

    # Validate the email address.
    if not isinstance(doctor.email, str) or not doctor.email.strip():
        errors["email"] = "Email is required."
    elif not re.fullmatch(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        doctor.email.strip()
    ):
        errors["email"] = "Email format is invalid."

    # Validate the password.
    if not isinstance(doctor.password, str) or not doctor.password.strip():
        errors["password"] = "Password is required."
    elif len(doctor.password) < 8:
        errors["password"] = "Password must contain at least 8 characters."

    # Validate the creation date.
    if not isinstance(doctor.createdAt, (date, datetime)):
        errors["createdAt"] = "Creation date must be a valid date."

    # Validate the doctor's active status.
    if type(doctor.active) is not bool:
        errors["active"] = "Active status must be a boolean."

    # Validate the enrollment number.
    if not isinstance(doctor.enrollment, str) or not doctor.enrollment.strip():
        errors["enrollment"] = "Enrollment is required."

    # Validate the medical specialization.
    if (
        not isinstance(doctor.especialitation, str)
        or not doctor.especialitation.strip()
    ):
        errors["especialitation"] = "Specialization is required."

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
            "name": doctor.name.strip(),
            "lastname": doctor.lastname.strip(),
            "email": doctor.email.strip(),
            "createdAt": doctor.createdAt.isoformat(),
            "active": doctor.active,
            "enrollment": doctor.enrollment.strip(),
            "especialitation": doctor.especialitation.strip()
        }
    }
