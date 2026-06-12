/* Spring Real Estate — concept interactions */

// Mobile menu
const burger = document.getElementById('burger');
const mobileMenu = document.getElementById('mobileMenu');
const mmClose = document.getElementById('mmClose');
if (burger) burger.addEventListener('click', () => mobileMenu.classList.add('open'));
if (mmClose) mmClose.addEventListener('click', () => mobileMenu.classList.remove('open'));

// Search tabs
const tabs = document.getElementById('searchTabs');
if (tabs) {
  tabs.addEventListener('click', e => {
    const btn = e.target.closest('button');
    if (!btn) return;
    tabs.querySelectorAll('button').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  });
}

// Language switcher (concept — stores choice; real site swaps content / routes /nl /en /es)
const lang = document.getElementById('lang');
if (lang) {
  lang.addEventListener('click', e => {
    const btn = e.target.closest('button');
    if (!btn) return;
    lang.querySelectorAll('button').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.documentElement.lang = btn.dataset.lang;
    try { localStorage.setItem('spring-lang', btn.dataset.lang); } catch (_) {}
  });
}
