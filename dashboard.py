import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import date

st.set_page_config(page_title="NewsFlow CMS", page_icon="📰", layout="wide")
# Lembre-se de alterar para o seu IP Público se estiver rodando na AWS
API_URL = "http://127.0.0.1:8000"

st.title("📰 NewsFlow: Sistema Distribuído")
st.markdown("---")

# MENU ATUALIZADO: Incluindo Atualizar e Remover
menu = st.sidebar.selectbox("Navegação", ["Dashboard", "Ler Notícias", "Cadastrar Notícia", "Atualizar Notícia", "Remover Notícia"])

# --- PÁGINA 1: DASHBOARD ---
if menu == "Dashboard":
    st.header("📊 Monitoramento")
    try:
        response = requests.get(f"{API_URL}/artigos")
        if response.status_code in [200, 201]:
            dados = response.json()
            if dados:
                df = pd.DataFrame(dados)
                st.metric("Total de Artigos", len(dados))
                
                coluna = 'category' if 'category' in df.columns else 'categoria'
                
                if coluna in df.columns:
                    contagem = df[coluna].value_counts()
                    fig = px.pie(values=contagem.values, names=contagem.index, title="Distribuição nos Shards")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Dados encontrados, mas sem categoria definida.")
            else:
                st.warning("Banco de dados vazio. Insira notícias!")
        else:
            st.error(f"Erro na API: {response.status_code}")
    except Exception as e:
        st.error(f"API Offline: {e}")

# --- PÁGINA 2: CADASTRAR ---
elif menu == "Cadastrar Notícia":
    st.header("✍️ Cadastro")
    with st.form("form"):
        titulo = st.text_input("Título")
        autor = st.text_input("Autor")
        categoria = st.selectbox("Categoria", ["Esportes", "Politica", "Tecnologia", "Saúde"])
        corpo = st.text_area("Texto")
        
        if st.form_submit_button("Enviar"):
            payload = {
                "titulo": titulo, 
                "autor": autor, 
                "category": categoria,  
                "corpo": corpo,
                "data_publicacao": str(date.today())
            }
            try:
                res = requests.post(f"{API_URL}/artigos", json=payload)
                if res.status_code in [200, 201]: 
                    st.success("✅ Sucesso! Notícia salva e distribuída.")
                else: 
                    st.error(f"❌ Erro: {res.status_code} - {res.text}")
            except Exception as e: 
                st.error(f"Erro: {e}")

# --- PÁGINA 3: LER NOTÍCIAS ---            
elif menu == "Ler Notícias":
    st.header("📂 Acervo")
    if st.button("Atualizar Lista"):
        try:
            r = requests.get(f"{API_URL}/artigos")
            if r.status_code in [200, 201]:
                for a in r.json():
                    cat = a.get('category', a.get('categoria', 'Geral'))
                    # Exibindo o ID para facilitar a cópia para as funções de Update/Delete
                    with st.expander(f"{a['titulo']} ({cat})"):
                        st.code(f"ID: {a.get('id', a.get('_id'))}") 
                        st.write(a['corpo'])
                        st.caption(f"Autor: {a['autor']} | Data: {a.get('data_publicacao', 'Hoje')}")
        except Exception as e: 
            st.error(f"Erro: {e}")

# --- PÁGINA 4: ATUALIZAR NOTÍCIA ---
elif menu == "Atualizar Notícia":
    st.header("📝 Editar Registro")
    id_artigo = st.text_input("ID do Artigo para atualizar")
    
    with st.form("update_form"):
        st.write("Novos dados:")
        new_titulo = st.text_input("Novo Título")
        new_autor = st.text_input("Novo Autor")
        new_cat = st.selectbox("Nova Categoria", ["Esportes", "Politica", "Tecnologia", "Saúde"])
        new_corpo = st.text_area("Novo Texto")
        
        if st.form_submit_button("Salvar Alterações"):
            payload = {
                "titulo": new_titulo, 
                "autor": new_autor, 
                "category": new_cat, 
                "corpo": new_corpo,
                "data_publicacao": str(date.today())
            }
            try:
                # Requer que você tenha a rota @app.put("/artigos/{id}") no main.py
                res = requests.put(f"{API_URL}/artigos/{id_artigo}", json=payload)
                if res.status_code == 200:
                    st.success("✅ Artigo atualizado com sucesso!")
                else:
                    st.error(f"Erro ao atualizar: {res.status_code}")
            except Exception as e:
                st.error(f"Erro: {e}")

# --- PÁGINA 5: REMOVER NOTÍCIA ---
elif menu == "Remover Notícia":
    st.header("🗑️ Excluir do Sistema")
    id_delete = st.text_input("Cole o ID do artigo que deseja remover")
    
    if st.button("Remover Permanentemente"):
        if id_delete:
            try:
                res = requests.delete(f"{API_URL}/artigos/{id_delete}")
                if res.status_code == 200:
                    st.success("✅ Notícia removida do cluster distribuído!")
                else:
                    st.error(f"Erro: {res.status_code} - {res.text}")
            except Exception as e:
                st.error(f"Erro de conexão: {e}")
        else:
            st.warning("Por favor, insira um ID válido.")
