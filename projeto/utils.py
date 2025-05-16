# utils.py
# Importing libs/ importando libs
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import warnings
import pickle
import streamlit as st
import hashlib
import fitz
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
import os
from datetime import datetime
from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd
from sentence_transformers import SentenceTransformer
from sentence_transformers import util as util_trans
import json
import numpy as np
import joblib
import torch
import requests
import zipfile
import io
warnings.simplefilter("ignore")

from pathlib import Path

# Load applicants database once
'''with open("applicants.json", "r", encoding="utf-8") as f:
    applicants_dict = json.load(f)
'''
# Load Sentence Transformer model (Portuguese-compatible)
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["GCP_SERVICE_ACCOUNT"]
)



project_id = 'tech-chlg'
client = bigquery.Client(credentials= credentials,project=project_id)

query_text = """
   SELECT *
   FROM app_embs.app_embs
   LIMIT 1000 """

df = client.query_and_wait(query_text).to_dataframe()
df = torch.from_numpy(df.values)
df = df.float()

# Function to extract job description text from uploaded file
def extract_job_text(job_json: dict) -> str:
    job_text = (
        job_json.get("perfil_vaga", {}).get("principais_atividades", "") + " " +
        " ".join(job_json.get("perfil_vaga", {}).get("competencia_tecnicas_e_comportamentais", []))
    )

    job_text = job_text.strip()

    job_text = preprocess(job_text)

    return job_text

# Function to get cleaned applicant CVs
def extract_applicant_skills(applicant):

    texts = []
    ids = []
    for app_id, data in applicants.items():
        cv = data.get("cv_pt", "").strip()
        skills = data["informacoes_profissionais"].get("conhecimentos_tecnicos", "")
        info_app = skills + " " + cv.lower()
        info_app = preprocess(info_app)
        if cv:
            ids.append(app_id)
            texts.append(info_app)

    return ids, texts


# Main recommendation function
def recommend_cvs_for_job(job_json: str, top_k: int = 5):
   
    job_text = extract_job_text(job_json)
    job_embedding = model.encode(job_text, convert_to_tensor=True)
    applicant_ids = joblib.load("app_ids.pkl")
    applicant_embeddings = df
    
    print(applicant_embeddings.dtype, job_embedding.dtype)
    # Compute similarities
    similarities = util_trans.cos_sim(job_embedding, applicant_embeddings)[0]
    top_results = np.argsort(-similarities)[:top_k]

    # Show top candidates
    print(f"\nTop {top_k} candidate recommendations for uploaded job:\n")
    for idx in top_results:
        app_id = applicant_ids[idx]
        st.write(f"Candidate ID: {app_id} | Similarity: {similarities[idx]:.4f}")
        applicant = applicants_dict.get(app_id)

        if not applicant:
            print(f"⚠️ Applicant ID {app_id} not found.")
            return

        basic = applicant.get("infos_basicas", {})
        personal = applicant.get("informacoes_pessoais", {})
        prof = applicant.get("informacoes_profissionais", {})
        education = applicant.get("formacao_e_idiomas", {})

        name = basic.get("nome") or personal.get("nome", "Nome não disponível")
        location = basic.get("local", "Local não informado")
        title = prof.get("titulo_profissional", "Título profissional não informado")
        academic = education.get("nivel_academico", "Nível acadêmico não informado")
        english = education.get("nivel_ingles", "Inglês não informado")
        cv = applicant.get("cv_pt", "")

        st.write(f"👤 Nome: {name} (ID: {app_id})")
        st.write(f"📍 Localização: {location}")
        st.write(f"💼 Título profissional: {title}")
        st.write(f"🎓 Formação: {academic}")
        st.write(f"🌍 Inglês: {english}")
        st.write("📄 CV (trecho):")
        st.write(cv[:500] + "..." if len(cv) > 500 else cv)

        if st.button("Ver mais informações", key=f"ver_{app_id}"):
            st.session_state.candidato_selecionado = app_id
            st.switch_page("pages/2_Detalhes_Candidato.py")
        
        st.write("--------------------------------------------------\n")



# Reading the jobs data/ lendo os dados de vagas
with open("vagas.pkl", "rb") as f:
    jobs = pickle.load(f)

# Loading models/ Carregando os modelos
logreg = joblib.load("logistic_model.pkl")
xgb = joblib.load("xgboost_model.pkl")
embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Getting the jobs embeddings' data/ Obtendo os embeddings dos dados de vagas
job_data = joblib.load("job_data.pkl")
job_ids = job_data["job_ids"]
job_titles = job_data["job_titles"]
job_embeddings = job_data["job_embeddings"]

