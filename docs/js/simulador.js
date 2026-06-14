/* ============================================
   AgroCalc Web - Simuladores
   Calculadora de Custos e Financiamento Agrícola
   ============================================ */

const AgroSimulador = {
  /* ============================================
     Custo de Produção (C(x) = CF + CV * x)
     ============================================ */
  custoProducao: {
    init() {
      this.form = document.getElementById('cp-form')
      this.setupEvents()
    },

    setupEvents() {
      if (!this.form) return
      this.form.addEventListener('submit', (e) => {
        e.preventDefault()
        this.calcular()
      })
    },

    async calcular() {
      const getVal = (id) => parseFloat(document.getElementById(id)?.value) || 0
      const cf = getVal('cp-cf')
      const cv = getVal('cp-cv')
      const producao = getVal('cp-producao')
      const preco = getVal('cp-preco')

      if (cf <= 0 || cv <= 0 || producao <= 0 || preco <= 0) {
        AgroCalc.showToast('Preencha todos os campos com valores positivos', 'error')
        return
      }

      const custoTotal = cf + cv * producao
      const receita = preco * producao
      const lucro = receita - custoTotal
      const custoMedio = custoTotal / producao
      const margemContrib = preco - cv
      let pe = null
      if (preco > cv) {
        pe = cf / (preco - cv)
      }

      this.setResult('cp-custo-total', AgroCalc.formatCurrency(custoTotal))
      this.setResult('cp-receita', AgroCalc.formatCurrency(receita))

      const lucroEl = document.getElementById('cp-lucro')
      const lucroCard = document.getElementById('cp-lucro-card')
      lucroEl.textContent = AgroCalc.formatCurrency(lucro)
      if (lucro > 0) {
        lucroCard.style.borderColor = 'var(--cor-primaria)'
        lucroEl.className = 'result-value text-primary'
      } else if (lucro < 0) {
        lucroCard.style.borderColor = '#ef4444'
        lucroEl.className = 'result-value'
        lucroEl.style.color = '#ef4444'
      } else {
        lucroCard.style.borderColor = 'var(--cor-destaque)'
        lucroEl.className = 'result-value'
      }

      this.setResult('cp-pe', pe !== null ? AgroCalc.formatNumber(pe) : 'N/A')
      this.setResult('cp-custo-medio', AgroCalc.formatCurrency(custoMedio))
      this.setResult('cp-margem', AgroCalc.formatCurrency(margemContrib))

      document.getElementById('cp-resultados').style.display = ''
      document.getElementById('cp-empty').style.display = 'none'

      this.drawChart(cf, cv, preco, producao, pe)
      AgroCalc.showToast('Cálculo realizado com sucesso!', 'success')
    },

    setResult(id, value) {
      const el = document.getElementById(id)
      if (el) el.textContent = value
    },

    drawChart(cf, cv, p, x, pe) {
      const canvas = document.getElementById('cp-chart')
      if (!canvas) return
      canvas.style.display = ''
      const container = canvas.parentElement
      const rect = container.getBoundingClientRect()
      const W = rect.width
      const H = 260
      const scale = window.devicePixelRatio || 1
      canvas.width = W * scale
      canvas.height = H * scale
      canvas.style.width = W + 'px'
      canvas.style.height = H + 'px'
      const ctx = canvas.getContext('2d')
      ctx.scale(scale, scale)

      const maxX = Math.max(x, pe || x) * 1.3
      const maxY = Math.max(cf + cv * maxX, p * maxX) * 1.15

      const pad = { top: 20, right: 20, bottom: 36, left: 56 }
      const chartW = W - pad.left - pad.right
      const chartH = H - pad.top - pad.bottom

      ctx.clearRect(0, 0, W, H)

      const style = getComputedStyle(document.documentElement)
      const gridColor = 'rgba(255,255,255,0.04)'
      const textColor = style.getPropertyValue('--text-muted').trim() || '#94a3b8'

      for (let i = 0; i <= 4; i++) {
        const y = pad.top + (chartH / 4) * i
        ctx.strokeStyle = gridColor
        ctx.lineWidth = 1
        ctx.beginPath()
        ctx.moveTo(pad.left, y)
        ctx.lineTo(W - pad.right, y)
        ctx.stroke()
        ctx.fillStyle = textColor
        ctx.font = '10px sans-serif'
        ctx.textAlign = 'right'
        ctx.fillText(Math.round(maxY - (maxY / 4) * i), pad.left - 8, y + 4)
      }

      const toX = (v) => pad.left + (v / maxX) * chartW
      const toY = (v) => pad.top + chartH - (v / maxY) * chartH

      const steps = 100
      const drawLine = (fn, color, label) => {
        ctx.beginPath()
        for (let i = 0; i <= steps; i++) {
          const v = (maxX / steps) * i
          const xPos = toX(v)
          const yPos = toY(fn(v))
          if (i === 0) ctx.moveTo(xPos, yPos)
          else ctx.lineTo(xPos, yPos)
        }
        ctx.strokeStyle = color
        ctx.lineWidth = 2.5
        ctx.stroke()

        ctx.fillStyle = color
        ctx.font = 'bold 11px sans-serif'
        ctx.textAlign = 'left'
        const lx = toX(maxX * 0.85)
        const ly = toY(fn(maxX * 0.85))
        ctx.fillText(label, lx + 4, ly - 4)
      }

      drawLine((v) => cf + cv * v, '#ef4444', 'Custo Total')
      drawLine((v) => p * v, '#00D084', 'Receita')

      if (pe !== null) {
        const peX = toX(pe)
        ctx.strokeStyle = '#8B5CF6'
        ctx.lineWidth = 1.5
        ctx.setLineDash([5, 4])
        ctx.beginPath()
        ctx.moveTo(peX, pad.top)
        ctx.lineTo(peX, pad.top + chartH)
        ctx.stroke()
        ctx.setLineDash([])

        ctx.fillStyle = '#8B5CF6'
        ctx.font = 'bold 11px sans-serif'
        ctx.textAlign = 'center'
        ctx.fillText('PE: ' + Math.round(pe), peX, pad.top + chartH + 16)
      }

      const prodX = toX(x)
      ctx.strokeStyle = textColor
      ctx.lineWidth = 1
      ctx.setLineDash([3, 3])
      ctx.beginPath()
      ctx.moveTo(prodX, pad.top)
      ctx.lineTo(prodX, pad.top + chartH)
      ctx.stroke()
      ctx.setLineDash([])

      ctx.fillStyle = textColor
      ctx.font = '10px sans-serif'
      ctx.textAlign = 'center'
      ctx.fillText('Produção: ' + Math.round(x), prodX, pad.top + chartH + 28)
    }
  },

  /* ============================================
     Calculadora de Custos
     ============================================ */
  custo: {
    init() {
      this.form = document.getElementById('custo-form')
      this.setupEvents()
    },

    setupEvents() {
      if (!this.form) return
      this.form.addEventListener('submit', (e) => {
        e.preventDefault()
        this.calcular()
      })
    },

    calcular() {
      const getVal = (id) => parseFloat(document.getElementById(id)?.value) || 0

      const area = getVal('custo-area')
      const sementes = getVal('custo-sementes')
      const fertilizantes = getVal('custo-fertilizantes')
      const defensivos = getVal('custo-defensivos')
      const maoObra = getVal('custo-mao-obra')
      const irrigacao = getVal('custo-irrigacao')
      const transporte = getVal('custo-transporte')
      const outros = getVal('custo-outros')
      const produtividade = getVal('custo-produtividade')
      const precoVenda = getVal('custo-preco-venda')

      if (area <= 0) {
        AgroCalc.showToast('Informe a área cultivada', 'error')
        return
      }

      const custoTotal = sementes + fertilizantes + defensivos + maoObra + irrigacao + transporte + outros
      const custoPorHa = custoTotal / area
      const producaoTotal = area * produtividade
      const receitaTotal = producaoTotal * precoVenda
      const lucroEstimado = receitaTotal - custoTotal
      const margem = receitaTotal > 0 ? (lucroEstimado / receitaTotal) * 100 : 0

      /* Atualizar resultados */
      this.setResult('custo-total', AgroCalc.formatCurrency(custoTotal))
      this.setResult('custo-por-ha', AgroCalc.formatCurrency(custoPorHa))
      this.setResult('custo-producao', AgroCalc.formatNumber(producaoTotal))
      this.setResult('custo-receita', AgroCalc.formatCurrency(receitaTotal))
      this.setResult('custo-lucro', AgroCalc.formatCurrency(lucroEstimado), lucroEstimado >= 0 ? 'text-primary' : '')
      this.setResult('custo-margem', AgroCalc.formatPercent(margem), margem >= 15 ? 'text-primary' : '')

      AgroCalc.showToast('Custos calculados com sucesso!', 'success')
    },

    setResult(id, value, extraClass = '') {
      const el = document.getElementById(id)
      if (el) {
        el.textContent = value
        if (extraClass) el.className = `result-value ${extraClass}`
      }
    }
  },

  /* ============================================
     Financiamento Agrícola
     ============================================ */
  financiamento: {
    init() {
      this.form = document.getElementById('fin-form')
      this.setupEvents()
      this.setupCsvExport()
    },

    setupEvents() {
      if (!this.form) return
      this.form.addEventListener('submit', (e) => {
        e.preventDefault()
        this.calcular()
      })
    },

    setupCsvExport() {
      const btn = document.getElementById('btn-export-csv')
      if (!btn) return
      btn.addEventListener('click', () => this.exportarCsv())
    },

    async calcular() {
      const getVal = (id) => parseFloat(document.getElementById(id)?.value) || 0

      const valor = getVal('fin-valor')
      const taxa = getVal('fin-taxa')
      const parcelas = getVal('fin-parcelas')

      if (valor <= 0 || parcelas <= 0) {
        AgroCalc.showToast('Preencha valor e número de parcelas', 'error')
        return
      }

      if (taxa < 0) {
        AgroCalc.showToast('Taxa de juros inválida', 'error')
        return
      }

      const payload = {
        valor: valor,
        taxa_juros: taxa,
        num_parcelas: parcelas,
      }

      try {
        const response = await fetch('/api/financiamento/calcular', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        })

        if (!response.ok) {
          const err = await response.json()
          throw new Error(err.detalhes || err.erro || 'Erro ao calcular')
        }

        const data = await response.json()

        this.ultimosDados = data
        this.ultimoPayload = payload

        /* Exibir resumo */
        document.getElementById('fin-resumo').style.display = 'grid'
        this.setResult('fin-parcela', AgroCalc.formatCurrency(data.parcela_mensal))
        this.setResult('fin-total-pago', AgroCalc.formatCurrency(data.total_pago))
        this.setResult('fin-total-juros', AgroCalc.formatCurrency(data.total_juros))

        /* Gerar tabela Price */
        this.gerarTabela(data.tabela)

        /* Desenhar gráfico */
        this.desenharGrafico(data.tabela)

        /* Mostrar botão CSV */
        document.getElementById('fin-export-area').style.display = 'block'

        AgroCalc.showToast('Simulação de financiamento concluída!', 'success')
      } catch (e) {
        AgroCalc.showToast(e.message || 'Erro ao calcular financiamento', 'error')
      }
    },

    gerarTabela(tabela) {
      const container = document.getElementById('fin-tabela')
      if (!container) return

      const maxLinhas = 60
      const mostrarMais = tabela.length > maxLinhas

      let html = `
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>Amortização</th>
                <th>Juros</th>
                <th>Parcela</th>
                <th>Saldo Devedor</th>
              </tr>
            </thead>
            <tbody>
      `

      const exibir = mostrarMais ? tabela.slice(0, maxLinhas) : tabela

      for (const row of exibir) {
        const isDestaque = row.parcela <= 12
        html += `
          <tr class="${isDestaque ? 'parcela-destaque' : ''}">
            <td><strong>${row.parcela}º</strong></td>
            <td>${AgroCalc.formatCurrency(row.amortizacao)}</td>
            <td>${AgroCalc.formatCurrency(row.juros)}</td>
            <td style="font-weight:600;color:var(--cor-primaria);">${AgroCalc.formatCurrency(row.parcela_total)}</td>
            <td>${AgroCalc.formatCurrency(row.saldo_devedor)}</td>
          </tr>
        `
      }

      if (mostrarMais) {
        html += `<tr><td colspan="5" style="text-align:center;color:var(--text-muted);padding:16px;">... mais ${tabela.length - maxLinhas} parcelas</td></tr>`
      }

      html += '</tbody></table></div>'
      container.innerHTML = html
    },

    desenharGrafico(tabela) {
      const container = document.getElementById('fin-chart-container')
      const canvas = document.getElementById('fin-chart')
      if (!container || !canvas) return

      container.style.display = ''

      const parent = canvas.parentElement
      const rect = parent.getBoundingClientRect()
      const W = rect.width || 600
      const H = 220
      const scale = window.devicePixelRatio || 1
      canvas.width = W * scale
      canvas.height = H * scale
      canvas.style.width = W + 'px'
      canvas.style.height = H + 'px'

      const ctx = canvas.getContext('2d')
      ctx.scale(scale, scale)

      const style = getComputedStyle(document.documentElement)
      const textColor = style.getPropertyValue('--text-muted').trim() || '#94a3b8'
      const gridColor = 'rgba(255,255,255,0.04)'

      ctx.clearRect(0, 0, W, H)

      const pad = { top: 20, right: 16, bottom: 32, left: 56 }
      const chartW = W - pad.left - pad.right
      const chartH = H - pad.top - pad.bottom

      const mostrar = Math.min(tabela.length, 60)
      const dados = tabela.slice(0, mostrar)

      const maxValor = Math.max(...dados.map(d => d.parcela_total)) * 1.15

      /* Grade */
      for (let i = 0; i <= 4; i++) {
        const y = pad.top + (chartH / 4) * i
        ctx.strokeStyle = gridColor
        ctx.lineWidth = 1
        ctx.beginPath()
        ctx.moveTo(pad.left, y)
        ctx.lineTo(W - pad.right, y)
        ctx.stroke()
        ctx.fillStyle = textColor
        ctx.font = '10px sans-serif'
        ctx.textAlign = 'right'
        ctx.fillText(AgroCalc.formatCurrency(maxValor - (maxValor / 4) * i), pad.left - 8, y + 4)
      }

      const barW = Math.min(14, (chartW / dados.length) * 0.8)
      const gap = (chartW - barW * dados.length) / (dados.length + 1)

      /* Barras empilhadas */
      for (let i = 0; i < dados.length; i++) {
        const d = dados[i]
        const x = pad.left + gap + i * (barW + gap)

        const hAmort = (d.amortizacao / maxValor) * chartH
        const hJuros = (d.juros / maxValor) * chartH

        /* Amortização (verde) */
        const yAmort = pad.top + chartH - hAmort
        const g1 = ctx.createLinearGradient(x, yAmort, x, pad.top + chartH)
        g1.addColorStop(0, '#00D084')
        g1.addColorStop(1, '#2DD4BF')
        ctx.fillStyle = g1
        ctx.fillRect(x, yAmort, barW, hAmort)

        /* Juros (roxo) */
        const yJuros = yAmort - hJuros
        const g2 = ctx.createLinearGradient(x, yJuros, x, yAmort)
        g2.addColorStop(0, '#8B5CF6')
        g2.addColorStop(1, '#A78BFA')
        ctx.fillStyle = g2
        ctx.fillRect(x, yJuros, barW, hJuros)

        /* Label do mês (a cada 6) */
        if (i % 6 === 0 || i === dados.length - 1) {
          ctx.fillStyle = textColor
          ctx.font = '9px sans-serif'
          ctx.textAlign = 'center'
          ctx.fillText(d.parcela + 'º', x + barW / 2, pad.top + chartH + 16)
        }
      }
    },

    async exportarCsv() {
      if (!this.ultimoPayload) {
        AgroCalc.showToast('Nenhuma simulação para exportar', 'error')
        return
      }

      try {
        const response = await fetch('/api/financiamento/exportar-csv', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.ultimoPayload),
        })

        if (!response.ok) {
          const err = await response.json()
          throw new Error(err.detalhes || err.erro || 'Erro ao exportar')
        }

        const blob = await response.blob()
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `financiamento_${this.ultimoPayload.num_parcelas}parcelas.csv`
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        URL.revokeObjectURL(url)

        AgroCalc.showToast('CSV exportado com sucesso!', 'success')
      } catch (e) {
        AgroCalc.showToast(e.message || 'Erro ao exportar CSV', 'error')
      }
    },

    setResult(id, value) {
      const el = document.getElementById(id)
      if (el) el.textContent = value
    }
  },

  /* ============================================
     Inicializar
     ============================================ */
  init() {
    this.custoProducao.init()
    this.custo.init()
    this.financiamento.init()
  }
}

document.addEventListener('DOMContentLoaded', () => AgroSimulador.init())
