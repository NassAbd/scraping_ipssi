## 📰 Scraper Doctolib

Ce projet permet de naviguer sur Doctolib et récupérer les informations de praticien (créneau, adresse...) puis les enregistrer en csv.

### 📁 Structure

* **Backend** : Python + Selenium + FastAPI
* **Frontend** : React + Vite

---

### 🚀 Démarrage rapide

#### 1. Backend

```bash
cd backend
pip install -r requirements.txt
cd ..
uvicorn backend.main:app --reload
```

* L'API sera dispo sur : `http://127.0.0.1:8000`

#### 2. Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

* L'interface sera dispo sur : `http://localhost:5173`