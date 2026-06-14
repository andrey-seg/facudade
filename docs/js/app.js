/* ============================================
   AgroCalc Web - Aplicação Principal
   Sidebar, Tema, Toast, Navigation, Loading
   ============================================ */

const AgroCalc = {
  /* --- Inicialização --- */
  init() {
    this.cacheElements()
    this.loadTheme()
    this.setupSidebar()
    this.setupThemeToggle()
    this.setupSearch()
    this.setupNavigation()
    this.setupToastDismiss()
    this.showWelcomeToast()
    this.setActiveNav()
  },

  /* --- Cache de Elementos DOM --- */
  cacheElements() {
    this.sidebar = document.querySelector('.sidebar')
    this.sidebarToggle = document.querySelector('.sidebar-toggle')
    this.sidebarOverlay = document.querySelector('.sidebar-overlay')
    this.themeToggle = document.querySelector('.theme-toggle')
    this.searchInput = document.querySelector('.header-search input')
    this.toastContainer = document.querySelector('.toast-container')
    this.navLinks = document.querySelectorAll('.sidebar-nav a')
  },

  /* --- Tema (Dark / Light) --- */
  loadTheme() {
    const saved = localStorage.getItem('agrocalc-theme') || 'dark'
    document.documentElement.setAttribute('data-theme', saved)
    this.updateThemeIcon(saved)
  },

  setupThemeToggle() {
    if (!this.themeToggle) return
    this.themeToggle.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme')
      const next = current === 'dark' ? 'light' : 'dark'
      document.documentElement.setAttribute('data-theme', next)
      localStorage.setItem('agrocalc-theme', next)
      this.updateThemeIcon(next)
      this.showToast(
        next === 'dark' ? 'Tema escuro ativado' : 'Tema claro ativado',
        'info'
      )
    })
  },

  updateThemeIcon(theme) {
    if (!this.themeToggle) return
    this.themeToggle.textContent = theme === 'dark' ? '\u2600\uFE0F' : '\uD83C\uDF19'
  },

  /* --- Sidebar (Mobile) --- */
  setupSidebar() {
    if (!this.sidebarToggle || !this.sidebar) return

    this.sidebarToggle.addEventListener('click', () => {
      this.sidebar.classList.toggle('open')
      this.sidebarOverlay?.classList.toggle('active')
    })

    if (this.sidebarOverlay) {
      this.sidebarOverlay.addEventListener('click', () => {
        this.sidebar.classList.remove('open')
        this.sidebarOverlay.classList.remove('active')
      })
    }

    window.addEventListener('resize', () => {
      if (window.innerWidth > 768) {
        this.sidebar?.classList.remove('open')
        this.sidebarOverlay?.classList.remove('active')
      }
    })
  },

  /* --- Navegação Ativa --- */
  setupNavigation() {
    this.navLinks.forEach(link => {
      link.addEventListener('click', function () {
        document.querySelectorAll('.sidebar-nav a').forEach(l => l.classList.remove('active'))
        this.classList.add('active')
      })
    })
  },

  setActiveNav() {
    const currentPath = window.location.pathname.split('/').pop() || 'index.html'
    this.navLinks.forEach(link => {
      const href = link.getAttribute('href')
      if (href === currentPath) {
        link.classList.add('active')
      }
    })
  },

  /* --- Search --- */
  setupSearch() {
    if (!this.searchInput) return
    this.searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        const query = this.searchInput.value.trim()
        if (query) {
          this.showToast(`Buscando por "${query}"...`, 'info')
        }
      }
    })
  },

  /* --- Toast Notifications --- */
  showToast(message, type = 'success', duration = 3500) {
    if (!this.toastContainer) {
      const container = document.createElement('div')
      container.className = 'toast-container'
      document.body.appendChild(container)
      this.toastContainer = container
    }

    const icons = {
      success: '\u2705',
      error: '\u274C',
      info: '\u2139\uFE0F'
    }

    const toast = document.createElement('div')
    toast.className = `toast ${type}`
    toast.innerHTML = `
      <span class="toast-icon">${icons[type] || ''}</span>
      <span>${message}</span>
      <button class="toast-close" aria-label="Fechar">&times;</button>
    `

    this.toastContainer.appendChild(toast)

    const closeBtn = toast.querySelector('.toast-close')
    closeBtn.addEventListener('click', () => this.dismissToast(toast))

    setTimeout(() => this.dismissToast(toast), duration)
  },

  dismissToast(toast) {
    if (!toast.parentNode) return
    toast.style.opacity = '0'
    toast.style.transform = 'translateX(100%)'
    toast.style.transition = 'all 0.3s ease'
    setTimeout(() => toast.remove(), 300)
  },

  setupToastDismiss() {
    document.addEventListener('click', (e) => {
      if (e.target.closest('.toast-close')) {
        const toast = e.target.closest('.toast')
        if (toast) this.dismissToast(toast)
      }
    })
  },

  showWelcomeToast() {
    setTimeout(() => {
      this.showToast('Bem-vindo ao AgroCalc Web', 'success', 3000)
    }, 500)
  },

  /* --- Loading State --- */
  showLoading(container) {
    const loader = document.createElement('div')
    loader.className = 'card'
    loader.style.cssText = 'display:flex;align-items:center;justify-content:center;padding:60px;'
    loader.innerHTML = '<div class="loading-spinner"></div>'
    container.innerHTML = ''
    container.appendChild(loader)
    return loader
  },

  /* --- Formatação --- */
  formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value)
  },

  formatNumber(value) {
    return new Intl.NumberFormat('pt-BR').format(value)
  },

  formatPercent(value) {
    return `${value.toFixed(1)}%`
  },

  formatDate(date) {
    return new Intl.DateTimeFormat('pt-BR').format(new Date(date))
  }
}

/* --- Inicializar quando o DOM estiver pronto --- */
document.addEventListener('DOMContentLoaded', () => AgroCalc.init())
