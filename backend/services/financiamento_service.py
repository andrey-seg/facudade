"""Serviço de simulação de financiamento agrícola (SAC e Price)."""

from typing import Dict, Any, List
import math


def simular_financiamento(dados: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simula um financiamento agrícola com tabelas SAC e Price.

    Args:
        dados: Dicionário com valor, entrada, prazo, taxa_anual, finalidade.

    Returns:
        Dicionário com parcela_price, total_pago, total_juros,
        e tabela SAC com amortização, juros, parcela e saldo devedor.
    """
    valor = float(dados["valor"])
    entrada = float(dados.get("entrada", 0))
    prazo = int(dados["prazo"])
    taxa_anual = float(dados["taxa_anual"])
    finalidade = dados.get("finalidade", "custeio")

    valor_financiado = valor - entrada
    taxa_mensal = (taxa_anual / 100) / 12
    meses = prazo * 12

    # Cálculo Price
    if taxa_mensal > 0:
        parcela_price = valor_financiado * (
            taxa_mensal * math.pow(1 + taxa_mensal, meses)
        ) / (math.pow(1 + taxa_mensal, meses) - 1)
    else:
        parcela_price = valor_financiado / meses

    total_pago_price = parcela_price * meses
    total_juros_price = total_pago_price - valor_financiado

    # Tabela SAC
    amortizacao_const = valor_financiado / meses
    tabela_sac: List[Dict[str, Any]] = []
    saldo = valor_financiado

    limite_exibicao = min(meses, 60)
    for i in range(1, limite_exibicao + 1):
        juros = saldo * taxa_mensal
        parcela_sac = amortizacao_const + juros
        saldo_atual = saldo
        saldo -= amortizacao_const
        if saldo < 0:
            saldo = 0
        tabela_sac.append({
            "parcela": i,
            "amortizacao": round(amortizacao_const, 2),
            "juros": round(juros, 2),
            "parcela_sac": round(parcela_sac, 2),
            "saldo_devedor": round(saldo_atual, 2),
        })

    total_amortizacao_sac = amortizacao_const * meses
    total_juros_sac = total_amortizacao_sac - valor_financiado

    return {
        "valor_financiado": round(valor_financiado, 2),
        "prazo_meses": meses,
        "taxa_mensal": round(taxa_mensal * 100, 4),
        "finalidade": finalidade,
        "price": {
            "parcela_mensal": round(parcela_price, 2),
            "total_pago": round(total_pago_price, 2),
            "total_juros": round(total_juros_price, 2),
        },
        "sac": {
            "tabela": tabela_sac,
            "total_amortizacao": round(total_amortizacao_sac, 2),
            "total_juros": round(total_juros_sac, 2),
        },
    }
