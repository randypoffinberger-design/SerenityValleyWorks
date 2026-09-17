// Navigation and filtering enhance pages that remain readable without JavaScript.
const year = document.getElementById('year');
if (year) year.textContent = new Date().getFullYear();
const menu = document.querySelector('.menu');
const nav = document.getElementById('nav');
if (menu && nav) {
  menu.hidden = false;
  document.documentElement.classList.add('enhanced');
  const closeMenu = () => {
    nav.classList.remove('open');
    menu.setAttribute('aria-expanded', 'false');
  };
  menu.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    menu.setAttribute('aria-expanded', String(open));
  });
  nav.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && nav.classList.contains('open')) {
      closeMenu();
      menu.focus();
    }
  });
  document.addEventListener('click', event => {
    if (!nav.contains(event.target) && !menu.contains(event.target)) closeMenu();
  });
  window.matchMedia('(min-width: 801px)').addEventListener('change', closeMenu);
}
const controls = document.querySelector('.library-controls');
if (controls) {
  controls.hidden = false;
  const search = document.getElementById('guide-search');
  const filters = [...document.querySelectorAll('[data-filter]')];
  const cards = [...document.querySelectorAll('#guide-results .article-card')];
  const groups = [...document.querySelectorAll('.guide-group')];
  const count = document.getElementById('results-count');
  const empty = document.querySelector('.empty-state');
  let selected = 'all';
  const apply = () => {
    const words = search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    let visible = 0;
    cards.forEach(card => {
      const match = (selected === 'all' || card.dataset.group === selected) && words.every(word => card.textContent.toLowerCase().includes(word));
      card.hidden = !match;
      if (match) visible++;
    });
    groups.forEach(group => { group.hidden = ![...group.querySelectorAll('.article-card')].some(card => !card.hidden); });
    filters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === selected)));
    count.textContent = `${visible} of ${cards.length} guides`;
    empty.hidden = visible !== 0;
  };
  filters.forEach(button => button.addEventListener('click', () => { selected = button.dataset.filter; apply(); }));
  search.addEventListener('input', apply);
  document.getElementById('clear-search').addEventListener('click', () => { search.value = ''; selected = 'all'; apply(); search.focus(); });
  // Topic deep links are normal document anchors, including without JavaScript.
  apply();
}
const printButton = document.querySelector('.print-button');
if (printButton) {
  printButton.hidden = false;
  printButton.addEventListener('click', () => window.print());
}
