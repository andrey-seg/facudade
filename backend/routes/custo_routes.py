"""Blueprint da API de Custos Agrícolas."""

import logging
from flask import Blueprint, request, jsonify
from backend.services.custo_service import calcular_custos
from backend.utils.validators import validate_custo_payload

logger = logging.getLogger(__name__)

custo_bp = Blueprint("custo", __name__, url_prefix="/api")


@custo_bp.route("/custo", methods=["POST"])
def custo():
    """
    Calcula custos operacionais agrícolas.
    ---
    tags:
      - Custos
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [area, sementes, fertilizantes, defensivos, mao_obra, irrigacao, transporte, outros]
          properties:
            area:
              type: number
              description: Área cultivada em hectares
            sementes:
              type: number
              description: Custo com sementes (R$)
            fertilizantes:
              type: number
              description: Custo com fertilizantes (R$)
            defensivos:
              type: number
              description: Custo com defensivos (R$)
            mao_obra:
              type: number
              description: Custo com mão de obra (R$)
            irrigacao:
              type: number
              description: Custo com irrigação (R$)
            transporte:
              type: number
              description: Custo com transporte (R$)
            outros:
              type: number
              description: Outros custos (R$)
            produtividade:
              type: number
              description: Produtividade em sc/ha
            preco_venda:
              type: number
              description: Preço de venda por sc (R$)
    responses:
      200:
        description: Custos calculados com sucesso
      400:
        description: Erro de validação
    """
    dados = request.get_json(silent=True) or {}
    erros = validate_custo_payload(dados)
    if erros:
        logger.warning("Validação de custo falhou: %s", erros)
        return jsonify({"erro": "Dados inválidos", "detalhes": erros}), 400

    try:
        resultado = calcular_custos(dados)
        logger.info("Custos calculados para área %.2f ha", dados.get("area", 0))
        return jsonify(resultado), 200
    except Exception as e:
        logger.exception("Erro ao calcular custos")
        return jsonify({"erro": "Erro interno ao calcular custos", "detalhes": str(e)}), 500
