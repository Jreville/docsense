---
title: Contexte et vision
tags: [docsense, contexte, vision, portfolio, carrière]
created: 2026-07-07
type: note
status: définitif
---

# Contexte et vision

## Qui construit ce projet

Développeur freelance basé à **La Réunion**, en cours de pivot vers le profil **Platform Engineer with AI**. L'objectif est de décrocher des missions **full remote** à **650–900€/jour** sur le marché français, depuis La Réunion, grâce au télétravail (décalage horaire ~2-3h, gérable).

Profil de départ : Symfony / Vue→React / Docker / Rancher / CI/CD GitLab.

→ Voir [[05 - Lien avec le plan de formation]] pour le détail du plan 4,5 mois.

---

## Pourquoi DocSense

DocSense est le **projet portfolio #1**. Il ne s'agit pas d'un exercice ou d'un tutoriel — c'est une vraie application conçue pour démontrer, de façon concrète et démontrable en 5 minutes à un recruteur, que je sais :

1. **Construire un produit IA complet** — pas un POC, pas un notebook
2. **Architecturer une application cloud-native** — Kubernetes, IaC Terraform, AWS
3. **Intégrer un LLM en production** — streaming, anti-hallucination, gestion des coûts
4. **Penser souveraineté/RGPD** — multi-modèles Claude + Mistral hébergé en Europe

### Le problème que DocSense résout

Les entreprises croulent sous des documents non structurés : factures, contrats, rapports, comptes-rendus. Extraire des données fiables de ces documents est long et source d'erreurs humaines.

DocSense automatise ce travail :
- L'utilisateur uploade un document (PDF, DOCX, CSV)
- L'IA extrait les données structurées **avec citation de la source exacte**
- Un rapport est généré **en streaming** (le texte s'écrit en live)
- L'utilisateur **valide** avant export — human-in-the-loop

### Le différenciateur concurrentiel

**Interface multi-modèles** : Claude (Anthropic) ou Mistral (hébergement européen, RGPD natif), interchangeables via un pattern Adapter. Le client choisit selon ses contraintes de conformité.

C'est l'argument qui sépare un dev qui « a branché une API LLM » d'un dev qui « a conçu une architecture IA maintenable ».

---

## Ce que ce projet prouve aux recruteurs

| Ce que le recruteur voit | Ce que ça prouve |
|---|---|
| Produit qui tourne en ligne | Je sais livrer, pas juste coder |
| Architecture polyglotte (PHP + Python + TS) | Je choisis le bon outil pour chaque couche |
| Streaming SSE en temps réel | Je maîtrise l'intégration LLM au-delà du basique |
| Citations dans les extractions | Je pense anti-hallucination et confiance |
| Multi-modèles (Claude + Mistral) | Je pense architecture, pas vendor lock-in |
| EKS + Terraform + GitHub Actions | Je suis cloud-native, j'ai une pratique DevOps réelle |
| Human-in-the-loop | Je comprends les enjeux prod de l'IA |

---

## Marché cible (contexte)

D'après les données Malt 2026 (sources francophones vérifiées) :
- Projets IA sur Malt : **+170% en un an**
- Compétences Claude : **+97%**
- TJM AI Integration : **400–700€/jour**
- TJM conseil IA : jusqu'à **840€/jour**
- **>70% des missions IT** sont hybrides ou full remote

DocSense positionne directement sur ces créneaux.

---

*Voir aussi : [[02 - Architecture]] · [[03 - Stack et décisions techniques]]*
