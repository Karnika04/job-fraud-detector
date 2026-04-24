## Online Job Fraud Detection Platform

**Online Job Fraud Detection Platform** is a production-ready end-to-end system for detecting whether a job posting is **real** or **fraudulent** using machine learning, NLP, explainable AI (SHAP), and rule-based heuristics.

### Tech Stack

- **Language**: Python 3.11
- **Backend**: FastAPI + Uvicorn
- **ML / NLP**: pandas, numpy, scikit-learn, nltk, spaCy, imbalanced-learn, xgboost, shap
- **Database**: PostgreSQL + SQLAlchemy ORM
- **Frontend**: React.js (Vite) + Axios
- **Scraping**: requests + BeautifulSoup
- **Environment**: python-dotenv
- **Deployment**: Docker, Docker Compose

### Repository Structure

- **backend/**
  - `main.py` – FastAPI app and endpoints
  - `model_loader.py` – Load trained model and vectorizer
  - `predictor.py` – End-to-end prediction logic
  - `preprocessing.py` – Text cleaning utilities
  - `fraud_rules.py` – Rule-based fraud scoring
  - `explainability.py` – SHAP-based explanation utilities
  - `database.py` – SQLAlchemy models and session
  - `schemas.py` – Pydantic schemas
  - `config.py` – Settings and environment variables
- **ml_pipeline/**
  - `train_model.py` – Orchestrates full training pipeline
  - `preprocessing.py` – EMSCAD cleaning and full_text creation
  - `feature_engineering.py` – TF-IDF + metadata features
  - `model_training.py` – Train LR, RF, XGBoost + SMOTE
  - `evaluation.py` – Plot metric comparison
  - `save_model.py` – Save model, vectorizer, and metrics
- **scraper/**
  - `linkedin_scraper.py` – Example scraper that posts to `/predict`
  - `internshala_scraper.py` – Example scraper that posts to `/predict`
- **frontend/**
  - React app with pages: Home, Job Checker, History
- **data/**
  - `raw_dataset.csv` – Placeholder EMSCAD CSV (replace with full dataset)
  - `processed_dataset.csv` – Example processed output
- **models/**
  - `job_fraud_model.pkl` – Placeholder model (overwritten after training)
  - `tfidf_vectorizer.pkl` – Placeholder vectorizer (overwritten after training)
- **notebooks/**
  - `EDA_analysis.ipynb` – Basic EDA starter notebook
- `.env.example` – Example environment configuration
- `requirements.txt` – Backend / ML dependencies
- `Dockerfile` – Backend container image
- `docker-compose.yml` – Backend, frontend, and PostgreSQL services

### Environment Variables

Copy `.env.example` to `.env` and adjust as needed:

```bash
cp .env.example .env
```

Main variables:

- `DATABASE_URL=postgresql://user:password@localhost:5432/jobfraud`
- `MODEL_PATH=models/job_fraud_model.pkl`
- `VECTORIZER_PATH=models/tfidf_vectorizer.pkl`
- `FRONTEND_ORIGIN=http://localhost:3000`

### Installation

From the `job-fraud-detector` directory:

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

You may need to install spaCy and its English model:

```bash
python -m spacy download en_core_web_sm
```

### Dataset

The pipeline expects the **Employment Scam Aegean Dataset (EMSCAD)** CSV at:

- `data/raw_dataset.csv`

Required columns:

- `job_title`
- `location`
- `department`
- `salary_range`
- `company_profile`
- `description`
- `requirements`
- `benefits`
- `fraudulent` (0 = real, 1 = fraudulent)

Replace the placeholder `data/raw_dataset.csv` with the full dataset before training.

### Model Pipeline

1. **Preprocessing**
   - Remove HTML tags, lowercase text.
   - Remove punctuation, stopwords (NLTK).
   - Lemmatization (NLTK + spaCy).
   - Concatenate `description + requirements + company_profile + benefits` into `full_text`.
   - Save cleaned data to `data/processed_dataset.csv`.
2. **Feature Engineering**
   - TF-IDF on `full_text` with `max_features=5000`, `ngram_range=(1, 2)`.
   - Metadata features:
     - `description_length`
     - `has_company_profile`
     - `salary_present`
     - `has_logo`
   - Combine TF-IDF vectors and metadata.
3. **Imbalance Handling**
   - Use **SMOTE** to balance classes.
4. **Model Training**
   - Train:
     - Logistic Regression
     - Random Forest
     - XGBoost
   - Evaluate with:
     - Accuracy, Precision, Recall, F1, ROC-AUC
   - Select best model by **F1-score**.
5. **Saving**
   - Save model to `models/job_fraud_model.pkl`.
   - Save vectorizer to `models/tfidf_vectorizer.pkl`.

### Running the Training Pipeline

From the project root:

```bash
python ml_pipeline/train_model.py
```

This will:

- Preprocess EMSCAD into `data/processed_dataset.csv`.
- Train models with SMOTE and select the best by F1.
- Save `models/job_fraud_model.pkl` and `models/tfidf_vectorizer.pkl`.

### Backend (FastAPI) – Local

Ensure PostgreSQL is running and `DATABASE_URL` is configured (see `.env`).

Start the backend:

```bash
uvicorn backend.main:app --reload
```

Endpoints:

- `GET /health`
  - Response:

```json
{
  "status": "running"
}
```

- `POST /predict`
  - Request JSON:

```json
{
  "title": "",
  "description": "",
  "company_profile": "",
  "requirements": ""
}
```

  - Response JSON:

```json
{
  "prediction": "Fraud or Real",
  "fraud_probability": 0.87,
  "rule_score": 4,
  "explanation": ["registration fee", "urgent hiring"]
}
```

- `GET /history`
  - Returns paginated list of past predictions stored in `jobs_checked`.

The backend:

- Cleans text and generates metadata features.
- Vectorizes text and runs the ML model.
- Runs the fraud rule engine.
- Generates SHAP-based explanations (top contributing features).
- Stores results in the `jobs_checked` table.

### Database

PostgreSQL connection is configured via `DATABASE_URL`.

- SQLAlchemy model: `jobs_checked` table with fields:
  - `id`
  - `title`
  - `description`
  - `prediction`
  - `fraud_probability`
  - `rule_score`
  - `created_at`
- Tables are created automatically on backend startup.

### Frontend (React)

From the `frontend` directory:

```bash
cd frontend
npm install
npm start
```

Pages:

- **Home** – Overview and quick links.
- **Job Checker** – Form to submit a job posting and view:
  - Fraud probability
  - Prediction (Fraud / Real)
  - Rule-based risk score
  - Top contributing SHAP features / suspicious phrases
- **History** – Table of previously analyzed jobs fetched from `/history`.

The frontend uses Axios (`src/services/api.js`) to call:

- `GET /health`
- `POST /predict`
- `GET /history`

### Web Scrapers

From the `scraper` directory:

- `linkedin_scraper.py`
- `internshala_scraper.py`

Each:

- Fetches example job postings from placeholder HTML pages.
- Extracts job title and description.
- Sends them to the backend `/predict` endpoint.

Run (after backend is up):

```bash
python scraper/linkedin_scraper.py
python scraper/internshala_scraper.py
```

You can adapt selectors and URLs to real sources (respecting terms of service).

### Docker Deployment

Build and run all services (Postgres, backend, frontend) with Docker Compose:

```bash
docker-compose up --build
```

Services:

- **db** – PostgreSQL
- **backend** – FastAPI app (port `8000`)
- **frontend** – React app (port `3000`)

The frontend talks to the backend via `VITE_BACKEND_URL=http://backend:8000`.

Access:

- Backend docs: `http://localhost:8000/docs`
- Frontend UI: `http://localhost:3000`

