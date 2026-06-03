import anthropic
from typing import Generator
from interfaces.llm_provider import LLMProviderInterface


EXTRACTION_TOOL = {
    "name": "extract_document_fields",
    "description": "Extrait des champs structurés d'un document avec citation exacte de la source.",
    "input_schema": {
        "type": "object",
        "properties": {
            "fields": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "field": {"type": "string", "description": "Nom du champ extrait"},
                        "value": {"type": "string", "description": "Valeur extraite"},
                        "citation": {"type": "string", "description": "Citation exacte du document source"},
                    },
                    "required": ["field", "value", "citation"],
                },
            }
        },
        "required": ["fields"],
    },
}


class ClaudeProvider(LLMProviderInterface):

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-opus-4-5"

    def extract_structured_data(self, document_text: str, fields: list[str]) -> dict:
        fields_list = ", ".join(fields)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            tools=[EXTRACTION_TOOL],
            tool_choice={"type": "tool", "name": "extract_document_fields"},
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Extrais les champs suivants du document : {fields_list}.\n"
                        f"Pour chaque champ, fournis la valeur ET une citation exacte du passage source.\n\n"
                        f"Document :\n{document_text}"
                    ),
                }
            ],
        )

        for block in response.content:
            if block.type == "tool_use" and block.name == "extract_document_fields":
                return {"provider": "claude", "fields": block.input["fields"]}

        return {"provider": "claude", "fields": []}

    def generate_report_stream(self, extracted_data: dict) -> Generator[str, None, None]:
        fields_summary = "\n".join(
            f"- {f['field']} : {f['value']} (source : {f['citation']})"
            for f in extracted_data.get("fields", [])
        )

        with self.client.messages.stream(
            model=self.model,
            max_tokens=1024,
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
        ) as stream:
            for text in stream.text_stream:
                yield text
