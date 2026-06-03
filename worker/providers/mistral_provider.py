import json
from typing import Generator
from mistralai import Mistral
from interfaces.llm_provider import LLMProviderInterface


EXTRACTION_PROMPT = """Tu es un extracteur de données structurées.
Extrais les champs demandés et retourne UNIQUEMENT un JSON valide avec ce format exact :
{
  "fields": [
    {
      "field": "nom_du_champ",
      "value": "valeur extraite",
      "citation": "citation exacte du passage source dans le document"
    }
  ]
}
Aucun texte avant ou après le JSON."""


class MistralProvider(LLMProviderInterface):

    def __init__(self):
        self.client = Mistral()
        self.model = "mistral-large-latest"

    def extract_structured_data(self, document_text: str, fields: list[str]) -> dict:
        fields_list = ", ".join(fields)

        response = self.client.chat.complete(
            model=self.model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": EXTRACTION_PROMPT},
                {
                    "role": "user",
                    "content": (
                        f"Extrais les champs suivants : {fields_list}.\n\n"
                        f"Document :\n{document_text}"
                    ),
                },
            ],
        )

        raw = response.choices[0].message.content
        parsed = json.loads(raw)
        return {"provider": "mistral", "fields": parsed.get("fields", [])}

    def generate_report_stream(self, extracted_data: dict) -> Generator[str, None, None]:
        fields_summary = "\n".join(
            f"- {f['field']} : {f['value']} (source : {f['citation']})"
            for f in extracted_data.get("fields", [])
        )

        response = self.client.chat.stream(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Génère un rapport d'analyse structuré à partir des données extraites suivantes :\n\n"
                        f"{fields_summary}\n\n"
                        f"Le rapport doit être clair, professionnel, en français."
                    ),
                }
            ],
        )

        for chunk in response:
            delta = chunk.data.choices[0].delta.content
            if delta:
                yield delta
