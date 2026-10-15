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

function setupFilters(controlsSelector, searchSelector, cardsSelector, resultSelector, emptySelector, singular, plural) {
  const controls = document.querySelector(controlsSelector);
  if (!controls) return;
  controls.hidden = false;
  const filters = [...controls.querySelectorAll('[data-filter]')];
  const search = document.querySelector(searchSelector);
  const cards = [...document.querySelectorAll(cardsSelector)];
  const count = document.querySelector(resultSelector);
  const empty = document.querySelector(emptySelector);
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
    count.textContent = `${visible} ${visible === 1 ? singular : plural}`;
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
setupFilters('.lab-controls', '#lab-search', '.lab-card', '#filter-result', '.empty-results', 'laboratorio disponible', 'laboratorios disponibles');
setupFilters('.credential-controls', '#credential-search', '.credential-card', '#credential-result', '.credential-empty', 'actividad documentada', 'actividades documentadas');

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
