from typing import Literal


class Login:
    email: str
    password: str
    userType: Literal["nurse", "patient", "admin", "doctor"]
