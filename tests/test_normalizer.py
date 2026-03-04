"""
Unit tests for app.utils.normalizer

Testa a normalização dos resultados do Azure AI Language.
Usa mock objects que simulam a estrutura retornada pelo SDK.
"""

import pytest
from app.utils.normalizer import (
    normalize_sentiment,
    normalize_key_phrases,
    normalize_entities,
    normalize_pii,
    normalize_language,
    build_analysis_result,
)


# ---------------------------------------------------------------------------
# Mock helpers — simulam os objetos retornados pelo SDK
# ---------------------------------------------------------------------------

class MockConfidenceScores:
    def __init__(self, positive=0.0, neutral=0.0, negative=0.0):
        self.positive = positive
        self.neutral = neutral
        self.negative = negative


class MockSentence:
    def __init__(self, text, sentiment, positive=0.0, neutral=0.0, negative=0.0):
        self.text = text
        self.sentiment = sentiment
        self.confidence_scores = MockConfidenceScores(positive, neutral, negative)
        self.mined_opinions = []


class MockSentimentDoc:
    def __init__(self, sentiment, positive, neutral, negative, sentences=None, is_error=False, error=None):
        self.sentiment = sentiment
        self.confidence_scores = MockConfidenceScores(positive, neutral, negative)
        self.sentences = sentences or []
        self.is_error = is_error
        self.error = error


class MockKeyPhrasesDoc:
    def __init__(self, key_phrases=None, is_error=False, error=None):
        self.key_phrases = key_phrases or []
        self.is_error = is_error
        self.error = error


class MockEntity:
    def __init__(self, text, category, subcategory=None, confidence_score=0.0):
        self.text = text
        self.category = category
        self.subcategory = subcategory
        self.confidence_score = confidence_score


class MockEntitiesDoc:
    def __init__(self, entities=None, is_error=False, error=None):
        self.entities = entities or []
        self.is_error = is_error
        self.error = error


class MockPiiEntity:
    def __init__(self, text, category, subcategory=None, confidence_score=0.0):
        self.text = text
        self.category = category
        self.subcategory = subcategory
        self.confidence_score = confidence_score


class MockPiiDoc:
    def __init__(self, redacted_text="", entities=None, is_error=False, error=None):
        self.redacted_text = redacted_text
        self.entities = entities or []
        self.is_error = is_error
        self.error = error


class MockPrimaryLanguage:
    def __init__(self, name, iso6391_name, confidence_score=0.0):
        self.name = name
        self.iso6391_name = iso6391_name
        self.confidence_score = confidence_score


class MockLanguageDoc:
    def __init__(self, primary_language=None, is_error=False, error=None):
        self.primary_language = primary_language
        self.is_error = is_error
        self.error = error


# ---------------------------------------------------------------------------
# normalize_sentiment
# ---------------------------------------------------------------------------

class TestNormalizeSentiment:
    def test_positive_sentiment(self):
        doc = MockSentimentDoc(
            sentiment="positive", positive=0.95, neutral=0.03, negative=0.02,
            sentences=[
                MockSentence("Adorei o produto!", "positive", 0.98, 0.01, 0.01),
            ]
        )
        result = normalize_sentiment([doc])
        assert result is not None
        assert result.sentiment == "positive"
        assert result.positive == 0.95
        assert len(result.sentences) == 1
        assert result.sentences[0].text == "Adorei o produto!"

    def test_negative_sentiment(self):
        doc = MockSentimentDoc(
            sentiment="negative", positive=0.05, neutral=0.10, negative=0.85,
            sentences=[
                MockSentence("Péssimo atendimento.", "negative", 0.02, 0.08, 0.90),
            ]
        )
        result = normalize_sentiment([doc])
        assert result is not None
        assert result.sentiment == "negative"
        assert result.negative == 0.85

    def test_mixed_sentiment_multiple_sentences(self):
        doc = MockSentimentDoc(
            sentiment="mixed", positive=0.50, neutral=0.10, negative=0.40,
            sentences=[
                MockSentence("A comida estava boa.", "positive", 0.85, 0.10, 0.05),
                MockSentence("Mas o serviço foi horrível.", "negative", 0.05, 0.10, 0.85),
            ]
        )
        result = normalize_sentiment([doc])
        assert result is not None
        assert result.sentiment == "mixed"
        assert len(result.sentences) == 2
        assert result.sentences[0].sentiment == "positive"
        assert result.sentences[1].sentiment == "negative"

    def test_neutral_sentiment(self):
        doc = MockSentimentDoc(
            sentiment="neutral", positive=0.10, neutral=0.80, negative=0.10,
        )
        result = normalize_sentiment([doc])
        assert result is not None
        assert result.sentiment == "neutral"
        assert result.neutral == 0.80

    def test_error_returns_none(self):
        doc = MockSentimentDoc(
            sentiment="", positive=0, neutral=0, negative=0,
            is_error=True, error="Service error"
        )
        result = normalize_sentiment([doc])
        assert result is None

    def test_empty_list_returns_none(self):
        result = normalize_sentiment([])
        assert result is None

    def test_none_returns_none(self):
        result = normalize_sentiment(None)
        assert result is None


