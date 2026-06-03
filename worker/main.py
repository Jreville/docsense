from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv

from providers.claude_provider import ClaudeProvider
from providers.mistral_provider import MistralProvider
from services.extraction_service import ExtractionService
from schemas.extraction import ExtractionRequest, ExtractionResponse, ReportRequest

load_dotenv()

app = FastAPI(
    title="DocSense Worker",
    description="Worker IA — extraction structurée et génération de rapports (Claude & Mistral)",
    version="0.1.0",
)

PROVIDERS = {
    "claude": ClaudeProvider,
    "mistral": MistralProvider,
}


def get_service(provider_name: str) -> ExtractionService:
    if provider_name not in PROVIDERS:
        raise HTTPException(status_code=400, detail=f"Provider inconnu : {provider_name}. Choix : {list(PROVIDERS.keys())}")
    return ExtractionService(PROVIDERS[provider_name]())


@app.get("/health")
def health():
    return {"status": "ok", "providers": list(PROVIDERS.keys())}


@app.post("/extract", response_model=ExtractionResponse)
def extract(request: ExtractionRequest):
    service = get_service(request.provider)
    result = service.extract(request.document_text, request.fields)
    return result


@app.post("/report/stream")
def report_stream(request: ReportRequest):
    service = get_service(request.provider)

    def generate():
        for chunk in service.report_stream(request.extracted_data.model_dump()):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
