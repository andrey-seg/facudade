"""Serviço de cálculo de custos agrícolas."""

from typing import Dict, Any


def calcular_custos(dados: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcula os custos operacionais de produção agrícola.

    Args:
        dados: Dicionário com area, sementes, fertilizantes, defensivos,
               mao_obra, irrigacao, transporte, outros, produtividade, preco_venda.

    Returns:
        Dicionário com custo_total, custo_por_ha, receita_total,
        producao_total, lucro_estimado, margem_liquida.
    """
    area = float(dados["area"])
    sementes = float(dados.get("sementes", 0))
    fertilizantes = float(dados.get("fertilizantes", 0))
    defensivos = float(dados.get("defensivos", 0))
    mao_obra = float(dados.get("mao_obra", 0))
    irrigacao = float(dados.get("irrigacao", 0))
    transporte = float(dados.get("transporte", 0))
    outros = float(dados.get("outros", 0))
    produtividade = float(dados.get("produtividade", 0))
    preco_venda = float(dados.get("preco_venda", 0))

    custo_total = sementes + fertilizantes + defensivos + mao_obra + irrigacao + transporte + outros
    custo_por_ha = custo_total / area if area > 0 else 0
    producao_total = area * produtividade
    receita_total = producao_total * preco_venda
    lucro_estimado = receita_total - custo_total
    margem_liquida = (lucro_estimado / receita_total * 100) if receita_total > 0 else 0

    return {
        "custo_total": round(custo_total, 2),
        "custo_por_ha": round(custo_por_ha, 2),
        "receita_total": round(receita_total, 2),
        "producao_total": round(producao_total, 2),
        "lucro_estimado": round(lucro_estimado, 2),
        "margem_liquida": round(margem_liquida, 2),
        "detalhes": {
            "sementes": round(sementes, 2),
            "fertilizantes": round(fertilizantes, 2),
            "defensivos": round(defensivos, 2),
            "mao_obra": round(mao_obra, 2),
            "irrigacao": round(irrigacao, 2),
            "transporte": round(transporte, 2),
            "outros": round(outros, 2),
        },
    }
