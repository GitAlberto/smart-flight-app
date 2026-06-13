# Méthode agile — smart-flight-app

## Méthode retenue : Scrum simplifié (projet solo)

La méthode Scrum est adaptée à un contexte solo en conservant les éléments structurants tout en supprimant les cérémonies collectives (stand-up d'équipe, sprint planning formel). Les sprints durent 1 à 2 jours chacun.

| Cérémonies conservées | Format solo |
|-----------------------|-------------|
| Daily | Note d'avancement de 5 min par jour dans ce fichier |
| Sprint review | Bilan à mi-projet (après Phase 3) |
| Sprint retrospective | Bilan final avant soutenance |

---

## Backlog priorisé

| Priorité | ID | Tâche | Compétence | Statut |
|----------|----|-------|------------|--------|
| 1 | T01 | Initialisation repo + structure | — | ✅ Done |
| 2 | T02 | Spécifications fonctionnelles (C14) | C14 | ✅ Done |
| 3 | T03 | Spécifications techniques (C15) | C15 | ✅ Done |
| 4 | T04 | Méthode agile — ce document (C16) | C16 | ✅ Done |
| 5 | T05 | Preuve de concept — appel API Bloc 2 | C15 | To Do |
| 6 | T06 | Interface Streamlit — formulaire | C17 | To Do |
| 7 | T07 | Intégration appel API + affichage INR | C17 | To Do |
| 8 | T08 | Conversion EUR via frankfurter.app | C17 | To Do |
| 9 | T09 | Gestion des erreurs (API down, timeout) | C17 | To Do |
| 10 | T10 | Journalisation des requêtes (logger.py) | C20 | To Do |
| 11 | T11 | Tests automatisés (pytest) | C17, C18 | To Do |
| 12 | T12 | Pipeline CI/CD GitHub Actions | C18, C19 | To Do |
| 13 | T13 | Documentation monitoring | C20 | To Do |
| 14 | T14 | Incident documenté (C21) | C21 | To Do |
| 15 | T15 | README complet | — | To Do |

---

## Tableau kanban

### To Do
- T05 — Preuve de concept API Bloc 2
- T06 — Interface Streamlit formulaire
- T07 — Intégration API + affichage INR
- T08 — Conversion EUR
- T09 — Gestion erreurs
- T10 — Logger JSONL
- T11 — Tests automatisés
- T12 — CI/CD GitHub Actions
- T13 — Documentation monitoring
- T14 — Incident documenté
- T15 — README

### In Progress
_(vide)_

### Done
- T01 — Init repo + structure
- T02 — Specs fonctionnelles
- T03 — Specs techniques
- T04 — Agile (ce document)

---

## Définition of Done (DoD)

Une tâche est considérée **Done** quand :
- Le code est écrit et fonctionne localement
- Les fichiers sont versionnés sur Git (commit avec message explicite)
- Les tests associés passent (si applicable)
- La documentation liée est rédigée (si applicable)

---

## Suivi daily — notes d'avancement

### Jour 1 — 2026-06-13
- Phase 0 complétée : repo initialisé, structure créée, `.gitignore` corrigé
- Phase 1 complétée : specs fonctionnelles, techniques et agile rédigées
- Prochain : Phase 2 — Interface Streamlit + intégration API Bloc 2

---

## Sprint review — mi-projet

_(À compléter après la Phase 3)_

---

## Sprint retrospective — bilan final

_(À compléter avant la soutenance)_
