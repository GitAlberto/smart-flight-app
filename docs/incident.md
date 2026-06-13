# Rapport d'incident — Ville de départ identique à la ville d'arrivée

## Date
2026-06-13

## Description
L'application acceptait une requête où la ville de départ et la ville d'arrivée étaient identiques (ex : Delhi → Delhi). La requête était transmise à l'API Bloc 2 sans aucune validation côté client, produisant une prédiction de prix pour un trajet inexistant.

## Cause identifiée
Aucune validation des données du formulaire n'était effectuée avant l'appel à l'API. Streamlit affiche deux `selectbox` indépendants pour `source_city` et `destination_city` sans contrainte entre eux. Un utilisateur pouvait donc sélectionner la même ville dans les deux champs et obtenir un résultat sans message d'erreur.

## Reproduction
1. Lancer l'application : `streamlit run app/main.py`
2. Sélectionner **Delhi** comme ville de départ
3. Sélectionner **Delhi** comme ville d'arrivée
4. Cliquer sur **Estimer le prix**
5. Résultat : l'application envoie la requête à l'API et affiche un prix — sans avertir l'utilisateur que le trajet est invalide

## Solution implémentée
Ajout d'une validation dans `app/main.py` après le clic sur le bouton, avant l'appel à l'API :

```python
if source_city == destination_city:
    st.warning("La ville de départ et la ville d'arrivée doivent être différentes.")
    st.stop()
```

`st.stop()` interrompt l'exécution du script Streamlit à ce point, empêchant tout appel API avec des données invalides.

## Commit de correction
```
fix: validation source_city != destination_city avant appel API (C21)
```

## Tests ajoutés
Un cas de test a été ajouté dans `tests/test_api_client.py` pour vérifier que `predict_price` n'est jamais appelé quand `source_city == destination_city` — couvert via le test d'intégration de l'interface.
