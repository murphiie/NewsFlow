from motor.motor_asyncio import AsyncIOMotorClient
import os

# Esta URL será configurada depois no Docker. 
MONGODB_URL = "mongodb://localhost:27017"

client = AsyncIOMotorClient("mongodb://mongos:27017")
db = client.newsflow_db
collection = db.get_collection("artigos")

# Função auxiliar para formatar os documentos do MongoDB (que usam _id) 
def artigo_helper(artigo) -> dict:
    return {
        "id": str(artigo["_id"]),
        "titulo": artigo["titulo"],
        "corpo": artigo["corpo"],
        "autor": artigo["autor"],
        "categoria": artigo["categoria"],
        "data_publicacao": artigo["data_publicacao"],
    }
