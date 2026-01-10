import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# URL de conexão 
MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "newsflow_db"
COLLECTION_NAME = "artigos"

# teste
CATEGORIAS = ["Tecnologia", "Política", "Esportes", "Saúde", "Cultura"]

def gerar_artigos(quantidade: int):
    artigos = []
    for i in range(quantidade):
        cat = CATEGORIAS[i % len(CATEGORIAS)] # Distribui entre as categorias
        artigo = {
            "titulo": f"Notícia de Teste Automático {i}",
            "corpo": f"Este é o conteúdo detalhado da notícia número {i} para teste de carga e sharding.",
            "autor": "Bot de Seed",
            "categoria": cat,
            "data_publicacao": datetime.utcnow().isoformat()
        }
        artigos.append(artigo)
    return artigos

async def rodar_seed():
    print(f"Iniciando conexão com {MONGODB_URL}...")
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    print("Gerando 50 artigos de teste...")
    dados = gerar_artigos(50)

    print("Inserindo no banco de dados distribuído...")
    resultado = await collection.insert_many(dados)
    
    print(f"Sucesso! {len(resultado.inserted_ids)} artigos foram inseridos.")
    client.close()

if __name__ == "__main__":
    asyncio.run(rodar_seed())