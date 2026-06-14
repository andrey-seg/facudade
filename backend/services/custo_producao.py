"""Serviço de cálculo de Custo de Produção (Função C(x) = CF + CV * x)."""

from typing import Dict, Any


def custo_total(cf: float, cv: float, x: float) -> float:
    """
    Calcula o custo total dado custo fixo, custo variável unitário e produção.

    Fórmula: C(x) = CF + CV * x

    Args:
        cf: Custo fixo total (R$).
        cv: Custo variável por unidade produzida (R$/un).
        x: Quantidade produzida (unidades).

    Returns:
        Custo total (R$).

    Raises:
        ValueError: Se cf, cv ou x forem negativos.
    """
    if cf < 0:
        raise ValueError("Custo fixo não pode ser negativo")
    if cv < 0:
        raise ValueError("Custo variável não pode ser negativo")
    if x < 0:
        raise ValueError("Produção não pode ser negativa")
    return cf + cv * x


def receita_total(p: float, x: float) -> float:
    """
    Calcula a receita total dado preço de venda e produção.

    Fórmula: R(x) = p * x

    Args:
        p: Preço de venda por unidade (R$/un).
        x: Quantidade produzida (unidades).

    Returns:
        Receita total (R$).

    Raises:
        ValueError: Se p ou x forem negativos.
    """
    if p < 0:
        raise ValueError("Preço de venda não pode ser negativo")
    if x < 0:
        raise ValueError("Produção não pode ser negativa")
    return p * x


def lucro(cf: float, cv: float, p: float, x: float) -> float:
    """
    Calcula o lucro total.

    Fórmula: L(x) = R(x) - C(x) = p*x - (CF + CV*x)

    Args:
        cf: Custo fixo total (R$).
        cv: Custo variável por unidade (R$/un).
        p: Preço de venda por unidade (R$/un).
        x: Quantidade produzida (unidades).

    Returns:
        Lucro total (R$). Pode ser negativo (prejuízo).

    Raises:
        ValueError: Se algum parâmetro for negativo.
    """
    if cf < 0:
        raise ValueError("Custo fixo não pode ser negativo")
    if cv < 0:
        raise ValueError("Custo variável não pode ser negativo")
    if p < 0:
        raise ValueError("Preço de venda não pode ser negativo")
    if x < 0:
        raise ValueError("Produção não pode ser negativa")
    return p * x - (cf + cv * x)


def ponto_equilibrio(cf: float, cv: float, p: float) -> float:
    """
    Calcula o ponto de equilíbrio contábil (break-even point).

    Fórmula: PE = CF / (p - CV)

    O ponto de equilíbrio é a quantidade produzida onde Receita = Custo Total,
    ou seja, Lucro = 0.

    Args:
        cf: Custo fixo total (R$).
        cv: Custo variável por unidade (R$/un).
        p: Preço de venda por unidade (R$/un).

    Returns:
        Quantidade no ponto de equilíbrio (unidades).

    Raises:
        ValueError: Se cf, cv ou p forem negativos, ou se p <= cv
                    (não é possível atingir equilíbrio).
    """
    if cf < 0:
        raise ValueError("Custo fixo não pode ser negativo")
    if cv < 0:
        raise ValueError("Custo variável não pode ser negativo")
    if p < 0:
        raise ValueError("Preço de venda não pode ser negativo")
    if p <= cv:
        raise ValueError(
            "Preço de venda deve ser maior que o custo variável "
            "para atingir o ponto de equilíbrio"
        )
    return cf / (p - cv)


def calcular(dados: Dict[str, Any]) -> Dict[str, Any]:
    """
    Função principal que executa todos os cálculos de Custo de Produção.

    Args:
        dados: Dicionário com cf, cv, producao, preco_venda.

    Returns:
        Dicionário com custo_total, receita, lucro, ponto_equilibrio,
        custo_medio, margem_contribuicao e indicadores de status.
    """
    try:
        cf = float(dados["cf"])
        cv = float(dados["cv"])
        x = float(dados["producao"])
        p = float(dados["preco_venda"])
    except (KeyError, ValueError, TypeError) as e:
        raise ValueError(f"Dados inválidos: {e}") from e

    ct = custo_total(cf, cv, x)
    rt = receita_total(p, x)
    l = lucro(cf, cv, p, x)
    cm = p - cv  # margem de contribuição unitária
    cme = ct / x if x > 0 else 0  # custo médio unitário

    try:
        pe = ponto_equilibrio(cf, cv, p)
    except ValueError:
        pe = None

    # Indicadores coloridos
    if l > 0:
        lucro_status = "positivo"
    elif l == 0:
        lucro_status = "neutro"
    else:
        lucro_status = "negativo"

    if x >= pe if pe else False:
        equilibrio_status = "acima"
    else:
        equilibrio_status = "abaixo"

    return {
        "custo_total": round(ct, 2),
        "receita": round(rt, 2),
        "lucro": round(l, 2),
        "ponto_equilibrio": round(pe, 2) if pe is not None else None,
        "custo_medio": round(cme, 2),
        "margem_contribuicao": round(cm, 2),
        "indicadores": {
            "lucro_status": lucro_status,
            "equilibrio_status": equilibrio_status,
        },
    }
