/* ============================================
   AGROCALC WEB — Scripts do Dashboard
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* ----- Inicializar Lucide Icons ----- */
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }

  /* ==========================================
     SIDEBAR — Mobile Toggle
     ========================================== */
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebarOverlay');
  const menuToggle = document.getElementById('menuToggle');

  function openSidebar() {
    sidebar.classList.add('open');
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeSidebar() {
    sidebar.classList.remove('open');
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  }

  menuToggle.addEventListener('click', openSidebar);
  overlay.addEventListener('click', closeSidebar);

  /* Fechar sidebar ao clicar em nav-item (mobile) */
  document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', () => {
      if (window.innerWidth <= 992) {
        closeSidebar();
      }
    });
  });

  /* ==========================================
     NAVEGAÇÃO — Troca de páginas
     ========================================== */
  const navItems = document.querySelectorAll('.nav-item');
  const pageSections = document.querySelectorAll('.page-section');

  navItems.forEach(item => {
    item.addEventListener('click', (e) => {
      e.preventDefault();

      navItems.forEach(n => n.classList.remove('active'));
      item.classList.add('active');

      const page = item.dataset.page;
      pageSections.forEach(s => s.classList.remove('active'));
      const target = document.getElementById(`page-${page}`);
      if (target) {
        target.classList.add('active');
      }
    });
  });

  /* ==========================================
     SEARCH — Atalho Ctrl+K
     ========================================== */
  const searchInput = document.querySelector('.search-bar input');

  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      searchInput?.focus();
    }
  });

  /* ==========================================
     COUNTER — Animação de números
     ========================================== */
  function animateCounter(el) {
    const target = parseInt(el.dataset.target, 10);
    if (isNaN(target)) return;

    const duration = 1500;
    const start = performance.now();

    function update(now) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      // Easing: easeOutExpo
      const eased = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
      const current = Math.round(eased * target);

      el.textContent = formatNumber(current);

      if (progress < 1) {
        requestAnimationFrame(update);
      }
    }

    requestAnimationFrame(update);
  }

  function formatNumber(num) {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1).replace('.', ',') + 'M';
    }
    if (num >= 1000) {
      return num.toLocaleString('pt-BR');
    }
    return num.toString();
  }

  /* Observar counters com IntersectionObserver */
  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        counterObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.3 });

  document.querySelectorAll('.counter').forEach(el => {
    counterObserver.observe(el);
  });

  /* ==========================================
     GRÁFICO — Barras de produção
     ========================================== */
  const productionData = [
    { month: 'Jan', value: 320, meta: '320 t' },
    { month: 'Fev', value: 450, meta: '450 t' },
    { month: 'Mar', value: 580, meta: '580 t' },
    { month: 'Abr', value: 720, meta: '720 t' },
    { month: 'Mai', value: 890, meta: '890 t' },
    { month: 'Jun', value: 1050, meta: '1.050 t' },
    { month: 'Jul', value: 1200, meta: '1.200 t' },
    { month: 'Ago', value: 1350, meta: '1.350 t' },
    { month: 'Set', value: 1100, meta: '1.100 t' },
    { month: 'Out', value: 850, meta: '850 t' },
    { month: 'Nov', value: 600, meta: '600 t' },
    { month: 'Dez', value: 400, meta: '400 t' },
  ];

  const metaData = [350, 480, 600, 750, 900, 1100, 1250, 1400, 1150, 900, 650, 450];

  const chartBars = document.getElementById('chartBars');
  const maxValue = Math.max(...productionData.map(d => d.value), ...metaData);

  function renderChart() {
    chartBars.innerHTML = '';

    productionData.forEach((item, index) => {
      const barHeight = (item.value / maxValue) * 100;
      const metaHeight = (metaData[index] / maxValue) * 100;

      const group = document.createElement('div');
      group.className = 'bar-group';

      const wrapper = document.createElement('div');
      wrapper.className = 'bar-wrapper';

      const bar = document.createElement('div');
      bar.className = 'bar';
      bar.style.height = '0%';

      const tooltip = document.createElement('div');
      tooltip.className = 'bar-tooltip';
      tooltip.textContent = item.meta;
      bar.appendChild(tooltip);

      const metaBar = document.createElement('div');
      metaBar.style.cssText = `
        width: 100%;
        height: 0%;
        border-radius: 8px 8px 4px 4px;
        background: rgba(0, 180, 216, 0.25);
        border: 1px dashed rgba(0, 180, 216, 0.3);
        transition: height 1s cubic-bezier(0.4, 0, 0.2, 1);
        transition-delay: ${0.3 + index * 0.05}s;
        margin-top: 2px;
      `;

      wrapper.appendChild(bar);

      const label = document.createElement('span');
      label.className = 'bar-label';
      label.textContent = item.month;

      group.appendChild(wrapper);
      group.appendChild(label);
      chartBars.appendChild(group);

      // Animação com delay
      setTimeout(() => {
        bar.style.height = `${barHeight}%`;
        metaBar.style.height = `${metaHeight}%`;
      }, 100 + index * 60);
    });
  }

  const chartObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        renderChart();
        chartObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });

  chartObserver.observe(chartBars);

  /* ==========================================
     CONVERSOR — Decimal / Binário / Hex
     ========================================== */
  const decInput = document.getElementById('decInput');
  const binOutput = document.getElementById('binOutput');
  const hexOutput = document.getElementById('hexOutput');

  function updateConversor() {
    let value = parseInt(decInput.value, 10);
    if (isNaN(value) || value < 0) {
      value = 0;
      decInput.value = 0;
    }
    binOutput.textContent = value.toString(2);
    hexOutput.textContent = value.toString(16).toUpperCase();
  }

  decInput.addEventListener('input', updateConversor);
  updateConversor();

  /* ==========================================
     PORTA LÓGICA AND — Irrigação
     ========================================== */
  let portaA = 1;
  let portaB = 1;

  const toggleBtns = document.querySelectorAll('.toggle-btn');
  const portaActiveRow = document.getElementById('portaActiveRow');
  const portaDecisao = document.getElementById('portaDecisao');

  function updatePorta() {
    const result = portaA && portaB;

    // Atualizar tabela verdade — destacar linha ativa
    const rows = document.querySelectorAll('.porta-tabela-row:not(.header)');
    rows.forEach((row, idx) => {
      const vals = [
        [0, 0, 0],
        [0, 1, 0],
        [1, 0, 0],
        [1, 1, 1]
      ];
      const v = vals[idx];
      const isActive = v[0] === portaA && v[1] === portaB;

      row.classList.toggle('highlight', isActive);
      if (idx === 3) portaActiveRow.classList.add('highlight');
    });

    // Atualizar decisão
    portaDecisao.innerHTML = '';
    if (result) {
      portaDecisao.classList.remove('inactive');
      portaDecisao.innerHTML = `
        <i data-lucide="droplets" size="20"></i>
        <span>Ativar Irrigação</span>
      `;
    } else {
      portaDecisao.classList.add('inactive');
      portaDecisao.innerHTML = `
        <i data-lucide="x-circle" size="20"></i>
        <span>Irrigação Desligada</span>
      `;
    }
    lucide.createIcons();
  }

  toggleBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const input = btn.dataset.input;
      const value = parseInt(btn.dataset.value, 10);

      // Desativar irmãos
      const siblings = btn.closest('.toggle-group').querySelectorAll('.toggle-btn');
      siblings.forEach(s => s.classList.remove('active'));

      btn.classList.add('active');

      if (input === 'a') portaA = value;
      if (input === 'b') portaB = value;

      updatePorta();
    });
  });

  updatePorta();

  /* ==========================================
     ANIMAÇÃO DE ENTRADA — Cards
     ========================================== */
  const animateCards = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        entry.target.style.animationDelay = `${index * 0.08}s`;
        entry.target.classList.add('animate-in');
        animateCards.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.destaque-card, .info-card').forEach(el => {
    animateCards.observe(el);
  });

  /* ==========================================
     RESIZE — Fechar sidebar em resize
     ========================================== */
  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      if (window.innerWidth > 992 && sidebar.classList.contains('open')) {
        closeSidebar();
      }
    }, 200);
  });

  console.log('%c AgroCalc Web ', 'background: #00e396; color: #000; font-size: 16px; font-weight: bold; padding: 8px 12px; border-radius: 4px;');
  console.log('%c Dashboard Agrícola Premium ', 'color: #00b4d8; font-size: 12px;');
});
