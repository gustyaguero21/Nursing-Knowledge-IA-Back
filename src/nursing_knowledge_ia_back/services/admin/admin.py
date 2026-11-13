
# Import the regular expression module to validate email addresses.
import re
import hashlib
import secrets

# Import date types to validate the administrator's creation date.
from datetime import date, datetime

class AdminService:
    def __init__(self, admin_repo):
        self.admin_repo = admin_repo

    # Validate the administrator's data.
    def validate_admin(self, admin):
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

        return True

    def create_admin(self, admin_data: dict) -> str:
        if not self.validate_admin(admin_data):
            return "Invalid administrator data"

        if self.admin_repo.checkExists(admin_data['name']):
            return "Administrator already exists"

        else:


            # Almacenar un hash con sal única, nunca la clave en texto plano.
            salt = secrets.token_bytes(16)
            iterations = 600_000
            password_hash = hashlib.pbkdf2_hmac(
                "sha256", admin_data['password'].encode('utf-8'), salt, iterations
            )
            hashed_admin_data = admin_data.copy()
            hashed_admin_data['password'] = (
                f"pbkdf2_sha256${iterations}${salt.hex()}${password_hash.hex()}"
            )
            self.admin_repo.create(hashed_admin_data)
            return "Administrator created successfully"

    def update_admin(self, name: str, update_data: dict) -> bool:
        if not self.validate_admin(update_data):
            return False

        if not self.admin_repo.checkExists(name):
            return False

        return self.admin_repo.update(name, update_data)

    def delete_admin(self, name: str) -> bool:
        if not self.admin_repo.checkExists(name):
            return False

        return self.admin_repo.delete(name)
