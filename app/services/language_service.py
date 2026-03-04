"""Azure AI Language service — Text Analytics.

Envia textos para a API do Azure AI Language e retorna os resultados brutos.
Suporta 5 features preconfigured: Sentiment, Key Phrases, NER, PII e Language Detection.

Referências:
- SDK: https://pypi.org/project/azure-ai-textanalytics/
- Docs: https://learn.microsoft.com/en-us/azure/ai-services/language-service/overview
"""

import logging
from typing import List

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

from app.config import settings

logger = logging.getLogger("app.services.language_service")

# Features disponíveis neste lab
AVAILABLE_FEATURES = {
    "sentiment":   "Análise de Sentimento",
    "key_phrases": "Extração de Frases-Chave",
    "entities":    "Reconhecimento de Entidades (NER)",
    "pii":         "Detecção de PII (Dados Pessoais)",
    "language":    "Detecção de Idioma",
}


def get_client() -> TextAnalyticsClient:
    """Cria o cliente do Azure AI Language usando endpoint + key do .env.

    O TextAnalyticsClient é o ponto de entrada do SDK para todas as
    features de Text Analytics do Azure AI Language.
    """
    if not settings.AZURE_LANGUAGE_ENDPOINT or not settings.AZURE_LANGUAGE_KEY:
        raise RuntimeError(
            "Azure AI Language not configured. "
            "Set AZURE_LANGUAGE_ENDPOINT and AZURE_LANGUAGE_KEY in your .env file."
        )
    return TextAnalyticsClient(
        endpoint=settings.AZURE_LANGUAGE_ENDPOINT.rstrip("/"),
        credential=AzureKeyCredential(settings.AZURE_LANGUAGE_KEY),
    )


def analyze_sentiment(client: TextAnalyticsClient, documents: List[str]) -> list:
    """Análise de Sentimento — identifica sentimento positivo, negativo, neutro ou misto.

    Também retorna opinion mining (análise de aspectos) para cada frase,
    conectando opiniões a alvos específicos no texto.

    Docs: https://learn.microsoft.com/en-us/azure/ai-services/language-service/sentiment-opinion-mining/overview
    """
    logger.info("Calling analyze_sentiment (%d documents)", len(documents))
    return client.analyze_sentiment(documents, show_opinion_mining=True)


def extract_key_phrases(client: TextAnalyticsClient, documents: List[str]) -> list:
    """Extração de Frases-Chave — identifica os termos e conceitos mais relevantes.

    Útil para resumir ou indexar grandes volumes de texto rapidamente.

    Docs: https://learn.microsoft.com/en-us/azure/ai-services/language-service/key-phrase-extraction/overview
    """
    logger.info("Calling extract_key_phrases (%d documents)", len(documents))
    return client.extract_key_phrases(documents)


def recognize_entities(client: TextAnalyticsClient, documents: List[str]) -> list:
    """Reconhecimento de Entidades (NER) — detecta e categoriza entidades no texto.

    Categorias: Person, Location, Organization, DateTime, Quantity, etc.
    O NER é preconfigured — não precisa treinar modelo.

    Docs: https://learn.microsoft.com/en-us/azure/ai-services/language-service/named-entity-recognition/overview
    """
    logger.info("Calling recognize_entities (%d documents)", len(documents))
    return client.recognize_entities(documents)


def recognize_pii_entities(client: TextAnalyticsClient, documents: List[str]) -> list:
    """Detecção de PII — identifica e redige dados pessoais no texto.

    Detecta: e-mail, telefone, CPF/SSN, cartão de crédito, endereço, nomes, etc.
    Retorna o texto com PII mascarado (redacted_text) e a lista de entidades.

    Docs: https://learn.microsoft.com/en-us/azure/ai-services/language-service/personally-identifiable-information/overview
    """
    logger.info("Calling recognize_pii_entities (%d documents)", len(documents))
    return client.recognize_pii_entities(documents)


def detect_language(client: TextAnalyticsClient, documents: List[str]) -> list:
    """Detecção de Idioma — identifica o idioma predominante do texto.

    Suporta mais de 100 idiomas e dialetos. Retorna o nome, código ISO e
    score de confiança.

    Docs: https://learn.microsoft.com/en-us/azure/ai-services/language-service/language-detection/overview
    """
    logger.info("Calling detect_language (%d documents)", len(documents))
    return client.detect_language(documents)
