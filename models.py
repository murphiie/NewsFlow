from pydantic import BaseModel, Field
from datetime import datetime

# Esta é a implementação da sua Tarefa 2: Modelos Pydantic 
class Artigo(BaseModel):
    titulo: str = Field(..., min_length=5)
    corpo: str
    autor: str
    categoria: str  # Campo crucial para a estratégia de Sharding [cite: 24, 54, 77]
    data_publicacao: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "titulo": "Sistemas Distribuídos na Prática",
                "corpo": "Conteúdo detalhado sobre escalabilidade...",
                "autor": "Geovana Rodrigues",
                "categoria": "Tecnologia"
            }
        }