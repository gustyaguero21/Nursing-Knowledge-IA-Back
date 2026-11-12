from threading import Lock

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure, OperationFailure


_clients: dict[str, MongoClient] = {}
_databases: dict[tuple[str, str], Database] = {}
_connection_lock = Lock()


def InitConnection(uri: str, db_name: str) -> Database | None:
    with _connection_lock:
        key = (uri, db_name)
        if key in _databases:
            return _databases[key]

        try:
            client = _clients.get(uri)
            if client is None:
                client = MongoClient(uri, serverSelectionTimeoutMS=5000)
                # Fuerza la conexión y autenticación inmediatamente en lugar de esperar al insert_one
                client.admin.command("ping")
                _clients[uri] = client

            db = client[db_name]
            if db_name not in client.list_database_names():
                # MongoDB materializa la base de datos al crear su primera colección.
                # check_exists=False permite que otro proceso la cree simultáneamente.
                db.create_collection("_init", check_exists=False)

            # Reutiliza el mismo cliente y la misma instancia de Database.
            _databases[key] = db
            return db
        except OperationFailure as e:
            print(f"Error de autenticación en MongoDB: {e}")
            return None
        except ConnectionFailure as e:
            print(f"No se pudo conectar al servidor MongoDB: {e}")
            return None
