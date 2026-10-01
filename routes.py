from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import config
from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()
_generator = None


def get_generator():
    global _generator
    if _generator is None:
        _generator = GeminiDocumentGenerator()
    return _generator


class DocumentRequest(BaseModel):
    document_type: str
    parties: str
    terms: str
    dates: str


@router.get("/health")
def health():
    return {"api_key_loaded": bool(config.GEMINI_API_KEY), "model": config.GEMINI_MODEL}


@router.post("/generate")
def generate_legal_document(request: DocumentRequest):
    try:
        text = get_generator().generate_document(
            request.document_type, request.parties, request.terms, request.dates
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"document": text}
