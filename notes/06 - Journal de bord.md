---
title: Journal de bord
tags: [docsense, journal, sessions]
created: 2026-07-07
type: journal
status: en cours
---

# Journal de bord

> Utiliser ce fichier pour noter les décisions prises en cours de développement, les blocages résolus, et les changements d'architecture. Chaque entrée = une session de travail.

---

## Template d'entrée

```
### YYYY-MM-DD — [sujet]

**Fait :**
- ...

**Décision :**
- ...

**Blocage / question ouverte :**
- ...

**Prochaine session :**
- ...
```

---

## Sessions

### 2026-07-07 — Initialisation du projet

**Fait :**
- Création du projet Claude Code (CLAUDE.md)
- Création du vault Obsidian (notes de contexte)
- Architecture définie, stack validée, MVP scopé

**Décisions :**
- Architecture polyglotte (PHP + Python + TS) validée
- Pattern Adapter pour les LLM retenu
- Mistral inclus dès le MVP (pas un stretch goal)
- Streaming SSE plutôt que WebSocket (plus simple, HTTP natif)

**Prochaine session :**
- Bootstrapper le projet Symfony (API Platform)
- Bootstrapper le worker Python (FastAPI)
- Bootstrapper le frontend Next.js
- Créer le `docker-compose.yml` de dev

---

<!-- Ajouter les entrées suivantes ici au fil du développement -->
