"""Normalização dos resultados do Azure AI Language.

Converte os objetos retornados pelo SDK (azure-ai-textanalytics) nos
Pydantic models do app, tratando erros individuais por feature.
"""

import logging
from typing import List, Optional

from app.models import (
    AnalysisResult,
    DetectedLanguage,
    EntitiesResult,
    KeyPhrasesResult,
    LanguageResult,
    PiiEntity,
    PiiResult,
    RecognizedEntity,
    SentimentResult,
    SentimentSentence,
)

logger = logging.getLogger("app.utils.normalizer")


def normalize_sentiment(raw_result) -> Optional[SentimentResult]:
    """Normaliza o resultado de analyze_sentiment.

    O SDK retorna uma lista de DocumentSentiment. Como neste lab enviamos
    sempre 1 documento, pegamos o primeiro item.
    """
    if not raw_result:
        return None

    doc = raw_result[0]
    if doc.is_error:
        logger.warning("Sentiment analysis error: %s", doc.error)
        return None

    sentences = []
    for s in doc.sentences:
        sentences.append(SentimentSentence(
            text=s.text,
            sentiment=s.sentiment,
            positive=s.confidence_scores.positive,
            neutral=s.confidence_scores.neutral,
            negative=s.confidence_scores.negative,
        ))

    return SentimentResult(
        sentiment=doc.sentiment,
        positive=doc.confidence_scores.positive,
        neutral=doc.confidence_scores.neutral,
        negative=doc.confidence_scores.negative,
        sentences=sentences,
    )


def normalize_key_phrases(raw_result) -> Optional[KeyPhrasesResult]:
    """Normaliza o resultado de extract_key_phrases.

    Retorna a lista de frases-chave extraídas do documento.
    """
    if not raw_result:
        return None

    doc = raw_result[0]
    if doc.is_error:
        logger.warning("Key phrases error: %s", doc.error)
        return None

    return KeyPhrasesResult(key_phrases=list(doc.key_phrases))


def normalize_entities(raw_result) -> Optional[EntitiesResult]:
    """Normaliza o resultado de recognize_entities.

    Cada entidade tem: text, category, subcategory e confidence_score.
    """
    if not raw_result:
        return None

    doc = raw_result[0]
    if doc.is_error:
        logger.warning("NER error: %s", doc.error)
        return None

    entities = []
    for e in doc.entities:
        entities.append(RecognizedEntity(
            text=e.text,
            category=e.category,
            subcategory=e.subcategory,
            confidence=e.confidence_score,
        ))

    return EntitiesResult(entities=entities)


def normalize_pii(raw_result) -> Optional[PiiResult]:
    """Normaliza o resultado de recognize_pii_entities.

    Retorna o texto com PII mascarado e a lista de entidades PII.
    """
    if not raw_result:
        return None

    doc = raw_result[0]
    if doc.is_error:
        logger.warning("PII error: %s", doc.error)
        return None

    entities = []
    for e in doc.entities:
        entities.append(PiiEntity(
            text=e.text,
            category=e.category,
            subcategory=e.subcategory,
            confidence=e.confidence_score,
        ))

    return PiiResult(
        redacted_text=doc.redacted_text,
        entities=entities,
    )


def normalize_language(raw_result) -> Optional[LanguageResult]:
    """Normaliza o resultado de detect_language.

    Retorna o idioma primário detectado com nome, código ISO e confiança.
    """
    if not raw_result:
        return None

    doc = raw_result[0]
    if doc.is_error:
        logger.warning("Language detection error: %s", doc.error)
        return None

    lang = doc.primary_language
    return LanguageResult(
        primary=DetectedLanguage(
            name=lang.name,
            iso_code=lang.iso6391_name,
            confidence=lang.confidence_score,
        )
    )


def build_analysis_result(
    analysis_id: str,
    input_text: str,
    features: List[str],
    sentiment_raw=None,
    key_phrases_raw=None,
    entities_raw=None,
    pii_raw=None,
    language_raw=None,
) -> AnalysisResult:
    """Constrói o AnalysisResult combinado a partir dos resultados brutos.

    Cada feature é normalizada independentemente. Se uma falhar, as demais
    continuam funcionando — o erro é registrado no campo 'errors'.
    """
    errors = {}
    sentiment = None
    key_phrases = None
    entities = None
    pii = None
    language = None

    if "sentiment" in features:
        try:
            sentiment = normalize_sentiment(sentiment_raw)
        except Exception as exc:
            logger.error("Error normalizing sentiment: %s", exc)
            errors["sentiment"] = str(exc)

    if "key_phrases" in features:
        try:
            key_phrases = normalize_key_phrases(key_phrases_raw)
        except Exception as exc:
            logger.error("Error normalizing key phrases: %s", exc)
            errors["key_phrases"] = str(exc)

    if "entities" in features:
        try:
            entities = normalize_entities(entities_raw)
        except Exception as exc:
            logger.error("Error normalizing entities: %s", exc)
            errors["entities"] = str(exc)

    if "pii" in features:
        try:
            pii = normalize_pii(pii_raw)
        except Exception as exc:
            logger.error("Error normalizing PII: %s", exc)
            errors["pii"] = str(exc)

    if "language" in features:
        try:
            language = normalize_language(language_raw)
        except Exception as exc:
            logger.error("Error normalizing language: %s", exc)
            errors["language"] = str(exc)

    return AnalysisResult(
        analysis_id=analysis_id,
        input_text=input_text,
        text_length=len(input_text),
        sentiment=sentiment,
        key_phrases=key_phrases,
        entities=entities,
        pii=pii,
        language=language,
        features_requested=features,
        errors=errors,
    )
