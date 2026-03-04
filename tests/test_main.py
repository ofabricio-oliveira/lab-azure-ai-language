"""
Unit tests for app.main (FastAPI routes and validation).
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app, _validate_text, _validate_features
from fastapi import HTTPException


client = TestClient(app)


# ---------------------------------------------------------------------------
# Index page
# ---------------------------------------------------------------------------

class TestIndexPage:
    def test_index_returns_200(self):
        response = client.get("/")
        assert response.status_code == 200

    def test_index_contains_title(self):
        response = client.get("/")
        assert "Analisador de Textos" in response.text

    def test_index_contains_form(self):
        response = client.get("/")
        assert '<form' in response.text
        assert 'name="text"' in response.text
        assert 'name="features"' in response.text

    def test_index_contains_all_features(self):
        response = client.get("/")
        assert 'value="sentiment"' in response.text
        assert 'value="key_phrases"' in response.text
        assert 'value="entities"' in response.text
        assert 'value="pii"' in response.text
        assert 'value="language"' in response.text


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

class TestValidateText:
    def test_valid_text(self):
        result = _validate_text("Hello World")
        assert result == "Hello World"

    def test_strips_whitespace(self):
        result = _validate_text("  Hello  ")
        assert result == "Hello"

    def test_empty_text_raises(self):
        with pytest.raises(HTTPException) as exc_info:
            _validate_text("")
        assert exc_info.value.status_code == 400
        assert "vazio" in exc_info.value.detail

    def test_whitespace_only_raises(self):
        with pytest.raises(HTTPException) as exc_info:
            _validate_text("   ")
        assert exc_info.value.status_code == 400

    def test_too_long_raises(self):
        long_text = "a" * 6000
        with pytest.raises(HTTPException) as exc_info:
            _validate_text(long_text)
        assert exc_info.value.status_code == 400
        assert "longo" in exc_info.value.detail


class TestValidateFeatures:
    def test_valid_features(self):
        result = _validate_features(["sentiment", "language"])
        assert result == ["sentiment", "language"]

    def test_filters_invalid(self):
        result = _validate_features(["sentiment", "invalid_feature"])
        assert result == ["sentiment"]

    def test_all_invalid_raises(self):
        with pytest.raises(HTTPException) as exc_info:
            _validate_features(["invalid1", "invalid2"])
        assert exc_info.value.status_code == 400

    def test_empty_raises(self):
        with pytest.raises(HTTPException) as exc_info:
            _validate_features([])
        assert exc_info.value.status_code == 400


# ---------------------------------------------------------------------------
# Download route (404 for missing results)
# ---------------------------------------------------------------------------

class TestDownloadRoute:
    def test_missing_result_returns_404(self):
        response = client.get("/download/json/nonexistent")
        assert response.status_code == 404
