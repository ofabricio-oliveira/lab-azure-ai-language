"""Pydantic models for structured data exchange within the application.

Cada model representa o resultado normalizado de uma feature do Azure AI Language.
São usados para trafegar dados entre o service, o normalizer e os templates.
"""

from typing import List, Optional
from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Sentiment Analysis
# ---------------------------------------------------------------------------

class SentimentSentence(BaseModel):
    """Sentimento de uma frase individual."""
    text: str
    sentiment: str                          # "positive", "negative", "neutral", "mixed"
    positive: float = 0.0
    neutral: float = 0.0
    negative: float = 0.0


class SentimentResult(BaseModel):
    """Resultado da Análise de Sentimento."""
    sentiment: str                          # sentimento geral do documento
    positive: float = 0.0
    neutral: float = 0.0
    negative: float = 0.0
    sentences: List[SentimentSentence] = []


# ---------------------------------------------------------------------------
# Key Phrase Extraction
# ---------------------------------------------------------------------------

class KeyPhrasesResult(BaseModel):
    """Resultado da Extração de Frases-Chave."""
    key_phrases: List[str] = []


# ---------------------------------------------------------------------------
# Named Entity Recognition (NER)
# ---------------------------------------------------------------------------

class RecognizedEntity(BaseModel):
    """Uma entidade reconhecida no texto."""
    text: str
    category: str                           # "Person", "Location", "Organization", "DateTime", etc.
    subcategory: Optional[str] = None
    confidence: float = 0.0


class EntitiesResult(BaseModel):
    """Resultado do Reconhecimento de Entidades (NER)."""
    entities: List[RecognizedEntity] = []


# ---------------------------------------------------------------------------
# PII Detection
# ---------------------------------------------------------------------------

class PiiEntity(BaseModel):
    """Uma entidade PII (dados pessoais) detectada no texto."""
    text: str
    category: str                           # "Email", "PhoneNumber", "CreditCardNumber", etc.
    subcategory: Optional[str] = None
    confidence: float = 0.0


class PiiResult(BaseModel):
    """Resultado da Detecção de PII (Dados Pessoais)."""
    redacted_text: str = ""                 # texto com PII mascarado (ex: "***@***.com")
    entities: List[PiiEntity] = []


# ---------------------------------------------------------------------------
# Language Detection
# ---------------------------------------------------------------------------

class DetectedLanguage(BaseModel):
    """Um idioma detectado no texto."""
    name: str                               # ex: "Portuguese"
    iso_code: str                           # ex: "pt"
    confidence: float = 0.0


class LanguageResult(BaseModel):
    """Resultado da Detecção de Idioma."""
    primary: Optional[DetectedLanguage] = None


# ---------------------------------------------------------------------------
# Combined analysis result (all features in one response)
# ---------------------------------------------------------------------------

class AnalysisResult(BaseModel):
    """Resultado combinado de todas as análises do Azure AI Language."""
    analysis_id: str
    input_text: str
    text_length: int = 0

    sentiment: Optional[SentimentResult] = None
    key_phrases: Optional[KeyPhrasesResult] = None
    entities: Optional[EntitiesResult] = None
    pii: Optional[PiiResult] = None
    language: Optional[LanguageResult] = None

    # Quais features foram solicitadas
    features_requested: List[str] = []
    # Erros por feature (se alguma falhar individualmente)
    errors: dict = {}
