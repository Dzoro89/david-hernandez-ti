'use strict';

const menuButton = document.querySelector('.menu-button');
const navigation = document.querySelector('#navigation');
if (menuButton && navigation) {
  menuButton.hidden = false;
  const closeMenu = () => {
    navigation.classList.remove('open');
    menuButton.setAttribute('aria-expanded', 'false');
  };
  menuButton.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') !== 'true';
    menuButton.setAttribute('aria-expanded', String(open));
    navigation.classList.toggle('open', open);
  });
  navigation.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
      closeMenu();
      menuButton.focus();
    }
  });
  window.matchMedia('(min-width: 681px)').addEventListener('change', closeMenu);
}

const controls = document.querySelector('.lab-controls');
if (controls) {
  controls.hidden = false;
  const filters = [...controls.querySelectorAll('[data-filter]')];
  const search = document.querySelector('#lab-search');
  const cards = [...document.querySelectorAll('.lab-card')];
  const count = document.querySelector('#filter-result');
  const empty = document.querySelector('.empty-results');
  let activeFilter = 'todos';
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
  const applyFilters = () => {
    const query = normalize(search.value);
    let visible = 0;
    for (const card of cards) {
      const matches = (activeFilter === 'todos' || card.dataset.category === activeFilter)
        && normalize(card.textContent).includes(query);
      card.hidden = !matches;
      if (matches) visible += 1;
    }
    count.textContent = `${visible} ${visible === 1 ? 'laboratorio disponible' : 'laboratorios disponibles'}`;
    empty.hidden = visible > 0;
  };
  for (const filter of filters) {
    filter.addEventListener('click', () => {
      activeFilter = filter.dataset.filter;
      for (const button of filters) {
        const active = button === filter;
        button.classList.toggle('active', active);
        button.setAttribute('aria-pressed', String(active));
      }
      applyFilters();
    });
  }
  search.addEventListener('input', applyFilters);
  applyFilters();
}

const copyButton = document.querySelector('.copy-email');
if (copyButton && navigator.clipboard) {
  copyButton.hidden = false;
  const toast = document.querySelector('.toast');
  let toastTimer;
  copyButton.addEventListener('click', async () => {
    let message;
    try {
      await navigator.clipboard.writeText('dave989172@gmail.com');
      message = 'Correo copiado: dave989172@gmail.com';
    } catch {
      message = 'Puedes copiar el correo directamente: dave989172@gmail.com';
    }
    clearTimeout(toastTimer);
    toast.textContent = message;
    toast.classList.add('visible');
    toastTimer = setTimeout(() => toast.classList.remove('visible'), 5000);
  });
}

const printButton = document.querySelector('.print-profile');
if (printButton) {
  printButton.hidden = false;
  printButton.addEventListener('click', () => window.print());
}
