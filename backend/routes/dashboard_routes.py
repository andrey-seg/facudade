"""Blueprint da API de Dashboard."""

import io
import logging
from flask import Blueprint, jsonify, send_file
from backend.services.dashboard_service import obter_dashboard

logger = logging.getLogger(__name__)

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api")


@dashboard_bp.route("/dashboard", methods=["GET"])
def dashboard():
    """
    Retorna dados consolidados para o dashboard principal.
    ---
    tags:
      - Dashboard
    responses:
      200:
        description: Dados do dashboard retornados com sucesso
    """
    try:
        dados = obter_dashboard()
        return jsonify(dados), 200
    except Exception as e:
        logger.exception("Erro ao obter dados do dashboard")
        return jsonify({"erro": "Erro interno ao carregar dashboard", "detalhes": str(e)}), 500


@dashboard_bp.route("/dashboard/grafico", methods=["GET"])
def grafico_dashboard():
    """
    Gera gráfico de produção mensal como imagem PNG usando Matplotlib.
    ---
    tags:
      - Dashboard
    responses:
      200:
        description: Imagem PNG do gráfico
        content:
          image/png:
            schema:
              type: string
              format: binary
    """
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        from datetime import datetime

        dados = obter_dashboard()
        prod_mensal = dados.get("graficos", {}).get("producao_mensal", [])

        meses = [p["mes"] for p in prod_mensal]
        valores = [p["sacas"] for p in prod_mensal]

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.set_facecolor("#1a1a2e")
        fig.patch.set_facecolor("#1a1a2e")

        bars = ax.bar(meses, valores, color="#00D084", width=0.6, edgecolor="#00e090", linewidth=0.5)

        for bar, val in zip(bars, valores):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 10, str(val),
                    ha="center", va="bottom", fontsize=9, color="#e0e0e0", fontweight="bold")

        ax.set_title("Produção Mensal (sacas)", color="#e0e0e0", fontsize=14, fontweight="bold", pad=16)
        ax.set_ylabel("Sacas", color="#94a3b8", fontsize=11)
        ax.tick_params(colors="#94a3b8", labelsize=10)
        ax.spines["bottom"].set_color("#2a2a4a")
        ax.spines["left"].set_color("#2a2a4a")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_axisbelow(True)
        ax.grid(axis="y", color="#2a2a4a", linewidth=0.5, alpha=0.5)

        buf = io.BytesIO()
        fig.tight_layout()
        fig.savefig(buf, format="png", dpi=120, bbox_inches="tight",
                    facecolor=fig.get_facecolor(), edgecolor="none")
        plt.close(fig)
        buf.seek(0)

        return send_file(buf, mimetype="image/png")

    except ImportError:
        return jsonify({"erro": "Matplotlib não está instalado"}), 500
    except Exception as e:
        logger.exception("Erro ao gerar gráfico")
        return jsonify({"erro": "Erro ao gerar gráfico", "detalhes": str(e)}), 500
