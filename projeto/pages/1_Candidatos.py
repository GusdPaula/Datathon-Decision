import streamlit as st

# Simulação de dados de candidatos (use seu dicionário real no lugar disso)
if not st.session_state.get("logged_in", False) or st.session_state.get("user_type") != "admin":
    st.error("Acesso negado. Você precisa estar logado como administrador para acessar esta página.")
    if st.button("Ir para Home"):
        st.switch_page("1_Home.py")
    st.stop()

from utils import applicants_dict  # Seu dicionário real de candidatos

st.set_page_config(page_title="Candidatos", layout="wide")

st.title("Lista de Candidatos")

# Inicializa o contador de candidatos visíveis
if "visible_count" not in st.session_state:
    st.session_state.visible_count = 10

# Lista de códigos (ids) dos candidatos para garantir ordem e slicing
codigos = list(applicants_dict.keys())

# Exibe só até visible_count candidatos
for codigo in codigos[:st.session_state.visible_count]:
    candidato = applicants_dict[codigo]
    with st.container():
        st.subheader(candidato["infos_basicas"]["nome"])
        st.caption(f"{candidato['infos_basicas']['objetivo_profissional']} - {candidato['infos_basicas']['local']}")
        st.write(f"Email: {candidato['infos_basicas']['email']}")

        if st.button("Ver mais informações", key=f"ver_{codigo}"):
            st.session_state.candidato_selecionado = codigo
            st.switch_page("pages/2_Detalhes_Candidato.py")

# Botão para carregar mais candidatos, só aparece se houver mais candidatos para mostrar
if st.session_state.visible_count < len(codigos):
    if st.button("Ver mais candidatos"):
        st.session_state.visible_count += 10
        st.experimental_rerun()  # recarrega a página para mostrar mais candidatos
