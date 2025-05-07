# 📰 Scraper d'Entreprises – Scrapy + MongoDB

Ce projet utilise **Scrapy**, un framework de scraping web, pour extraire des données publiques d'entreprises depuis plusieurs sources (Consult, eJustice, KBO). Les données sont ensuite enregistrées dans une base de données **MongoDB** pour une gestion centralisée.

## 📁 Structure

- **Spiders** : Scrapy
- **Database** : MongoDB

## 🚀 Démarrage rapide

### 1. Installation des dépendances

Avant de pouvoir lancer les spiders, vous devez installer les bibliothèques nécessaires :

```bash
pip install -r requirements.txt
```

#### 2. Lancer les spiders

```bash
cd tp_scrapy
python run_all_scrapers.py
```

---

### 📝 Attention

* MongoDB doit être lancé localement (`mongodb://localhost:27017`)