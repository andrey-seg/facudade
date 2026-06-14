import re
from typing import Any, Dict, List, Optional


def validate_positive_float(value: Any, field_name: str) -> Optional[str]:
    """Valida se o valor é um número float positivo."""
    if value is None:
        return f"{field_name} é obrigatório"
    try:
        v = float(value)
        if v < 0:
            return f"{field_name} não pode ser negativo"
    except (ValueError, TypeError):
        return f"{field_name} deve ser um número válido"
    return None


def validate_positive_int(value: Any, field_name: str, min_val: int = 0, max_val: Optional[int] = None) -> Optional[str]:
    """Valida se o valor é um número inteiro positivo dentro de um intervalo."""
    if value is None:
        return f"{field_name} é obrigatório"
    try:
        v = int(value)
        if v < min_val:
            return f"{field_name} deve ser maior ou igual a {min_val}"
        if max_val is not None and v > max_val:
            return f"{field_name} deve ser menor ou igual a {max_val}"
    except (ValueError, TypeError):
        return f"{field_name} deve ser um número inteiro válido"
    return None


def validate_base(value: Any) -> Optional[str]:
    """Valida se a base numérica é 2, 8, 10 ou 16."""
    try:
        v = int(value)
        if v not in {2, 8, 10, 16}:
            return "Base deve ser 2 (binário), 8 (octal), 10 (decimal) ou 16 (hexadecimal)"
    except (ValueError, TypeError):
        return "Base deve ser um número inteiro"
    return None


def validate_required_string(value: Any, field_name: str) -> Optional[str]:
    """Valida se o valor é uma string não vazia."""
    if not value or (isinstance(value, str) and not value.strip()):
        return f"{field_name} é obrigatório"
    return None


def validate_custo_payload(data: Dict[str, Any]) -> List[str]:
    """Valida o payload da rota de custos."""
    errors = []
    required_fields = ["area", "sementes", "fertilizantes", "defensivos", "mao_obra",
                       "irrigacao", "transporte", "outros"]
    for field in required_fields:
        err = validate_positive_float(data.get(field), field)
        if err:
            errors.append(err)

    if data.get("produtividade") is not None:
        err = validate_positive_float(data.get("produtividade"), "produtividade")
        if err:
            errors.append(err)

    if data.get("preco_venda") is not None:
        err = validate_positive_float(data.get("preco_venda"), "preco_venda")
        if err:
            errors.append(err)

    area = data.get("area", 0)
    if area is not None:
        try:
            if float(area) <= 0:
                errors.append("Área deve ser maior que zero")
        except (ValueError, TypeError):
            errors.append("Área deve ser um número válido")

    return errors


def validate_financiamento_payload(data: Dict[str, Any]) -> List[str]:
    """Valida o payload da rota de financiamento."""
    errors = []

    err = validate_positive_float(data.get("valor"), "valor")
    if err:
        errors.append(err)

    if data.get("entrada") is not None:
        err = validate_positive_float(data.get("entrada"), "entrada")
        if err:
            errors.append(err)

    err = validate_positive_int(data.get("prazo"), "prazo", min_val=1, max_val=30)
    if err:
        errors.append(err)

    err = validate_positive_float(data.get("taxa_anual"), "taxa_anual")
    if err:
        errors.append(err)

    finalidade = data.get("finalidade")
    if finalidade and finalidade not in ("custeio", "investimento", "comercializacao", "industrializacao"):
        errors.append("Finalidade inválida. Use: custeio, investimento, comercializacao, industrializacao")

    valor = data.get("valor", 0)
    entrada = data.get("entrada", 0)
    try:
        if float(valor) <= 0:
            errors.append("Valor do financiamento deve ser maior que zero")
    except (ValueError, TypeError):
        errors.append("Valor do financiamento deve ser um número válido")

    return errors


def validate_conversor_payload(data: Dict[str, Any]) -> List[str]:
    """Valida o payload da rota de conversão de bases."""
    errors = []

    err = validate_required_string(data.get("valor"), "valor")
    if err:
        errors.append(err)

    err = validate_base(data.get("base_origem"))
    if err:
        errors.append(err)

    err = validate_base(data.get("base_destino"))
    if err:
        errors.append(err)

    return errors


