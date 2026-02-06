# NewsFlow - CMS de Noticias Distribuido

O NewsFlow e um sistema de gerenciamento de conteudo (CMS) desenvolvido para demonstrar conceitos de alta disponibilidade, escalabilidade e transparencia em Sistemas Distribuidos.

## Visao Geral do Projeto

O sistema permite a publicacao, listagem e filtragem de noticias de forma assincrona. A arquitetura foi projetada para suportar alto volume de acessos atraves de um banco de dados NoSQL distribuido com fragmentacao (Sharding), garantindo balanceamento de carga e tolerancia a falhas, hospedado em infraestrutura de nuvem.

## Arquitetura do Sistema e Transparencia

O projeto foi estruturado seguindo principios de sistemas distribuidos, composto por tres camadas principais:

1. Frontend (Visualizacao): Interface desenvolvida em Streamlit, oferecendo um dashboard interativo para leitura e cadastro de noticias.
2. Backend (API): Desenvolvido em FastAPI (Python), atua como gateway, realizando validacoes de dados e orquestracao das requisicoes.
3. Persistencia (Banco de Dados): Cluster MongoDB configurado com Sharding para distribuicao fisica dos dados entre diferentes instancias.

### Estrategia de Distribuicao de Dados (Sharding)

A camada de dados utiliza a estrategia de Range-based Sharding (Particionamento por Faixa).

* Shard Key (Chave de Particionamento): Campo `categoria`.
* Justificativa: A escolha por categoria permite agrupar noticias de temas similares, otimizando consultas de leitura que filtram por assunto e garantindo localidade de dados.

O cluster divide alfabeticamente as categorias entre os nos disponiveis:
* Shard 1: Armazena categorias do inicio do alfabeto (Ex: Artes, Biologia, Economia).
* Shard 2: Armazena categorias do final do alfabeto (Ex: Tecnologia, Zoologia).

Os usuarios acessam os endpoints sem saber em qual fragmento (Shard) do banco de dados a noticia esta armazenada (Transparencia de Localizacao).

## Tecnologias Utilizadas

* Linguagem: Python 3.12
* Framework Web: FastAPI (Async ASGI)
* Interface Grafica: Streamlit
* Banco de Dados: MongoDB 6.0 (Cluster Sharded + Replica Set)
* Driver do Banco: Motor (Conexao Assincrona)
* Validacao de Dados: Pydantic
* Infraestrutura: AWS EC2 (Linux Ubuntu)

## Documentacao da API (Endpoints)

A API conta com documentacao automatica via Swagger UI. Com o servidor rodando, acesse: http://localhost:8000/docs.

| Metodo | Endpoint | Descricao |
| :--- | :--- | :--- |
| POST | /artigos/ | Cria uma nova noticia (com injecao automatica de data) |
| GET | /artigos/ | Lista todas as noticias cadastradas no cluster |
| GET | /artigos/categoria/{cat} | Busca noticias por categoria (Direcionamento via Mongos) |
| DELETE | /artigos/{id} | Remove uma noticia pelo ID unico |

## Como Executar o Projeto (Ambiente Linux/AWS)

Siga os passos abaixo para executar a aplicacao nas instancias EC2.

1. Clonar o repositorio e configurar ambiente:
   git clone https://github.com/murphiie/Projeto_Sistemas_Distribuidos.git
   cd Projeto_Sistemas_Distribuidos
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

2. Configurar o Banco de Dados (Sharding):
   Certifique-se que o cluster MongoDB esta rodando nas instancias de banco. Utilize o script localizado em `scripts/setup_sharding.js` no terminal do `mongos` para configurar as regras de fragmentacao e popular o banco com dados iniciais.

3. Executar a API (Backend):
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload

4. Executar o Dashboard (Frontend):
   Em um novo terminal (com o venv ativado):
   python3 -m streamlit run dashboard.py

## Equipe

| Integrante | Funcoes Principais | GitHub |
| :--- | :--- | :--- |
| Geovana Rodrigues | Engenharia de Backend, Modelagem Pydantic e Documentacao de API | https://github.com/murphiie |
| Rafaela Ramos | Engenharia de Infraestrutura, AWS EC2 e Cluster MongoDB Sharding | https://github.com/RafaellaRamos1 |
