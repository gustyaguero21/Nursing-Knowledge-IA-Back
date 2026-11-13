from nursing_knowledge_ia_back.routes.server.server import StartServer
from nursing_knowledge_ia_back.config.env import GetDBName, GetUri, LoadEnv
from nursing_knowledge_ia_back.database.connection import InitConnection
from nursing_knowledge_ia_back.repositories.patient.patient import PatientRepository
from nursing_knowledge_ia_back.services.patient.patient import PatientService
from datetime import datetime

def StartApp():
    LoadEnv()
    app=StartServer()
    client=InitConnection(GetUri(),GetDBName())





    patientRepo=PatientRepository(client)
    patientService=PatientService(patientRepo)
    patientService.create_patient({
        "name": "Jane",
        "lastname": "Doe",
        "pid": "PID123",
        "email": "jane.doe@example.com",
        "password": "password123",
        "createdAt": datetime(2023, 1, 1),
        "active": True,
        "age": 30,
        "sex": "female",
        "currentDiagnosis": "Hypertension",
        "dateOfEntry": datetime(2023, 1, 1)
    })


    app.run(debug=True,port=8080)

if __name__ == '__main__':
    StartApp()