def validate_talhao_payload(data: Dict[str, Any]) -> List[str]:
    """Valida o payload da rota de talhões."""
    errors = []

    err = validate_required_string(data.get("nome"), "nome")
    if err:
        errors.append(err)

    err = validate_positive_float(data.get("area"), "area")
    if err:
        errors.append(err)

    try:
        if float(data.get("area", 0)) <= 0:
            errors.append("Área deve ser maior que zero")
    except (ValueError, TypeError):
        errors.append("Área deve ser um número válido")

    cultura = data.get("cultura")
    culturas_validas = ("soja", "milho", "cafe", "algodao")
    if cultura and cultura not in culturas_validas:
        errors.append(f"Cultura inválida. Use: {', '.join(culturas_validas)}")

    status = data.get("status")
    status_validos = ("ok", "atencao", "pousio")
    if status and status not in status_validos:
        errors.append(f"Status inválido. Use: {', '.join(status_validos)}")

    if data.get("produtividade") is not None:
        err = validate_positive_float(data.get("produtividade"), "produtividade")
        if err:
            errors.append(err)

    return errors


def validate_custo_producao_payload(data: Dict[str, Any]) -> List[str]:
    """Valida o payload da rota de custo de produção."""
    errors = []
    required = ["cf", "cv", "producao", "preco_venda"]
    for field in required:
        err = validate_positive_float(data.get(field), field)
        if err:
            errors.append(err)

    cf = data.get("cf", 0)
    try:
        if float(cf) < 0:
            errors.append("Custo fixo não pode ser negativo")
    except (ValueError, TypeError):
        errors.append("Custo fixo deve ser um número válido")

    cv = data.get("cv", 0)
    try:
        if float(cv) < 0:
            errors.append("Custo variável não pode ser negativo")
    except (ValueError, TypeError):
        errors.append("Custo variável deve ser um número válido")

    producao = data.get("producao", 0)
    try:
        if float(producao) < 0:
            errors.append("Produção não pode ser negativa")
    except (ValueError, TypeError):
        errors.append("Produção deve ser um número válido")

    preco = data.get("preco_venda", 0)
    try:
        if float(preco) < 0:
            errors.append("Preço de venda não pode ser negativo")
    except (ValueError, TypeError):
        errors.append("Preço de venda deve ser um número válido")

    try:
        if float(cf) > 0 and float(preco) <= float(cv):
            errors.append(
                "Preço de venda deve ser maior que o custo variável "
                "para atingir o ponto de equilíbrio"
            )
    except (ValueError, TypeError):
        pass

    return errors


def validate_blend_payload(data: Dict[str, Any]) -> List[str]:
    """Valida o payload da rota de blend de fertilizantes."""
    errors = []

    if data.get("nome") is not None:
        err = validate_required_string(data.get("nome"), "nome")
        if err:
            errors.append(err)

    err = validate_positive_float(data.get("area"), "area")
    if err:
        errors.append(err)

    try:
        if float(data.get("area", 0)) <= 0:
            errors.append("Área deve ser maior que zero")
    except (ValueError, TypeError):
        errors.append("Área deve ser um número válido")

    for nutriente in ["n", "p", "k"]:
        err = validate_positive_float(data.get(nutriente), nutriente.upper())
        if err:
            errors.append(err)
        try:
            v = float(data.get(nutriente, 0))
            if v < 0 or v > 100:
                errors.append(f"{nutriente.upper()} deve estar entre 0 e 100")
        except (ValueError, TypeError):
            errors.append(f"{nutriente.upper()} deve ser um número válido")

    err = validate_positive_float(data.get("dose"), "dose")
    if err:
        errors.append(err)

    try:
        if float(data.get("dose", 0)) <= 0:
            errors.append("Dose deve ser maior que zero")
    except (ValueError, TypeError):
        errors.append("Dose deve ser um número válido")

    tipo_cultura = data.get("tipo_cultura")
    culturas_validas = ("soja", "milho", "cafe", "algodao")
    if tipo_cultura and tipo_cultura not in culturas_validas:
        errors.append(f"Tipo de cultura inválida. Use: {', '.join(culturas_validas)}")

    return errors
