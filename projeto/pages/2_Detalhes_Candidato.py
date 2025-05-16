import streamlit as st
from utils import applicants_dict 

st.set_page_config(page_title="Detalhes do Candidato", layout="wide")

if not st.session_state.get("logged_in", False) or st.session_state.get("user_type") != "admin":
    st.error("Acesso negado. Você precisa estar logado como administrador para acessar esta página.")
    if st.button("Ir para Home"):
        st.switch_page("1_Home.py")
    st.stop()

codigo = st.session_state.get("candidato_selecionado")

if not codigo or codigo not in applicants_dict:
    st.warning("Nenhum candidato selecionado.")
    st.stop()

candidato = applicants_dict[codigo]

st.title(candidato["infos_basicas"]["nome"])

st.header("Objetivo Profissional")
st.write(candidato["infos_basicas"]["objetivo_profissional"])

st.header("Informações Pessoais")
st.json(candidato["informacoes_pessoais"])

st.header("Informações Profissionais")
st.json(candidato["informacoes_profissionais"])

st.header("Formação e Idiomas")
st.json(candidato["formacao_e_idiomas"])

st.header("Currículo (PT)")
st.markdown(f"```text\n{candidato['cv_pt']}\n```")
