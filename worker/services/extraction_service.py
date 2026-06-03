from interfaces.llm_provider import LLMProviderInterface


class ExtractionService:
    def __init__(self, provider: LLMProviderInterface):
        self.provider = provider

    def extract(self, document_text: str, fields: list[str]) -> dict:
        return self.provider.extract_structured_data(document_text, fields)

    def report_stream(self, extracted_data: dict):
        return self.provider.generate_report_stream(extracted_data)