# ---------------------------------------------------------------------------
# normalize_key_phrases
# ---------------------------------------------------------------------------

class TestNormalizeKeyPhrases:
    def test_basic_extraction(self):
        doc = MockKeyPhrasesDoc(key_phrases=["inteligência artificial", "Azure", "análise de textos"])
        result = normalize_key_phrases([doc])
        assert result is not None
        assert len(result.key_phrases) == 3
        assert "Azure" in result.key_phrases

    def test_empty_phrases(self):
        doc = MockKeyPhrasesDoc(key_phrases=[])
        result = normalize_key_phrases([doc])
        assert result is not None
        assert result.key_phrases == []

    def test_error_returns_none(self):
        doc = MockKeyPhrasesDoc(is_error=True, error="Service error")
        result = normalize_key_phrases([doc])
        assert result is None

    def test_none_returns_none(self):
        result = normalize_key_phrases(None)
        assert result is None


# ---------------------------------------------------------------------------
# normalize_entities
# ---------------------------------------------------------------------------

class TestNormalizeEntities:
    def test_multiple_entities(self):
        doc = MockEntitiesDoc(entities=[
            MockEntity("Microsoft", "Organization", confidence_score=0.98),
            MockEntity("São Paulo", "Location", subcategory="City", confidence_score=0.95),
            MockEntity("2026", "DateTime", subcategory="DateRange", confidence_score=0.90),
        ])
        result = normalize_entities([doc])
        assert result is not None
        assert len(result.entities) == 3
        assert result.entities[0].text == "Microsoft"
        assert result.entities[0].category == "Organization"
        assert result.entities[1].subcategory == "City"

    def test_empty_entities(self):
        doc = MockEntitiesDoc(entities=[])
        result = normalize_entities([doc])
        assert result is not None
        assert result.entities == []

    def test_error_returns_none(self):
        doc = MockEntitiesDoc(is_error=True, error="Service error")
        result = normalize_entities([doc])
        assert result is None

    def test_none_returns_none(self):
        result = normalize_entities(None)
        assert result is None

    def test_entity_confidence(self):
        doc = MockEntitiesDoc(entities=[
            MockEntity("Fabricio", "Person", confidence_score=0.92),
        ])
        result = normalize_entities([doc])
        assert result.entities[0].confidence == 0.92


# ---------------------------------------------------------------------------
# normalize_pii
# ---------------------------------------------------------------------------

class TestNormalizePii:
    def test_pii_detected(self):
        doc = MockPiiDoc(
            redacted_text="Meu e-mail é ***@***.com e meu CPF é ***.***.***-**",
            entities=[
                MockPiiEntity("joao@email.com", "Email", confidence_score=0.99),
                MockPiiEntity("123.456.789-00", "BRCPFNumber", confidence_score=0.97),
            ]
        )
        result = normalize_pii([doc])
        assert result is not None
        assert "***" in result.redacted_text
        assert len(result.entities) == 2
        assert result.entities[0].category == "Email"
        assert result.entities[1].category == "BRCPFNumber"

    def test_no_pii_found(self):
        doc = MockPiiDoc(
            redacted_text="O tempo está bom hoje.",
            entities=[]
        )
        result = normalize_pii([doc])
        assert result is not None
        assert result.entities == []
        assert result.redacted_text == "O tempo está bom hoje."

    def test_pii_with_phone(self):
        doc = MockPiiDoc(
            redacted_text="Ligue para ************",
            entities=[
                MockPiiEntity("+55 11 99999-0000", "PhoneNumber", confidence_score=0.95),
            ]
        )
        result = normalize_pii([doc])
        assert result.entities[0].text == "+55 11 99999-0000"

    def test_error_returns_none(self):
        doc = MockPiiDoc(is_error=True, error="Service error")
        result = normalize_pii([doc])
        assert result is None

    def test_none_returns_none(self):
        result = normalize_pii(None)
        assert result is None


