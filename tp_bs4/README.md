## 📰 Scraper d'Articles – React + FastAPI

Ce projet permet de scraper des pages d'articles (du site https://www.blogdumoderateur.com/) depuis leur URL, les enregistrer dans MongoDB, puis les rechercher ou afficher depuis une interface React.

### 📁 Structure

* **Backend** : FastAPI
* **Frontend** : React + Vite
* **Database** : MongoDB

---

### 🚀 Démarrage rapide

#### 1. Backend (FastAPI)

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

* L'API sera dispo sur : `http://127.0.0.1:8000`

#### 2. Frontend (React)

```bash
cd scraper_front
npm install
npm run dev
```

* L'interface sera dispo sur : `http://localhost:5173`

---

### 📝 Attention

* MongoDB doit être lancé localement (`mongodb://localhost:27017`)