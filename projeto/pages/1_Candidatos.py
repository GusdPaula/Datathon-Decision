import streamlit as st

# Simulação de dados de candidatos (use seu dicionário real no lugar disso)
if not st.session_state.get("logged_in", False) or st.session_state.get("user_type") != "admin":
    st.error("Acesso negado. Você precisa estar logado como administrador para acessar esta página.")
    if st.button("Ir para Home"):
        st.switch_page("1_Home.py")
    st.stop()

from utils import applicants_dict  # Suponha que este é o dicionário que você já enviou

st.set_page_config(page_title="Candidatos", layout="wide")

st.title("Lista de Candidatos")

for codigo, candidato in applicants_dict.items():
    with st.container(border=True):
        st.subheader(candidato["infos_basicas"]["nome"])
        st.caption(f"{candidato['infos_basicas']['objetivo_profissional']} - {candidato['infos_basicas']['local']}")
        st.write(f"Email: {candidato['infos_basicas']['email']}")
        
        if st.button("Ver mais informações", key=f"ver_{codigo}"):
            st.session_state.candidato_selecionado = codigo
            st.switch_page("pages/2_Detalhes_Candidato.py")
