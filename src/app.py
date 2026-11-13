from nursing_knowledge_ia_back.routes.server.server import StartServer
from nursing_knowledge_ia_back.config.env import GetDBName, GetUri, LoadEnv
from nursing_knowledge_ia_back.database.connection import InitConnection
from nursing_knowledge_ia_back.repositories.admin.admin import AdminRepository
from nursing_knowledge_ia_back.services.admin.admin import AdminService
from datetime import datetime

def StartApp():
    LoadEnv()
    app=StartServer()
    client=InitConnection(GetUri(),GetDBName())


    adminRepo=AdminRepository(client)
    adminService=AdminService(adminRepo)
    adminService.create_admin({
        "name": "Jane",
        "lastname": "Doe",
        "email": "jane.doe@example.com",
        "password": "password123",
        "createdAt": datetime(2023, 1, 1),
        "active": True,
        "accessLevel": 1
    })


    app.run(debug=True,port=8080)

if __name__ == '__main__':
    StartApp()
