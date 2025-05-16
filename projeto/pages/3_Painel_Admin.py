# pages/3_Painel_Admin.py
import streamlit as st
import pandas as pd # Para dados de exemplo dos gráficos
import numpy as np # Para dados de exemplo dos gráficos
from utils import hide_streamlit_sidebar_css

st.set_page_config(page_title="Painel Administrativo - Admin", layout="wide", initial_sidebar_state="collapsed")
hide_streamlit_sidebar_css()

if not st.session_state.get("logged_in", False) or st.session_state.get("user_type") != "admin":
    st.error("Acesso negado. Você precisa estar logado como administrador para acessar esta página.")
    if st.button("Ir para Home"):
        st.switch_page("1_Home.py")
    st.stop()

st.title("Painel Administrativo")
st.caption(f"Logado como: {st.session_state.user_name} (Admin)")
st.write("Bem-vindo ao painel de controle. Aqui você pode visualizar estatísticas e informações importantes sobre a plataforma.")

st.divider()

st.subheader("Estatísticas de Vagas (Exemplo)")

# Dados de exemplo para gráficos
chart_data_vagas_status = pd.DataFrame(
    {
        "Status": ["Abertas", "Preenchidas", "Em Pausa"],
        "Quantidade": [np.random.randint(10, 50), np.random.randint(5, 30), np.random.randint(1, 10)]
    }
)
chart_data_vagas_status = chart_data_vagas_status.set_index("Status")

chart_data_candidaturas_dia = pd.DataFrame(
    np.random.randn(10, 2), # 10 dias, 2 séries
    columns=["Novas Candidaturas", "Candidaturas Aprovadas"],
    index=pd.to_datetime([f"2024-05-{i+1:02d}" for i in range(10)])
)
# Garantir que os valores sejam positivos para contagem
chart_data_candidaturas_dia = chart_data_candidaturas_dia.abs() * 10
chart_data_candidaturas_dia = chart_data_candidaturas_dia.astype(int)


col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("**Vagas por Status**")
    st.bar_chart(chart_data_vagas_status)
    st.caption("Este gráfico mostra a distribuição de vagas por status atual.")

with col_chart2:
    st.markdown("**Novas Candidaturas por Dia (Últimos 10 dias)**")
    st.line_chart(chart_data_candidaturas_dia)
    st.caption("Este gráfico mostra o volume de novas candidaturas e aprovações nos últimos 10 dias.")

st.divider()

st.subheader("Outras Métricas (Exemplo)")
metric_cols = st.columns(3)
with metric_cols[0]:
    st.metric(label="Total de Usuários Ativos", value=f"{np.random.randint(100, 500)}", delta=f"{np.random.randint(1, 20)} novos esta semana")
with metric_cols[1]:
    st.metric(label="Total de Vagas Publicadas", value=f"{np.random.randint(50, 150)}", delta=f"{np.random.randint(1, 10)} novas esta semana")
with metric_cols[2]:
    st.metric(label="Taxa de Conversão Média", value=f"{np.random.randint(5, 25)}%", delta=f"{np.random.uniform(-2,2):.1f}% vs mês passado", delta_color="inverse")

st.divider()

st.subheader("Navegação Rápida")
col_nav1, col_nav2 = st.columns(2)
with col_nav1:
    if st.button("Voltar para Home (Admin)", key="home_admin_painel", use_container_width=True):
        st.switch_page("1_Home.py") # Corrigido para usar st.switch_page
with col_nav2:
    if st.button("Criar Nova Vaga", key="criar_vaga_painel", use_container_width=True):
        st.switch_page("pages/2_Criar_Vaga.py")

st.markdown("--- ")
st.markdown("*Observação: Todos os dados e gráficos apresentados nesta página são apenas para fins de demonstração.*")