# ---------------------------------------------------------------------------
# normalize_language
# ---------------------------------------------------------------------------

class TestNormalizeLanguage:
    def test_portuguese(self):
        doc = MockLanguageDoc(
            primary_language=MockPrimaryLanguage("Portuguese", "pt", 1.0)
        )
        result = normalize_language([doc])
        assert result is not None
        assert result.primary.name == "Portuguese"
        assert result.primary.iso_code == "pt"
        assert result.primary.confidence == 1.0

    def test_english(self):
        doc = MockLanguageDoc(
            primary_language=MockPrimaryLanguage("English", "en", 0.98)
        )
        result = normalize_language([doc])
        assert result.primary.name == "English"
        assert result.primary.iso_code == "en"

    def test_spanish(self):
        doc = MockLanguageDoc(
            primary_language=MockPrimaryLanguage("Spanish", "es", 0.95)
        )
        result = normalize_language([doc])
        assert result.primary.iso_code == "es"

    def test_error_returns_none(self):
        doc = MockLanguageDoc(is_error=True, error="Service error")
        result = normalize_language([doc])
        assert result is None

    def test_none_returns_none(self):
        result = normalize_language(None)
        assert result is None


# ---------------------------------------------------------------------------
# build_analysis_result
# ---------------------------------------------------------------------------

class TestBuildAnalysisResult:
    def test_all_features(self):
        sentiment_raw = [MockSentimentDoc("positive", 0.90, 0.05, 0.05, sentences=[
            MockSentence("Texto positivo.", "positive", 0.90, 0.05, 0.05)
        ])]
        key_phrases_raw = [MockKeyPhrasesDoc(["Azure", "análise"])]
        entities_raw = [MockEntitiesDoc([MockEntity("Azure", "Organization", confidence_score=0.95)])]
        pii_raw = [MockPiiDoc("Texto limpo.", [])]
        language_raw = [MockLanguageDoc(MockPrimaryLanguage("Portuguese", "pt", 1.0))]

        result = build_analysis_result(
            analysis_id="test123",
            input_text="Texto positivo. Azure é ótimo.",
            features=["sentiment", "key_phrases", "entities", "pii", "language"],
            sentiment_raw=sentiment_raw,
            key_phrases_raw=key_phrases_raw,
            entities_raw=entities_raw,
            pii_raw=pii_raw,
            language_raw=language_raw,
        )

        assert result.analysis_id == "test123"
        assert result.text_length == len("Texto positivo. Azure é ótimo.")
        assert result.sentiment is not None
        assert result.sentiment.sentiment == "positive"
        assert result.key_phrases is not None
        assert "Azure" in result.key_phrases.key_phrases
        assert result.entities is not None
        assert len(result.entities.entities) == 1
        assert result.pii is not None
        assert result.language is not None
        assert result.language.primary.iso_code == "pt"
        assert result.errors == {}
        assert len(result.features_requested) == 5

    def test_partial_features(self):
        """Testa com apenas algumas features selecionadas."""
        sentiment_raw = [MockSentimentDoc("neutral", 0.10, 0.80, 0.10)]

        result = build_analysis_result(
            analysis_id="partial01",
            input_text="Teste parcial.",
            features=["sentiment"],
            sentiment_raw=sentiment_raw,
        )

        assert result.sentiment is not None
        assert result.key_phrases is None
        assert result.entities is None
        assert result.pii is None
        assert result.language is None
        assert len(result.features_requested) == 1

    def test_no_raw_data(self):
        """Testa quando nenhum dado bruto é passado (todas as chamadas falharam)."""
        result = build_analysis_result(
            analysis_id="empty01",
            input_text="Teste sem dados.",
            features=["sentiment", "key_phrases"],
        )

        assert result.sentiment is None
        assert result.key_phrases is None

    def test_text_length_calculated(self):
        text = "Hello World!"
        result = build_analysis_result(
            analysis_id="len01",
            input_text=text,
            features=[],
        )
        assert result.text_length == 12

    def test_features_requested_preserved(self):
        result = build_analysis_result(
            analysis_id="feat01",
            input_text="Test",
            features=["sentiment", "language"],
        )
        assert result.features_requested == ["sentiment", "language"]
