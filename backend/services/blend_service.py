"""Serviço de cálculo de blend de fertilizantes NPK."""

from typing import Dict, Any

# Preços médios por kg de nutriente (R$/kg)
PRECOS_NUTRIENTES = {
    "n": 4.50,
    "p": 6.20,
    "k": 3.80,
}

# Recomendações NPK por cultura (%)
RECOMENDACOES_NPK = {
    "soja": {"n": 20, "p": 30, "k": 50},
    "milho": {"n": 40, "p": 25, "k": 35},
    "cafe": {"n": 25, "p": 20, "k": 55},
    "algodao": {"n": 35, "p": 30, "k": 35},
}


def calcular_blend(dados: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcula a composição e custo de um blend de fertilizantes NPK.

    Args:
        dados: Dicionário com nome, area, n, p, k, tipo_cultura, dose.

    Returns:
        Dicionário com composição NPK, quantidades por nutriente,
        total do blend, custo total, e recomendação para a cultura.
    """
    nome = dados.get("nome", "Blend Personalizado")
    area = float(dados["area"])
    n = float(dados.get("n", 0))
    p = float(dados.get("p", 0))
    k = float(dados.get("k", 0))
    tipo_cultura = dados.get("tipo_cultura", "soja")
    dose = float(dados["dose"])

    total_pct = n + p + k
    if total_pct == 0:
        n = p = k = 33.33
        total_pct = 100.0

    pct_n = round((n / total_pct) * 100, 1)
    pct_p = round((p / total_pct) * 100, 1)
    pct_k = round((k / total_pct) * 100, 1)

    total_blend_kg = area * dose

    kg_n = total_blend_kg * (pct_n / 100)
    kg_p = total_blend_kg * (pct_p / 100)
    kg_k = total_blend_kg * (pct_k / 100)

    custo_n = kg_n * PRECOS_NUTRIENTES["n"]
    custo_p = kg_p * PRECOS_NUTRIENTES["p"]
    custo_k = kg_k * PRECOS_NUTRIENTES["k"]
    custo_total = custo_n + custo_p + custo_k

    recomendacao = RECOMENDACOES_NPK.get(tipo_cultura, {})

    return {
        "nome": nome,
        "area": area,
        "dose_kg_ha": dose,
        "tipo_cultura": tipo_cultura,
        "composicao": {
            "n": {"percentual": pct_n, "kg": round(kg_n, 2), "custo": round(custo_n, 2)},
            "p": {"percentual": pct_p, "kg": round(kg_p, 2), "custo": round(custo_p, 2)},
            "k": {"percentual": pct_k, "kg": round(kg_k, 2), "custo": round(custo_k, 2)},
        },
        "total_blend_kg_ha": dose,
        "quantidade_total_kg": round(total_blend_kg, 2),
        "custo_total": round(custo_total, 2),
        "custo_por_ha": round(custo_total / area, 2) if area > 0 else 0,
        "recomendacao_cultura": recomendacao,
    }
