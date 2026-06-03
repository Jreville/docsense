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

### 2026-06-03 — Bootstrap repo + Worker Python

> [!NOTE] Contexte
> Session de démarrage anticipée (J-34 avant le kick-off officiel du 7 juillet). Mise en place des fondations du projet.

**Fait :**
- Création de la structure du repo (`frontend/`, `api/`, `worker/`, `infra/terraform`, `infra/k8s`, `.github/workflows/`)
- `docker-compose.yml` complet : postgres/pgvector, LocalStack (SQS + S3), api, worker, frontend
- `.gitignore` sécurisé pour repo public (secrets, `.env`, Terraform state, clés AWS, IDE/OS)
- Repo GitHub public créé et pushé → [Jreville/docsense](https://github.com/Jreville/docsense)
- Bootstrap complet du Worker Python :
  - `LLMProviderInterface` (ABC) — contrat `extract_structured_data` + `generate_report_stream`
  - `ClaudeProvider` — tool use pour extraction structurée avec citations, streaming SSE
  - `MistralProvider` — JSON mode, même interface, hébergement EU/RGPD
  - `ExtractionService` — injection de dépendance, découplage provider/logique
  - Schémas Pydantic (`ExtractionRequest`, `ExtractionResponse`, `ExtractedField`, `ReportRequest`)
  - FastAPI : `GET /health`, `POST /extract`, `POST /report/stream`
  - `Dockerfile` + `requirements.txt` (versions épinglées) + `.env.example`
- Installation du skill Obsidian (`obsidian-skills` de kepano) → 5 skills actifs

**Décisions :**
- Pattern ABC Python pour l'interface LLM → contrat fort, erreur à l'instanciation si méthode manquante
- Tool use Claude (pas prompt engineering) pour forcer le JSON structuré + citations
- Mistral en JSON mode (`response_format`) — pas de tool use natif identique à Anthropic
- Factory dict `PROVIDERS = {"claude": ..., "mistral": ...}` dans `main.py` — zéro `if/else` dans la logique métier
- `.env` exclu du git dès le départ (sécurité clés API)

**Blocage résolu :**
- Push GitHub bloqué : token sans scope `workflow` → `.github/workflows/.gitkeep` retiré du commit initial
- Push SSH échoué (clé non configurée) → basculé en HTTPS

**Prochaine session :**
- Lancer `test_extraction.py` → valider appel Claude réel avec citations
- Bootstrapper l'API Symfony (entité `Document`, endpoint upload, publication SQS)
- Configurer clé SSH GitHub pour éviter le fallback HTTPS

---

<!-- Ajouter les entrées suivantes ici au fil du développement -->
