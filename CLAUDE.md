# DocSense — Contexte projet Claude Code

> Ce fichier est lu automatiquement par Claude Code à chaque session.
> Il contient tout le contexte nécessaire pour reprendre le projet sans se répéter.

---

## 🎯 Qui je suis & pourquoi ce projet

Je suis un développeur freelance basé à La Réunion, en cours de pivot vers le profil **Platform Engineer with AI** pour décrocher des missions full remote à 650–900€/jour.

DocSense est le **projet portfolio #1** d'un plan de formation de 4,5 mois (démarrage 7 juillet 2026, 40h/semaine). Son rôle est double :
- **Prouver** que je sais construire un produit IA complet, cloud-native, en production
- **Différencier** mon profil sur Malt/LinkedIn avec l'argument multi-modèles + RGPD/souveraineté

---

## 🧠 Ce qu'est DocSense

**Plateforme d'intelligence documentaire multi-modèles.**

L'utilisateur uploade des documents (PDF, DOCX, CSV) → l'app extrait des données structurées fiables (avec citation de la source exacte) → génère un rapport d'analyse en streaming → l'utilisateur valide avant export PDF.

**Le différenciateur clé** : interface LLMProvider commune avec deux implémentations — Claude (Anthropic) et Mistral (hébergé en Europe, conforme RGPD). Un recruteur/client peut tester avec les deux modèles. C'est le pattern Adapter appliqué à l'IA.

---

## 🏗️ Architecture

```
[ Next.js / React ]     — Upload, streaming UI (SSE), revue & validation
       │ REST / SSE
       ▼
[ Symfony API ]         — Logique métier, auth JWT, persistance, orchestration
       │ publie un job
       ▼
[ SQS ] ──────────────▶ [ Worker Python / FastAPI ]
                              — Parsing PDF/DOCX/CSV
                              — Chunking, embeddings
                              — Appel Claude ou Mistral (interface commune)
                              ▼
                        [ S3 ] + [ RDS Postgres + pgvector ]

────────────────────────────────────────────────────────
Déployé sur EKS (Kubernetes) · Infra Terraform · CI/CD GitHub Actions
```

### Pourquoi polyglotte ?
- **Symfony** → logique métier, auth, persistance (ma force, terrain connu)
- **Python** → couche IA/ingestion (l'écosystème IA — parsing, embeddings, SDK — est ici)
- **Next.js** → frontend moderne, App Router, streaming UI (très demandé en 2026)
- Argument fort en entretien : *"j'ai choisi le bon outil pour chaque couche"*

---

## 🛠️ Stack complète

| Couche | Techno | Justification |
|---|---|---|
| Frontend | Next.js (React) | App Router, SSE, dashboard de revue |
| API métier | Symfony 7 + API Platform | Auth JWT, persistance, orchestration |
| Worker IA | Python 3.12 + FastAPI | Parsing, embeddings, appels LLM |
| IA | Claude (Anthropic) + Mistral | Multi-modèles, RGPD, pattern Adapter |
| Cloud | AWS | EKS, S3, RDS, SQS, Secrets Manager, ALB, ECR |
| Orchestration | Kubernetes (EKS) | HPA (scaling worker), secrets, ingress |
| IaC | Terraform | VPC, EKS, RDS, IAM, ECR — reproductible |
| Source & CI | GitHub + Actions | Lint/tests/build, push ECR, deploy EKS |

---

## 🔑 Décisions techniques clés

### Pattern LLMProvider (anti-vendor lock-in)
```python
# interfaces/llm_provider.py
from abc import ABC, abstractmethod

class LLMProviderInterface(ABC):
    @abstractmethod
    def generate_report(self, data: dict, on_chunk=None) -> str:
        pass

class ClaudeProvider(LLMProviderInterface):
    # Messages API Anthropic, streaming SSE
    pass

class MistralProvider(LLMProviderInterface):
    # La Plateforme Mistral, hébergement EU
    pass
```
→ Ajouter un 3ᵉ modèle = 1 seule classe, zéro refactoring.

### Streaming SSE
- Côté Symfony : `StreamedResponse` avec `text/event-stream`
- Côté Next.js : `EventSource` ou `fetch()` avec `ReadableStream`
- Effet démo immédiat — le rapport s'écrit en live

### Citations anti-hallucination
Claude répond en JSON structuré via tool use :
```json
{
  "field": "chiffre_affaires",
  "value": "2.3M€",
  "citation": "Page 4, paragraphe 2 : 'Le CA annuel s'élève à 2.3M€'"
}
```
→ Chaque donnée extraite est traçable dans le document source.

### Sécurité des clés API
- Clés Anthropic/Mistral dans AWS Secrets Manager
- Jamais dans le code, jamais dans Git
- Injectées dans les pods k8s via External Secrets Operator

---

## 📦 Périmètre MVP (priorité absolue)

- [ ] Upload PDF/CSV + extraction Claude
- [ ] Rapport en streaming + export
- [ ] Sélecteur Claude / Mistral
- [ ] Déploiement EKS via Terraform
- [ ] CI/CD GitHub Actions → ECR → EKS

## 🚀 Stretch goals (si le temps)

- [ ] RAG sur pgvector (recherche sémantique)
- [ ] Auto-scaling HPA du worker selon file SQS
- [ ] Multi-tenant + quotas
- [ ] Observabilité (Prometheus + Grafana)
- [ ] Support DOCX

---

## 📅 Timing dans le plan de formation

| Phase | Dates | Ce qui se construit |
|---|---|---|
| Phase 1 (sem. 3-4) | 21 juil → 17 août | MVP fonctionnel local, README, GIF démo |
| Phase 2 (sem. 10-13) | sept-oct | Déploiement EKS + Terraform + RDS AWS |
| Phase 2 (sem. 14-16) | oct | IaC complète (.tf versionnés) |
| Phase 3 | oct-nov | RAG, scaling, observabilité (stretch) |

---

## 🎯 Ce que ce projet prouve aux recruteurs

1. **Produit IA complet** — pas un notebook ou un POC
2. **Architecture distribuée** — polyglotte, découplée, scalable
3. **Cloud-native** — EKS, Terraform IaC, CI/CD propre
4. **Sensibilité production** — secrets, streaming, anti-hallucination, human-in-the-loop
5. **Souveraineté / RGPD** — Mistral hébergé en Europe, différenciant pour les clients FR

---

## 📁 Structure du repo (cible)

```
docsense/
├── CLAUDE.md                    ← ce fichier
├── notes/                       ← vault Obsidian (contexte)
├── docker-compose.yml           ← dev local
├── frontend/                    ← Next.js
├── api/                         ← Symfony
├── worker/                      ← Python FastAPI
├── infra/
│   ├── terraform/               ← VPC, EKS, RDS, ECR, IAM
│   └── k8s/                     ← manifests Kubernetes
└── .github/
    └── workflows/               ← CI/CD
```

---

## 🔗 Contexte carrière (rappel)

- **Profil actuel** : Dev Symfony, Vue→React, Docker, Rancher, CI/CD GitLab
- **Profil cible** : Platform Engineer with AI, full remote, TJM 650–900€
- **Localisation** : La Réunion → missions nationales via télétravail
- **Plan** : 4,5 mois, 40h/sem, démarrage 7 juillet 2026
- **Projet #2** : ShipMate (copilote CI/CD avec Claude dans la pipeline)
- **Pas de CKA ni CCA-F** dans le plan — compétences prouvées par les projets
- **Stack certifiée** : AWS SAA-C03 (150$, examen prévu ~oct 2026)
