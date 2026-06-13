# Documentation monitoring — smart-flight-app

## Stratégie de monitoring

Le monitoring de smart-flight-app est **applicatif** : il porte sur le comportement de l'application elle-même (requêtes, erreurs, latence), et non sur l'infrastructure système. Chaque appel utilisateur est journalisé dans un fichier JSONL exploitable sans outil externe.

---

## Journalisation — monitoring/logger.py

### Format d'un log

Chaque requête produit une ligne JSON dans `monitoring/logs/app.jsonl` :

```json
{
  "timestamp": "2026-06-13T14:32:05.123456",
  "inputs": {
    "airline": "Vistara",
    "source_city": "Delhi",
    "destination_city": "Mumbai",
    "stops": "zero",
    "class": "Economy",
    "duration": 2.0,
    "days_left": 30
  },
  "result": {
    "predicted_price": 7838.42,
    "currency": "INR",
    "model_version": "1.0.0"
  },
  "latency_ms": 142.37,
  "error": null
}
```

En cas d'erreur API, le champ `result` vaut `null` et `error` contient le motif :

```json
{
  "timestamp": "2026-06-13T14:35:12.654321",
  "inputs": { ... },
  "result": null,
  "latency_ms": 5023.11,
  "error": "API indisponible"
}
```

### Implémentation

```python
# monitoring/logger.py
def log_request(inputs, result, latency_ms, error):
    os.makedirs(LOG_DIR, exist_ok=True)
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "inputs": inputs,
        "result": result,
        "latency_ms": round(latency_ms, 2),
        "error": error,
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
```

Le logger est appelé dans `app/main.py` **après chaque soumission du formulaire**, qu'il y ait succès ou erreur.

---

## Métriques définies

| # | Métrique | Seuil d'alerte | Justification |
|---|----------|----------------|---------------|
| M1 | Nombre de requêtes par heure | > 100/h | Détection d'un pic inhabituel (bot, boucle) |
| M2 | Taux d'erreurs API Bloc 2 | > 10% | L'API Bloc 2 devient instable ou inaccessible |
| M3 | Latence de réponse | > 3 000 ms | L'expérience utilisateur se dégrade significativement |
| M4 | Échecs consécutifs API de change | > 3 fois | Le fallback taux fixe est activé — conversion moins fiable |

### Calcul des métriques depuis les logs

Les métriques sont dérivables directement du fichier `app.jsonl` :

```bash
# M1 — requêtes sur la dernière heure
grep "$(date -u +'%Y-%m-%dT%H')" monitoring/logs/app.jsonl | wc -l

# M2 — taux d'erreurs (ratio lignes avec error != null)
grep '"error": "' monitoring/logs/app.jsonl | wc -l

# M3 — requêtes avec latence > 3000ms
grep -v '"error": null' monitoring/logs/app.jsonl | python -c "
import sys, json
for line in sys.stdin:
    e = json.loads(line)
    if e['latency_ms'] > 3000:
        print(line.strip())
"

# M4 — erreurs de conversion (à tracer via logs applicatifs étendus)
```

---

## Alertes

Les alertes sont documentées sous forme de règles. Dans le cadre de ce projet solo, elles sont **vérifiées manuellement** à partir des logs. Une implémentation automatisée nécessiterait un outil dédié (ex : Grafana, Prometheus AlertManager).

| Alerte | Condition | Action recommandée |
|--------|-----------|-------------------|
| Pic de trafic | M1 > 100 requêtes/h | Vérifier les logs, identifier la source |
| API Bloc 2 dégradée | M2 > 10% d'erreurs | Vérifier que `smart-flight-pricer` est lancé et répond sur `/health` |
| Latence élevée | M3 > 3 000 ms | Vérifier la charge réseau et l'état de l'API Bloc 2 |
| Fallback devise activé | M4 > 3 échecs consécutifs | Vérifier la disponibilité de `api.frankfurter.app` |

---

## Procédure de consultation des logs

```bash
# Afficher les 10 dernières entrées
tail -n 10 monitoring/logs/app.jsonl | python -m json.tool

# Filtrer les erreurs uniquement
grep '"error": "' monitoring/logs/app.jsonl

# Compter le total de requêtes
wc -l monitoring/logs/app.jsonl
```

---

## Lien avec l'incident C21

Le monitoring a permis d'identifier le cas Delhi → Delhi : une requête valide côté API (pas d'erreur retournée) mais sémantiquement incorrecte. Cette observation a conduit à l'ajout d'une validation côté client documentée dans [incident.md](incident.md).
