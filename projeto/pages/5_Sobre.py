import streamlit as st

st.set_page_config(page_title="Sobre - Decision", layout="wide", initial_sidebar_state="collapsed")

# Adiciona CSS para ocultar completamente a barra lateral
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            display: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Botões de Navegação
col_nav_home, col_nav_vagas, col_nav_spacer_sobre = st.columns([1, 1, 8])
with col_nav_home:
    if st.button("Home", key="home_sobre_page"):
        # IMPORTANTE: Substitua "NOME_DO_SEU_SCRIPT_PRINCIPAL.py" pelo nome real do seu arquivo principal Streamlit (ex: app.py, main.py, ou o nome que você deu ao script principal)
        st.switch_page("1_Home.py")
with col_nav_vagas:
    if st.button("Vagas", key="vagas_sobre_page"):
        st.switch_page("pages/2_Vagas.py")

st.divider()

st.title("Sobre a Plataforma Decision")
st.write(
    "Bem-vindo à página Sobre da plataforma Decision. Aqui você encontrará mais informações sobre nosso projeto e equipe."
)
st.write(
    "A Decision é uma plataforma de recrutamento inovadora projetada para conectar talentos a oportunidades de forma eficiente e intuitiva."
)
# Adicionar mais conteúdo conforme necessário

