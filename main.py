from fastapi import FastAPI, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from bson import ObjectId

# Importando a lógica de conexão e os modelos que você criou
from database import collection, artigo_helper
from models import Artigo

# Inicialização da API 
app = FastAPI(
    title="NewsFlow - CMS Distribuído",
    description="Backend para gerenciamento de notícias com suporte a alta concorrência."
)

# 1. ROTA DE VERIFICAÇÃO 
@app.get("/", tags=["Status"])
async def root():
    return {"status": "Online", "sistema": "NewsFlow CMS"}

#  2. CRIAR ARTIGO (POST) 
@app.post("/artigos/", status_code=status.HTTP_201_CREATED, response_model=dict, tags=["Artigos"])
async def criar_artigo(artigo: Artigo = Body(...)):
    """Publica um novo artigo no banco de dados distribuído."""
    artigo_dict = jsonable_encoder(artigo)
    #  conexão assíncrona (Motor) 
    novo_artigo = await collection.insert_one(artigo_dict)
    criado = await collection.find_one({"_id": novo_artigo.inserted_id})
    return artigo_helper(criado)

#  3. LISTAR TODOS OS ARTIGOS (GET) 
@app.get("/artigos/", response_model=List[dict], tags=["Artigos"])
async def listar_artigos():
    """Consulta massiva de artigos com baixa latência."""
    artigos = []
    #  Non-blocking I/O 
    async for documento in collection.find():
        artigos.append(artigo_helper(documento))
    return artigos

#  4. BUSCAR POR CATEGORIA (GET) 
@app.get("/artigos/categoria/{categoria}", response_model=List[dict], tags=["Artigos"])
async def buscar_por_categoria(categoria: str):
    """Filtra artigos pela Shard Key (Categoria)."""
    artigos = []
    async for documento in collection.find({"categoria": categoria}):
        artigos.append(artigo_helper(documento))
    return artigos

#  5. DELETAR ARTIGO (DELETE) 
@app.delete("/artigos/{id}", tags=["Artigos"])
async def deletar_artigo(id: str):
    """Remove um artigo pelo ID."""
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
        
    delete_result = await collection.delete_one({"_id": ObjectId(id)})
    
    if delete_result.deleted_count == 1:
        return {"mensagem": "Artigo removido com sucesso"}
        
    raise HTTPException(status_code=404, detail="Artigo não encontrado")