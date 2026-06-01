---
title: Architecture
tags: [docsense, architecture, technique, aws, kubernetes]
created: 2026-07-07
type: note
status: définitif
---

# Architecture

## Vue d'ensemble

```
┌─────────────────────────────────────┐
│         Next.js / React             │
│  Upload · Streaming UI · Revue      │
└──────────────┬──────────────────────┘
               │ REST / SSE
               ▼
┌─────────────────────────────────────┐
│         Symfony 7 + API Platform    │
│  Auth JWT · Persistance · Jobs SQS  │
└──────────────┬──────────────────────┘
               │ publie un job
               ▼
┌──────────────────────────────────────────────┐
│  AWS SQS  ──▶  Worker Python / FastAPI       │
│                Parsing PDF/DOCX/CSV          │
│                Chunking · Embeddings         │
│                Appel LLM (Claude ou Mistral) │
│                        │                    │
│               ┌────────┴────────┐           │
│               ▼                 ▼           │
│           AWS S3           RDS Postgres      │
│        (documents)         (+ pgvector)      │
└──────────────────────────────────────────────┘

────────────────────────────────────────────
Déployé sur EKS (Kubernetes)
Infra provisionnée par Terraform
CI/CD via GitHub Actions
────────────────────────────────────────────
```

---

## Composants détaillés

### Frontend — Next.js / React

- **App Router** (Next.js 14+)
- Upload de fichiers avec feedback de progression
- **Streaming UI** : `EventSource` ou `fetch()` + `ReadableStream` pour afficher le rapport en temps réel (mot par mot)
- Dashboard de revue : l'utilisateur voit les données extraites + citations, peut corriger, puis exporte
- Sélecteur de modèle : Claude ↔ Mistral

### API métier — Symfony 7 + API Platform

- **Auth JWT** via LexikJWTAuthenticationBundle
- Entités Doctrine : `Document`, `Report`, `ExtractionResult`
- Endpoint `POST /api/reports` → valide, persiste, publie un job SQS
- Endpoint `GET /api/reports/{id}/stream` → `StreamedResponse` SSE
- Gestion des erreurs (retry, DLQ SQS)

### Worker IA — Python 3.12 / FastAPI

- Consomme la file SQS en continu
- **Parsing** : `pypdf` (PDF), `python-docx` (DOCX), `pandas` (CSV)
- **Chunking** : découpage intelligent selon le type de document
- **Appel LLM** : via [[03 - Stack et décisions techniques#Pattern LLMProvider]]
- Renvoie du JSON structuré + citations (via tool use Claude)
- Met à jour le statut du rapport dans RDS

### Pattern LLMProvider

```python
class LLMProviderInterface(ABC):
    @abstractmethod
    def generate_report(self, data: dict, on_chunk=None) -> str:
        pass

class ClaudeProvider(LLMProviderInterface):
    # Anthropic Messages API · streaming · tool use
    pass

class MistralProvider(LLMProviderInterface):
    # Mistral La Plateforme · hébergement EU · RGPD
    pass
```

→ Voir [[03 - Stack et décisions techniques#Pourquoi polyglotte]] pour la justification.

---

## Infrastructure AWS

| Service AWS | Rôle |
|---|---|
| **EKS** | Cluster Kubernetes (frontend, api, worker) |
| **ECR** | Registry Docker (images des 3 services) |
| **SQS** | File de messages asynchrones |
| **S3** | Stockage des documents uploadés |
| **RDS Postgres** | Base de données + extension pgvector |
| **Secrets Manager** | Clés API Anthropic/Mistral |
| **ALB** | Load balancer + terminaison HTTPS |
| **IAM** | Roles IRSA (pods → services AWS sans clés) |

---

## Kubernetes (EKS)

Chaque service = un `Deployment` :
- `docsense-frontend` : Next.js, 2 replicas
- `docsense-api` : Symfony, 2 replicas
- `docsense-worker` : Python, **HPA** (scaling auto selon la longueur de la file SQS)

Secrets injectés via **External Secrets Operator** (ESO) depuis AWS Secrets Manager. Jamais de secrets dans les manifests Git.

---

## Flux de données complet

```
1. User uploade un PDF sur Next.js
2. Next.js → POST /api/documents → Symfony
3. Symfony stocke le fichier sur S3, persiste en RDS, publie job SQS
4. Worker Python consomme le job SQS
5. Worker parse le PDF, appelle Claude (tool use)
6. Claude retourne JSON structuré + citations
7. Worker met à jour RDS (status: "ready")
8. User ouvre le rapport → GET /api/reports/{id}/stream
9. Symfony streame via SSE le contenu depuis RDS
10. Next.js affiche en temps réel
11. User valide → export PDF
```

---

*Voir aussi : [[01 - Contexte et vision]] · [[03 - Stack et décisions techniques]] · [[04 - Périmètre MVP]]*
