from fastapi import FastAPI, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from typing import List
from bson import ObjectId
from datetime import datetime  # <--- IMPORTAÇÃO DA DATA ADICIONADA

from database import collection, artigo_helper
from models import Artigo

# Organização das seções no Swagger
tags_metadata = [
    {
        "name": "Acervo Público",
        "description": "Exploração e leitura de notícias. Acesso livre ao conhecimento.",
    },
    {
        "name": "Gestão de Conteúdo",
        "description": "Operações de curadoria: inclusão, edição e remoção no banco distribuído.",
    },
    {
        "name": "Monitoramento",
        "description": "Verificação de saúde e conectividade do sistema.",
    }
]

app = FastAPI(
    title="📚 NewsFlow: Biblioteca Digital de Notícias",
    description="""
    ## Sistema de Gerenciamento de Conteúdo Distribuído (CMS)
    
    Este projeto implementa uma arquitetura de alta disponibilidade utilizando:
    * **Distribuição de Dados:** MongoDB Sharded Cluster.
    * **Escalabilidade:** Sharding baseado em categorias.
    
    **Curadoria do Projeto:** Geovana & Rafaela
    """,
    version="2.2.0",
    openapi_tags=tags_metadata,
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,  
        "filter": True,                  
        "docExpansion": "list",         
    }
)

# --- 1. ROTA DE MONITORAMENTO (DASHBOARD VISUAL) ---
@app.get("/", tags=["Monitoramento"], response_class=HTMLResponse, summary="Dashboard do Sistema")
async def root():
    """Retorna a interface visual de monitoramento do NewsFlow."""
    return f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NewsFlow | Dashboard</title>
        <style>
            :root {{
                --bg-primary: #001a23;
                --bg-surface: #002531;
                --action-primary: #00d1ff;
                --text-main: #e0e6ed;
                --status-success: #00e676;
            }}
            body {{
                background-color: var(--bg-primary);
                color: var(--text-main);
                font-family: 'Segoe UI', sans-serif;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}
            .dashboard-card {{
                background-color: var(--bg-surface);
                padding: 3rem;
                border-radius: 24px;
                border: 1px solid rgba(0, 209, 255, 0.3);
                text-align: center;
                box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
                max-width: 450px;
                width: 90%;
            }}
            h1 {{ color: var(--action-primary); font-size: 2.5rem; margin-bottom: 0.5rem; }}
            .badge {{
                display: inline-block;
                padding: 6px 16px;
                background-color: rgba(0, 230, 118, 0.15);
                color: var(--status-success);
                border-radius: 100px;
                font-weight: 600;
                margin-bottom: 2rem;
            }}
            .btn-docs {{
                display: block;
                background-color: var(--action-primary);
                color: var(--bg-primary);
                text-decoration: none;
                padding: 16px;
                border-radius: 12px;
                font-weight: 700;
                text-transform: uppercase;
            }}
        </style>
    </head>
    <body>
        <div class="dashboard-card">
            <h1>📚 NewsFlow</h1>
            <div class="badge">● SISTEMA OPERACIONAL</div>
            <p><strong>Ambiente:</strong> AWS Cloud (Cérebro)</p>
            <p><strong>Curadoria:</strong> Geovana & Rafaela</p>
            <a href="/docs" class="btn-docs">Explorar API (Swagger)</a>
        </div>
    </body>
    </html>
    """

# --- 2. LISTAR TODOS OS ARTIGOS (GET) ---
@app.get("/artigos/", response_model=List[dict], tags=["Acervo Público"], summary="Consultar acervo completo")
async def listar_artigos():
    artigos = []
    async for documento in collection.find():
        artigos.append(artigo_helper(documento))
    return artigos

# --- 3. BUSCAR POR CATEGORIA (GET) ---
@app.get("/artigos/categoria/{category}", response_model=List[dict], tags=["Acervo Público"], summary="Filtrar por Categoria")
async def buscar_por_categoria(category: str):
    artigos = []
    async for documento in collection.find({"category": category}):
        artigos.append(artigo_helper(documento))
    return artigos

# --- 4. CRIAR ARTIGO (POST) - CORRIGIDO COM DATA AUTOMÁTICA ---
@app.post("/artigos/", status_code=status.HTTP_201_CREATED, response_model=dict, tags=["Gestão de Conteúdo"], summary="Catalogar nova notícia")
async def criar_artigo(artigo: Artigo = Body(...)):
    artigo_dict = jsonable_encoder(artigo)
    
    # --- CORREÇÃO: Adiciona a data de hoje automaticamente ---
    if "data_publicacao" not in artigo_dict or not artigo_dict["data_publicacao"]:
        artigo_dict["data_publicacao"] = datetime.now().strftime("%Y-%m-%d")
    
    novo_artigo = await collection.insert_one(artigo_dict)
    
    criado = await collection.find_one({"_id": novo_artigo.inserted_id})
    if criado:
        return artigo_helper(criado)
    raise HTTPException(status_code=400, detail="Erro ao catalogar")

# --- 5. ATUALIZAR ARTIGO (PUT) ---
@app.put("/artigos/{id}", tags=["Gestão de Conteúdo"], summary="Atualizar notícia existente")
async def atualizar_artigo(id: str, artigo: Artigo = Body(...)):
    """Atualiza um registro no cluster distribuído via ID."""
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    artigo_dict = jsonable_encoder(artigo)
    
    # Mantém a data original se não for enviada nova
    if "data_publicacao" not in artigo_dict:
         artigo_dict["data_publicacao"] = datetime.now().strftime("%Y-%m-%d")

    update_result = await collection.update_one(
        {"_id": ObjectId(id)}, 
        {"$set": artigo_dict}
    )
    
    if update_result.modified_count == 1:
        return {"mensagem": "Registro atualizado com sucesso"}
    
    # Se não modificou nada (dados iguais), mas o ID existe, retornamos sucesso ou aviso
    if update_result.matched_count == 1:
        return {"mensagem": "Nenhuma alteração necessária (dados idênticos)"}
        
    raise HTTPException(status_code=404, detail="Artigo não encontrado para atualização")

# --- 6. DELETAR ARTIGO (DELETE) ---
@app.delete("/artigos/{id}", tags=["Gestão de Conteúdo"], summary="Remover registro do acervo")
async def deletar_artigo(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Identificador inválido")
        
    delete_result = await collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"mensagem": "Registro removido com sucesso"}
    raise HTTPException(status_code=404, detail="Registro não encontrado")
