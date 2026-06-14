"""AgroCalc Web - Backend Flask
Aplicação principal com blueprints, Swagger, tratamento global de erros e logs.
"""

import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template, jsonify

try:
    from flask_cors import CORS
    CORS_AVAILABLE = True
except ModuleNotFoundError:
    CORS_AVAILABLE = False

from backend.routes.custo_routes import custo_bp
from backend.routes.financiamento_routes import financiamento_bp
from backend.routes.conversor_routes import conversor_bp
from backend.routes.talhoes_routes import talhoes_bp
from backend.routes.blend_routes import blend_bp
from backend.routes.custo_producao_routes import custo_producao_bp
from backend.routes.dashboard_routes import dashboard_bp


def create_app() -> Flask:
    """
    Cria e configura a aplicação Flask.

    Returns:
        Instância configurada do Flask.
    """
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
        static_url_path="/static",
    )

    # Configurações
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "agrocalc-dev-key")
    app.config["JSON_AS_ASCII"] = False
    app.config["JSON_SORT_KEYS"] = False

    # CORS para desenvolvimento (opcional)
    if CORS_AVAILABLE:
        CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Configurar logging
    _configurar_logging(app)

    # Registrar blueprints
    app.register_blueprint(custo_bp)
    app.register_blueprint(financiamento_bp)
    app.register_blueprint(conversor_bp)
    app.register_blueprint(talhoes_bp)
    app.register_blueprint(blend_bp)
    app.register_blueprint(custo_producao_bp)
    app.register_blueprint(dashboard_bp)

    # Tratamento global de erros
    _registrar_handlers_erro(app)

    # Rotas das páginas HTML
    _registrar_rotas_paginas(app)

    # Swagger UI via rota estática
    _configurar_swagger(app)

    return app


def _configurar_logging(app: Flask) -> None:
    """
    Configura o sistema de logs com rotação de arquivos e saída no console.

    Args:
        app: Instância do Flask.
    """
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Handler de arquivo com rotação
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "agrocalc.log"),
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Handler de console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)

    logging.getLogger("backend").addHandler(file_handler)
    logging.getLogger("backend").addHandler(console_handler)
    logging.getLogger("backend").setLevel(logging.INFO)

    app.logger.info("Logging configurado com sucesso")


def _registrar_handlers_erro(app: Flask) -> None:
    """
    Registra handlers globais para tratamento de erros HTTP e exceções.

    Args:
        app: Instância do Flask.
    """
    @app.errorhandler(400)
    def bad_request(error):
        app.logger.warning("Requisição inválida: %s", error)
        return jsonify({"erro": "Requisição inválida", "detalhes": str(error)}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"erro": "Recurso não encontrado"}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"erro": "Método não permitido", "detalhes": str(error)}), 405

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.exception("Erro interno do servidor")
        return jsonify({"erro": "Erro interno do servidor"}), 500

    @app.errorhandler(Exception)
    def unhandled_exception(error):
        app.logger.exception("Exceção não tratada: %s", error)
        return jsonify({"erro": "Erro interno do servidor"}), 500


def _registrar_rotas_paginas(app: Flask) -> None:
    """
    Registra as rotas que servem as páginas HTML do frontend.

    Args:
        app: Instância do Flask.
    """
    paginas = {
        "/": "index.html",
        "/custo": "custo.html",
        "/financiamento": "financiamento.html",
        "/conversor": "conversor.html",
        "/talhoes": "talhoes.html",
        "/blend": "blend.html",
        "/custo-producao": "custo_producao.html",
        "/computacao": "computacao.html",
    }

    for rota, template in paginas.items():
        app.add_url_rule(
            rota,
            endpoint=template.replace(".html", ""),
            view_func=lambda tmpl=template: render_template(tmpl),
        )


