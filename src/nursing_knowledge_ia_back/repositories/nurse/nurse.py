from pymongo import MongoClient

class NurseRepository:
    def __init__(self, client: MongoClient):
        self.client = client
        self.collection = self.client["nursing_knowledge_ia"]["nurses"]
    def create_nurse(self, nurse_data: dict) -> str:
        result = self.collection.insert_one(nurse_data)
        return str(result.inserted_id)
    def get_nurse_by_id(self, nurse_id: str) -> dict:
        nurse = self.collection.find_one({"_id": nurse_id})
        return nurse
    def update_nurse(self, nurse_id: str, update_data: dict) -> bool:
        result = self.collection.update_one({"_id": nurse_id}, {"$set": update_data})
        return result.modified_count > 0

    def delete_nurse(self, nurse_id: str) -> bool:
        result = self.collection.delete_one({"_id": nurse_id})
        return result.deleted_count > 0