from pymongo import MongoClient

def InitConnection(URI: str, dbName: str)->MongoClient:
    try:
        client = MongoClient(URI)
        db = client[dbName]
        return db
    except pymongo.errors.ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")
        return None
