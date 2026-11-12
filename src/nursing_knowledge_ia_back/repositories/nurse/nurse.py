from pymongo import MongoClient

class NurseRepository:
    def checkExist(self,nurse_password: str, nurse_email: str) -> bool:
        nurse = self.collection.find_one({"email": nurse_email, "password": nurse_password})
        return nurse is not False
    
    def __init__(self, client: MongoClient):
        self.client = client
        self.collection = self.client["nursing_knowledge_ia"]["nurses"]

    def create(self, nurse_data: dict) -> str:
        result = self.collection.insert_one(nurse_data)
        return str(result.inserted_id)
    
    def get_by_id(self, nurse_id: str) -> dict:
        nurse = self.collection.find({"_id": nurse_id, "name": nurse_id, "lastname": nurse_id, "email": nurse_id, "createdAt": nurse_id, "active": nurse_id, "institution": nurse_id, "ageCourse": nurse_id, "file": nurse_id})
        return nurse

    def update(self, nurse_id: str, update_data: dict) -> bool:
        result = self.collection.update_one({"_id": nurse_id}, {"$set": update_data})
        return result.modified_count > 0

    def delete(self, nurse_id: str) -> bool:
        result = self.collection.delete_one({"_id": nurse_id})
        return result.deleted_count > 0