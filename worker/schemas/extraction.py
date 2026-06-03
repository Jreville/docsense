from pydantic import BaseModel
from typing import Literal


class ExtractionRequest(BaseModel):
    document_text: str
    fields: list[str]
    provider: Literal["claude", "mistral"] = "claude"


class ExtractedField(BaseModel):
    field: str
    value: str
    citation: str


class ExtractionResponse(BaseModel):
    provider: str
    fields: list[ExtractedField]


class ReportRequest(BaseModel):
    extracted_data: ExtractionResponse
    provider: Literal["claude", "mistral"] = "claude"
