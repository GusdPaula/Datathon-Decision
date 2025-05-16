# 1_Home.py (Modificado com upload de currículo)
import streamlit as st
# Importar register_candidate e USUARIOS_DB de utils
from utils import check_login, hide_streamlit_sidebar_css, USUARIOS_DB, register_candidate

st.set_page_config(
    page_title="Plataforma de Vagas - Decision",
    layout="wide",
    initial_sidebar_state="collapsed"
)

hide_streamlit_sidebar_css()

# Inicialização do estado da sessão
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'user_type' not in st.session_state:
    st.session_state.user_type = ""
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# --- Tela Inicial ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #2E86C1;'>Bem-vindo à <span style='color: #1ABC9C;'>Plataforma de Vagas Decision</span></h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Conectando talentos às oportunidades certas</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Nossa missão é facilitar o encontro entre candidatos qualificados e empresas que buscam os melhores profissionais.</p>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("👤 Área do Candidato", use_container_width=True, key="btn_area_candidato"):
            st.session_state.login_area = "candidato"
            st.rerun() # Usar rerun para atualizar a exibição da seção correta
    with col2:
        if st.button("🧑‍💼 Área do Recrutador (Admin)", use_container_width=True, key="btn_area_admin"):
            st.session_state.login_area = "admin"
            st.rerun()
    with col3:
        if st.button("📝 Cadastrar-se como Candidato", use_container_width=True, key="btn_cadastrar_candidato"):
            st.session_state.login_area = "cadastro"
            st.rerun()

    if 'login_area' in st.session_state:
        st.markdown("---")
        if st.button("🔙 Voltar", key="btn_voltar_login_area"):
            del st.session_state.login_area
            st.rerun()

        if st.session_state.login_area == "candidato":
            st.subheader("Login do Candidato")
            with st.form("login_candidato_form"):
                username_cand = st.text_input("Usuário do Candidato", key="user_cand_login")
                password_cand = st.text_input("Senha", type="password", key="pass_cand_login")
                login_button_cand = st.form_submit_button("Entrar")

                if login_button_cand:
                    success, user_type, user_name = check_login(username_cand, password_cand)
                    if success and user_type == "candidato":
                        st.session_state.logged_in = True
                        st.session_state.username = username_cand
                        st.session_state.user_type = user_type
                        st.session_state.user_name = user_name
                        # Ao invés de st.switch_page aqui, vamos usar st.rerun() para que a parte 'else' do if not st.session_state.logged_in seja executada
                        st.rerun()
                    else:
                        st.error("Credenciais inválidas ou perfil não autorizado.")
            st.markdown("---")
            st.markdown("**Usuários de Demonstração (Candidatos):**")
            st.markdown("- Usuário: `candidato1`, Senha: `candidato123`")
            st.markdown("- Usuário: `candidato2`, Senha: `senha456`")

        elif st.session_state.login_area == "admin":
            st.subheader("Login do Recrutador (Admin)")
            with st.form("login_admin_form"):
                username_adm = st.text_input("Usuário do Recrutador", key="user_adm_login")
                password_adm = st.text_input("Senha", type="password", key="pass_adm_login")
                login_button_adm = st.form_submit_button("Entrar")

                if login_button_adm:
                    success, user_type, user_name = check_login(username_adm, password_adm)
                    if success and user_type == "admin":
                        st.session_state.logged_in = True
                        st.session_state.username = username_adm
                        st.session_state.user_type = user_type
                        st.session_state.user_name = user_name
                        st.rerun()
                    else:
                        st.error("Credenciais inválidas ou perfil não autorizado.")
            st.markdown("---")
            st.markdown("**Usuário de Demonstração (Admin):**")
            st.markdown("- Usuário: `admin`, Senha: `admin123`")

        elif st.session_state.login_area == "cadastro":
            st.subheader("Cadastro de Novo Candidato")
            with st.form("cadastro_form_candidato"):
                reg_nome = st.text_input("Nome completo", key="reg_nome_cand")
                # Mantendo os campos que o usuário tinha, embora não todos sejam usados por register_candidate
                reg_email = st.text_input("E-mail", key="reg_email_cand") 
                reg_cpf = st.text_input("CPF", key="reg_cpf_cand")
                reg_telefone = st.text_input("Telefone", key="reg_tel_cand")
                reg_usuario = st.text_input("Nome de usuário desejado", key="reg_user_cand")
                reg_senha = st.text_input("Senha", type="password", key="reg_pass_cand")
                reg_senha_confirm = st.text_input("Confirme a Senha", type="password", key="reg_pass_conf_cand")
                reg_formacao = st.selectbox("Formação", ["Ensino Médio", "Técnico", "Superior Incompleto", "Superior Completo", "Pós-graduação"], key="reg_form_cand")
                reg_area_interesse = st.selectbox("Área de Interesse", ["Tecnologia", "Administração", "Saúde", "Educação", "Outro"], key="reg_area_cand")
                reg_experiencia = st.text_area("Experiências anteriores", key="reg_exp_cand")
                # Campo de upload de currículo adicionado aqui
                reg_curriculo_file = st.file_uploader("Envie seu Currículo (PDF, DOC, DOCX)", type=["pdf", "doc", "docx"], key="reg_cv_cand")
                
                cadastrar_button = st.form_submit_button("Finalizar Cadastro")

                if cadastrar_button:
                    if not all([reg_nome, reg_usuario, reg_senha, reg_senha_confirm]):
                        st.warning("Por favor, preencha os campos obrigatórios: Nome completo, Nome de usuário e Senha.")
                    elif reg_senha != reg_senha_confirm:
                        st.error("As senhas não coincidem.")
                    else:
                        # Chamar a função de registro do utils.py
                        # A função register_candidate espera (nome_completo, username, password, uploaded_file)
                        success_reg, message_reg = register_candidate(reg_nome, reg_usuario, reg_senha, reg_curriculo_file)
                        if success_reg:
                            st.success(message_reg)
                            st.info("Cadastro realizado! Agora você pode fazer login na seção 'Área do Candidato'.")
                            # Não faz login automático, usuário deve ir para a tela de login.
                        else:
                            st.error(message_reg)

