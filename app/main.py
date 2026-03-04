"""
Azure AI Language — Analisador de Textos LAB
Main FastAPI application.
"""

import logging
import uuid
from typing import List

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.models import AnalysisResult
from app.services.language_service import (
    AVAILABLE_FEATURES,
    analyze_sentiment,
    detect_language,
    extract_key_phrases,
    get_client,
    recognize_entities,
    recognize_pii_entities,
)
from app.utils.exporter import generate_json
from app.utils.normalizer import build_analysis_result

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = FastAPI(title="Azure AI Language — Analisador de Textos LAB")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")

# Static and template setup
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# In-memory result store (keyed by analysis_id)
# In a real app this would be a database; for this lab a simple dict is enough.
_results: dict = {}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _validate_text(text: str) -> str:
    """Valida e limpa o texto de entrada."""
    text = text.strip()
    if not text:
        raise HTTPException(
            status_code=400,
            detail="Texto vazio. Digite ou cole um texto para analisar.",
        )
    if len(text) > settings.MAX_TEXT_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Texto muito longo ({len(text)} caracteres). "
                f"Máximo permitido: {settings.MAX_TEXT_LENGTH} caracteres."
            ),
        )
    return text


def _validate_features(features: List[str]) -> List[str]:
    """Valida as features selecionadas."""
    valid = [f for f in features if f in AVAILABLE_FEATURES]
    if not valid:
        raise HTTPException(
            status_code=400,
            detail="Selecione pelo menos uma análise para executar.",
        )
    return valid


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the input form."""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "max_length": settings.MAX_TEXT_LENGTH,
            "features": AVAILABLE_FEATURES,
        },
    )


@app.post("/analyze")
async def analyze(
    request: Request,
    text: str = Form(...),
    features: List[str] = Form(...),
):
    """
    Recebe o texto e as features selecionadas, chama o Azure AI Language
    para cada feature, normaliza os resultados e renderiza a página de resultado.

    Fluxo:
    1. Valida texto e features
    2. Cria cliente Azure
    3. Chama cada feature selecionada
    4. Normaliza resultados em AnalysisResult
    5. Renderiza result.html
    """
    analysis_id = uuid.uuid4().hex[:12]
    logger.info("analysis_id=%s — starting (features=%s)", analysis_id, features)

    # --- Validate ---
    text = _validate_text(text)
    features = _validate_features(features)

    # --- Create Azure client ---
    try:
        client = get_client()
    except RuntimeError as exc:
        logger.error("analysis_id=%s — config error: %s", analysis_id, exc)
        raise HTTPException(status_code=500, detail=str(exc))

    documents = [text]

    # --- Call each selected feature ---
    # Cada chamada é independente: se uma falhar, as outras continuam.
    sentiment_raw = None
    key_phrases_raw = None
    entities_raw = None
    pii_raw = None
    language_raw = None

    if "sentiment" in features:
        try:
            sentiment_raw = analyze_sentiment(client, documents)
        except Exception as exc:
            logger.error("analysis_id=%s — sentiment failed: %s", analysis_id, exc)

    if "key_phrases" in features:
        try:
            key_phrases_raw = extract_key_phrases(client, documents)
        except Exception as exc:
            logger.error("analysis_id=%s — key_phrases failed: %s", analysis_id, exc)

    if "entities" in features:
        try:
            entities_raw = recognize_entities(client, documents)
        except Exception as exc:
            logger.error("analysis_id=%s — entities failed: %s", analysis_id, exc)

    if "pii" in features:
        try:
            pii_raw = recognize_pii_entities(client, documents)
        except Exception as exc:
            logger.error("analysis_id=%s — pii failed: %s", analysis_id, exc)

    if "language" in features:
        try:
            language_raw = detect_language(client, documents)
        except Exception as exc:
            logger.error("analysis_id=%s — language failed: %s", analysis_id, exc)

    # --- Normalize & build result ---
    result = build_analysis_result(
        analysis_id=analysis_id,
        input_text=text,
        features=features,
        sentiment_raw=sentiment_raw,
        key_phrases_raw=key_phrases_raw,
        entities_raw=entities_raw,
        pii_raw=pii_raw,
        language_raw=language_raw,
    )

    _results[analysis_id] = result
    logger.info("analysis_id=%s — done (%d features)", analysis_id, len(features))

    return templates.TemplateResponse(
        "result.html",
        {"request": request, "result": result, "feature_names": AVAILABLE_FEATURES},
    )


# ---------------------------------------------------------------------------
# Download route
# ---------------------------------------------------------------------------

def _get_result(analysis_id: str) -> AnalysisResult:
    """Retrieve a cached result or raise 404."""
    result = _results.get(analysis_id)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Resultado não encontrado. Execute uma nova análise.",
        )
    return result


@app.get("/download/json/{analysis_id}")
async def download_json(analysis_id: str):
    """Download analysis result as JSON."""
    result = _get_result(analysis_id)
    json_text = generate_json(result)
    logger.info("analysis_id=%s — JSON download", analysis_id)
    return Response(
        content=json_text,
        media_type="application/json",
        headers={
            "Content-Disposition": f'attachment; filename="analysis_{analysis_id}.json"'
        },
    )