# Function that will process the CV text/ Função que processará o texto do CV.
def preprocess(text):
    import re, string
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    stop_words = set(stopwords.words('portuguese'))
    
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text, language="portuguese")
    tokens = [word for word in tokens if word not in stop_words and len(word) > 2]
    return ' '.join(tokens)

# This function will use the loaded models and embeddings to calculate similarity and predict the probability to be hired from one uploaded CV.
# Esta função usará os modelos carregados e embeddings para calcular a similaridade e predizer a probabilidade de ser contratado com o text de um CV.
def predict_jobs_for_cv(cv_text, top_n=5):

    # Precessing and cleaning CV text/ Preccessando e limpando texto do CV
    cleaned_cv = preprocess(cv_text)

    # Calculate the CV text embedding/ calculando o embedding do texto do cv
    cv_vec = embedding_model.encode([cleaned_cv])
    
    # Calculating the similirarity between jobs and cv vectors
    # Calculando similiridade entre vetores de vagas e do cv
    sims = cosine_similarity(cv_vec, job_embeddings).flatten()


    # Looping through the jobs, calculating the hire probability and getting job's data
    # Iterando pelas vagas, calculando a probilidade de ser contratado e obtendo informações das vagas

    results = []
    for i, sim in enumerate(sims):
        # Predicting the hire probability/ Predizendo a probabilidade de ser contratado
        logreg_prob = logreg.predict_proba([[sim]])[0][1]
        xgb_prob = xgb.predict_proba([[sim]])[0][1]
        ensemble_prob = (logreg_prob + xgb_prob) / 2

        # Getting the jobs' data/ Obtendo dados das vagas
        job = jobs.get(job_ids[i], {})
        title = job.get("informacoes_basicas", {}).get("titulo_vaga", "N/A")
        area = job.get("perfil_vaga", {}).get("areas_atuacao", "N/A")
        skills = job.get("perfil_vaga", {}).get("competencia_tecnicas_e_comportamentais", "")
        activities = job.get("perfil_vaga", {}).get("principais_atividades", "")

        results.append({
            "job_id": job_ids[i],
            "title": title,
            "area": area,
            "skills": skills,
            "activities": activities,
            "similarity": sim,
            "hire_prob": ensemble_prob
        })

    # Sort and display/ Ordenar e mostrar
    with st.container(border=True):

        top_jobs = sorted(results, key=lambda x: x["hire_prob"], reverse=True)[:top_n]

        for idx, job in enumerate(top_jobs, 1):

            st.write(f"\n🔹 Recomendação #{idx}")
            if st.session_state.user_type == "candidato":
                from utils import CANDIDATURAS_DB

                ja_candidatou_real = any(
                    c["id_vaga"] == job['job_id'] and c["username_candidato"] == st.session_state.username
                    for c in CANDIDATURAS_DB
                )

                if ja_candidatou_real:
                    st.success("Você já se candidatou!")
                elif st.button("Candidatar-se", key=f"apply_{job['job_id']}", use_container_width=True):
                    success, message = registrar_candidatura(job['job_id'], st.session_state.username)
                    if success:
                        st.switch_page("pages/5_Minhas_Candidaturas.py")
                        st.success(message)
                        st.rerun()
                        
                    else:
                        st.error(message)
            st.write(f"🏢 Título da vaga       : {job['title']}")
            st.write(f"📍 Área            : {preprocess(job['area'])}")
            st.write(f"📈 Similarity Score: {job['similarity']:.2f}")
            st.write(f"🤖 Hire Probability: {job['hire_prob']:.2%}")
            st.write(f"🔧 Skills Required : {preprocess(job['skills'][:200])}...")
            st.write(f"📋 Activities      : {preprocess(job['activities'][:200])}...")
            st.write("-" * 80)

# --- Funções de Autenticação e Usuário ---
USUARIOS_DB = {
    "admin": {
        "senha_hash": hashlib.sha256("admin123".encode()).hexdigest(),
        "tipo": "admin",
        "nome": "Administrador",
        "curriculo": None
    },
    "candidato1": {
        "senha_hash": hashlib.sha256("candidato123".encode()).hexdigest(),
        "tipo": "candidato",
        "nome": "João Silva",
        "curriculo": None # Adicionar campo para currículo
    },
    "candidato2": {
        "senha_hash": hashlib.sha256("senha456".encode()).hexdigest(),
        "tipo": "candidato",
        "nome": "Maria Souza",
        "curriculo": None # Adicionar campo para currículo
    }
}

# Diretório para salvar currículos (simulação)
CURRICULOS_DIR = "curriculos_uploaded"
if not os.path.exists(CURRICULOS_DIR):
    os.makedirs(CURRICULOS_DIR)

VAGAS_DB = jobs

CANDIDATURAS_DB = [] # Lista de dicionários: {"id_candidatura", "id_vaga", "username_candidato", "status", "data_candidatura"}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password, hashed_password):
    return hash_password(plain_password) == hashed_password

