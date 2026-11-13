from typing import Any

from nursing_knowledge_ia_back.repositories.login.login import LoginRepository


class LoginService:
    """Validates credentials before delegating authentication to the repository."""

    def __init__(self, repository: LoginRepository) -> None:
        self._repository = repository

    def login(self, email: str, password: str) -> dict[str, Any] | None:
        if not isinstance(email, str):
            raise ValueError("The email must be a string.")
        if not isinstance(password, str):
            raise ValueError("The password must be a string.")

        email = email.strip()
        if not email:
            raise ValueError("The email cannot be empty.")
        if not password or password.isspace():
            raise ValueError("The password cannot be empty or contain only whitespace.")

        return self._repository.login(email, password)
