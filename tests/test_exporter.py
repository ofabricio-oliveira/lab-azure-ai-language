"""
Unit tests for app.utils.exporter (JSON generation).
"""

import json
import pytest

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
from app.utils.exporter import generate_json


@pytest.fixture
def full_result():
    """Um AnalysisResult completo com todas as features."""
    return AnalysisResult(
        analysis_id="exp001",
        input_text="Adorei o atendimento da Microsoft em São Paulo. Meu e-mail é joao@test.com.",
        text_length=73,
        features_requested=["sentiment", "key_phrases", "entities", "pii", "language"],
        sentiment=SentimentResult(
            sentiment="positive",
            positive=0.90,
            neutral=0.05,
            negative=0.05,
            sentences=[
                SentimentSentence(
                    text="Adorei o atendimento da Microsoft em São Paulo.",
                    sentiment="positive",
                    positive=0.95,
                    neutral=0.03,
                    negative=0.02,
                ),
            ],
        ),
        key_phrases=KeyPhrasesResult(
            key_phrases=["atendimento", "Microsoft", "São Paulo"],
        ),
        entities=EntitiesResult(
            entities=[
                RecognizedEntity(text="Microsoft", category="Organization", confidence=0.98),
                RecognizedEntity(text="São Paulo", category="Location", subcategory="City", confidence=0.95),
            ],
        ),
        pii=PiiResult(
            redacted_text="Adorei o atendimento da Microsoft em São Paulo. Meu e-mail é *************.",
            entities=[
                PiiEntity(text="joao@test.com", category="Email", confidence=0.99),
            ],
        ),
        language=LanguageResult(
            primary=DetectedLanguage(name="Portuguese", iso_code="pt", confidence=1.0),
        ),
    )


@pytest.fixture
def minimal_result():
    """Um AnalysisResult com apenas uma feature."""
    return AnalysisResult(
        analysis_id="exp002",
        input_text="Hello World",
        text_length=11,
        features_requested=["language"],
        language=LanguageResult(
            primary=DetectedLanguage(name="English", iso_code="en", confidence=0.99),
        ),
    )


# ---------------------------------------------------------------------------
# generate_json
# ---------------------------------------------------------------------------

class TestGenerateJson:
    def test_full_result_is_valid_json(self, full_result):
        json_text = generate_json(full_result)
        data = json.loads(json_text)
        assert data["analysis_id"] == "exp001"

    def test_contains_all_features(self, full_result):
        json_text = generate_json(full_result)
        data = json.loads(json_text)
        assert "sentiment" in data
        assert "key_phrases" in data
        assert "entities" in data
        assert "pii" in data
        assert "language" in data

    def test_sentiment_data(self, full_result):
        data = json.loads(generate_json(full_result))
        assert data["sentiment"]["sentiment"] == "positive"
        assert data["sentiment"]["positive"] == 0.90
        assert len(data["sentiment"]["sentences"]) == 1

    def test_key_phrases_data(self, full_result):
        data = json.loads(generate_json(full_result))
        assert "Microsoft" in data["key_phrases"]["key_phrases"]

    def test_entities_data(self, full_result):
        data = json.loads(generate_json(full_result))
        assert len(data["entities"]["entities"]) == 2
        assert data["entities"]["entities"][0]["category"] == "Organization"

    def test_pii_data(self, full_result):
        data = json.loads(generate_json(full_result))
        assert "*" in data["pii"]["redacted_text"]
        assert data["pii"]["entities"][0]["category"] == "Email"

    def test_language_data(self, full_result):
        data = json.loads(generate_json(full_result))
        assert data["language"]["primary"]["iso_code"] == "pt"

    def test_minimal_result(self, minimal_result):
        json_text = generate_json(minimal_result)
        data = json.loads(json_text)
        assert data["analysis_id"] == "exp002"
        assert data["language"]["primary"]["iso_code"] == "en"
        # Features not requested should be excluded (exclude_none)
        assert "sentiment" not in data
        assert "key_phrases" not in data

    def test_preserves_unicode(self, full_result):
        """Garante que caracteres Unicode (acentos) são preservados no JSON."""
        json_text = generate_json(full_result)
        assert "São Paulo" in json_text
        assert "Adorei" in json_text

    def test_features_requested_in_output(self, full_result):
        data = json.loads(generate_json(full_result))
        assert data["features_requested"] == ["sentiment", "key_phrases", "entities", "pii", "language"]
