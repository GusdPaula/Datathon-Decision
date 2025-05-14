from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd
from sentence_transformers import SentenceTransformer
from sentence_transformers import util as util_trans
import json
import numpy as np
import pandas as pd
import tqdm as notebook_tqdm
import joblib
import torch

from pathlib import Path

# Load applicants database once
with open("applicants.json", "r", encoding="utf-8") as f:
    applicants_dict = json.load(f)

# Load Sentence Transformer model (Portuguese-compatible)
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
credentials = service_account.Credentials.from_service_account_file(r'C:\Users\vc\Documents\fiap\Datathon-Decision\tech-chlg-5c139f98b4ec.json')

project_id = 'tech-chlg'
client = bigquery.Client(credentials= credentials,project=project_id)

query_text = """
   SELECT *
   FROM app_embs.app_embs
   LIMIT 1000 """

df = client.query_and_wait(query_text).to_dataframe()
df = torch.from_numpy(df.values)
df = df.float()

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

# Function to extract job description text from uploaded file
def extract_job_text(job_json: dict) -> str:
    job_text = (
        job_json.get("informacoes_basicas", {}).get("descricao", "") + " " +
        job_json.get("perfil_vaga", {}).get("atividades", "") + " " +
        " ".join(job_json.get("perfil_vaga", {}).get("competencias_tecnicas", []))
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
def recommend_cvs_for_job(job_file_path: str, top_k: int = 5):
    # Load uploaded job file
    with open(job_file_path, "r", encoding="utf-8") as f:
        job_json = json.load(f)

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
        print(f"Candidate ID: {app_id} | Similarity: {similarities[idx]:.4f}")
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

        print(f"👤 Nome: {name} (ID: {app_id})")
        print(f"📍 Localização: {location}")
        print(f"💼 Título profissional: {title}")
        print(f"🎓 Formação: {academic}")
        print(f"🌍 Inglês: {english}")
        print("📄 CV (trecho):")
        print(cv[:500] + "..." if len(cv) > 500 else cv)
        print("--------------------------------------------------\n")

# Example usage
recommend_cvs_for_job(r"C:\Users\vc\Documents\fiap\Datathon-Decision\uploaded_job.json")  # replace with your actual uploaded file path
