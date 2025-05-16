import streamlit as st
import pandas as pd
from utils import VAGAS_DB, recommend_cvs_for_job

# Configuração da página - DEVE SER A PRIMEIRA COMANDO DO STREAMLIT
st.set_page_config(page_title="Cvs - Decision", layout="wide")

if not st.session_state.get("logged_in", False) or st.session_state.get("user_type") != "admin":
    st.error("Acesso negado. Você precisa estar logado como administrador para acessar esta página.")
    if st.button("Ir para Home"):
        st.switch_page("1_Home.py")
    st.stop()


# Botões de Navegação
col_nav_home, col_nav_sobre, col_nav_spacer_cvs = st.columns([1, 1, 8]) 
with col_nav_home:
    if st.button("Home", key="home_cvs"):
        # IMPORTANTE: Substitua "NOME_DO_SEU_SCRIPT_PRINCIPAL.py" pelo nome real do seu arquivo principal Streamlit (ex: app.py, main.py, Home.py ou o nome que você deu ao script principal)
        st.switch_page('1_Home.py') 
with col_nav_sobre:
    if st.button("Sobre", key="sobre_cvs"):
        st.switch_page("pages/5_Sobre.py") # Navega para a página Sobre dentro da pasta pages

st.divider()

# Título da página de cvs
st.title("Recomendação de Cvs")

if "nova_vaga_id" in st.session_state:
    recommend_cvs_for_job(VAGAS_DB[st.session_state.nova_vaga_id])

else:
    st.warning("Nada a mostrar")


