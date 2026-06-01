---
title: Stack et décisions techniques
tags: [docsense, technique, stack, décisions]
created: 2026-07-07
type: note
status: définitif
---

# Stack et décisions techniques

## Stack complète

| Couche | Techno | Version cible |
|---|---|---|
| Frontend | Next.js + React | 14+ / 18+ |
| API métier | Symfony + API Platform | 7.x / 4.x |
| Worker IA | Python + FastAPI | 3.12 / 0.111+ |
| IA | Claude (Anthropic) + Mistral | Sonnet / Large |
| Cloud | AWS | — |
| Orchestration | Kubernetes (EKS) | 1.30+ |
| IaC | Terraform | 1.8+ |
| CI/CD | GitHub Actions | — |
| Containers | Docker + ECR | — |

---

## Pourquoi polyglotte

**Argument clé à mettre en avant en entretien** :

> « J'ai choisi Symfony pour la logique métier parce que c'est mature, typé, et que c'est mon terrain. J'ai choisi Python pour le worker IA parce que l'écosystème — parsing, embeddings, SDKs LLM — est incomparablement plus riche qu'en PHP. Ce n'est pas de la complexité pour le plaisir, c'est le bon outil au bon endroit. »

| Service | Langage | Justification |
|---|---|---|
| Frontend | TypeScript (Next.js) | Typage bout-en-bout, App Router, très demandé |
| API | PHP (Symfony) | Ma force, maturité, API Platform accélère |
| Worker | Python | Écosystème IA : pypdf, sentence-transformers, SDK Anthropic |

---

## Pattern LLMProvider

Le cœur différenciant du projet.

```python
# worker/interfaces/llm_provider.py
from abc import ABC, abstractmethod
from typing import Generator

class LLMProviderInterface(ABC):
    @abstractmethod
    def extract_structured(
        self,
        document_text: str,
        schema: dict
    ) -> dict:
        """Extraction structurée avec citations."""
        pass

    @abstractmethod
    def generate_report(
        self,
        extracted_data: dict,
        on_chunk: callable = None
    ) -> Generator[str, None, None]:
        """Génération de rapport en streaming."""
        pass
```

```python
# worker/providers/claude_provider.py
import anthropic

class ClaudeProvider(LLMProviderInterface):
    def __init__(self):
        self.client = anthropic.Anthropic()  # clé via env
        self.model = "claude-sonnet-4-5"

    def extract_structured(self, document_text, schema):
        # tool use → JSON structuré + citations
        pass

    def generate_report(self, extracted_data, on_chunk=None):
        # streaming SSE
        with self.client.messages.stream(...) as stream:
            for text in stream.text_stream:
                if on_chunk:
                    on_chunk(text)
                yield text
```

```python
# worker/providers/mistral_provider.py
from mistralai import Mistral

class MistralProvider(LLMProviderInterface):
    def __init__(self):
        self.client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])
        self.model = "mistral-large-latest"
    # ... même interface
```

**Pourquoi ça compte** : ajouter GPT-4, Gemini, ou un modèle open-source local = une seule classe. Zéro refactoring du reste de l'app.

---

## Streaming SSE — les deux bouts

### Côté Symfony (émetteur)

```php
// src/Controller/ReportController.php
#[Route('/api/reports/{id}/stream', methods: ['GET'])]
public function stream(Report $report): StreamedResponse
{
    return new StreamedResponse(function () use ($report) {
        // Lire le contenu du rapport depuis RDS par chunks
        foreach ($this->reportRepository->streamChunks($report) as $chunk) {
            echo "data: " . json_encode(['chunk' => $chunk]) . "\n\n";
            ob_flush();
            flush();
        }
        echo "data: [DONE]\n\n";
        ob_flush();
        flush();
    }, 200, [
        'Content-Type' => 'text/event-stream',
        'Cache-Control' => 'no-cache',
        'X-Accel-Buffering' => 'no',
    ]);
}
```

### Côté Next.js (récepteur)

```typescript
// app/reports/[id]/page.tsx
const streamReport = async (reportId: string) => {
  const response = await fetch(`/api/reports/${reportId}/stream`);
  const reader = response.body!.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    const lines = decoder.decode(value).split('\n\n');
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = JSON.parse(line.slice(6));
        if (data.chunk) setReport(prev => prev + data.chunk);
      }
    }
  }
};
```

---

## Citations anti-hallucination (tool use Claude)

```python
EXTRACTION_TOOL = {
    "name": "extract_data",
    "description": "Extraire des données structurées avec citations",
    "input_schema": {
        "type": "object",
        "properties": {
            "fields": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "field_name": {"type": "string"},
                        "value": {"type": "string"},
                        "citation": {
                            "type": "string",
                            "description": "Extrait exact du document justifiant la valeur"
                        },
                        "confidence": {"type": "number", "minimum": 0, "maximum": 1}
                    }
                }
            }
        }
    }
}
```

Chaque donnée extraite est traçable → confiance du client → argument de vente.

---

## Secrets — sécurité en production

- **Jamais** de clés dans le code ou dans Git
- Clés Anthropic/Mistral dans **AWS Secrets Manager**
- Injectées dans les pods via **External Secrets Operator** (ESO)
- Pods accèdent à AWS via **IRSA** (IAM Roles for Service Accounts) — zéro clé AWS dans les containers

---

## Décisions à documenter en README

Ces choix techniques méritent d'être expliqués dans le README du projet :

1. **Pourquoi polyglotte ?** → cf. [[#Pourquoi polyglotte]]
2. **Pourquoi le pattern Adapter pour les LLM ?** → anti-vendor lock-in, flexibilité RGPD
3. **Pourquoi Mistral en option ?** → hébergement EU, conforme RGPD par défaut
4. **Pourquoi SSE plutôt que WebSocket ?** → plus simple, HTTP natif, pas d'état serveur
5. **Pourquoi tool use pour l'extraction ?** → JSON typé + citations, anti-hallucination

---

*Voir aussi : [[02 - Architecture]] · [[04 - Périmètre MVP]]*
