# pages/2_Criar_Vaga.py
import streamlit as st
from utils import hide_streamlit_sidebar_css, criar_vaga

st.set_page_config(page_title="Criar Nova Vaga - Admin", layout="wide", initial_sidebar_state="collapsed")
hide_streamlit_sidebar_css()

if not st.session_state.get("logged_in", False) or st.session_state.get("user_type") != "admin":
    st.error("Acesso negado. Você precisa estar logado como administrador para acessar esta página.")
    if st.button("Ir para Home"):
        st.switch_page("1_Home.py")
    st.stop()

st.title("Criar Nova Vaga")
st.caption(f"Logado como: {st.session_state.user_name} (Admin)")

with st.form("criar_vaga_form"):
    st.subheader("Detalhes da Vaga")
    titulo = st.text_input("Título da Vaga", placeholder="Ex: Desenvolvedor Python Sênior")
    empresa = st.text_input("Nome da Empresa", placeholder="Ex: InovaTech Soluções")
    local = st.text_input("Localização", placeholder="Ex: Remoto, São Paulo - SP, Híbrido")
    tipo_contrato = st.selectbox("Tipo de Contrato", ["CLT", "PJ", "Estágio", "Temporário", "Freelancer"])
    salario = st.text_input("Faixa Salarial (opcional)", placeholder="Ex: R$ 5.000 - R$ 7.000 ou A Combinar")
    descricao = st.text_area("Descrição Completa da Vaga", height=200, placeholder="Descreva as responsabilidades, a cultura da empresa, etc.")
    requisitos = st.text_area("Requisitos da Vaga", height=150, placeholder="Liste as habilidades, experiências e qualificações necessárias. Separe por vírgulas ou quebras de linha.")
    
    submit_button = st.form_submit_button("Publicar Vaga")

if submit_button:
    if titulo and empresa and local and descricao and requisitos and tipo_contrato:
        try:
            id_nova_vaga = criar_vaga(titulo, empresa, local, descricao, requisitos, tipo_contrato, salario)
            # Corrigido o f-string abaixo:
            st.success(f"Vaga '{titulo}' publicada com sucesso! ID da Vaga: {id_nova_vaga}")
            st.session_state.nova_vaga_id = id_nova_vaga
            st.switch_page("pages/2_Recomendacao_CVs.py")
        except Exception as e:
            st.error(f"Erro ao criar vaga: {e}")
    else:
        st.warning("Por favor, preencha todos os campos obrigatórios (Título, Empresa, Local, Descrição, Requisitos, Tipo de Contrato).")

st.divider()

col_nav1, col_nav2 = st.columns(2)
with col_nav1:
    # Uso correto de st.switch_page para navegação
    if st.button("Voltar para Home (Admin)", key="home_admin_criar_vaga", use_container_width=True):
        st.switch_page("1_Home.py")
with col_nav2:
    if st.button("Ir para Painel Administrativo", key="painel_admin_criar_vaga", use_container_width=True):
        st.switch_page("pages/3_Painel_Admin.py")

