# pages/4_Listar_Vagas.py
import streamlit as st
from utils import hide_streamlit_sidebar_css, listar_vagas_todas, registrar_candidatura, buscar_vaga_por_id

st.set_page_config(page_title="Vagas Disponíveis - Decision", layout="wide", initial_sidebar_state="collapsed")
hide_streamlit_sidebar_css()

if not st.session_state.get("logged_in", False):
    st.error("Acesso negado. Você precisa estar logado para ver as vagas.")
    if st.button("Ir para Home"):
        st.switch_page("1_Home.py")
    st.stop()

st.title("Vagas Disponíveis")
st.caption(f"Logado como: {st.session_state.user_name} ({st.session_state.user_type.capitalize()})")

# --- Filtros (Simples) ---
vagas_disponiveis = listar_vagas_todas()

# Inicializa o contador de vagas a mostrar
if "vagas_visiveis" not in st.session_state:
    st.session_state.vagas_visiveis = 10  # Começa com 10

if not vagas_disponiveis:
    st.info("Nenhuma vaga encontrada com os filtros aplicados.")
else:
    st.write(f"Exibindo {st.session_state.vagas_visiveis} de {len(vagas_disponiveis)} vagas.")
    st.divider()



# Lista de todas as vagas (transforma o dict em lista de tuplas para preservar o ID)
vagas_lista = list(vagas_disponiveis.items())

# Renderiza somente as vagas visíveis até agora
for vaga_id, vaga in vagas_lista[:st.session_state.vagas_visiveis]:
    info = vaga["informacoes_basicas"]
    perfil = vaga["perfil_vaga"]

    with st.container(border=True):
        cols_vaga = st.columns([0.7, 0.3])
        with cols_vaga[0]:
            st.subheader(info.get("titulo_vaga", "Título não informado"))
            st.caption(f"{info.get('cliente', 'Empresa não informada')} - {perfil.get('cidade', '')}, {perfil.get('estado', '')}")
            st.write(f"**Tipo de Contrato:** {info.get('tipo_contratacao', 'Não informado')}")
            
            if perfil.get("demais_observacoes"):
                st.write(f"**Salário / Observações:** {perfil['demais_observacoes']}")

            with st.expander("Ver mais detalhes e requisitos"):
                st.markdown("**Descrição:**")
                st.write(perfil.get("principais_atividades", "Não informado"))

                st.markdown("**Requisitos:**")
                requisitos = perfil.get("competencia_tecnicas_e_comportamentais", "Não informado")
                st.write(requisitos.replace(",", ", "))  # Melhor formatação

        with cols_vaga[1]:
            if st.session_state.user_type == "candidato":
                from utils import CANDIDATURAS_DB

                ja_candidatou_real = any(
                    c["id_vaga"] == vaga_id and c["username_candidato"] == st.session_state.username
                    for c in CANDIDATURAS_DB
                )

                if ja_candidatou_real:
                    st.success("Você já se candidatou!")
                elif st.button("Candidatar-se", key=f"apply_{vaga_id}", use_container_width=True):
                    success, message = registrar_candidatura(vaga_id, st.session_state.username)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)

            elif st.session_state.user_type == "admin":
                st.button("Editar Vaga (Admin)", key=f"edit_{vaga_id}", disabled=True, use_container_width=True)
                st.button("Excluir Vaga (Admin)", key=f"delete_{vaga_id}", disabled=True, use_container_width=True)

# Botão para mostrar mais 10 vagas, se houver mais
if st.session_state.vagas_visiveis < len(vagas_lista):
    if st.button("Mostrar mais vagas"):
        st.session_state.vagas_visiveis += 10
        st.rerun()



st.divider()
# Corrigido para usar st.switch_page diretamente
if st.button("Voltar para Home", key="home_listar_vagas", use_container_width=True):
    st.switch_page("1_Home.py")

