# Spécifications techniques — smart-flight-app

## Architecture n-tiers

L'application suit une architecture 3 couches :

| Couche | Rôle | Technologie |
|--------|------|-------------|
| Présentation | Interface utilisateur web | Streamlit (Python) |
| Service IA | Prédiction de prix via modèle ML | FastAPI + RandomForest (Bloc 2) |
| Données externes | Taux de change en temps réel | frankfurter.app (API REST publique) |

L'application Bloc 3 est un **client pur** : elle ne contient aucun modèle ML, aucune base de données. Toute la logique métier de prédiction est déléguée à l'API Bloc 2.

---

## Stack technique

| Couche | Technologie | Version | Justification |
|--------|-------------|---------|---------------|
| Interface | Streamlit | ≥ 1.30 | Framework Python natif, pas de CSS requis, déploiement simplifié |
| Client HTTP | requests | ≥ 2.31 | Bibliothèque standard Python, simple à mocker en tests |
| Conversion devise | frankfurter.app | API publique | Gratuit, sans clé API, taux de change en temps réel (BCE) |
| Tests | pytest + pytest-cov | ≥ 8.0 | Cohérence avec Bloc 2, couverture de code intégrée |
| CI/CD | GitHub Actions | — | Cohérence avec Bloc 2, gratuit pour dépôts publics |
| Logs | JSONL (fichier plat) | — | Léger, lisible par tout outil, cohérent avec Bloc 2 |
| Variables d'env | python-dotenv | ≥ 1.0 | Séparation config/code, standard Python |

---

## Diagramme de flux de données (DFD)

```
Utilisateur (navigateur)
        |
        | [saisie formulaire]
        v
+-------------------------+
|  smart-flight-app       |
|  Streamlit — port 8501  |
|  app/main.py            |
+-------------------------+
        |                          \
        | POST /predict             \ GET /latest?from=INR&to=EUR
        | header: X-API-Key          \
        v                            v
+-------------------------+    +--------------------+
|  smart-flight-pricer    |    |  frankfurter.app   |
|  FastAPI — port 8000    |    |  API taux de change|
|  api/main.py (Bloc 2)   |    +--------------------+
+-------------------------+          |
        |                            | taux INR/EUR
        | {"predicted_price": float} |
        v                            v
+--------------------------------------------------+
|  Affichage résultat                              |
|  "Prix estimé : 7 838 INR — soit ~86.42 €"       |
+--------------------------------------------------+
        |
        | log_request(inputs, result, latency_ms, error)
        v
+-------------------------+
|  monitoring/logs/       |
|  app.jsonl              |
+-------------------------+
```

---

## Variables d'environnement

Le fichier `.env` (non versionné) doit contenir les variables suivantes :

| Variable | Valeur par défaut | Description |
|----------|-------------------|-------------|
| `API_URL` | `http://127.0.0.1:8000` | URL de base de l'API Bloc 2 |
| `API_KEY` | — | Clé d'authentification `X-API-Key` de l'API Bloc 2 |
| `LOG_DIR` | `monitoring/logs` | Répertoire de stockage des logs JSONL |

Exemple de fichier `.env` :
```
API_URL=http://127.0.0.1:8000
API_KEY=votre_cle_secrete_bloc2
LOG_DIR=monitoring/logs
```

---

## Preuve de concept — appel API Bloc 2

Avant de développer l'interface, vérifier que l'endpoint `/predict` est accessible avec un appel curl :

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "X-API-Key: votre_cle" \
  -H "Content-Type: application/json" \
  -d '{
    "airline": "Vistara",
    "source_city": "Delhi",
    "destination_city": "Mumbai",
    "stops": "zero",
    "class": "Economy",
    "duration": 2.17,
    "days_left": 30
  }'
```

Réponse attendue :
```json
{
  "predicted_price": 7838.42,
  "currency": "INR",
  "model_version": "1.0.0"
}
```

Vérifier également la disponibilité de frankfurter.app :
```bash
curl "https://api.frankfurter.app/latest?from=INR&to=EUR"
```

---

## Contraintes de sécurité (OWASP)

| Risque | Mesure appliquée |
|--------|-----------------|
| Exposition de la clé API | Stockage dans `.env` (gitignorée), jamais en dur dans le code |
| Injection via formulaire | Tous les champs sont des `selectbox` ou `number_input` — pas de saisie libre |
| Timeout non géré | `requests.post(..., timeout=5)` sur tous les appels HTTP |
| Crash sur erreur externe | Tous les appels HTTP sont encapsulés dans un bloc `try/except` |
