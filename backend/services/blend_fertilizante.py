"""Módulo de resolução de sistema linear 3x3 para blend de fertilizantes."""

from typing import Dict
import numpy as np


def _float(val) -> float:
    """Converte numpy float para float nativo do Python."""
    return float(val)

# Matriz de composição dos fertilizantes (fração de N, P, K)
# Cada linha: [%N, %P, %K] do fertilizante
# Ureia: 45% N, 0% P, 0% K
# Superfosfato Simples: 0% N, 18% P, 0% K
# KCl (Cloreto de Potássio): 0% N, 0% P, 58% K
MATRIZ_COMPOSICAO: np.ndarray = np.array([
    [0.45, 0.0,  0.0 ],
    [0.0,  0.18, 0.0 ],
    [0.0,  0.0,  0.58],
], dtype=float)

FERTILIZANTES = ["Ureia", "Superfosfato", "KCl"]


def resolver_blend(n_alvo: float, p_alvo: float, k_alvo: float) -> Dict:
    """
    Resolve o sistema linear 3x3 para encontrar as quantidades de
    Ureia, Superfosfato e KCl necessárias para atingir as metas NPK.

    Sistema:
        0.45 * U + 0.00 * S + 0.00 * K = N_alvo
        0.00 * U + 0.18 * S + 0.00 * K = P_alvo
        0.00 * U + 0.00 * S + 0.58 * K = K_alvo

    Args:
        n_alvo: Quantidade desejada de Nitrogênio (kg).
        p_alvo: Quantidade desejada de Fósforo (kg).
        k_alvo: Quantidade desejada de Potássio (kg).

    Returns:
        Dicionário com quantidades de cada fertilizante, determinante,
        meta NPK, e totais.

    Raises:
        ValueError: Se o determinante for zero (sistema sem solução única).
    """
    A = MATRIZ_COMPOSICAO
    b = np.array([n_alvo, p_alvo, k_alvo], dtype=float)

    det = np.linalg.det(A)
    if abs(det) < 1e-12:
        raise ValueError(
            "Determinante da matriz de composição é zero. "
            "O sistema não possui solução única. "
            "Verifique os fertilizantes selecionados."
        )

    solucao = np.linalg.solve(A, b)
    ureia, superfosfato, kcl = solucao

    quantidades = {}
    total_kg = 0.0
    for i, nome in enumerate(FERTILIZANTES):
        qtd = max(0.0, float(solucao[i]))
        quantidades[nome.lower()] = round(qtd, 2)
        total_kg += qtd

    n_fornecido = float(ureia) * 0.45
    p_fornecido = float(superfosfato) * 0.18
    k_fornecido = float(kcl) * 0.58

    return {
        "meta_npk": {
            "n": round(float(n_alvo), 2),
            "p": round(float(p_alvo), 2),
            "k": round(float(k_alvo), 2),
        },
        "quantidades": {
            "ureia": round(float(ureia), 2),
            "superfosfato": round(float(superfosfato), 2),
            "kcl": round(float(kcl), 2),
        },
        "fornecido_npk": {
            "n": round(n_fornecido, 2),
            "p": round(p_fornecido, 2),
            "k": round(k_fornecido, 2),
        },
        "total_fertilizantes_kg": round(total_kg, 2),
        "determinante": round(float(det), 6),
        "sistema_valido": True,
    }
