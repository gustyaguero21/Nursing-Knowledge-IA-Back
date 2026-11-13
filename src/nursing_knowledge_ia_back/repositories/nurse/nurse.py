from typing import Union

from pymongo import MongoClient

class NurseRepository:
    def __init__(self, client: MongoClient):
        self.client = client
        self.collection = self.client["nursing_knowledge_ia"]["nurses"]

    def create(self, nurse_data: dict) -> Union[str, Exception]:
        try:
            result = self.collection.insert_one(nurse_data)
            return str(result.inserted_id)
        except Exception as error:
            return error

    def get(self) -> Union[list, Exception]:
        try:
            return list(self.collection.find({},{"password":0}))
        except Exception as error:
            return error

    def get_by_file(self, nurse_file: str) -> Union[dict, None, Exception]:
        try:
            nurse = self.collection.find_one({"file": nurse_file}, {"password": 0})
            return nurse
        except Exception as error:
            return error


    def update(self, nurse_file: str, update_data: dict) -> Union[bool, Exception]:
        try:
            result = self.collection.update_one({"file": nurse_file}, {"$set": update_data})
            return result.modified_count > 0
        except Exception as error:
            return error

    def delete(self, nurse_file: str) -> Union[bool, Exception]:
        try:
            result = self.collection.delete_one({"file": nurse_file})
            return result.deleted_count > 0
        except Exception as error:
            return error


    def checkExists(self, nurse_file: str) -> Union[bool, Exception]:
        try:
            nurse = self.collection.find_one({"file": nurse_file})
            return nurse is not None
        except Exception as error:
            return error
