from pymongo import MongoClient

class PatientRepository:
    def __init__(self, client: MongoClient):
        self.client = client
        self.collection = self.client["nursing_knowledge_ia"]["patients"]

    def create_patient(self, patient_data: dict) -> str:
        result = self.collection.insert_one(patient_data)
        return str(result.inserted_id)

    def get_patient_by_id(self, patient_id: str) -> dict:
        patient = self.collection.find_one({"_id": patient_id})
        return patient

    def update_patient(self, patient_id: str, update_data: dict) -> bool:
        result = self.collection.update_one({"_id": patient_id}, {"$set": update_data})
        return result.modified_count > 0

    def delete_patient(self, patient_id: str) -> bool:
        result = self.collection.delete_one({"_id": patient_id})
        return result.deleted_count > 0