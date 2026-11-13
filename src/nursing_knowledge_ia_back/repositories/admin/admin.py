from typing import Union

from pymongo import MongoClient
from pymongo.errors import PyMongoError

class adminRepository:
    def __init__(self, client: MongoClient):
        self.client = client
        self.collection = self.client["nursing_knowledge_ia"]["admins"]

    def create(self, admin_data: dict) -> Union[str, PyMongoError]:
        try:
            result = self.collection.insert_one(admin_data)
            return str(result.inserted_id)
        except PyMongoError as error:
            return error

    def update(self, admin_id: str, update_data: dict) -> Union[bool, PyMongoError]:
        try:
            result = self.collection.update_one({"_id": admin_id}, {"$set": update_data})
            return result.modified_count > 0
        except PyMongoError as error:
            return error

    def delete(self, admin_id: str) -> Union[bool, PyMongoError]:
        try:
            result = self.collection.delete_one({"_id": admin_id})
            return result.deleted_count > 0
        except PyMongoError as error:
            return error
