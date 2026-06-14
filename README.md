# AgroCalc Web

Plataforma inteligente para cálculos do agronegócio — simulação de financiamentos, custos, blend de fertilizantes, conversão de bases numéricas e mais.

## Funcionalidades

- **Dashboard** — Visão geral da produção com gráficos e cards de indicadores
- **Custos** — Cálculo de custos operacionais, receita, lucro e margem
- **Custo de Produção** — Ponto de equilíbrio usando C(x) = CF + CV × x
- **Financiamento** — Simulação Price com tabela de amortização, gráfico e exportação CSV
- **Conversor** — Conversão Decimal ↔ Binário / Decimal ↔ Hexadecimal com passo a passo + Simulador AND
- **Talhões** — CRUD de talhões com resumo estatístico
- **Fertilizantes** — Resolução de sistema linear 3×3 (Ureia, Superfosfato, KCl) para meta NPK
- **Computação** — Como funciona (CPU, RAM, Armazenamento, SO), arquitetura do AgroCalc, linha do tempo

## Estrutura

```
├── app.py                    # Ponto de entrada principal
├── backend/
│   ├── app.py                # Fábrica Flask (create_app)
│   ├── routes/               # Blueprints das rotas (API REST)
│   ├── services/             # Lógica de negócio (cálculos, CSV)
│   ├── templates/            # Templates Jinja2 (herdam base.html)
│   ├── static/               # CSS, JS servidos pelo Flask
│   └── logs/                 # Logs rotativos (agrocalc.log)
├── frontend/                 # Código-fonte HTML/JS/CSS
└── requirements.txt
```

## Requisitos

- Python 3.14+
- Flask 3
- NumPy, Matplotlib
- Flask-CORS (opcional, fallback automático)

## Instalação

```bash
git clone https://github.com/seu-usuario/agrocalc-web.git
cd agrocalc-web
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Executar

```bash
python3 app.py
```

Acesse: [http://localhost:5000](http://localhost:5000)

## APIs REST

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/dashboard` | Dados do dashboard |
| POST | `/api/custo` | Calcular custos |
| POST | `/api/custo-producao` | Calcular custo de produção |
| POST | `/api/financiamento` | Simular financiamento |
| POST | `/api/financiamento/calcular` | Calcular Price (valor, taxa, parcelas) |
| POST | `/api/financiamento/exportar-csv` | Exportar tabela CSV |
| POST | `/api/conversor` | Converter base numérica |
| GET/POST | `/api/talhoes` | Listar / criar talhões |
| PUT/DELETE | `/api/talhoes/{id}` | Atualizar / excluir talhão |
| GET | `/api/talhoes/resumo` | Resumo dos talhões |
| POST | `/api/blend` | Calcular blend de fertilizantes |
| POST | `/api/blend/resolver` | Resolver sistema linear NPK |

Documentação interativa em `/api/docs`.

## Licença

MIT
