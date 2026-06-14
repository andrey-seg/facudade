"""Blueprint da API de Financiamento Agrícola."""

import logging
from flask import Blueprint, request, jsonify, Response
from backend.services.financiamento_service import simular_financiamento
from backend.services.financiamento import simular, gerar_csv
from backend.utils.validators import validate_financiamento_payload

logger = logging.getLogger(__name__)

financiamento_bp = Blueprint("financiamento", __name__, url_prefix="/api")


def _extrair_dados_simples(dados: dict) -> tuple:
    """Extrai e valida os campos do payload simplificado."""
    valor = float(dados.get("valor", 0))
    taxa_juros = float(dados.get("taxa_juros", 0)) / 100
    num_parcelas = int(dados.get("num_parcelas", 0))
    return valor, taxa_juros, num_parcelas


@financiamento_bp.route("/financiamento", methods=["POST"])
def financiamento():
    """
    Simula financiamento agrícola (Price + SAC).
    ---
    tags:
      - Financiamento
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [valor, prazo, taxa_anual]
          properties:
            valor:
              type: number
              description: Valor total do financiamento (R$)
            entrada:
              type: number
              description: Valor de entrada (R$)
            prazo:
              type: integer
              description: Prazo em anos (1-30)
            taxa_anual:
              type: number
              description: Taxa de juros anual (%)
            finalidade:
              type: string
              enum: [custeio, investimento, comercializacao, industrializacao]
              description: Finalidade do financiamento
    responses:
      200:
        description: Simulação concluída com sucesso
      400:
        description: Erro de validação
    """
    dados = request.get_json(silent=True) or {}
    erros = validate_financiamento_payload(dados)
    if erros:
        logger.warning("Validação de financiamento falhou: %s", erros)
        return jsonify({"erro": "Dados inválidos", "detalhes": erros}), 400

    try:
        resultado = simular_financiamento(dados)
        logger.info("Financiamento simulado: R$ %.2f em %d anos",
                     dados.get("valor", 0), dados.get("prazo", 0))
        return jsonify(resultado), 200
    except Exception as e:
        logger.exception("Erro ao simular financiamento")
        return jsonify({"erro": "Erro interno ao simular financiamento", "detalhes": str(e)}), 500


@financiamento_bp.route("/financiamento/calcular", methods=["POST"])
def calcular():
    """
    Calcula financiamento pelo sistema Price (PMT).
    ---
    tags:
      - Financiamento
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [valor, taxa_juros, num_parcelas]
          properties:
            valor:
              type: number
              description: Valor financiado (R$)
            taxa_juros:
              type: number
              description: Taxa de juros mensal (%)
            num_parcelas:
              type: integer
              description: Número de parcelas
    responses:
      200:
        description: Cálculo realizado com sucesso
      400:
        description: Erro de validação
    """
    dados = request.get_json(silent=True) or {}
    erros = _validar_payload_simples(dados)
    if erros:
        logger.warning("Validação do cálculo falhou: %s", erros)
        return jsonify({"erro": "Dados inválidos", "detalhes": erros}), 400

    try:
        valor, taxa_juros, num_parcelas = _extrair_dados_simples(dados)
        resultado = simular(valor, taxa_juros, num_parcelas)
        logger.info(
            "Financiamento calculado: R$ %.2f em %d parcelas",
            valor, num_parcelas,
        )
        return jsonify(resultado), 200
    except ValueError as e:
        logger.warning("Erro de validação nos dados: %s", e)
        return jsonify({"erro": "Dados inválidos", "detalhes": str(e)}), 400
    except Exception as e:
        logger.exception("Erro ao calcular financiamento")
        return jsonify({"erro": "Erro interno ao calcular financiamento", "detalhes": str(e)}), 500


@financiamento_bp.route("/financiamento/exportar-csv", methods=["POST"])
def exportar_csv():
    """
    Exporta tabela de amortização em CSV.
    ---
    tags:
      - Financiamento
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [valor, taxa_juros, num_parcelas]
          properties:
            valor:
              type: number
              description: Valor financiado (R$)
            taxa_juros:
              type: number
              description: Taxa de juros mensal (%)
            num_parcelas:
              type: integer
              description: Número de parcelas
    responses:
      200:
        description: Arquivo CSV gerado
      400:
        description: Erro de validação
    """
    dados = request.get_json(silent=True) or {}
    erros = _validar_payload_simples(dados)
    if erros:
        logger.warning("Validação da exportação CSV falhou: %s", erros)
        return jsonify({"erro": "Dados inválidos", "detalhes": erros}), 400

    try:
        valor, taxa_juros, num_parcelas = _extrair_dados_simples(dados)
        from backend.services.financiamento import tabela_amortizacao
        tabela = tabela_amortizacao(valor, taxa_juros, num_parcelas)
        csv_content = gerar_csv(tabela)

        logger.info("CSV exportado: R$ %.2f em %d parcelas", valor, num_parcelas)

        return Response(
            csv_content,
            mimetype="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=financiamento_{num_parcelas}parcelas.csv",
                "Content-Type": "text/csv; charset=utf-8",
            },
        )
    except ValueError as e:
        logger.warning("Erro de validação nos dados: %s", e)
        return jsonify({"erro": "Dados inválidos", "detalhes": str(e)}), 400
    except Exception as e:
        logger.exception("Erro ao exportar CSV")
        return jsonify({"erro": "Erro interno ao exportar CSV", "detalhes": str(e)}), 500


def _validar_payload_simples(dados: dict) -> list:
    """Valida o payload simplificado de financiamento."""
    erros = []
    valor = dados.get("valor")
    if valor is None:
        erros.append("valor é obrigatório")
    else:
        try:
            v = float(valor)
            if v <= 0:
                erros.append("valor deve ser maior que zero")
        except (ValueError, TypeError):
            erros.append("valor deve ser um número válido")

    taxa = dados.get("taxa_juros")
    if taxa is None:
        erros.append("taxa_juros é obrigatório")
    else:
        try:
            t = float(taxa)
            if t < 0:
                erros.append("taxa_juros não pode ser negativa")
        except (ValueError, TypeError):
            erros.append("taxa_juros deve ser um número válido")

    parcelas = dados.get("num_parcelas")
    if parcelas is None:
        erros.append("num_parcelas é obrigatório")
    else:
        try:
            n = int(parcelas)
            if n < 1:
                erros.append("num_parcelas deve ser maior que zero")
        except (ValueError, TypeError):
            erros.append("num_parcelas deve ser um número inteiro")

    return erros
