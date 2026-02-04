import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# URL de conexão: localhost aponta para o Mongos rodando na Instância 1 [cite: 43]
MONGODB_URL = "mongodb://localhost:27017" 
DATABASE_NAME = "newsflow_db"
COLLECTION_NAME = "artigos"

# Categorias para testar a distribuição (Shard Key) [cite: 24, 54]
CATEGORIAS = ["Tecnologia", "Política", "Esportes", "Saúde", "Cultura"]

def gerar_artigos(quantidade: int):
    artigos = []
    for i in range(quantidade):
        cat = CATEGORIAS[i % len(CATEGORIAS)] # Distribui entre as categorias
        artigo = {
            "titulo": f"Notícia de Teste Automático {i}",
            "corpo": f"Este é o conteúdo detalhado da notícia número {i} para teste de carga e sharding. [cite: 78]",
            "autor": "Bot de Seed",
            "categoria": cat, # CORRIGIDO: Deve ser igual à Shard Key definida no cluster 
            "data_publicacao": datetime.utcnow().isoformat()
        }
        artigos.append(artigo)
    return artigos

async def rodar_seed():
    print(f"Iniciando conexão com {MONGODB_URL}...")
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    print(f"Gerando {50} artigos de teste...")
    dados = gerar_artigos(50)

    print("Inserindo no banco de dados distribuído via Mongos... [cite: 43]")
    try:
        resultado = await collection.insert_many(dados)
        print(f"Sucesso! {len(resultado.inserted_ids)} artigos foram inseridos.")
        print("A distribuição entre Shards foi processada automaticamente. [cite: 59]")
    except Exception as e:
        print(f"Erro ao inserir: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(rodar_seed())
