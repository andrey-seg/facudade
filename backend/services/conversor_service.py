"""Serviço de conversão entre bases numéricas."""

from typing import Dict, Any


def converter_base(dados: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converte um número entre bases (2, 8, 10, 16).

    Args:
        dados: Dicionário com valor, base_origem, base_destino.

    Returns:
        Dicionário com valor_original, base_origem, valor_convertido,
        base_destino, e timestamp.
    """
    valor = dados["valor"].strip()
    base_origem = int(dados["base_origem"])
    base_destino = int(dados["base_destino"])

    decimal = int(str(valor), base_origem)

    if base_destino == 10:
        convertido = str(decimal)
    elif base_destino == 16:
        convertido = hex(decimal)[2:].upper()
    elif base_destino == 8:
        convertido = oct(decimal)[2:]
    elif base_destino == 2:
        convertido = bin(decimal)[2:]
    else:
        convertido = decimal_to_base(decimal, base_destino)

    nomes_bases = {2: "Binário", 8: "Octal", 10: "Decimal", 16: "Hexadecimal"}

    return {
        "valor_original": valor,
        "base_origem": base_origem,
        "base_origem_nome": nomes_bases.get(base_origem, f"Base {base_origem}"),
        "valor_convertido": convertido,
        "base_destino": base_destino,
        "base_destino_nome": nomes_bases.get(base_destino, f"Base {base_destino}"),
        "decimal": decimal,
    }


def decimal_to_base(numero: int, base: int) -> str:
    """Converte um número decimal para qualquer base (2-36)."""
    if numero == 0:
        return "0"
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    resultado = ""
    while numero > 0:
        resultado = digits[numero % base] + resultado
        numero //= base
    return resultado
