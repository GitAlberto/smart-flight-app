# smart-flight-app

[![CI](https://github.com/GitAlberto/smart-flight-app/actions/workflows/ci.yml/badge.svg)](https://github.com/GitAlberto/smart-flight-app/actions/workflows/ci.yml)

Application web de prédiction du prix d'un billet d'avion, construite avec **Streamlit**.  
Elle consomme l'API de prédiction IA développée en Bloc 2 (`smart-flight-pricer`) et affiche le prix estimé en INR avec conversion automatique en euros via un taux de change en temps réel.

---

## Lien avec le Bloc 2

Ce projet est le **client applicatif** du service IA `smart-flight-pricer` (Bloc 2).  
Il ne contient aucun modèle ML — toute la prédiction est déléguée à l'endpoint `POST /predict` de l'API FastAPI du Bloc 2.

```
[Utilisateur — navigateur]
        ↓ formulaire Streamlit
[smart-flight-app — port 8501]
        ↓ POST /predict + X-API-Key
[smart-flight-pricer — port 8000]
        ↓ prix en INR
[frankfurter.app — taux de change]
        ↓ conversion INR → EUR
[Affichage : "7 838 INR — soit ~86 €"]
```

---

## Installation

```bash
git clone https://github.com/GitAlberto/smart-flight-app.git
cd smart-flight-app
python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt
```

---

## Configuration

Créer un fichier `.env` à la racine du projet :

```
API_URL=http://127.0.0.1:8000
API_KEY=votre_cle_api_bloc2
LOG_DIR=monitoring/logs
```

---

## Lancer l'application

L'API Bloc 2 doit tourner avant de lancer l'application.

**Terminal 1 — API Bloc 2 :**
```bash
cd ../smart-flight-pricer
.venv\Scripts\uvicorn api.main:app --reload
```

**Terminal 2 — Application :**
```bash
.venv\Scripts\streamlit run app/main.py
```

L'interface est accessible sur [http://localhost:8501](http://localhost:8501).

---

## Lancer les tests

```bash
.venv\Scripts\pytest tests/ --cov=app --cov-report=term -v
```

Résultat attendu : **8 tests passent**, couverture 100% sur `api_client.py` et `currency.py`.

---

## Structure du projet

```
smart-flight-app/
├── .github/workflows/ci.yml     # Pipeline CI/CD GitHub Actions
├── app/
│   ├── main.py                  # Interface Streamlit
│   ├── api_client.py            # Client HTTP → API Bloc 2
│   └── currency.py              # Conversion INR → EUR
├── monitoring/
│   └── logger.py                # Journalisation JSONL
├── tests/
│   ├── conftest.py
│   ├── test_api_client.py
│   └── test_currency.py
├── docs/
│   ├── specs_fonctionnelles.md  # C14
│   ├── specs_techniques.md      # C15
│   ├── agile.md                 # C16
│   ├── monitoring.md            # C20
│   └── incident.md              # C21
├── .env                         # Non versionné
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Compétences couvertes — Bloc 3 (C14 → C21)

| Compétence | Description | Livrable |
|------------|-------------|----------|
| C14 | Spécifications fonctionnelles, user stories, parcours utilisateur | `docs/specs_fonctionnelles.md` |
| C15 | Architecture technique, stack, DFD, preuve de concept | `docs/specs_techniques.md` |
| C16 | Méthode agile — backlog, kanban, rituels documentés | `docs/agile.md` |
| C17 | Développement Streamlit, intégration API, gestion erreurs, tests | `app/`, `tests/` |
| C18 | CI/CD — GitHub Actions, tests automatiques sur push | `.github/workflows/ci.yml` |
| C19 | Livraison continue — packaging, pipeline documenté | `.github/workflows/ci.yml` |
| C20 | Monitoring applicatif — logs, métriques, alertes | `monitoring/`, `docs/monitoring.md` |
| C21 | Résolution d'incident — identification, correction, documentation | `docs/incident.md` |
