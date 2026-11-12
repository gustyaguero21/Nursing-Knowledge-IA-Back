from pymongo import MongoClient

class DoctorRepository:
    def checkExist(self,doctor_register:str) -> bool:
        doctor = self.collection.find_one({"register": doctor_register})
        return doctor is not None
    
    def __init__(self, client: MongoClient):
        self.client = client
        self.collection = self.client["nursing_knowledge_ia"]["doctors"]

    def create(self, doctor_data: dict) -> str:
        result = self.collection.insert_one(doctor_data)
        return str(result.inserted_id)

    def get(self, doctor_id: str) -> dict:
        doctor = self.collection.find({ "name": doctor_id, "lastname": doctor_id, "email": doctor_id, "register": doctor_id, "especialitation": doctor_id, "enrollment": doctor_id, "createdAt": doctor_id, "active": doctor_id})
        return doctor 

    def update(self, doctor_id: str, update_data: dict) -> bool:
        result = self.collection.update_one({"_id": doctor_id}, {"$set": update_data})
        return result.modified_count > 0

    def delete(self, doctor_id: str) -> bool:
        result = self.collection.delete_one({"_id": doctor_id})
        return result.deleted_count > 0