# Spécifications fonctionnelles — smart-flight-app

## Contexte et objectifs

Un voyageur souhaitant estimer le coût d'un billet d'avion doit aujourd'hui consulter plusieurs plateformes sans disposer d'une vue claire sur les facteurs qui influencent réellement le prix. Il n'existe pas d'outil simple lui permettant d'obtenir immédiatement une estimation à partir de ses paramètres de voyage, avec une conversion automatique dans sa devise locale.

**smart-flight-app** répond à ce besoin en proposant une interface web minimaliste : l'utilisateur saisit les caractéristiques de son vol, l'application interroge le service de prédiction IA développé en Bloc 2 (`smart-flight-pricer`) et affiche le prix estimé en roupies indiennes (INR) converti en euros (EUR).

### Objectifs fonctionnels

- Permettre la saisie des paramètres d'un vol via un formulaire web
- Afficher une estimation de prix en INR et en EUR après soumission
- Informer l'utilisateur en cas d'indisponibilité du service de prédiction
- Journaliser chaque requête pour permettre un suivi applicatif

---

## Acteurs

| Acteur | Description |
|--------|-------------|
| Voyageur français | Utilisateur final, non technicien, souhaitant estimer le prix d'un billet d'avion au départ ou à destination de l'Inde |
| API smart-flight-pricer | Service IA (Bloc 2) qui réalise la prédiction de prix via un modèle RandomForest |
| frankfurter.app | Service externe de taux de change, utilisé pour la conversion INR → EUR |

---

## Parcours utilisateur

```
[1] L'utilisateur ouvre l'application dans son navigateur (port 8501)
        |
        v
[2] L'interface affiche le formulaire de saisie
        |
        v
[3] L'utilisateur sélectionne : compagnie, ville de départ, ville d'arrivée,
    nombre d'escales, classe, durée du vol, jours avant le départ
        |
        v
[4] L'utilisateur clique sur "Estimer le prix"
        |
        v
[5] L'application envoie une requête POST /predict à l'API Bloc 2
        |
        +--[API disponible]---> [6a] Réception du prix en INR
        |                              |
        |                              v
        |                       [7a] Appel frankfurter.app pour taux INR/EUR
        |                              |
        |                              v
        |                       [8a] Affichage : "7 838 INR — soit ~86 €"
        |
        +--[API indisponible]--> [6b] Affichage d'un message d'erreur clair
                                        (sans crash de l'application)
        |
        v
[9] La requête est journalisée (inputs, résultat, latence, erreur éventuelle)
```

---

## User stories

| ID | User Story | Critère d'acceptation |
|----|------------|----------------------|
| US1 | En tant que voyageur, je veux sélectionner ma compagnie aérienne, mon trajet et ma classe afin de paramétrer mon estimation | Le formulaire affiche toutes les valeurs disponibles sous forme de listes déroulantes ; aucune saisie libre n'est requise |
| US2 | En tant que voyageur, je veux obtenir un prix estimé affiché en INR et en euros afin de comprendre le coût dans ma devise locale | Après soumission, l'application affiche les deux devises simultanément ; la conversion utilise un taux en temps réel |
| US3 | En tant que voyageur, je veux être informé clairement si le service est indisponible afin de ne pas croire que l'application est cassée | Un message d'erreur explicite s'affiche sans que l'application plante ; l'utilisateur peut retenter sans recharger la page |

---

## Critères d'acceptation détaillés

### US1 — Formulaire de saisie

- [ ] La compagnie aérienne est sélectionnable parmi : Air India, Vistara, Indigo, GO FIRST, AirAsia, SpiceJet
- [ ] La ville de départ est sélectionnable parmi : Delhi, Mumbai, Bangalore, Kolkata, Hyderabad, Chennai
- [ ] La ville d'arrivée est sélectionnable parmi les mêmes villes
- [ ] Le nombre d'escales est sélectionnable parmi : zero, one, two_or_more
- [ ] La classe est sélectionnable parmi : Economy, Business
- [ ] La durée du vol est saisie via un champ numérique (min : 0.5h, max : 50h)
- [ ] Les jours avant le départ sont saisis via un curseur (min : 1, max : 365)

### US2 — Affichage du résultat

- [ ] Le prix en INR est affiché avec séparateur de milliers (ex : 7 838 INR)
- [ ] Le prix en EUR est affiché arrondi à 2 décimales (ex : ~86.42 €)
- [ ] Le résultat est affiché dans un bloc visuellement distinct du formulaire

### US3 — Gestion des erreurs

- [ ] Si l'API Bloc 2 est inaccessible, un message `st.error()` s'affiche
- [ ] L'application ne lève pas d'exception non gérée
- [ ] Si l'API de change est inaccessible, un taux de repli fixe est utilisé (0.011)

---

## Objectifs d'accessibilité (WCAG 2.1 niveau AA)

- Tous les champs du formulaire sont accompagnés d'un label explicite
- Les messages d'erreur sont distincts visuellement et textuellement
- Les contrastes de couleur respectent un ratio minimum de 4.5:1
- L'interface est utilisable sans interaction à la souris (navigation clavier)
- Les listes déroulantes utilisent les composants natifs Streamlit (accessibles par défaut)
