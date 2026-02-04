import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import date

st.set_page_config(page_title="NewsFlow CMS", page_icon="📰", layout="wide")
API_URL = "http://127.0.0.1:8000"

st.title("📰 NewsFlow: Sistema Distribuído")
st.markdown("---")

menu = st.sidebar.selectbox("Navegação", ["Dashboard", "Ler Notícias", "Cadastrar Notícia"])

# --- PÁGINA 1: DASHBOARD ---
if menu == "Dashboard":
    st.header("📊 Monitoramento")
    try:
        response = requests.get(f"{API_URL}/artigos")
        # Aceita 200 (OK) ou 201 (Criado)
        if response.status_code in [200, 201]:
            dados = response.json()
            if dados:
                df = pd.DataFrame(dados)
                st.metric("Total de Artigos", len(dados))
                
                # Inteligência para achar a coluna certa (Inglês ou Português)
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
                # A CORREÇÃO MÁGICA: Aceita 201 como Sucesso também!
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
                    with st.expander(f"{a['titulo']} ({cat})"):
                        st.write(a['corpo'])
                        st.caption(f"Autor: {a['autor']} | Data: {a.get('data_publicacao', 'Hoje')}")
        except Exception as e: 
            st.error(f"Erro: {e}")
