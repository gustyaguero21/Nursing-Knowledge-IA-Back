import os
from dotenv import load_dotenv


def LoadEnv():
    env_path = os.path.join(os.getcwd(), ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path, override=True)
    else:
        raise FileNotFoundError("error loading .env file")


def GetDBName() -> str:
    return str(os.getenv("DB_NAME"))


def GetDBUser() -> str:
    return str(os.getenv("DB_USER"))


def GetDBPort() -> str:
    return str(os.getenv("DB_PORT"))


def GetDBPassword() -> str:
    return str(os.getenv("DB_PASSWORD"))


def GetUri() -> str:
    return f"mongodb://{GetDBUser()}:{GetDBPassword()}@localhost:{GetDBPort()}/{GetDBName()}?authSource=admin"