def check_login(username, password):
    if username in USUARIOS_DB and verify_password(password, USUARIOS_DB[username]["senha_hash"]):
        return True, USUARIOS_DB[username]["tipo"], USUARIOS_DB[username]["nome"]
    return False, None, None


# Function that will convert PDF into TXT/ Função que converterá PDF em TXT
def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


def register_candidate(nome_completo, username, password, uploaded_file):
    if username in USUARIOS_DB:
        return False, "Nome de usuário já existe."
    
    curriculo_filename = None
    if uploaded_file is not None:
        # Salvar o arquivo (simulação)
        # Em um app real, você faria upload para um storage seguro (S3, GCS, etc.)
        # e salvaria o caminho/ID no banco de dados.
        curriculo_filename = os.path.join(CURRICULOS_DIR, f"{username}_{uploaded_file.name}")
        try:
            with open(curriculo_filename, "wb") as f:
                f.write(uploaded_file.getbuffer())
        except Exception as e:
            return False, f"Erro ao salvar currículo: {e}"
        
        # Converting CV text/ convertendo texto do cv
        cv_text = extract_text_from_pdf(curriculo_filename)

    USUARIOS_DB[username] = {
        "senha_hash": hash_password(password),
        "tipo": "candidato",
        "nome": nome_completo,
        "curriculo": cv_text # Salva o caminho do arquivo ou None
    }
    return True, "Cadastro realizado com sucesso! Faça login para continuar."


# --- Funções de Estilo e UI ---
def hide_streamlit_sidebar_css():
    ...

def load_css(file_name="style.css"):
    try:
        with open(file_name, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Arquivo CSS \'{file_name}\' não encontrado.")

# --- Funções de Vagas (Simulação) ---
def criar_vaga(titulo, empresa, local, descricao, requisitos, tipo_contrato, salario):
    id_vaga =  len(VAGAS_DB) + 1
    nova_vaga = {
        "informacoes_basicas": {
            "data_requicisao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "limite_esperado_para_contratacao": None,
            "titulo_vaga": titulo,
            "vaga_sap": None,
            "cliente": empresa,
            "solicitante_cliente": None,
            "empresa_divisao": "Decision São Paulo",
            "requisitante": None,
            "analista_responsavel": None,
            "tipo_contratacao": tipo_contrato,
            "prazo_contratacao": None,
            "data_inicial": None,
            "data_final": None,
            "objetivo_vaga": "Contratação",
            "prioridade_vaga": None,
            "origem_vaga": None,
            "superior_imediato": None
        },
        "perfil_vaga": {
            "pais": None,
            "estado": None,
            "cidade": None,
            "bairro": "",
            "regiao": "",
            "local_trabalho": local,
            "vaga_especifica_para_pcd": None,
            "faixa_etaria": salario,
            "horario_trabalho": None,
            "nivel profissional": None,
            "nivel_academico": None,
            "nivel_ingles": None,
            "nivel_espanhol": None,
            "outro_idioma": None,
            "areas_atuacao": None,
            "principais_atividades": descricao,
            "competencia_tecnicas_e_comportamentais": requisitos,
            "demais_observacoes": None,
            "viagens_requeridas": None,
            "equipamentos_necessarios": None
        },
        "beneficios": {
            "valor_venda": None,
            "valor_compra_1": None,
            "valor_compra_2": None
        }
    }
    VAGAS_DB[id_vaga] = nova_vaga
    return id_vaga

def listar_vagas_todas():
    return VAGAS_DB

def buscar_vaga_por_id(id_vaga):
    for vaga_id, vaga in VAGAS_DB.items():
        
        if vaga_id == id_vaga:
            return vaga
    return None

# --- Funções de Candidaturas (Simulação) ---
def registrar_candidatura(id_vaga, username_candidato):
    
    if any(c["id_vaga"] == id_vaga and c["username_candidato"] == username_candidato for c in CANDIDATURAS_DB):
        return False, "Você já se candidatou para esta vaga."
    
    nova_candidatura = {
        "id_candidatura": f"cand{len(CANDIDATURAS_DB) + 1}",
        "id_vaga": id_vaga,
        "username_candidato": username_candidato,
        "status": "Em Análise",
        "data_candidatura": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    CANDIDATURAS_DB.append(nova_candidatura)
    return True, "Candidatura registrada com sucesso!"

def listar_candidaturas_por_usuario(username_candidato):
    return [c for c in CANDIDATURAS_DB if c["username_candidato"] == username_candidato]

def get_vaga_titulo(id_vaga):
    vaga = buscar_vaga_por_id(id_vaga)
    info = vaga["informacoes_basicas"]

    return info.get("titulo_vaga", "Título não informado")


