from nursing_knowledge_ia_back.routes.server.server import StartServer
from nursing_knowledge_ia_back.config.env import GetDBName, GetUri, LoadEnv
from nursing_knowledge_ia_back.database.connection import InitConnection
from nursing_knowledge_ia_back.repositories.doctor.doctor import DoctorRepository
from nursing_knowledge_ia_back.services.doctor.doctor import DoctorService

def StartApp():
    LoadEnv()
    app=StartServer()
    client=InitConnection(GetUri(),GetDBName())
    doctorRepo=DoctorRepository(client)
    doctorService=DoctorService(doctorRepo)
    doctorService.create_doctor({
        "name": "John",
        "lastname": "Doe",
        "email": "john.doe@example.com",
        "password": "password123",
        "createdAt": "2023-01-01",
        "active": True,
        "enrollment": "ENR123",
        "especialitation": "Cardiology",
        "register": "REG123"
    })

    app.run(debug=True,port=8080)

if __name__ == '__main__':
    StartApp()
