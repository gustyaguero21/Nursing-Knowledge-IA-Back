import os
from dotenv import load_dotenv

def LoadEnv():
    env_path = os.path.join(os.getcwd(), ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        raise FileNotFoundError("error loading .env file")


def GetDBName()->str:
    db_name=os.getenv('DB_NAME')

    return str(db_name)


def GetDBUser():
    db_user=os.getenv('DB_USER')

    return db_user


def GetDBPassword():
    db_password=os.getenv('DB_PASSWORD')

    return db_password


def GetUri()->str:
    return f"mongodb://{GetDBUser()}:{GetDBPassword()}@localhost:27017/{GetDBName()}"
