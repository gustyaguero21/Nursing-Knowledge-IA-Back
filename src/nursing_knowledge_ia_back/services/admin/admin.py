
# Import the regular expression module to validate email addresses.
import re

# Import date types to validate the administrator's creation date.
from datetime import date, datetime


# Validate the administrator's data.
def validate_admin(admin):

    # Validate the administrator's name.
    if not isinstance(admin.name, str) or not admin.name.strip():
        return False

    if any(character.isdigit() for character in admin.name):
        return False

    # Validate the administrator's last name.
    if not isinstance(admin.lastname, str) or not admin.lastname.strip():
        return False

    if any(character.isdigit() for character in admin.lastname):
        return False

    # Validate the email address.
    if not isinstance(admin.email, str) or not admin.email.strip():
        return False

    if not re.fullmatch(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        admin.email.strip()
    ):
        return False

    # Validate the password.
    if not isinstance(admin.password, str) or not admin.password.strip():
        return False

    if len(admin.password) < 8:
        return False

    # Validate the creation date.
    if not isinstance(admin.createdAt, (date, datetime)):
        return False

    # Validate the administrator's active status.
    if type(admin.active) is not bool:
        return False

    # Validate the access level.
    if not isinstance(admin.accessLevel, str) or not admin.accessLevel.strip():
        return False

    # Return True when all validations are successful.
    return True
