"""Blueprint da API de Talhões."""

import logging
from flask import Blueprint, request, jsonify
from backend.services.talhoes_service import (
    listar_talhoes, obter_talhao, criar_talhao,
    atualizar_talhao, excluir_talhao, resumo_talhoes,
)
from backend.utils.validators import validate_talhao_payload

logger = logging.getLogger(__name__)

talhoes_bp = Blueprint("talhoes", __name__, url_prefix="/api")


@talhoes_bp.route("/talhoes", methods=["GET"])
def listar():
    """
    Lista todos os talhões cadastrados.
    ---
    tags:
      - Talhões
    responses:
      200:
        description: Lista de talhões retornada com sucesso
    """
    talhoes = listar_talhoes()
    return jsonify({"talhoes": talhoes, "total": len(talhoes)}), 200


@talhoes_bp.route("/talhoes/resumo", methods=["GET"])
def resumo():
    """
    Retorna resumo estatístico dos talhões.
    ---
    tags:
      - Talhões
    responses:
      200:
        description: Resumo retornado com sucesso
    """
    return jsonify(resumo_talhoes()), 200


@talhoes_bp.route("/talhoes/<int:talhao_id>", methods=["GET"])
def obter(talhao_id: int):
    """
    Retorna um talhão específico.
    ---
    tags:
      - Talhões
    parameters:
      - in: path
        name: talhao_id
        type: integer
        required: true
        description: ID do talhão
    responses:
      200:
        description: Talhão encontrado
      404:
        description: Talhão não encontrado
    """
    talhao = obter_talhao(talhao_id)
    if not talhao:
        return jsonify({"erro": "Talhão não encontrado"}), 404
    return jsonify(talhao), 200


@talhoes_bp.route("/talhoes", methods=["POST"])
def criar():
    """
    Cria um novo talhão.
    ---
    tags:
      - Talhões
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [nome, area]
          properties:
            nome:
              type: string
              description: Nome do talhão
            area:
              type: number
              description: Área em hectares
            cultura:
              type: string
              enum: [soja, milho, cafe, algodao]
              description: Cultura plantada
            status:
              type: string
              enum: [ok, atencao, pousio]
              description: Status do talhão
            previsao_colheita:
              type: string
              description: Previsão de colheita
            produtividade:
              type: number
              description: Produtividade estimada (sc/ha)
    responses:
      201:
        description: Talhão criado com sucesso
      400:
        description: Erro de validação
    """
    dados = request.get_json(silent=True) or {}
    erros = validate_talhao_payload(dados)
    if erros:
        logger.warning("Validação de talhão falhou: %s", erros)
        return jsonify({"erro": "Dados inválidos", "detalhes": erros}), 400

    talhao = criar_talhao(dados)
    logger.info("Talhão criado: %s (ID %d)", talhao["nome"], talhao["id"])
    return jsonify(talhao), 201


@talhoes_bp.route("/talhoes/<int:talhao_id>", methods=["PUT"])
def atualizar(talhao_id: int):
    """
    Atualiza um talhão existente.
    ---
    tags:
      - Talhões
    parameters:
      - in: path
        name: talhao_id
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
            area:
              type: number
            cultura:
              type: string
            status:
              type: string
            previsao_colheita:
              type: string
            produtividade:
              type: number
    responses:
      200:
        description: Talhão atualizado
      400:
        description: Erro de validação
      404:
        description: Talhão não encontrado
    """
    dados = request.get_json(silent=True) or {}
    talhao = atualizar_talhao(talhao_id, dados)
    if not talhao:
        return jsonify({"erro": "Talhão não encontrado"}), 404
    logger.info("Talhão atualizado: %s (ID %d)", talhao["nome"], talhao["id"])
    return jsonify(talhao), 200


@talhoes_bp.route("/talhoes/<int:talhao_id>", methods=["DELETE"])
def excluir(talhao_id: int):
    """
    Exclui um talhão.
    ---
    tags:
      - Talhões
    parameters:
      - in: path
        name: talhao_id
        type: integer
        required: true
    responses:
      200:
        description: Talhão excluído
      404:
        description: Talhão não encontrado
    """
    if excluir_talhao(talhao_id):
        logger.info("Talhão ID %d excluído", talhao_id)
        return jsonify({"mensagem": "Talhão excluído com sucesso"}), 200
    return jsonify({"erro": "Talhão não encontrado"}), 404
