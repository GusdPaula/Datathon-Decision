
# Aplicação de Inteligência Artificial em Recrutamento e Seleção

## 🎯 Objetivo do Projeto  
Desenvolver um sistema inteligente para otimizar o processo de recrutamento e seleção, utilizando técnicas avançadas de Inteligência Artificial para:

- **Triagem automatizada de currículos:** automatizar a análise inicial, identificando candidatos que atendam aos critérios técnicos e comportamentais da vaga.
- **Análise de aderência ao perfil:** mensurar a compatibilidade do candidato com a cultura e perfil organizacional, utilizando análise semântica e de comportamento.
- **Previsão de desempenho futuro:** estimar a probabilidade de sucesso do candidato no cargo com base em dados históricos e perfis similares.

## 🧠 Técnicas de IA Aplicadas

### 1. Processamento de Linguagem Natural (PLN)  
- **Extração de entidades e informações:** Utilização de bibliotecas como NLTK para identificar informações chave nos currículos, como experiência, formação, competências e certificações.  
- **Vetorização de texto:** Aplicação de TF-IDF e Word Embeddings (paraphrase-multilingual-MiniLM-L12-v2) para transformar textos em vetores numéricos para análise comparativa.
- **Análise semântica e similaridade:** Comparação entre perfil do candidato e descrição da vaga usando métricas de similaridade (cosine similarity).

### 2. Modelos Preditivos  
- **Regressão Logística:** Modelo inicial para classificar candidatos entre adequados ou não, interpretável e eficiente para pequenas e médias bases.  
- **XGBoost:** Modelo de boosting que combina múltiplas árvores de decisão para aumentar a acurácia da previsão de sucesso do candidato, lidando bem com dados desbalanceados e complexos.  
- **Ensemble:** Uso de técnicas como Grid Search para otimização dos hiperparâmetros dos modelos.

## 🛠️ Tecnologias Utilizadas

- **Python:** Principal linguagem para desenvolvimento, suporte a bibliotecas de ciência de dados e IA.  
- **Pandas e NumPy:** Manipulação eficiente de datasets, limpeza e transformação dos dados.  
- **Scikit-learn:** Construção e avaliação de modelos tradicionais de machine learning.  
- **XGBoost:** Implementação do modelo de boosting para classificação avançada.  
- **NLTK:** Processamento de linguagem natural para análise textual.  
- **Streamlit:** Construção de dashboards e interfaces web interativas para upload de currículos, visualização de análises e feedbacks.
- **sentence_transformers:** Biblioteca utilizada para obter o modelo de embeddings paraphrase-multilingual-MiniLM-L12-v2.

## 📂 Arquitetura do Projeto

- **Coleta e Pré-processamento dos Dados:**  
  - Importação e limpeza dos dados brutos dos currículos.  
  - Extração de features textuais e categóricas.  
  - Balanceamento da base com técnicas como SMOTE para mitigar viés.

- **Desenvolvimento dos Modelos:**  
  - Treinamento e validação dos modelos de regressão logística e XGBoost.  
  - Análise de importância das variáveis para explicar as decisões do modelo.

- **Interface e Visualização:**  
  - Plataforma web para upload dos currículos em PDF.  
  - Exibição dos resultados com scores de compatibilidade e recomendações.
  - Dashboard intuitivo para administrador gerenciar vagas e candidatos.

- **Pipeline Automatizado:**  
  - Processo contínuo que integra entrada de dados, processamento, predição e saída dos resultados para rápida resposta.

## 📊 Funcionalidades da aplicação

- **Upload de Currículos:** Suporte para PDF, com parser inteligente para extração das informações relevantes automaticamente.  
- **Análise detalhada do candidato:** Compatibilidade técnica, comportamental e cultural com a vaga desejada.  
- **Previsão de Desempenho:** Score preditivo baseado no histórico de candidatos similares e resultados anteriores da empresa.   
- **Monitoramento e Logs:** Registro das análises para auditoria e melhoria contínua dos modelos.

## ⚠️ Estrutura do Repositório
O repositório contém diversos arquivos e diretórios que indicam um fluxo completo de desenvolvimento de modelos de machine learning:

### 1. Notebooks Jupyter (.ipynb):

datathon.ipynb, model.ipynb, final.ipynb: Incluem análise exploratória de dados, desenvolvimento e avaliação de modelos.

cv_reco.ipynb: Relacionado a recomendações de currículos (CVs).

Scripts Python (.py):

cv_recomendation.py: Funções para recomendação de currículos.

### 2. Arquivos de Dados:

applicants.json, vagas.json, uploaded_job.json: Arquivos JSON que contem dados de candidatos e vagas de emprego.

app_ids.pkl, job_data.pkl, vagas.pkl: Arquivos serializados com dados processados ou identificadores.

### 3. Modelos Treinados:

logistic_model.pkl, xgboost_model.pkl: Modelos de machine learning treinados, utilizando regressão logística e XGBoost.

### 4. Dependências:

requirements.txt: Lista de bibliotecas Python necessárias para executar o projeto.

### 5. Streamlit Script:

Dentro da pasta projeto é possível encontrar os scripts que estão sendo utilizados no server do streamlit e são responsáveis pelo funcionamento da aplicação.

- **Sub-estrutura:** 
  - 1_Home.py (Responsável pelo acionamente das demais páginas e da página central)
  - requirements.txt (lista de libs utilizadas)
  - utils.py (funções e base de dados fictícias para o funcionamento da aplicação)
  - pages (pasta de sub-páginas)
    - 1_Candidatos.py (lista os candidatos para o adm)
    - 2_Criar_Vaga.py (abre um form para criação de vagas para o adm)
    - 2_Detalhes_Candidato.py (mostra as informações detalhadas para cada candidato para o adm)
    - 2_Recomendacao_CVS.py (recomenda cvs após a criação de uma vaga pelo adm)
    - 3_Painel_Admin.py (mostra um dashboard a ser integrado com os dados para o adm)
    - 4_Listar_Vagas.py (lista todas as vagas para o candidato ou adm)
    - 5_Minhas_Candidaturas.py (mostra todas as aplicações em vagas feitas pelo candidato)
    - 5_Sobre.py (breve explicação do site)
    - 6_Recomendacao_Vagas.py (recomenda vagas com base no cv para o candidato)

## ⚠️ Desafios e Considerações Éticas

- **Viés Algorítmico:**  
  - Análise e mitigação de vieses provenientes de dados históricos, evitando discriminação por gênero, idade, raça ou outras características irrelevantes.  
  - Uso de fairness metrics para monitorar o impacto dos modelos.

- **Base de dados:**
 - Devido a grande quantidade dados e recursos limitados, a base de dados de aplicantes foi diminuída para este projeto piloto. Futuramente, será necessário otimizar a leitura e o armazenamento dos dados.

- **Dashboard:** 
 - O Dashboard da página Painel Admin não foi conectado ao banco de dados para que os gráficos refletissem a realidade, por falta de tempo ao decorrer do projeto.

- **Demais otimizações:** 
  - Seria necessário fazer o modelo de sugestão de vagas rodar apenas uma vez ao se candidatar.
  - Mostrar apenas as páginas disponíveis de acordo com a função do usuário na sidebar.
  - Validação de dados ao cadastrar novos usuários.



