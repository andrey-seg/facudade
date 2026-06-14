"""Blueprint da API de Conversor de Bases."""

import logging
from flask import Blueprint, request, jsonify
from backend.services.conversor_service import converter_base
from backend.utils.validators import validate_conversor_payload

logger = logging.getLogger(__name__)

conversor_bp = Blueprint("conversor", __name__, url_prefix="/api")


@conversor_bp.route("/conversor", methods=["POST"])
def conversor():
    """
    Converte números entre bases numéricas.
    ---
    tags:
      - Conversor
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [valor, base_origem, base_destino]
          properties:
            valor:
              type: string
              description: Valor a ser convertido
            base_origem:
              type: integer
              enum: [2, 8, 10, 16]
              description: Base de origem
            base_destino:
              type: integer
              enum: [2, 8, 10, 16]
              description: Base de destino
    responses:
      200:
        description: Conversão realizada com sucesso
      400:
        description: Erro de validação
    """
    dados = request.get_json(silent=True) or {}
    erros = validate_conversor_payload(dados)
    if erros:
        logger.warning("Validação de conversor falhou: %s", erros)
        return jsonify({"erro": "Dados inválidos", "detalhes": erros}), 400

    try:
        resultado = converter_base(dados)
        logger.info("Conversão: %s base %s -> %s base %s",
                     dados["valor"], dados["base_origem"],
                     resultado["valor_convertido"], dados["base_destino"])
        return jsonify(resultado), 200
    except ValueError as e:
        logger.warning("Erro de conversão: %s", str(e))
        return jsonify({"erro": "Valor inválido para a base de origem"}), 400
    except Exception as e:
        logger.exception("Erro ao realizar conversão")
        return jsonify({"erro": "Erro interno ao converter", "detalhes": str(e)}), 500