else:
    # --- Conteúdo Pós-Login (Mesma lógica da versão anterior) ---
    header_cols = st.columns([0.8, 0.2])
    with header_cols[0]:
        st.title(f"Bem-vindo(a), {st.session_state.user_name}!")
        st.caption(f"Você está logado como: {st.session_state.user_type.capitalize()}")
    with header_cols[1]:
        if st.button("Logout", key="logout_home_main", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.user_type = ""
            st.session_state.user_name = ""
            if 'login_area' in st.session_state: # Limpar a área de login ao deslogar
                del st.session_state.login_area
            st.rerun()

    st.divider()
    st.subheader("Navegação Principal")

    if st.session_state.user_type == "admin":
        nav_cols_admin = st.columns(3)
        with nav_cols_admin[0]:
            if st.button("Criar Nova Vaga", key="nav_criar_vaga_adm", use_container_width=True):
                st.switch_page("pages/2_Criar_Vaga.py")
        with nav_cols_admin[1]:
            if st.button("Painel Administrativo", key="nav_painel_admin_adm", use_container_width=True):
                st.switch_page("pages/3_Painel_Admin.py")
        with nav_cols_admin[2]:
            if st.button("Listar Todas as Vagas (Visão Admin)", key="nav_listar_vagas_adm_main", use_container_width=True):
                st.switch_page("pages/4_Listar_Vagas.py")

    elif st.session_state.user_type == "candidato":
        nav_cols_candidato = st.columns(3)
        with nav_cols_candidato[0]:
            if st.button("Ver Vagas Disponíveis", key="nav_listar_vagas_cand", use_container_width=True):
                st.switch_page("pages/4_Listar_Vagas.py")
        with nav_cols_candidato[1]:
            if st.button("Minhas Candidaturas", key="nav_minhas_candidaturas_cand", use_container_width=True):
                st.switch_page("pages/5_Minhas_Candidaturas.py")
        with nav_cols_candidato[2]:
            if st.button("Recomendações de Vagas", key="nav_recomendacoes_cand", use_container_width=True):
                st.switch_page("pages/6_Recomendacao_Vagas.py")
    else:
        st.error("Tipo de usuário desconhecido. Por favor, faça logout e tente novamente.")

    st.divider()
    st.markdown("Esta é a página inicial da plataforma. Use os botões acima para navegar.")