def _configurar_swagger(app: Flask) -> None:
    """
    Configura a documentação Swagger via Swagger UI estático.

    Args:
        app: Instância do Flask.
    """
    SWAGGER_UI_HTML = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>AgroCalc API - Swagger</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
        <style>
            body { margin: 0; background: #1a1a2e; }
            .swagger-ui .topbar { display: none; }
            .swagger-ui .info .title { color: #00D084; }
            .swagger-ui .scheme-container { background: #16213e; }
            .swagger-ui .opblock-tag { color: #e0e0e0; }
            .swagger-ui .opblock .opblock-summary-description { color: #94a3b8; }
            .swagger-ui .opblock-description-wrapper p { color: #cbd5e1; }
            .swagger-ui .parameter__name { color: #e2e8f0; }
            .swagger-ui .parameter__type { color: #94a3b8; }
            .swagger-ui .model-title { color: #e0e0e0; }
            .swagger-ui table thead tr td { color: #94a3b8; }
            .swagger-ui .response-col_status { color: #e0e0e0; }
            .swagger-ui .response-col_description { color: #cbd5e1; }
            .swagger-ui .btn.execute { background: #00D084; border-color: #00D084; }
            .custom-header {
                padding: 20px; text-align: center;
                background: linear-gradient(135deg, #0f0f23, #1a1a2e);
                border-bottom: 1px solid #2a2a4a;
            }
            .custom-header h1 {
                margin: 0; color: #00D084; font-family: sans-serif;
                font-size: 28px;
            }
            .custom-header p {
                margin: 8px 0 0; color: #94a3b8; font-family: sans-serif; font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="custom-header">
            <h1>AgroCalc API</h1>
            <p>Documentação interativa das APIs do AgroCalc Web</p>
        </div>
        <div id="swagger-ui"></div>
        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
        <script>
            SwaggerUIBundle({
                url: '/api/docs/swagger.json',
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [SwaggerUIBundle.presets.apis],
                layout: "BaseLayout",
            });
        </script>
    </body>
    </html>
    """

    SWAGGER_JSON = {
        "openapi": "3.0.3",
        "info": {
            "title": "AgroCalc API",
            "description": "API REST do AgroCalc Web - Plataforma inteligente para o agronegócio",
            "version": "1.0.0",
            "contact": {"name": "AgroCalc", "email": "contato@agrocalc.com.br"},
        },
        "servers": [{"url": "/", "description": "Servidor local"}],
        "paths": {
            "/api/custo": {
                "post": {
                    "tags": ["Custos"],
                    "summary": "Calcular custos operacionais",
                    "description": "Calcula custos, receita, lucro e margem da produção agrícola",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/CustoInput"
                                }
                            }
                        },
                    },
                    "responses": {
                        "200": {"description": "Custos calculados"},
                        "400": {"description": "Dados inválidos"},
                    },
                }
            },
            "/api/financiamento": {
                "post": {
                    "tags": ["Financiamento"],
                    "summary": "Simular financiamento",
                    "description": "Simula financiamento agrícola com tabelas Price e SAC",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/FinanciamentoInput"
                                }
                            }
                        },
                    },
                    "responses": {
                        "200": {"description": "Simulação concluída"},
                        "400": {"description": "Dados inválidos"},
                    },
                }
            },
            "/api/conversor": {
                "post": {
                    "tags": ["Conversor"],
                    "summary": "Converter base numérica",
                    "description": "Converte números entre bases binária, octal, decimal e hexadecimal",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ConversorInput"
                                }
                            }
                        },
                    },
                    "responses": {
                        "200": {"description": "Conversão realizada"},
                        "400": {"description": "Dados inválidos"},
                    },
                }
            },
            "/api/talhoes": {
                "get": {
                    "tags": ["Talhões"],
                    "summary": "Listar talhões",
                    "description": "Retorna todos os talhões cadastrados",
                    "responses": {
                        "200": {"description": "Lista de talhões"}
                    },
                },
                "post": {
                    "tags": ["Talhões"],
                    "summary": "Criar talhão",
                    "description": "Cadastra um novo talhão na propriedade",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/TalhaoInput"
                                }
                            }
                        },
                    },
                    "responses": {
                        "201": {"description": "Talhão criado"},
                        "400": {"description": "Dados inválidos"},
                    },
                },
            },
            "/api/talhoes/resumo": {
                "get": {
                    "tags": ["Talhões"],
                    "summary": "Resumo dos talhões",
                    "description": "Retorna resumo estatístico dos talhões",
                    "responses": {
                        "200": {"description": "Resumo dos talhões"}
                    },
                }
            },
            "/api/talhoes/{id}": {
                "get": {
                    "tags": ["Talhões"],
                    "summary": "Obter talhão",
                    "parameters": [
                        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
                    ],
                    "responses": {
                        "200": {"description": "Talhão encontrado"},
                        "404": {"description": "Talhão não encontrado"},
                    },
                },
                "put": {
                    "tags": ["Talhões"],
                    "summary": "Atualizar talhão",
                    "parameters": [
                        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/TalhaoInput"
                                }
                            }
                        },
                    },
                    "responses": {
                        "200": {"description": "Talhão atualizado"},
                        "404": {"description": "Talhão não encontrado"},
                    },
                },
                "delete": {
                    "tags": ["Talhões"],
                    "summary": "Excluir talhão",
                    "parameters": [
                        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
                    ],
                    "responses": {
                        "200": {"description": "Talhão excluído"},
                        "404": {"description": "Talhão não encontrado"},
                    },
                },
            },
            "/api/blend": {
                "post": {
                    "tags": ["Fertilizantes"],
                    "summary": "Calcular blend NPK",
                    "description": "Calcula composição e custo de blend de fertilizantes",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/BlendInput"
                                }
                            }
                        },
                    },
                    "responses": {
                        "200": {"description": "Blend calculado"},
                        "400": {"description": "Dados inválidos"},
                    },
                }
            },
            "/api/custo-producao": {
                "post": {
                    "tags": ["Custo de Produção"],
                    "summary": "Calcular custo de produção",
                    "description": "Calcula custo total, receita, lucro e ponto de equilíbrio usando C(x) = CF + CV*x",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/CustoProducaoInput"
                                }
                            }
                        },
                    },
                    "responses": {
                        "200": {"description": "Cálculo realizado"},
                        "400": {"description": "Dados inválidos"},
                    },
                }
            },
            "/api/financiamento/calcular": {
                "post": {
                    "tags": ["Financiamento"],
                    "summary": "Calcular financiamento Price (PMT)",
                    "description": "Calcula parcela, tabela de amortização, total pago e juros pelo sistema Price",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/FinanciamentoCalcInput"
                                }
                            }
                        },
                    },
                    "responses": {
                        "200": {"description": "Cálculo realizado"},
                        "400": {"description": "Dados inválidos"},
                    },
                }
            },
            "/api/financiamento/exportar-csv": {
                "post": {
                    "tags": ["Financiamento"],
                    "summary": "Exportar tabela de amortização em CSV",
                    "description": "Gera arquivo CSV com a tabela de amortização completa",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/FinanciamentoCalcInput"
                                }
                            }
                        },
                    },
                    "responses": {
                        "200": {"description": "Arquivo CSV gerado"},
                        "400": {"description": "Dados inválidos"},
                    },
                }
            },
            "/api/blend/resolver": {
                "post": {
                    "tags": ["Fertilizantes"],
                    "summary": "Resolver sistema linear 3x3 (Ureia, Superfosfato, KCl)",
                    "description": "Calcula as quantidades de Ureia, Superfosfato e KCl para atingir a meta NPK usando numpy.linalg.solve()",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/BlendResolverInput"
                                }
                            }
                        },
                    },
                    "responses": {
                        "200": {"description": "Sistema resolvido"},
                        "400": {"description": "Dados inválidos ou determinante zero"},
                    },
                }
            },
            "/api/dashboard": {
                "get": {
                    "tags": ["Dashboard"],
                    "summary": "Dados do dashboard",
                    "description": "Retorna dados consolidados da produção agrícola",
                    "responses": {
                        "200": {"description": "Dados do dashboard"}
                    },
                }
            },
        },
        "components": {
            "schemas": {
                "CustoInput": {
                    "type": "object",
                    "required": ["area"],
                    "properties": {
                        "area": {"type": "number", "example": 100},
                        "sementes": {"type": "number", "example": 15000.00},
                        "fertilizantes": {"type": "number", "example": 25000.00},
                        "defensivos": {"type": "number", "example": 12000.00},
                        "mao_obra": {"type": "number", "example": 30000.00},
                        "irrigacao": {"type": "number", "example": 8000.00},
                        "transporte": {"type": "number", "example": 5000.00},
                        "outros": {"type": "number", "example": 2000.00},
                        "produtividade": {"type": "number", "example": 60},
                        "preco_venda": {"type": "number", "example": 120.00},
                    },
                },
                "FinanciamentoInput": {
                    "type": "object",
                    "required": ["valor", "prazo", "taxa_anual"],
                    "properties": {
                        "valor": {"type": "number", "example": 500000.00},
                        "entrada": {"type": "number", "example": 100000.00},
                        "prazo": {"type": "integer", "example": 5},
                        "taxa_anual": {"type": "number", "example": 12.50},
                        "finalidade": {
                            "type": "string",
                            "enum": ["custeio", "investimento", "comercializacao", "industrializacao"],
                            "example": "custeio",
                        },
                    },
                },
                "ConversorInput": {
                    "type": "object",
                    "required": ["valor", "base_origem", "base_destino"],
                    "properties": {
                        "valor": {"type": "string", "example": "255"},
                        "base_origem": {"type": "integer", "enum": [2, 8, 10, 16], "example": 10},
                        "base_destino": {"type": "integer", "enum": [2, 8, 10, 16], "example": 16},
                    },
                },
                "TalhaoInput": {
                    "type": "object",
                    "required": ["nome", "area"],
                    "properties": {
                        "nome": {"type": "string", "example": "Talhão E1"},
                        "area": {"type": "number", "example": 35},
                        "cultura": {"type": "string", "enum": ["soja", "milho", "cafe", "algodao"], "example": "soja"},
                        "status": {"type": "string", "enum": ["ok", "atencao", "pousio"], "example": "ok"},
                        "previsao_colheita": {"type": "string", "example": "Setembro/2026"},
                        "produtividade": {"type": "number", "example": 62},
                    },
                },
                "CustoProducaoInput": {
            "type": "object",
            "required": ["cf", "cv", "producao", "preco_venda"],
            "properties": {
                "cf": {"type": "number", "example": 50000.00},
                "cv": {"type": "number", "example": 80.00},
                "producao": {"type": "number", "example": 1000},
                "preco_venda": {"type": "number", "example": 150.00},
            },
        },
        "FinanciamentoCalcInput": {
            "type": "object",
            "required": ["valor", "taxa_juros", "num_parcelas"],
            "properties": {
                "valor": {"type": "number", "description": "Valor financiado (R$)", "example": 500000.00},
                "taxa_juros": {"type": "number", "description": "Taxa de juros mensal (%)", "example": 1.0},
                "num_parcelas": {"type": "integer", "description": "Número de parcelas", "example": 60},
            },
        },
        "BlendResolverInput": {
            "type": "object",
            "required": ["n", "p", "k"],
            "properties": {
                "n": {"type": "number", "description": "Meta de Nitrogênio (kg)", "example": 100.0},
                "p": {"type": "number", "description": "Meta de Fósforo (kg)", "example": 50.0},
                "k": {"type": "number", "description": "Meta de Potássio (kg)", "example": 80.0},
            },
        },
        "BlendInput": {
                    "type": "object",
                    "required": ["area", "n", "p", "k", "dose"],
                    "properties": {
                        "nome": {"type": "string", "example": "Blend Premium Soja"},
                        "area": {"type": "number", "example": 100},
                        "n": {"type": "number", "example": 20},
                        "p": {"type": "number", "example": 30},
                        "k": {"type": "number", "example": 40},
                        "tipo_cultura": {"type": "string", "enum": ["soja", "milho", "cafe", "algodao"], "example": "soja"},
                        "dose": {"type": "number", "example": 350},
                    },
                },
            }
        },
    }

    @app.route("/api/docs")
    def swagger_ui():
        return SWAGGER_UI_HTML

    @app.route("/api/docs/swagger.json")
    def swagger_json():
        return jsonify(SWAGGER_JSON)


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV", "development") == "development"
    app.logger.info("Iniciando AgroCalc Web na porta %d (debug=%s)", port, debug)
    app.run(host="0.0.0.0", port=port, debug=debug)
