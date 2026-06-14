/* ============================================
   AgroCalc Web - Conversor de Bases + Simulador AND
   ============================================ */

const AgroConversor = {
  history: [],

  init() {
    this.cacheElements()
    this.setupEvents()
    this.loadHistory()
    this.setupAndSimulator()
  },

  cacheElements() {
    this.form = document.getElementById('conversor-form')
    this.input = document.getElementById('conv-input')
    this.fromBase = document.getElementById('conv-from')
    this.toBase = document.getElementById('conv-to')
    this.resultDiv = document.getElementById('conv-result')
    this.stepsDiv = document.getElementById('conv-steps')
    this.historyList = document.getElementById('conv-history')
  },

  setupEvents() {
    if (!this.form) return

    this.form.addEventListener('submit', (e) => {
      e.preventDefault()
      this.convert()
    })

    this.input?.addEventListener('input', () => {
      clearTimeout(this._debounce)
      this._debounce = setTimeout(() => this.convert(), 400)
    })

    const clearBtn = document.getElementById('conv-clear')
    clearBtn?.addEventListener('click', () => this.clearHistory())
  },

  convert() {
    const value = this.input?.value.trim()
    if (!value) {
      this.showResult('', '')
      this.showSteps('')
      return
    }

    const from = parseInt(this.fromBase?.value || '10')
    const to = parseInt(this.toBase?.value || '2')

    try {
      const decimal = this.toDecimal(value, from)
      if (decimal === null || isNaN(decimal)) {
        this.showResult('Valor inválido para a base selecionada', 'error')
        this.showSteps('')
        return
      }

      const result = this.fromDecimal(decimal, to)

      if (from === 10 && to === 2) {
        this.showResult(result, 'success', 'Binário')
        this.showSteps(this.gerarPassosDecParaBin(value, result))
      } else if (from === 10 && to === 16) {
        this.showResult(result, 'success', 'Hexadecimal')
        this.showSteps(this.gerarPassosDecParaHex(value, result))
      } else if (from === 2 && to === 10) {
        this.showResult(result, 'success', 'Decimal')
        this.showSteps(this.gerarPassosBinParaDec(value, result))
      } else if (from === 16 && to === 10) {
        this.showResult(result, 'success', 'Decimal')
        this.showSteps(this.gerarPassosHexParaDec(value, result))
      } else {
        this.showResult(result, 'success', this.nomeBase(to))
        this.showSteps('')
      }

      this.addHistory(value, from, result, to)

    } catch (err) {
      this.showResult('Erro na conversão', 'error')
      this.showSteps('')
    }
  },

  /* --- Passo a passo: Decimal -> Binário --- */
  gerarPassosDecParaBin(valor, resultado) {
    let n = parseInt(valor)
    const passos = []
    while (n > 0) {
      const resto = n % 2
      passos.push({ divisao: `${n} ÷ 2`, quociente: Math.floor(n / 2), resto })
      n = Math.floor(n / 2)
    }
    passos.reverse()
    let html = `<h4 style="font-size:14px;font-weight:600;color:var(--text-primary);margin-bottom:12px;">Passo a passo (Decimal → Binário)</h4>
      <div class="table-container"><table><thead><tr><th>Divisão</th><th>Quociente</th><th>Resto</th></tr></thead><tbody>`
    for (const p of passos) {
      html += `<tr><td>${p.divisao}</td><td>${p.quociente}</td><td style="font-weight:700;color:var(--cor-primaria);">${p.resto}</td></tr>`
    }
    html += `</tbody></table></div>
      <p style="margin-top:12px;color:var(--text-secondary);font-size:13px;">
        Resultado: leia os restos de <strong>baixo para cima</strong> → <strong style="color:var(--cor-primaria);font-size:15px;">${resultado}</strong>
      </p>`
    return html
  },

  /* --- Passo a passo: Decimal -> Hexadecimal --- */
  gerarPassosDecParaHex(valor, resultado) {
    let n = parseInt(valor)
    const digitos = '0123456789ABCDEF'
    const passos = []
    while (n > 0) {
      const resto = n % 16
      passos.push({ divisao: `${n} ÷ 16`, quociente: Math.floor(n / 16), resto, digito: digitos[resto] })
      n = Math.floor(n / 16)
    }
    passos.reverse()
    let html = `<h4 style="font-size:14px;font-weight:600;color:var(--text-primary);margin-bottom:12px;">Passo a passo (Decimal → Hexadecimal)</h4>
      <div class="table-container"><table><thead><tr><th>Divisão</th><th>Quociente</th><th>Resto</th><th>Dígito Hex</th></tr></thead><tbody>`
    for (const p of passos) {
      html += `<tr><td>${p.divisao}</td><td>${p.quociente}</td><td>${p.resto}</td><td style="font-weight:700;color:var(--cor-destaque);">${p.digito}</td></tr>`
    }
    html += `</tbody></table></div>
      <p style="margin-top:12px;color:var(--text-secondary);font-size:13px;">
        Resultado: leia os dígitos de <strong>baixo para cima</strong> → <strong style="color:var(--cor-destaque);font-size:15px;">${resultado}</strong>
      </p>`
    return html
  },

  /* --- Passo a passo: Binário -> Decimal --- */
  gerarPassosBinParaDec(valor, resultado) {
    const digitos = valor.split('').reverse()
    const passos = []
    for (let i = digitos.length - 1; i >= 0; i--) {
      const pos = digitos.length - 1 - i
      const d = parseInt(digitos[i])
      const v = d * Math.pow(2, pos)
      passos.push({ pos, digito: d, potencia: `${d} × 2^${pos}`, valor: v })
    }
    let html = `<h4 style="font-size:14px;font-weight:600;color:var(--text-primary);margin-bottom:12px;">Passo a passo (Binário → Decimal)</h4>
      <div class="table-container"><table><thead><tr><th>Posição</th><th>Dígito</th><th>Cálculo</th><th>Valor</th></tr></thead><tbody>`
    for (const p of passos) {
      html += `<tr><td>2<sup>${p.pos}</sup></td><td>${p.digito}</td><td>${p.potencia}</td><td style="font-weight:700;color:var(--cor-primaria);">${p.valor}</td></tr>`
    }
    const total = passos.reduce((s, p) => s + p.valor, 0)
    html += `<tr style="background:rgba(0,208,132,0.06);"><td colspan="3" style="font-weight:700;">Soma</td><td style="font-weight:800;color:var(--cor-primaria);font-size:16px;">${total}</td></tr>`
    html += `</tbody></table></div>
      <p style="margin-top:12px;color:var(--text-secondary);font-size:13px;">
        Resultado: <strong style="color:var(--cor-primaria);font-size:15px;">${resultado}</strong>
      </p>`
    return html
  },

  /* --- Passo a passo: Hexadecimal -> Decimal --- */
  gerarPassosHexParaDec(valor, resultado) {
    const digitos = valor.split('').reverse()
    const hexMap = { '0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,A:10,B:11,C:12,D:13,E:14,F:15 }
    const passos = []
    for (let i = digitos.length - 1; i >= 0; i--) {
      const pos = digitos.length - 1 - i
      const d = digitos[i].toUpperCase()
      const v = hexMap[d] * Math.pow(16, pos)
      passos.push({ pos, digito: d, potencia: `${hexMap[d]} × 16^${pos}`, valor: v })
    }
    let html = `<h4 style="font-size:14px;font-weight:600;color:var(--text-primary);margin-bottom:12px;">Passo a passo (Hexadecimal → Decimal)</h4>
      <div class="table-container"><table><thead><tr><th>Posição</th><th>Dígito</th><th>Cálculo</th><th>Valor</th></tr></thead><tbody>`
    for (const p of passos) {
      html += `<tr><td>16<sup>${p.pos}</sup></td><td>${p.digito}</td><td>${p.potencia}</td><td style="font-weight:700;color:var(--cor-destaque);">${p.valor}</td></tr>`
    }
    const total = passos.reduce((s, p) => s + p.valor, 0)
    html += `<tr style="background:rgba(139,92,246,0.06);"><td colspan="3" style="font-weight:700;">Soma</td><td style="font-weight:800;color:var(--cor-destaque);font-size:16px;">${total}</td></tr>`
    html += `</tbody></table></div>
      <p style="margin-top:12px;color:var(--text-secondary);font-size:13px;">
        Resultado: <strong style="color:var(--cor-destaque);font-size:15px;">${resultado}</strong>
      </p>`
    return html
  },

  /* --- Conversões básicas --- */
  toDecimal(value, base) {
    const str = value.toString().toUpperCase()
    const digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for (const ch of str) {
      if (!digits.slice(0, base).includes(ch)) return null
    }
    return parseInt(str, base)
  },

  fromDecimal(decimal, base) {
    if (decimal === 0) return '0'
    return decimal.toString(base).toUpperCase()
  },

  nomeBase(base) {
    const nomes = { 2: 'Binário', 10: 'Decimal', 16: 'Hexadecimal' }
    return nomes[base] || `Base ${base}`
  },

  /* --- Exibir resultado --- */
  showResult(text, type, baseName) {
    if (!this.resultDiv) return
    if (!text) {
      this.resultDiv.style.display = 'none'
      return
    }

    const fromVal = this.input?.value.trim()
    const from = parseInt(this.fromBase?.value || '10')
    const to = parseInt(this.toBase?.value || '2')

    this.resultDiv.style.display = 'block'

    if (type === 'error') {
      this.resultDiv.style.background = 'rgba(239,68,68,0.06)'
      this.resultDiv.style.borderColor = 'rgba(239,68,68,0.2)'
      this.resultDiv.innerHTML = `
        <div class="conv-label">Erro</div>
        <div class="conv-value" style="color:#ef4444;font-size:18px;">${text}</div>`
    } else {
      this.resultDiv.style.background = 'rgba(0,208,132,0.04)'
      this.resultDiv.style.borderColor = 'rgba(0,208,132,0.2)'
      const bName = baseName || this.nomeBase(to)
      this.resultDiv.innerHTML = `
        <div class="conv-label">${this.nomeBase(from)} → ${bName}</div>
        <div class="conv-value" style="font-size:24px;">${text}</div>
        <div style="margin-top:8px;font-size:13px;color:var(--text-muted);">
          ${fromVal}<sub style="color:var(--text-secondary);">${from}</sub> = ${text}<sub style="color:var(--text-secondary);">${to}</sub>
        </div>`
    }
  },

  showSteps(html) {
    if (!this.stepsDiv) return
    if (!html) {
      this.stepsDiv.style.display = 'none'
      return
    }
    this.stepsDiv.style.display = 'block'
    this.stepsDiv.innerHTML = html
  },

  /* --- Histórico --- */
  addHistory(fromVal, fromBase, toVal, toBase) {
    const entry = {
      id: Date.now(), fromVal, fromBase, toVal, toBase,
      time: new Date().toLocaleTimeString('pt-BR')
    }
    this.history.unshift(entry)
    if (this.history.length > 20) this.history.pop()
    this.saveHistory()
    this.renderHistory()
  },

  renderHistory() {
    if (!this.historyList) return
    if (this.history.length === 0) {
      this.historyList.innerHTML = `<div class="empty-state"><div class="empty-icon">&#128203;</div><h3>Nenhuma conversão ainda</h3></div>`
      return
    }
    const baseNames = { 2: 'BIN', 10: 'DEC', 16: 'HEX' }
    this.historyList.innerHTML = this.history.map(e => `
      <div class="history-item">
        <div>
          <span class="h-value">${e.fromVal}</span>
          <span class="h-base">${baseNames[e.fromBase] || `B${e.fromBase}`}</span>
          <span style="color:var(--text-muted);margin:0 8px;">→</span>
          <span class="h-value">${e.toVal}</span>
          <span class="h-base">${baseNames[e.toBase] || `B${e.toBase}`}</span></div>
        <span class="h-time">${e.time}</span></div>`).join('')
  },

  saveHistory() {
    try { localStorage.setItem('agrocalc-conv-history', JSON.stringify(this.history)) } catch (e) { }
  },

  loadHistory() {
    try {
      const saved = localStorage.getItem('agrocalc-conv-history')
      if (saved) { this.history = JSON.parse(saved); this.renderHistory() }
    } catch (e) { }
  },

  clearHistory() {
    this.history = []
    this.saveHistory()
    this.renderHistory()
    AgroCalc.showToast('Histórico limpo', 'info')
  },

  /* ============================================
     Simulador AND
     ============================================ */
  setupAndSimulator() {
    this.btnAnd = document.getElementById('btn-and-simular')
    this.andUmidade = document.getElementById('and-umidade')
    this.andTemperatura = document.getElementById('and-temperatura')
    this.andResultado = document.getElementById('and-resultado')

    if (!this.btnAnd) return

    this.btnAnd.addEventListener('click', () => this.simularAnd())

    this.andUmidade?.addEventListener('change', () => this.atualizarTabelaAnd())
    this.andTemperatura?.addEventListener('change', () => this.atualizarTabelaAnd())
  },

  simularAnd() {
    const u = parseInt(this.andUmidade?.value || '0')
    const t = parseInt(this.andTemperatura?.value || '0')
    const resultado = u && t

    this.andResultado.style.display = 'block'

    if (resultado) {
      this.andResultado.style.background = 'rgba(0,208,132,0.08)'
      this.andResultado.style.border = '1px solid rgba(0,208,132,0.3)'
      this.andResultado.style.color = 'var(--cor-primaria)'
      this.andResultado.innerHTML = '&#10004; SIM — Irrigação ligada!'
    } else {
      this.andResultado.style.background = 'rgba(239,68,68,0.08)'
      this.andResultado.style.border = '1px solid rgba(239,68,68,0.3)'
      this.andResultado.style.color = '#ef4444'
      this.andResultado.innerHTML = '&#10008; NÃO — Irrigação desligada.'
    }

    this.atualizarTabelaAnd()
  },

  atualizarTabelaAnd() {
    const selU = parseInt(this.andUmidade?.value || '0')
    const selT = parseInt(this.andTemperatura?.value || '0')

    const linhas = ['00', '01', '10', '11']
    for (const id of linhas) {
      const row = document.getElementById(`and-row-${id}`)
      if (!row) continue
      row.style.background = ''
      row.style.outline = ''
    }

    const chave = `${selU}${selT}`
    const rowSel = document.getElementById(`and-row-${chave}`)
    if (rowSel) {
      rowSel.style.background = selU && selT
        ? 'rgba(0,208,132,0.08)'
        : 'rgba(239,68,68,0.06)'
      rowSel.style.outline = '2px solid var(--cor-primaria)'
      rowSel.style.outlineOffset = '-2px'
    }
  }
}

document.addEventListener('DOMContentLoaded', () => AgroConversor.init())
