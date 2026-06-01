---
title: Périmètre MVP
tags: [docsense, mvp, planning, livrables]
created: 2026-07-07
type: note
status: en cours
---

# Périmètre MVP

## Philosophie

> Livrer un projet qui tourne et qui impressionne sur 3 fonctionnalités bien faites vaut 10× un projet avec 20 features à moitié implémentées.

L'objectif MVP = **démontrable à un recruteur en 5 minutes** : upload, extraction, streaming, sélecteur de modèle.

---

## MVP obligatoire (phase 1 — avant fin août)

- [ ] Upload PDF + extraction Claude (tool use, JSON + citations)
- [ ] Rapport généré en streaming (SSE Symfony → EventSource Next.js)
- [ ] Sélecteur Claude / Mistral (pattern Adapter fonctionnel)
- [ ] Interface Next.js propre (upload, loading, affichage rapport)
- [ ] Export basique (copier/coller ou PDF simple)
- [ ] Docker Compose local (tout en une commande)
- [ ] README avec GIF de démo + installation en 3 commandes

---

## Ajouté en phase 2 (sept–oct, avec le déploiement AWS)

- [ ] Déploiement EKS via Terraform
- [ ] CI/CD GitHub Actions → build → push ECR → deploy EKS
- [ ] RDS Postgres (persistence des rapports)
- [ ] S3 (stockage des documents)
- [ ] Secrets Manager + ESO (clés API sécurisées)
- [ ] HTTPS + domaine (ALB + certificat)
- [ ] **Démo en ligne** (URL cliquable dans le README)

---

## Stretch goals (phase 3 ou après missions)

- [ ] RAG sur pgvector (recherche dans les anciens rapports)
- [ ] HPA du worker selon longueur file SQS
- [ ] Multi-tenant (plusieurs utilisateurs, quotas)
- [ ] Observabilité (Prometheus + Grafana)
- [ ] Support DOCX
- [ ] Webhook Slack (notification quand le rapport est prêt)

---

## Ce que ce projet prouve aux recruteurs

Une fois le MVP en ligne :

| Preuve | Signal recruteur |
|---|---|
| URL de démo fonctionnelle | Je sais livrer, pas juste coder |
| GIF de démo dans le README | Je pense à l'expérience du lecteur |
| README avec choix techniques commentés | Je raisonne, je ne subis pas |
| Code polyglotte propre (PHP + Python + TS) | Je maîtrise plusieurs environnements |
| Streaming en temps réel | Compétence LLM avancée |
| Citations dans les extractions | Sensibilité à la fiabilité en prod |
| Pattern Adapter multi-modèles | Vision architecture, pas juste feature |
| Infra Terraform reproductible | Culture DevOps réelle |

---

## Ordre de construction recommandé

```
Semaine 3 (21 juil)
├── J1-J2 : Setup Symfony API + endpoint POST /documents
├── J3-J4 : Worker Python + intégration Claude (extraction basique)
└── J5 : Interface Next.js minimale (upload + affichage JSON)

Semaine 4 (28 juil)
├── J1-J2 : Streaming SSE bout-en-bout
├── J3 : Pattern Adapter + intégration Mistral
├── J4 : Docker Compose complet (tout en une commande)
└── J5 : README + GIF démo + buffer/polish
```

---

*Voir aussi : [[02 - Architecture]] · [[05 - Lien avec le plan de formation]]*
