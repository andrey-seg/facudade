# AgroCalc Web — Documentação do Front-End

## Visão Geral

Dashboard agrícola premium com tema dark, glassmorphism e design responsivo. Desenvolvido em HTML5, CSS3 e JavaScript puro — **sem frameworks**.

---

## Estrutura de Arquivos

```
Complementares/
├── index.html        → Estrutura HTML completa (475 linhas)
├── style.css         → Estilos CSS (1390 linhas)
├── script.js         → Lógica JavaScript (333 linhas)
└── documentacao.md   → Este arquivo
```

---

## Arquitetura do Layout

```
┌──────────────────────────────────────────────────┐
│                    HEADER                         │
│  [☰]  [🔍 Pesquisar...]    [🔔]  [👤 André C.]  │
├──────────┬───────────────────────────────────────┤
│          │  DESTAQUE (4 cards)                    │
│          │  ┌──────┐┌──────┐┌──────┐┌──────┐     │
│ SIDEBAR  │  │Área  ││Prod. ││Receita││Custos│     │
│ 260px    │  └──────┘└──────┘└──────┘└──────┘     │
│ fixa     │                                        │
│          │  GRÁFICO (Produção por Mês)            │
│          │  ██████████████████████████████         │
│          │                                        │
│          │  GRID (3 colunas × 2 linhas)           │
│          │  ┌─────────┐┌─────────┐┌─────────┐    │
│          │  │ Custo   ││Financia.││Conversor│    │
│          │  ├─────────┼┼─────────┼┼─────────┤    │
│          │  │ Talhões ││Fertiliz.││Porta AND│    │
│          │  └─────────┘└─────────┘└─────────┘    │
└──────────┴───────────────────────────────────────┘
```

### Sidebar (esquerda, fixa)
- Largura: `260px`
- 7 itens de navegação com ícones Lucide
- Indicador ativo com borda verde à esquerda
- Em mobile (< 992px): sidebar esconde e aparece com toggle

### Header (topo, sticky)
- Altura: `72px`
- Campo de busca com atalho `Ctrl+K`
- Botão de notificação com dot verde
- Avatar do usuário com iniciais

### Main Content
- **4 cards de destaque**: indicadores principais da safra
- **Gráfico de barras**: produção mensal (Jan–Dez)
- **Grid de 6 cards**: funcionalidades do sistema

---

## Dados Fictícios Atuais (para referência do back-end)

### Cards de Destaque
| Indicador | Valor | Variação |
|-----------|-------|----------|
| Área Cultivada | 2.450 ha | +12,5% |
| Produção Estimada | 8.520 ton | +8,3% |
| Receita Prevista | R$ 1.850.000 | +15,2% |
| Custos Totais | R$ 720.000 | -3,1% |

### Produção por Mês (toneladas)
| Jan | Fev | Mar | Abr | Mai | Jun | Jul | Ago | Set | Out | Nov | Dez |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 320 | 450 | 580 | 720 | 890 | 1050| 1200| 1350| 1100| 850 | 600 | 400 |

**Meta mensal:** [350, 480, 600, 750, 900, 1100, 1250, 1400, 1150, 900, 650, 450]

---

## Componentes e Seus Dados

### 1. Custo de Produção
```
Total:          R$ 245.800,00
├─ Insumos:     R$ 98.320,00  (40%)
├─ Mão de Obra: R$ 61.450,00  (25%)
├─ Maquinário:  R$ 49.160,00  (20%)
└─ Logística:   R$ 36.870,00  (15%)
```

### 2. Financiamento Agrícola
```
Parcela Atual:    R$ 12.450,00
Meses Restantes:  24
Taxa:             8,5% a.a.
Parcelas Pagas:   12
Progresso:        33%
```

### 3. Conversor de Dados
- Input: número decimal (ex: 42)
- Output: binário (101010) e hexadecimal (2A)
- Conversão em tempo real via JavaScript

### 4. Mapa de Talhões
| Talhão | Área | Cultura | Status |
|--------|------|---------|--------|
| Norte  | 580 ha | Soja    | Ativo  |
| Sul    | 420 ha | Milho   | Ativo  |
| Leste  | 350 ha | Algodão | Ativo  |
| Oeste  | 280 ha | Café    | Pausa  |
| Central| 820 ha | Cana    | Ativo  |

### 5. Blend de Fertilizantes
```
Ureia (45% N):            450 kg  (100%)
Superfosfato Simples:     320 kg  (71%)
Cloreto de Potássio (KCl): 280 kg (62%)
Total:                    1.050 kg/ha
```

### 6. Porta Lógica AND (Irrigação)
```
Entrada A: Umidade do solo < 30%  (0 ou 1)
Entrada B: Previsão de chuva > 50% (0 ou 1)

Tabela Verdade:
A | B | A AND B | Irrigar?
0   0     0        Não
0   1     0        Não
1   0     0        Não
1   1     1        Sim  ← ativa irrigação
```

---

## API de Dados — O que o back-end precisa fornecer

### Endpoints Sugeridos

