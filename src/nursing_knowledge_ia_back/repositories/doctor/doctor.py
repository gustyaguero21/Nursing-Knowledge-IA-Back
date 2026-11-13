from typing import Union

from pymongo import MongoClient
from pymongo.errors import PyMongoError

class DoctorRepository:

    def __init__(self, client: MongoClient):
        self.client = client
        self.collection = self.client["nursing_knowledge_ia"]["doctors"]

    def create(self, doctor_data: dict) -> str:
        try:
            result = self.collection.insert_one(doctor_data)
            return str(result.inserted_id)
        except PyMongoError as error:
            return str(error)

    def get(self) -> Union[list, str]:
        try:
            return list(self.collection.find({}, {"password": 0}))
        except PyMongoError as error:
            return str(error)

    def get_by_id(self, doctor_register: str) -> Union[dict, str]:
        try:
            doctor = self.collection.find_one({"register": doctor_register}, {"password": 0})
            return doctor
        except PyMongoError as error:
            return str(error)


    def update(self, register: str, update_data: dict) -> Union[bool, str]:
        try:
            result = self.collection.update_one({"register": register}, {"$set": update_data})
            return result.modified_count > 0
        except PyMongoError as error:
            return str(error)

    def delete(self, doctor_register: str) -> Union[bool, str]:
        try:
            result = self.collection.delete_one({"register": doctor_register})
            return result.deleted_count > 0
        except PyMongoError as error:
            return str(error)


    def checkExist(self,doctor_register:str) -> Union[bool, str]:
        try:
            doctor = self.collection.find_one({"register": doctor_register})
            return doctor is not None
        except PyMongoError as error:
            return str(error)
