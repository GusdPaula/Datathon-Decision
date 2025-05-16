# pages/6_Recomendacao_Vagas.py
import streamlit as st
from utils import hide_streamlit_sidebar_css
from utils import USUARIOS_DB
from utils import predict_jobs_for_cv

st.set_page_config(page_title="Recomendações de Vagas - Decision", layout="wide", initial_sidebar_state="collapsed")
hide_streamlit_sidebar_css()

if not st.session_state.get("logged_in", False) or st.session_state.get("user_type") != "candidato":
    st.error("Acesso negado. Você precisa estar logado como candidato para acessar esta página.")
    if st.button("Ir para Home"):
        st.switch_page("1_Home.py")
    st.stop()

st.title("Recomendações de Vagas para Você")
st.caption(f"Logado como: {st.session_state.user_name} (Candidato)")


cv_text = USUARIOS_DB[st.session_state.username]['curriculo']

st.subheader("Vagas Recomendadas")

predict_jobs_for_cv(cv_text)

st.divider()
# Corrigido para usar st.switch_page diretamente
if st.button("Voltar para Home", key="home_recomendacoes", use_container_width=True):
    st.switch_page("1_Home.py")

