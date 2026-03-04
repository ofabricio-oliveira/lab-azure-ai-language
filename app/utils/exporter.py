"""Exportação dos resultados da análise para JSON.

Gera um arquivo JSON estruturado com todos os resultados, ideal para
integração com outros sistemas ou para documentação da análise.
"""

import json
from typing import Union

from app.models import AnalysisResult


def generate_json(result: AnalysisResult) -> str:
    """Gera um JSON formatado com o resultado completo da análise.

    Usa model_dump() do Pydantic para serializar todos os campos,
    incluindo apenas os que têm valor (exclude_none=True).
    """
    data = result.model_dump(exclude_none=True)
    return json.dumps(data, indent=2, ensure_ascii=False)