#### `GET /api/dashboard/resumo`
**Retorna** os dados dos 4 cards de destaque:
```json
{
  "areaCultivada": { "valor": 2450, "unidade": "ha", "variacao": 12.5 },
  "producaoEstimada": { "valor": 8520, "unidade": "ton", "variacao": 8.3 },
  "receitaPrevista": { "valor": 1850000, "unidade": "BRL", "variacao": 15.2 },
  "custosTotais": { "valor": 720000, "unidade": "BRL", "variacao": -3.1 },
  "safra": "2025/2026"
}
```

#### `GET /api/dashboard/producao-mensal`
**Retorna** os dados do gráfico:
```json
{
  "ano": 2025,
  "meses": [
    { "mes": "Jan", "producao": 320, "meta": 350 },
    { "mes": "Fev", "producao": 450, "meta": 480 },
    ...
  ]
}
```

#### `GET /api/custos`
**Retorna** os dados de custo de produção:
```json
{
  "total": 245800.00,
  "itens": [
    { "nome": "Insumos", "valor": 98320.00, "percentual": 40 },
    { "nome": "Mão de Obra", "valor": 61450.00, "percentual": 25 },
    { "nome": "Maquinário", "valor": 49160.00, "percentual": 20 },
    { "nome": "Logística", "valor": 36870.00, "percentual": 15 }
  ]
}
```

#### `GET /api/financiamento`
**Retorna** dados do financiamento:
```json
{
  "parcelaAtual": 12450.00,
  "mesesRestantes": 24,
  "taxaAnual": 8.5,
  "parcelasPagas": 12,
  "totalParcelas": 36,
  "progressoPercentual": 33
}
```

#### `GET /api/talhoes`
**Retorna** lista de talhões:
```json
{
  "talhoes": [
    { "id": 1, "nome": "Norte", "area": 580, "unidade": "ha", "cultura": "Soja", "status": "ativo" },
    { "id": 2, "nome": "Sul", "area": 420, "unidade": "ha", "cultura": "Milho", "status": "ativo" },
    { "id": 3, "nome": "Leste", "area": 350, "unidade": "ha", "cultura": "Algodão", "status": "ativo" },
    { "id": 4, "nome": "Oeste", "area": 280, "unidade": "ha", "cultura": "Café", "status": "pausa" },
    { "id": 5, "nome": "Central", "area": 820, "unidade": "ha", "cultura": "Cana", "status": "ativo" }
  ]
}
```

#### `GET /api/fertilizantes`
**Retorna** dados do blend:
```json
{
  "itens": [
    { "nome": "Ureia (45% N)", "quantidade": 450, "unidade": "kg", "percentual": 100 },
    { "nome": "Superfosfato Simples", "quantidade": 320, "unidade": "kg", "percentual": 71 },
    { "nome": "Cloreto de Potássio (KCl)", "quantidade": 280, "unidade": "kg", "percentual": 62 }
  ],
  "total": 1050,
  "unidade": "kg/ha"
}
```

---

## Como Integrar o Back-End

### Passo 1: Servir os arquivos estáticos
Coloque `index.html`, `style.css` e `script.js` na pasta pública do seu servidor (ex: `public/` ou `static/`).

### Passo 2: Criar os endpoints da API
Implemente os endpoints sugeridos acima no seu back-end (Node.js, PHP, Python, Java, etc.).

### Passo 3: Substituir dados fictícios no `script.js`
No arquivo `script.js`, substitua os `productionData` e `metaData` por chamadas `fetch()` para sua API. Exemplo:

```javascript
// Substituir dados fixos do gráfico
async function carregarProducaoMensal() {
  const response = await fetch('/api/dashboard/producao-mensal');
  const data = await response.json();
  // usar data.meses para renderizar o gráfico
}
```

Os demais cards usam dados fixos no HTML (valores inline). Para integrá-los, crie funções similares que atualizem o DOM com `innerText` ou `textContent`.

### Passo 4: Autenticação (futuro)
O header já possui campo de usuário (André Carvalho) e avatar. Para autenticação real, basta:
- Adicionar um token JWT no `localStorage`
- Incluir header `Authorization: Bearer <token>` nas requisições `fetch`
- Atualizar nome/avatar dinamicamente via API

---

## Responsividade

| Breakpoint | Comportamento |
|------------|---------------|
| > 1200px   | Layout completo: sidebar + 4 colunas destaque + 3 colunas grid |
| 992–1200px | 2 colunas destaque + 2 colunas grid |
| < 992px    | Sidebar oculta (toggle por hamburger), 1 coluna destaque, 1 coluna grid |
| < 480px    | Header simplificado, shortcuts escondidos |

---

## Dependências Externas

| Recurso | CDN | Uso |
|---------|-----|-----|
| **Poppins** | Google Fonts | Fonte principal do sistema |
| **Lucide Icons** | unpkg.com/lucide | Todos os ícones da interface |

Nenhuma outra dependência. Zero frameworks.

---

## Convenções de Código

- **CSS**: Variáveis no `:root` para tema, cores, sombras e raios
- **HTML**: `data-*` attributes para binding com JavaScript (ex: `data-page`, `data-target`, `data-input`)
- **JS**: Organizado em seções comentadas, sem classes — funções puras e event listeners
- **Semântica**: `<aside>` para sidebar, `<main>` para conteúdo, `<section>` para páginas
