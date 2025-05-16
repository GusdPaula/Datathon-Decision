# pages/5_Minhas_Candidaturas.py
import streamlit as st
from utils import hide_streamlit_sidebar_css, listar_candidaturas_por_usuario, get_vaga_titulo

st.set_page_config(page_title="Minhas Candidaturas - Decision", layout="wide", initial_sidebar_state="collapsed")
hide_streamlit_sidebar_css()

if not st.session_state.get("logged_in", False) or st.session_state.get("user_type") != "candidato":
    st.error("Acesso negado. Você precisa estar logado como candidato para acessar esta página.")
    if st.button("Ir para Home"):
        st.switch_page("1_Home.py")
    st.stop()

st.title("Minhas Candidaturas")
st.caption(f"Logado como: {st.session_state.user_name} (Candidato)")

username_candidato = st.session_state.username
candidaturas = listar_candidaturas_por_usuario(username_candidato)

if not candidaturas:
    st.info("Você ainda não se candidatou a nenhuma vaga.")
    if st.button("Ver Vagas Disponíveis", use_container_width=True):
        st.switch_page("pages/4_Listar_Vagas.py")
else:
    st.write(f"Você se candidatou para {len(candidaturas)} vaga(s):")
    st.divider()

    for candidatura in candidaturas:
        with st.container(border=True):
            vaga_titulo = get_vaga_titulo(candidatura["id_vaga"])
            st.subheader(f"Vaga: {vaga_titulo}")
            st.write(f"**ID da Vaga:** {candidatura["id_vaga"]}")
            st.write(f"**Data da Candidatura:** {candidatura["data_candidatura"]}")
            
            status_cor = "gray"
            if candidatura["status"] == "Em Análise":
                status_cor = "orange"
            elif candidatura["status"] == "Aprovado":
                status_cor = "green"
            elif candidatura["status"] == "Rejeitado":
                status_cor = "red"
            
            st.markdown(f"**Status:** <span style=\'color:{status_cor}; font-weight:bold;\'>{candidatura["status"]}</span>", unsafe_allow_html=True)
            # Adicionar mais detalhes se necessário, como feedback (se houver)

st.divider()
# Corrigido para usar st.switch_page diretamente
if st.button("Voltar para Home", key="home_minhas_candidaturas", use_container_width=True):
    st.switch_page("1_Home.py")

