"""Serviço de dashboard com dados consolidados do AgroCalc."""

from typing import Dict, Any


def obter_dashboard() -> Dict[str, Any]:
    """
    Retorna dados consolidados para o dashboard principal.

    Inclui estatísticas de produção, custos, lucro, talhões e culturas.
    """
    from .talhoes_service import resumo_talhoes

    talhoes = resumo_talhoes()

    area_total = talhoes["area_total"]
    total_talhoes = talhoes["total_talhoes"]
    culturas = talhoes["culturas"]
    qtd_culturas = len(culturas)

    produtividade_media = 62.4
    producao_total = area_total * produtividade_media

    custo_por_ha = 1274.29
    custos_totais = area_total * custo_por_ha

    preco_medio_venda = 120.0
    receita_total = producao_total * preco_medio_venda
    lucro_estimado = receita_total - custos_totais
    margem_liquida = (lucro_estimado / receita_total * 100) if receita_total > 0 else 0

    return {
        "producao_total_sacas": round(producao_total, 2),
        "lucro_estimado": round(lucro_estimado, 2),
        "custos_operacionais": round(custos_totais, 2),
        "produtividade_media_sc_ha": produtividade_media,
        "margem_liquida": round(margem_liquida, 2),
        "area_total_ha": area_total,
        "total_talhoes": total_talhoes,
        "qtd_culturas": qtd_culturas,
        "area_ocupada_percentual": 92.0,
        "culturas": {c: {"area_ha": round(a, 2)} for c, a in culturas.items()},
        "graficos": {
            "producao_mensal": [
                {"mes": "Jan", "sacas": 420},
                {"mes": "Fev", "sacas": 380},
                {"mes": "Mar", "sacas": 510},
                {"mes": "Abr", "sacas": 480},
                {"mes": "Mai", "sacas": 620},
                {"mes": "Jun", "sacas": 590},
                {"mes": "Jul", "sacas": 680},
                {"mes": "Ago", "sacas": 720},
                {"mes": "Set", "sacas": 650},
                {"mes": "Out", "sacas": 780},
                {"mes": "Nov", "sacas": 820},
                {"mes": "Dez", "sacas": 910},
            ],
            "receita_despesas": [
                {"mes": "Jan", "receita": 28, "despesas": 22},
                {"mes": "Fev", "receita": 32, "despesas": 24},
                {"mes": "Mar", "receita": 30, "despesas": 25},
                {"mes": "Abr", "receita": 35, "despesas": 26},
                {"mes": "Mai", "receita": 38, "despesas": 28},
                {"mes": "Jun", "receita": 42, "despesas": 30},
                {"mes": "Jul", "receita": 40, "despesas": 29},
                {"mes": "Ago", "receita": 45, "despesas": 31},
                {"mes": "Set", "receita": 48, "despesas": 33},
                {"mes": "Out", "receita": 52, "despesas": 35},
                {"mes": "Nov", "receita": 55, "despesas": 36},
                {"mes": "Dez", "receita": 62, "despesas": 38},
            ],
        },
    }
