"""Blueprint da API de Blend de Fertilizantes."""

import logging
from flask import Blueprint, request, jsonify
from backend.services.blend_service import calcular_blend
from backend.services.blend_fertilizante import resolver_blend
from backend.utils.validators import validate_blend_payload

logger = logging.getLogger(__name__)

blend_bp = Blueprint("blend", __name__, url_prefix="/api")


@blend_bp.route("/blend", methods=["POST"], strict_slashes=False)
def blend():
    """
    Calcula composição e custo de blend NPK.
    ---
    tags:
      - Fertilizantes
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [area, n, p, k, dose]
          properties:
            nome:
              type: string
              description: Nome do blend
            area:
              type: number
              description: Área de aplicação (ha)
            n:
              type: number
              description: Proporção de Nitrogênio (0-100)
            p:
              type: number
              description: Proporção de Fósforo (0-100)
            k:
              type: number
              description: Proporção de Potássio (0-100)
            tipo_cultura:
              type: string
              enum: [soja, milho, cafe, algodao]
              description: Cultura alvo
            dose:
              type: number
              description: Dose recomendada (kg/ha)
    responses:
      200:
        description: Blend calculado com sucesso
      400:
        description: Erro de validação
    """
    dados = request.get_json(silent=True) or {}
    erros = validate_blend_payload(dados)
    if erros:
        logger.warning("Validação de blend falhou: %s", erros)
        return jsonify({"erro": "Dados inválidos", "detalhes": erros}), 400

    try:
        resultado = calcular_blend(dados)
        logger.info("Blend calculado: %s - NPK (%.0f-%.0f-%.0f)",
                     dados.get("nome", "Blend"), dados.get("n", 0),
                     dados.get("p", 0), dados.get("k", 0))
        return jsonify(resultado), 200
    except Exception as e:
        logger.exception("Erro ao calcular blend")
        return jsonify({"erro": "Erro interno ao calcular blend", "detalhes": str(e)}), 500


@blend_bp.route("/blend/resolver", methods=["POST"])
def resolver():
    """
    Resolve sistema linear 3x3 para blend de fertilizantes (Ureia, Superfosfato, KCl).
    ---
    tags:
      - Fertilizantes
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [n, p, k]
          properties:
            n:
              type: number
              description: Meta de Nitrogênio (kg)
            p:
              type: number
              description: Meta de Fósforo (kg)
            k:
              type: number
              description: Meta de Potássio (kg)
    responses:
      200:
        description: Sistema resolvido com sucesso
      400:
        description: Erro de validação ou determinante zero
    """
    dados = request.get_json(silent=True) or {}
    erros = _validar_resolver_payload(dados)
    if erros:
        logger.warning("Validação resolver blend falhou: %s", erros)
        return jsonify({"erro": "Dados inválidos", "detalhes": erros}), 400

    try:
        n = float(dados["n"])
        p = float(dados["p"])
        k = float(dados["k"])
        resultado = resolver_blend(n, p, k)
        logger.info("Blend resolvido: N=%.1f P=%.1f K=%.1f", n, p, k)
        return jsonify(resultado), 200
    except ValueError as e:
        logger.warning("Erro ao resolver blend: %s", e)
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        logger.exception("Erro ao resolver blend")
        return jsonify({"erro": "Erro interno ao resolver blend", "detalhes": str(e)}), 500


def _validar_resolver_payload(dados: dict) -> list:
    erros = []
    for campo in ["n", "p", "k"]:
        val = dados.get(campo)
        if val is None:
            erros.append(f"{campo} é obrigatório")
        else:
            try:
                v = float(val)
                if v < 0:
                    erros.append(f"{campo} não pode ser negativo")
            except (ValueError, TypeError):
                erros.append(f"{campo} deve ser um número válido")
    return erros
