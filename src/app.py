from nursing_knowledge_ia_back.routes.server.server import StartServer
from nursing_knowledge_ia_back.config.env import GetDBName, GetUri, LoadEnv
from nursing_knowledge_ia_back.database.connection import InitConnection
from nursing_knowledge_ia_back.routes.api_routes.api_routes import ApiRoutes
from datetime import datetime

def StartApp():
    LoadEnv()
    app=StartServer()
    client=InitConnection(GetUri(),GetDBName())
    api_routes = ApiRoutes(client)
    api_routes.register_routes(app)
    app.run(debug=True,port=8080)

if __name__ == '__main__':
    StartApp()
