from nursing_knowledge_ia_back.routes.server.server import StartServer
from nursing_knowledge_ia_back.config.env import GetDBName, GetUri, LoadEnv
from nursing_knowledge_ia_back.database.connection import InitConnection

def StartApp():
    LoadEnv()
    app=StartServer()
    InitConnection(GetUri(),GetDBName())

    app.run(debug=True,port=8080)

if __name__ == '__main__':
    StartApp()
