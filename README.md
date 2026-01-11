#  NewsFlow - CMS de Notícias Distribuído

O **NewsFlow** é um sistema de gerenciamento de conteúdo (CMS) desenvolvido para demonstrar conceitos de alta disponibilidade, escalabilidade e transparência em **Sistemas Distribuídos**.

##  Visão Geral do Projeto
O sistema permite a publicação, listagem e filtragem de notícias de forma assíncrona, utilizando um banco de dados NoSQL fragmentado (Sharding) para garantir que o sistema suporte um alto volume de acessos.

##  Tecnologias Utilizadas
* **Linguagem:** Python 3.12
* **Framework Web:** [FastAPI](https://fastapi.tiangolo.com/) (Async ASGI)
* **Banco de Dados:** MongoDB (Cluster com Sharding)
* **Driver do Banco:** [Motor](https://motor.readthedocs.io/) (Conexão Assíncrona)
* **Validação de Dados:** [Pydantic](https://docs.pydantic.dev/)
* **Containerização:** Docker & Docker Compose

## Arquitetura e Transparência
Este projeto foi estruturado seguindo princípios de sistemas distribuídos:
1.  **Processamento Assíncrono:** Uso de `async/await` para operações de I/O não bloqueantes.
2.  **Transparência de Localização:** O usuário acessa os endpoints sem saber em qual fragmento (Shard) do banco de dados a notícia está armazenada.
3.  **Fragmentação de Dados (Sharding):** Utilizamos o campo `categoria` como **Shard Key** para distribuir a carga entre diferentes servidores de dados.

##  Documentação da API (Endpoints)
A API conta com documentação automática via **Swagger UI**. Com o servidor rodando, acesse: `http://localhost:8000/docs`.

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| **POST** | `/artigos/` | Cria uma nova notícia (Validação Pydantic) |
| **GET** | `/artigos/` | Lista todas as notícias cadastradas |
| **GET** | `/artigos/categoria/{cat}` | Busca notícias por categoria (Uso da Shard Key) |
| **DELETE** | `/artigos/{id}` | Remove uma notícia pelo ID único |

##  Como Executar o Projeto

1. **Clonar o repositório:**
   ```bash
   git clone [https://github.com/murphiie/Projeto_Sistemas_Distribuidos.git](https://github.com/murphiie/Projeto_Sistemas_Distribuidos.git)

2. **Configurar o Ambiente Virtual (VENV):**
    ```bash
    python -m venv venv
    source venv/bin/activate

3. **Instalar Dependências:**
    ```bash
    pip install -r requirements.txt

4. **Executar a API:**
    ```bash
    uvicorn main:app --reload

## 👥 Equipe

| Integrante | Funções Principais | GitHub |
| :--- | :--- | :--- |
| **Geovana Rodrigues** | Engenharia de Backend, Modelagem Pydantic e Documentação de API | [@murphiie](https://github.com/murphiie) |
| **Rafaela Ramos** | Engenharia de Infraestrutura, Configuração de Docker e Cluster MongoDB Sharding | [@RafaellaRamos1](https://github.com/RafaellaRamos1) |
# Projeto Sistemas Distribuídos - API

## Como rodar a API

1. Instalar Docker e Docker Compose
2. Clonar o projeto:
 
   git clone https://github.com/murphiie/Projeto_Sistemas_Distribuidos.git
   cd Projeto_Sistemas_Distribuidos/api
#Subir os containers:

docker-compose up --build                                                                                   Inicializar o Replica Set do MongoDB (uma vez):

docker exec -it mongo1 mongo
#No shell do Mongo, rode:

rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongo1:27017" },
    { _id: 1, host: "mongo2:27017" },
    { _id: 2, host: "mongo3:27017" }
  ]
})
#A API estará disponível em:

http://localhost:8000
Para parar os containers:

docker-compose down
