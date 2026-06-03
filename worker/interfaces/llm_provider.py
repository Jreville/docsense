from abc import ABC, abstractmethod
from typing import Generator

class LLMProviderInterface(ABC):
    @abstractmethod
    def extract_structured_data(
        self, 
        document_text: str, 
        fields: list[str]
    ) -> dict:
        """Extraction -> retourne du JSON structuré."""
        pass

    @abstractmethod
    def generate_report_stream(
        self, 
        extracted_data: dict
    ) -> Generator[str, None, None]:
        """Génère le rapport en streaming."""
        pass