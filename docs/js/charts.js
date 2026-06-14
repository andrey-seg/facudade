/* ============================================
   AgroCalc Web - Gráficos (Canvas API)
   Gráfico de Barras e Linha sem bibliotecas
   ============================================ */

const AgroCharts = {
  /* --- Cores do tema --- */
  colors: {
    primary: '#00D084',
    secondary: '#2DD4BF',
    destaque: '#8B5CF6',
    card: '#111827',
    text: '#94a3b8',
    border: '#1e293b',
    grid: 'rgba(255,255,255,0.04)'
  },

  /* --- Inicializar todos os gráficos --- */
  init() {
    this.loadThemeColors()
    this.createBarChart()
    this.createLineChart()

    window.addEventListener('resize', () => {
      this.createBarChart()
      this.createLineChart()
    })

    const observer = new MutationObserver(() => {
      this.loadThemeColors()
      this.createBarChart()
      this.createLineChart()
    })
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['data-theme']
    })
  },

  /* --- Carregar cores do tema --- */
  loadThemeColors() {
    const style = getComputedStyle(document.documentElement)
    this.colors.primary = style.getPropertyValue('--cor-primaria').trim() || '#00D084'
    this.colors.secondary = style.getPropertyValue('--cor-secundaria').trim() || '#2DD4BF'
    this.colors.destaque = style.getPropertyValue('--cor-destaque').trim() || '#8B5CF6'
    this.colors.card = style.getPropertyValue('--card').trim() || '#111827'
    this.colors.text = style.getPropertyValue('--text-muted').trim() || '#94a3b8'
    this.colors.border = style.getPropertyValue('--border').trim() || '#1e293b'
    this.colors.grid = `rgba(255,255,255,0.04)`
  },

  /* --- DPI Scaling para telas retina --- */
  getScale() {
    return window.devicePixelRatio || 1
  },

  /* ============================================
     Gráfico de Barras - Evolução da Produção
     ============================================ */
  createBarChart() {
    const canvas = document.getElementById('chart-barras')
    if (!canvas) return

    const container = canvas.parentElement
    const rect = container.getBoundingClientRect()
    const W = rect.width
    const H = rect.height || 280
    const scale = this.getScale()

    canvas.width = W * scale
    canvas.height = H * scale
    canvas.style.width = W + 'px'
    canvas.style.height = H + 'px'

    const ctx = canvas.getContext('2d')
    ctx.scale(scale, scale)

    const data = [
      { label: 'Jan', value: 420 },
      { label: 'Fev', value: 380 },
      { label: 'Mar', value: 510 },
      { label: 'Abr', value: 480 },
      { label: 'Mai', value: 620 },
      { label: 'Jun', value: 590 },
      { label: 'Jul', value: 680 },
      { label: 'Ago', value: 720 },
      { label: 'Set', value: 650 },
      { label: 'Out', value: 780 },
      { label: 'Nov', value: 820 },
      { label: 'Dez', value: 910 }
    ]

    const padding = { top: 20, right: 20, bottom: 36, left: 50 }
    const chartW = W - padding.left - padding.right
    const chartH = H - padding.top - padding.bottom
    const barW = chartW / data.length * 0.65
    const gap = chartW / data.length * 0.35
    const maxVal = Math.max(...data.map(d => d.value)) * 1.15

    ctx.clearRect(0, 0, W, H)

    /* Grade horizontal */
    ctx.strokeStyle = this.colors.grid
    ctx.lineWidth = 1
    for (let i = 0; i <= 4; i++) {
      const y = padding.top + (chartH / 4) * i
      ctx.beginPath()
      ctx.moveTo(padding.left, y)
      ctx.lineTo(W - padding.right, y)
      ctx.stroke()

      ctx.fillStyle = this.colors.text
      ctx.font = '10px sans-serif'
      ctx.textAlign = 'right'
      ctx.fillText(Math.round(maxVal - (maxVal / 4) * i), padding.left - 8, y + 4)
    }

    /* Barras */
    data.forEach((d, i) => {
      const x = padding.left + (chartW / data.length) * i + gap / 2
      const barH = (d.value / maxVal) * chartH
      const y = padding.top + chartH - barH

      const gradient = ctx.createLinearGradient(x, y, x, padding.top + chartH)
      gradient.addColorStop(0, this.colors.primary)
      gradient.addColorStop(1, this.colors.secondary)
      ctx.fillStyle = gradient

      const radius = 4
      const bw = barW
      ctx.beginPath()
      ctx.moveTo(x + radius, y)
      ctx.lineTo(x + bw - radius, y)
      ctx.quadraticCurveTo(x + bw, y, x + bw, y + radius)
      ctx.lineTo(x + bw, padding.top + chartH)
      ctx.lineTo(x, padding.top + chartH)
      ctx.lineTo(x, y + radius)
      ctx.quadraticCurveTo(x, y, x + radius, y)
      ctx.fill()

      /* Label */
      ctx.fillStyle = this.colors.text
      ctx.font = '10px sans-serif'
      ctx.textAlign = 'center'
      ctx.fillText(d.label, x + bw / 2, padding.top + chartH + 16)
    })
  },

  /* ============================================
     Gráfico de Linha - Receita x Despesas
     ============================================ */
  createLineChart() {
    const canvas = document.getElementById('chart-linha')
    if (!canvas) return

    const container = canvas.parentElement
    const rect = container.getBoundingClientRect()
    const W = rect.width
    const H = rect.height || 280
    const scale = this.getScale()

    canvas.width = W * scale
    canvas.height = H * scale
    canvas.style.width = W + 'px'
    canvas.style.height = H + 'px'

    const ctx = canvas.getContext('2d')
    ctx.scale(scale, scale)

    const months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    const receita = [28, 32, 30, 35, 38, 42, 40, 45, 48, 52, 55, 62]
    const despesas = [22, 24, 25, 26, 28, 30, 29, 31, 33, 35, 36, 38]

    const padding = { top: 20, right: 20, bottom: 36, left: 56 }
    const chartW = W - padding.left - padding.right
    const chartH = H - padding.top - padding.bottom
    const maxVal = Math.max(...receita, ...despesas) * 1.2

    ctx.clearRect(0, 0, W, H)

    /* Grade horizontal */
    ctx.strokeStyle = this.colors.grid
    ctx.lineWidth = 1
    for (let i = 0; i <= 4; i++) {
      const y = padding.top + (chartH / 4) * i
      ctx.beginPath()
      ctx.moveTo(padding.left, y)
      ctx.lineTo(W - padding.right, y)
      ctx.stroke()

      ctx.fillStyle = this.colors.text
      ctx.font = '10px sans-serif'
      ctx.textAlign = 'right'
      ctx.fillText(Math.round(maxVal - (maxVal / 4) * i), padding.left - 8, y + 4)
    }

    const stepX = chartW / (months.length - 1)

    /* Eixo X labels */
    ctx.fillStyle = this.colors.text
    ctx.font = '10px sans-serif'
    ctx.textAlign = 'center'
    months.forEach((m, i) => {
      ctx.fillText(m, padding.left + stepX * i, padding.top + chartH + 16)
    })

    /* Função para desenhar linha com gradiente */
    const drawLine = (data, color, fillColor) => {
      ctx.beginPath()
      data.forEach((v, i) => {
        const x = padding.left + stepX * i
        const y = padding.top + chartH - (v / maxVal) * chartH
        if (i === 0) ctx.moveTo(x, y)
        else {
          const prevX = padding.left + stepX * (i - 1)
          const prevY = padding.top + chartH - (data[i - 1] / maxVal) * chartH
          const cpx = (prevX + x) / 2
          ctx.bezierCurveTo(cpx, prevY, cpx, y, x, y)
        }
      })

      /* Preenchimento sob a linha */
      const lastX = padding.left + stepX * (data.length - 1)
      const lastY = padding.top + chartH - (data[data.length - 1] / maxVal) * chartH
      ctx.lineTo(lastX, padding.top + chartH)
      ctx.lineTo(padding.left, padding.top + chartH)
      ctx.closePath()

      const gradient = ctx.createLinearGradient(0, padding.top, 0, padding.top + chartH)
      gradient.addColorStop(0, fillColor || color + '40')
      gradient.addColorStop(1, (fillColor || color) + '05')
      ctx.fillStyle = gradient
      ctx.fill()

      /* Linha principal */
      ctx.beginPath()
      data.forEach((v, i) => {
        const x = padding.left + stepX * i
        const y = padding.top + chartH - (v / maxVal) * chartH
        if (i === 0) ctx.moveTo(x, y)
        else {
          const prevX = padding.left + stepX * (i - 1)
          const prevY = padding.top + chartH - (data[i - 1] / maxVal) * chartH
          const cpx = (prevX + x) / 2
          ctx.bezierCurveTo(cpx, prevY, cpx, y, x, y)
        }
      })
      ctx.strokeStyle = color
      ctx.lineWidth = 2.5
      ctx.stroke()

      /* Pontos */
      data.forEach((v, i) => {
        const x = padding.left + stepX * i
        const y = padding.top + chartH - (v / maxVal) * chartH
        ctx.beginPath()
        ctx.arc(x, y, 4, 0, Math.PI * 2)
        ctx.fillStyle = color
        ctx.fill()
        ctx.strokeStyle = this.colors.card
        ctx.lineWidth = 2
        ctx.stroke()
      })
    }

    drawLine(despesas, '#ef4444', 'rgba(239,68,68,0.15)')
    drawLine(receita, this.colors.primary, 'rgba(0,208,132,0.15)')
  }
}

/* --- Inicializar --- */
document.addEventListener('DOMContentLoaded', () => AgroCharts.init())
