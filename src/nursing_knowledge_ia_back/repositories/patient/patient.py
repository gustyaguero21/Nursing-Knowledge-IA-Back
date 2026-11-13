from typing import Union

from pymongo import MongoClient

class PatientRepository:
    def checkExist(self,patient_password: str, patient_email: str) -> Union[bool, Exception]:
        try:
            patient = self.collection.find_one({"email": patient_email, "password": patient_password})
            return patient is not False
        except Exception as error:
            return error

    def __init__(self, client: MongoClient):
        self.client = client
        self.collection = self.client["nursing_knowledge_ia"]["patients"]

    def create(self, patient_data: dict) -> Union[str, Exception]:
        try:
            result = self.collection.insert_one(patient_data)
            return str(result.inserted_id)
        except Exception as error:
            return error

    def get(self) -> Union[list, Exception]:
        try:
            return list(self.collection.find({},{"password":0}))
        except Exception as error:
            return error

    def get_by_pid(self, pid: str) -> Union[dict, Exception]:
        try:
            patient = self.collection.find_one({"pid": pid}, {"password": 0})
            return patient
        except Exception as error:
            return error


    def update(self, pid: str, update_data: dict) -> Union[bool, Exception]:
        try:
            result = self.collection.update_one({"pid": pid}, {"$set": update_data})
            return result.modified_count > 0
        except Exception as error:
            return error

    def delete(self, pid: str) -> Union[bool, Exception]:
        try:
            result = self.collection.delete_one({"pid": pid})
            return result.deleted_count > 0
        except Exception as error:
            return error
