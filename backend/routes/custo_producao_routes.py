"""Blueprint da API de Custo de Produção."""

import logging
from flask import Blueprint, request, jsonify
from backend.services.custo_producao import calcular
from backend.utils.validators import validate_custo_producao_payload

logger = logging.getLogger(__name__)

custo_producao_bp = Blueprint("custo_producao", __name__, url_prefix="/api")


@custo_producao_bp.route("/custo-producao", methods=["POST"])
def custo_producao():
    """
    Calcula custo de produção, receita, lucro e ponto de equilíbrio.
    ---
    tags:
      - Custo de Produção
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [cf, cv, producao, preco_venda]
          properties:
            cf:
              type: number
              description: Custo fixo total (R$)
            cv:
              type: number
              description: Custo variável por unidade (R$/un)
            producao:
              type: number
              description: Quantidade produzida (unidades)
            preco_venda:
              type: number
              description: Preço de venda por unidade (R$/un)
    responses:
      200:
        description: Cálculo realizado com sucesso
      400:
        description: Erro de validação
    """
    dados = request.get_json(silent=True) or {}
    erros = validate_custo_producao_payload(dados)
    if erros:
        logger.warning("Validação de custo de produção falhou: %s", erros)
        return jsonify({"erro": "Dados inválidos", "detalhes": erros}), 400

    try:
        resultado = calcular(dados)
        logger.info(
            "Custo de produção calculado: CF=%.2f, CV=%.2f, x=%.2f, p=%.2f",
            dados.get("cf", 0),
            dados.get("cv", 0),
            dados.get("producao", 0),
            dados.get("preco_venda", 0),
        )
        return jsonify(resultado), 200
    except ValueError as e:
        logger.warning("Erro de validação nos dados: %s", e)
        return jsonify({"erro": "Dados inválidos", "detalhes": str(e)}), 400
    except Exception as e:
        logger.exception("Erro ao calcular custo de produção")
        return jsonify({"erro": "Erro interno ao calcular custo de produção", "detalhes": str(e)}), 500
