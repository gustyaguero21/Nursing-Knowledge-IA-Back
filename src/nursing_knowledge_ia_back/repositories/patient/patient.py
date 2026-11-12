from pymongo import MongoClient

class PatientRepository:
    def checkExist(self,patient_password: str, patient_email: str) -> bool:
        patient = self.collection.find_one({"email": patient_email, "password": patient_password})
        return patient is not False
    
    def __init__(self, client: MongoClient):
        self.client = client
        self.collection = self.client["nursing_knowledge_ia"]["patients"]

    def create(self, patient_data: dict) -> str:
        result = self.collection.insert_one(patient_data)
        return str(result.inserted_id)

    def get_by_id(self, patient_id: str) -> dict:
        patient = self.collection.find({"_id": patient_id, "name": patient_id, "lastname": patient_id, "email": patient_id, "createdAt": patient_id, "active": patient_id, "age": patient_id, "sex": patient_id, "currentDiagnosis": patient_id, "dateOfEntry": patient_id})
        return patient

    def update(self, patient_id: str, update_data: dict) -> bool:
        result = self.collection.update_one({"_id": patient_id}, {"$set": update_data})
        return result.modified_count > 0

    def delete(self, patient_id: str) -> bool:
        result = self.collection.delete_one({"_id": patient_id})
        return result.deleted_count > 0
    