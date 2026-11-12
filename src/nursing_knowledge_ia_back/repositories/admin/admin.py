from pymongo import MongoClient

class adminRepository:
    def __init__(self, client: MongoClient):
        self.client = client
        self.collection = self.client["nursing_knowledge_ia"]["admins"]

    def create_admin(self, admin_data: dict) -> str:
        result = self.collection.insert_one(admin_data)
        return str(result.inserted_id)

    def get_admin_by_id(self, admin_id: str) -> dict:
        admin = self.collection.find_one({"_id": admin_id})
        return admin

    def update_admin(self, admin_id: str, update_data: dict) -> bool:
        result = self.collection.update_one({"_id": admin_id}, {"$set": update_data})
        return result.modified_count > 0

    def delete_admin(self, admin_id: str) -> bool:
        result = self.collection.delete_one({"_id": admin_id})
        return result.deleted_count > 0