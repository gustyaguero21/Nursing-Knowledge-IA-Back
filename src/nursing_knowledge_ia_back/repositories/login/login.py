
import hashlib
import hmac
from typing import Any

from bson import ObjectId
from pymongo import MongoClient


class LoginRepository:
    """Repositorio de autenticación para las cuatro colecciones de usuarios.

    ``client`` es el MongoClient compartido por la aplicación;
    la conexión se inicializa fuera de este repositorio.
    Se utiliza la base de datos ``nursing_knowledge_ia``.
    Los documentos deben tener los campos ``email`` y ``password``,
    con la contraseña almacenada como pbkdf2_sha256$iteraciones$salt_hex$hash_hex.
    """

    COLLECTIONS = ("admins", "nurses", "doctors", "patients")

    def __init__(self, client: MongoClient) -> None:
        self.client = client
        self._db = self.client["nursing_knowledge_ia"]

    @staticmethod
    def _verify_password(password: str, password_hash: Any) -> bool:
        if not isinstance(password_hash, str):
            return False

        try:
            algorithm, iterations_text, salt_hex, hash_hex = password_hash.split("$")
            if algorithm != "pbkdf2_sha256":
                return False
            iterations = int(iterations_text)
            salt = bytes.fromhex(salt_hex)
            expected_hash = bytes.fromhex(hash_hex)
            if iterations <= 0 or not salt or len(expected_hash) != 32:
                return False
            actual_hash = hashlib.pbkdf2_hmac(
                "sha256", password.encode("utf-8"), salt, iterations
            )
            return hmac.compare_digest(actual_hash, expected_hash)
        except (ValueError, TypeError, OverflowError):
            # Un hash inválido no debe permitir autenticar al usuario.
            return False

    def login(self, email: str, password: str) -> dict[str, Any] | None:
        """Devuelve el usuario sin su hash y su colección, o None.

        Busca por email y verifica el hash localmente; nunca consulta
        MongoDB con la contraseña en texto plano. Los errores de conexión
        se propagan para que el service pueda gestionarlos.
        """
        if not isinstance(email, str) or not isinstance(password, str):
            return None
        if not email or not password:
            return None

        for collection_name in self.COLLECTIONS:
            users = self._db[collection_name].find({"email": email})
            try:
                for user in users:
                    if self._verify_password(password, user.get("password")):
                        safe_user = {
                            key: value
                            for key, value in user.items()
                            if key != "password"
                        }
                        if isinstance(safe_user.get("_id"), ObjectId):
                            safe_user["_id"] = str(safe_user["_id"])
                        return {"user": safe_user, "collection": collection_name}
            finally:
                users.close()

        return None
