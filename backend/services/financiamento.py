"""Módulo de cálculo de Financiamento Agrícola (Sistema Price)."""

from typing import Dict, Any, List
import math
import csv
from io import StringIO


def calcular_parcela(valor: float, taxa_juros: float, num_parcelas: int) -> float:
    """
    Calcula o valor da parcela pelo sistema Price (PMT).

    Fórmula: PMT = PV * [i * (1+i)^n] / [(1+i)^n - 1]

    Args:
        valor: Valor financiado (PV).
        taxa_juros: Taxa de juros mensal em decimal (ex: 0.01 para 1%).
        num_parcelas: Número de parcelas (n).

    Returns:
        Valor da parcela mensal (PMT).
    """
    if taxa_juros > 0:
        pmt = valor * (
            taxa_juros * math.pow(1 + taxa_juros, num_parcelas)
        ) / (math.pow(1 + taxa_juros, num_parcelas) - 1)
    else:
        pmt = valor / num_parcelas
    return pmt


def tabela_amortizacao(
    valor: float, taxa_juros: float, num_parcelas: int
) -> List[Dict[str, Any]]:
    """
    Gera a tabela de amortização completa (sistema Price).

    Cada entrada contém: parcela, amortizacao, juros, saldo_devedor.

    Args:
        valor: Valor financiado (PV).
        taxa_juros: Taxa de juros mensal em decimal.
        num_parcelas: Número de parcelas.

    Returns:
        Lista com dicionários da tabela de amortização.
    """
    parcela = calcular_parcela(valor, taxa_juros, num_parcelas)
    tabela: List[Dict[str, Any]] = []
    saldo = valor

    for i in range(1, num_parcelas + 1):
        juros = saldo * taxa_juros
        amortizacao = parcela - juros
        if amortizacao < 0:
            amortizacao = 0
        saldo_atual = saldo
        saldo -= amortizacao
        if saldo < 0:
            saldo = 0

        tabela.append({
            "parcela": i,
            "amortizacao": round(amortizacao, 2),
            "juros": round(juros, 2),
            "parcela_total": round(parcela, 2),
            "saldo_devedor": round(saldo, 2),
        })

    return tabela


def simular(valor: float, taxa_juros: float, num_parcelas: int) -> Dict[str, Any]:
    """
    Função principal que executa a simulação completa do financiamento.

    Args:
        valor: Valor financiado.
        taxa_juros: Taxa de juros mensal em decimal.
        num_parcelas: Número de parcelas.

    Returns:
        Dicionário com parcela, tabela, total_pago, total_juros.
    """
    parcela = calcular_parcela(valor, taxa_juros, num_parcelas)
    tabela = tabela_amortizacao(valor, taxa_juros, num_parcelas)
    total_pago = parcela * num_parcelas
    total_juros = total_pago - valor

    return {
        "valor_financiado": round(valor, 2),
        "num_parcelas": num_parcelas,
        "taxa_juros_mensal": round(taxa_juros * 100, 4),
        "taxa_juros_anual": round(taxa_juros * 12 * 100, 4),
        "parcela_mensal": round(parcela, 2),
        "total_pago": round(total_pago, 2),
        "total_juros": round(total_juros, 2),
        "tabela": tabela,
    }


def gerar_csv(tabela: List[Dict[str, Any]]) -> str:
    """
    Gera string CSV da tabela de amortização.

    Args:
        tabela: Lista de dicionários da tabela de amortização.

    Returns:
        Conteúdo CSV como string.
    """
    output = StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Parcela", "Amortizacao (R$)", "Juros (R$)",
        "Parcela Total (R$)", "Saldo Devedor (R$)",
    ])

    for row in tabela:
        writer.writerow([
            row["parcela"],
            f'{row["amortizacao"]:.2f}',
            f'{row["juros"]:.2f}',
            f'{row["parcela_total"]:.2f}',
            f'{row["saldo_devedor"]:.2f}',
        ])

    return output.getvalue()
