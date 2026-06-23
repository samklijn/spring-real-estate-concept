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

// Moving hero banner (auto crossfade, with pause/play) — Colliers best practice
(function () {
  const bg = document.getElementById('heroBg');
  const toggle = document.getElementById('heroToggle');
  const dotsWrap = document.getElementById('heroDots');
  if (!bg) return;
  const slides = [...bg.querySelectorAll('img')];
  if (slides.length < 2) return;
  let i = 0, timer = null;
  const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let playing = !reduce;
  // dots
  const dots = slides.map((_, idx) => {
    const b = document.createElement('button');
    b.setAttribute('aria-label', 'Toon beeld ' + (idx + 1));
    if (idx === 0) b.classList.add('is-active');
    b.addEventListener('click', () => { show(idx); restart(); });
    dotsWrap && dotsWrap.appendChild(b);
    return b;
  });
  function show(n) {
    i = (n + slides.length) % slides.length;
    slides.forEach((s, idx) => s.classList.toggle('is-active', idx === i));
    dots.forEach((d, idx) => d.classList.toggle('is-active', idx === i));
  }
  function next() { show(i + 1); }
  function start() { stop(); timer = setInterval(next, 6000); }
  function stop() { if (timer) { clearInterval(timer); timer = null; } }
  function restart() { if (playing) start(); }
  function setPlaying(p) {
    playing = p;
    if (toggle) {
      toggle.querySelector('.ht-pause').style.display = p ? '' : 'none';
      toggle.querySelector('.ht-play').style.display = p ? 'none' : '';
      toggle.querySelector('.ht-label').textContent = p ? 'Pauze' : 'Afspelen';
    }
    p ? start() : stop();
  }
  if (toggle) toggle.addEventListener('click', () => setPlaying(!playing));
  setPlaying(playing);
})();

// Working filters + search (team page, resources) on .filterable sections
(function () {
  document.querySelectorAll('.filterable').forEach(scope => {
    const grid = scope.querySelector('.people-grid, .blog-grid');
    if (!grid) return;
    const items = [...grid.children];
    const chips = [...scope.querySelectorAll('.team-filter a')];
    const search = scope.querySelector('.list-search input');
    const empty = scope.querySelector('.filter-empty');
    let key = 'alle';
    function apply() {
      const q = (search ? search.value : '').toLowerCase().trim();
      let shown = 0;
      items.forEach(it => {
        const txt = it.textContent.toLowerCase();
        const cat = (it.getAttribute('data-cat') || '').toLowerCase();
        const okKey = key === 'alle' || (cat ? cat === key : txt.indexOf(key) >= 0);
        const okQ = !q || txt.indexOf(q) >= 0;
        const show = okKey && okQ;
        it.style.display = show ? '' : 'none';
        if (show) shown++;
      });
      if (empty) empty.style.display = shown ? 'none' : '';
    }
    chips.forEach(c => c.addEventListener('click', e => {
      e.preventDefault();
      key = (c.getAttribute('data-key') || c.textContent.trim().toLowerCase());
      if (key === 'alle' || c.textContent.trim().toLowerCase() === 'alle') key = 'alle';
      chips.forEach(x => x.classList.remove('active'));
      const tab = chips.find(x => (x.getAttribute('data-key') || x.textContent.trim().toLowerCase()) === key);
      (tab || chips[0]).classList.add('active');
      apply();
    }));
    // "toon alle" reset link inside empty-state
    scope.querySelectorAll('.filter-empty [data-key]').forEach(a => a.addEventListener('click', e => {
      e.preventDefault(); key = 'alle'; if (search) search.value = '';
      chips.forEach(x => x.classList.remove('active')); if (chips[0]) chips[0].classList.add('active'); apply();
    }));
    if (search) search.addEventListener('input', apply);
  });
})();

// Count-up animation for stat numbers ("resultaten laten oplopen")
(function () {
  const sel = '.hero-stats b, .stats-band b, .sf-stat b, .stat-pop b';
  const nodes = [...document.querySelectorAll(sel)].filter(el => /^\d[\d.]*(\+|%)?$/.test(el.textContent.trim()));
  if (!nodes.length || !('IntersectionObserver' in window)) return;
  function run(el) {
    const txt = el.textContent.trim();
    const m = txt.match(/^(\d[\d.]*)(\+|%)?$/);
    const hadDot = m[1].includes('.');
    const target = parseInt(m[1].replace(/\./g, ''), 10);
    const suffix = m[2] || '';
    const dur = 1100, t0 = performance.now();
    function fmt(n) { return hadDot && n >= 1000 ? n.toLocaleString('nl-NL') : String(n); }
    function step(now) {
      const p = Math.min(1, (now - t0) / dur);
      const e = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(Math.round(target * e)) + suffix;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  const obs = new IntersectionObserver((entries, o) => {
    entries.forEach(en => { if (en.isIntersecting) { run(en.target); o.unobserve(en.target); } });
  }, { threshold: 0.5 });
  nodes.forEach(n => obs.observe(n));
})();

// Clickable team members -> modal with their info
(function () {
  function buildModal() {
    const m = document.createElement('div');
    m.className = 'pmodal';
    m.innerHTML = '<div class="pmodal-ov" data-close></div>' +
      '<div class="pmodal-card"><button class="pmodal-close" data-close aria-label="Sluiten">&times;</button>' +
      '<div class="pm-photo"><img alt=""></div>' +
      '<div class="pm-body"><div class="pm-role"></div><h3></h3><p class="pm-bio"></p><div class="pm-contact"></div></div></div>';
    document.body.appendChild(m);
    m.addEventListener('click', e => { if (e.target.hasAttribute('data-close')) m.classList.remove('open'); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') m.classList.remove('open'); });
    return m;
  }
  let modal;
  const ICON = {
    mail: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
    phone: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.4-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>',
    linkedin: '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5A2.5 2.5 0 1 1 5 8.5a2.5 2.5 0 0 1-.02-5zM3 9h4v12H3zM9 9h3.8v1.7h.05c.53-1 1.8-2 3.7-2 4 0 4.75 2.6 4.75 6V21H21v-5.3c0-1.3 0-3-1.8-3s-2.1 1.4-2.1 2.9V21H13z"/></svg>'
  };
  document.addEventListener('click', e => {
    const card = e.target.closest('.person, .agent');
    if (!card) return;
    if (e.target.closest('a[href]')) return; // let real links work
    e.preventDefault();
    // each team member has their own page — navigate there when available
    const directProfile = card.getAttribute('data-profile');
    if (directProfile) { window.location.href = directProfile; return; }
    if (!modal) modal = buildModal();
    const img = card.querySelector('img');
    const name = (card.querySelector('.name') || {}).textContent || '';
    const role = (card.querySelector('.role') || {}).textContent || '';
    const bio = (card.querySelector('.bio') || {}).textContent ||
      (name + ' is specialist bij Spring Real Estate. Neem gerust contact op voor een kennismaking en persoonlijk advies.');
    modal.querySelector('.pm-photo img').src = img ? img.src : '';
    modal.querySelector('.pm-role').textContent = role;
    modal.querySelector('h3').textContent = name;
    modal.querySelector('.pm-bio').textContent = bio;
    const mail = (name.toLowerCase().replace(/[^a-z]+/g, '.').replace(/^\.|\.$/g, '') || 'info') + '@springrealestate.com';
    modal.querySelector('.pm-contact').innerHTML =
      '<a href="mailto:' + mail + '">' + ICON.mail + ' ' + mail + '</a>' +
      '<a href="tel:+31302001020">' + ICON.phone + ' +31 30 200 10 20</a>' +
      '<a href="#">' + ICON.linkedin + ' LinkedIn-profiel</a>';
    // link to a full profile page when one exists for this person
    const ROSTER = ['daan-van-der-meer', 'sofia-martin', 'lars-bakker', 'emma-de-vries', 'thomas-jansen', 'nina-aydin'];
    const slug = name.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
    const prof = card.getAttribute('data-profile') || (ROSTER.indexOf(slug) >= 0 ? 'profile-' + slug + '.html' : '');
    let pl = modal.querySelector('.pm-profile-link');
    if (!pl) { pl = document.createElement('a'); pl.className = 'btn btn--primary pm-profile-link'; pl.style.marginTop = '18px'; pl.textContent = 'Bekijk volledig profiel'; modal.querySelector('.pm-body').appendChild(pl); }
    if (prof) { pl.href = prof; pl.style.display = 'inline-flex'; } else { pl.style.display = 'none'; }
    modal.classList.add('open');
  });
})();

// Listings page — working filters (checkboxes + area + search), dynamic count & chips
(function () {
  const grid = document.querySelector('.results-grid');
  const filters = document.getElementById('filters');
  if (!grid || !filters) return;
  const cards = [...grid.querySelectorAll('.prop-card')];
  const checks = [...filters.querySelectorAll('input[type=checkbox][data-fgroup]')];
  const amin = document.getElementById('fAreaMin');
  const amax = document.getElementById('fAreaMax');
  const search = document.querySelector('.page-hero .search input');
  const rcCount = document.getElementById('rcCount');
  const chipbar = document.getElementById('chipbar');
  const empty = document.getElementById('listEmpty');
  const LABELS = { huur: 'Te huur', koop: 'Te koop', kantoor: 'Kantoorruimte', bedrijf: 'Bedrijfsruimte', winkel: 'Winkelruimte', belegging: 'Beleggingsobject', amsterdam: 'Amsterdam', utrecht: 'Utrecht', valencia: 'Valencia', estepona: 'Estepona' };
  function apply() {
    const groups = {};
    checks.filter(c => c.checked).forEach(c => { (groups[c.dataset.fgroup] = groups[c.dataset.fgroup] || new Set()).add(c.dataset.val); });
    const mn = parseFloat(amin && amin.value) || 0;
    const mx = parseFloat(amax && amax.value) || Infinity;
    const q = (search ? search.value : '').toLowerCase().trim();
    let shown = 0;
    cards.forEach(card => {
      let ok = true;
      for (const g in groups) { if (!groups[g].has(card.dataset[g])) { ok = false; break; } }
      if (ok) { const a = parseFloat(card.dataset.area) || 0; if (a < mn || a > mx) ok = false; }
      if (ok && q) ok = card.textContent.toLowerCase().indexOf(q) >= 0;
      card.style.display = ok ? '' : 'none';
      if (ok) shown++;
    });
    if (rcCount) rcCount.textContent = shown;
    if (empty) empty.style.display = shown ? 'none' : '';
    if (chipbar) {
      chipbar.innerHTML = '';
      checks.filter(c => c.checked).forEach(c => {
        const chip = document.createElement('span'); chip.className = 'fchip';
        chip.innerHTML = (LABELS[c.dataset.val] || c.dataset.val) + ' <button aria-label="Verwijder">&times;</button>';
        chip.querySelector('button').addEventListener('click', e => { e.preventDefault(); c.checked = false; apply(); });
        chipbar.appendChild(chip);
      });
    }
  }
  checks.forEach(c => c.addEventListener('change', apply));
  [amin, amax].forEach(el => el && el.addEventListener('input', apply));
  if (search) search.addEventListener('input', apply);
  function clearAll(e) { if (e) e.preventDefault(); checks.forEach(c => c.checked = false); if (amin) amin.value = ''; if (amax) amax.value = ''; if (search) search.value = ''; apply(); }
  const fc = document.getElementById('fClear'); if (fc) fc.addEventListener('click', clearAll);
  const fc2 = document.getElementById('listClear2'); if (fc2) fc2.addEventListener('click', clearAll);
  const ft = document.getElementById('filterToggle'); if (ft) ft.addEventListener('click', () => filters.classList.toggle('open'));
  apply();
})();

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

/* ============================================================
   NEXT-LEVEL ENHANCEMENTS (additive — appended)
   ============================================================ */

// 1. Scroll-reveal animations
(function () {
  if (!('IntersectionObserver' in window)) return;
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const sel = '.sec-head,.cards-grid,.kat-grid,.values-grid,.units-grid,.units-acc,.two-col,.statfeature,.txn-list,.news-wrap,.glossary,.vac-list,.people-grid,.dark-cards,.logos-row,.results-grid,.team-grid,.svc-grid,.sector-grid,.timeline,.pf-facts,.split,.panel';
  const els = [...document.querySelectorAll(sel)];
  els.forEach(e => e.classList.add('reveal'));
  const io = new IntersectionObserver((ents) => {
    ents.forEach(en => { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  els.forEach(e => io.observe(e));
  // failsafe: never leave content hidden
  setTimeout(() => els.forEach(e => e.classList.add('in')), 1800);
})();

// 2. Sticky shrinking header
(function () {
  const h = document.querySelector('.header'); if (!h) return;
  const on = () => h.classList.toggle('scrolled', window.scrollY > 24);
  on(); addEventListener('scroll', on, { passive: true });
})();

// 3. Active nav highlight
(function () {
  const page = (location.pathname.split('/').pop() || 'index.html');
  document.querySelectorAll('.nav a[href]').forEach(a => {
    const href = a.getAttribute('href');
    if (href === page) a.classList.add('active-nav');
  });
})();

// 4. Back-to-top button
(function () {
  const b = document.createElement('button');
  b.className = 'to-top'; b.setAttribute('aria-label', 'Terug naar boven');
  b.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M12 19V5M5 12l7-7 7 7"/></svg>';
  document.body.appendChild(b);
  const on = () => b.classList.toggle('show', window.scrollY > 600);
  on(); addEventListener('scroll', on, { passive: true });
  b.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
})();

// 5. Cookie consent banner
(function () {
  try { if (localStorage.getItem('spring-cookie')) return; } catch (_) {}
  const lang = (document.documentElement.lang || 'nl');
  const txt = lang === 'en' ? 'We use cookies to improve your experience and analyse traffic.'
    : lang === 'es' ? 'Usamos cookies para mejorar tu experiencia y analizar el tráfico.'
      : 'We gebruiken cookies om je ervaring te verbeteren en het gebruik te analyseren.';
  const ok = lang === 'en' ? 'Accept' : lang === 'es' ? 'Aceptar' : 'Akkoord';
  const c = document.createElement('div');
  c.className = 'cookie';
  c.innerHTML = '<p>' + txt + ' <a href="#">Privacy</a></p><button class="btn btn--primary">' + ok + '</button>';
  document.body.appendChild(c);
  c.querySelector('button').addEventListener('click', () => { try { localStorage.setItem('spring-cookie', '1'); } catch (_) {} c.remove(); });
})();

// 6. Favorites (hearts persist in localStorage)
(function () {
  const KEY = 'spring-favs';
  let favs; try { favs = JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (_) { favs = []; }
  document.querySelectorAll('.prop-card .fav').forEach(fav => {
    const card = fav.closest('.prop-card');
    const id = ((card.querySelector('h3') || {}).textContent || card.getAttribute('href') || '').trim();
    if (favs.indexOf(id) >= 0) fav.classList.add('is-fav');
    fav.addEventListener('click', e => {
      e.preventDefault(); e.stopPropagation();
      const i = favs.indexOf(id);
      if (i >= 0) { favs.splice(i, 1); fav.classList.remove('is-fav'); }
      else { favs.push(id); fav.classList.add('is-fav'); }
      try { localStorage.setItem(KEY, JSON.stringify(favs)); } catch (_) {}
    });
  });
})();

// 7. Working search → listings.html?q=… (and prefill/apply on listings)
(function () {
  const onListings = !!document.querySelector('.results-grid');
  document.querySelectorAll('form.search').forEach(f => {
    f.addEventListener('submit', e => {
      e.preventDefault();
      const inp = f.querySelector('input[type=text]') || f.querySelector('input');
      const q = inp ? inp.value.trim() : '';
      if (onListings) return; // listings filters live via its own module
      location.href = 'listings.html' + (q ? ('?q=' + encodeURIComponent(q)) : '');
    });
  });
  if (onListings) {
    const q = new URLSearchParams(location.search).get('q');
    if (q) { const inp = document.querySelector('.page-hero .search input'); if (inp) { inp.value = q; inp.dispatchEvent(new Event('input')); } }
  }
})();

// 8. Listing-detail gallery: thumbnail swap + lightbox
(function () {
  const main = document.querySelector('.g-main img');
  const thumbs = [...document.querySelectorAll('.g-side .g-thumb img')];
  if (!main && !thumbs.length) return;
  thumbs.forEach(th => th.addEventListener('click', () => { if (main) { const s = main.getAttribute('src'); main.setAttribute('src', th.getAttribute('src')); th.setAttribute('src', s); } }));
  const lb = document.createElement('div');
  lb.className = 'lightbox';
  lb.innerHTML = '<button class="lb-close" aria-label="Sluiten">&times;</button><img alt="">';
  document.body.appendChild(lb);
  const lbImg = lb.querySelector('img');
  if (main) main.addEventListener('click', () => { lbImg.src = main.src; lb.classList.add('open'); });
  lb.addEventListener('click', e => { if (e.target !== lbImg) lb.classList.remove('open'); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') lb.classList.remove('open'); });
})();

// 11. Skip-to-content link + main landmark
(function () {
  const target = document.querySelector('.hero, .page-hero, .detail-top, main, section');
  if (target && !target.id) target.id = 'main';
  const a = document.createElement('a');
  a.className = 'skip-link'; a.href = '#' + (target ? target.id : 'main');
  a.textContent = 'Naar inhoud';
  document.body.insertBefore(a, document.body.firstChild);
})();

// 12. Lazy-load images (skip above-the-fold hero/gallery)
(function () {
  document.querySelectorAll('img:not([loading])').forEach(img => {
    if (img.closest('.hero, .page-hero, .g-main, .logo')) return;
    img.loading = 'lazy'; img.decoding = 'async';
  });
})();

// 13. Form submit feedback (non-search forms)
(function () {
  function toast(msg) {
    let t = document.querySelector('.toast');
    if (!t) { t = document.createElement('div'); t.className = 'toast'; document.body.appendChild(t); }
    t.textContent = msg; t.classList.add('show');
    clearTimeout(t._h); t._h = setTimeout(() => t.classList.remove('show'), 3400);
  }
  document.querySelectorAll('form').forEach(f => {
    if (f.classList.contains('search')) return;
    f.addEventListener('submit', e => {
      e.preventDefault();
      const lang = document.documentElement.lang || 'nl';
      toast(lang === 'en' ? 'Thank you! We will be in touch shortly.' : lang === 'es' ? '¡Gracias! Te contactaremos en breve.' : 'Bedankt! We nemen snel contact met u op.');
      try { f.reset(); } catch (_) {}
    });
  });
})();

// 9 + 10. Structured data (JSON-LD) + Open Graph / Twitter meta
(function () {
  const head = document.head, origin = location.origin;
  function ld(obj) { const s = document.createElement('script'); s.type = 'application/ld+json'; s.textContent = JSON.stringify(obj); head.appendChild(s); }
  function meta(key, val, attr) { if (!val) return; const m = document.createElement('meta'); m.setAttribute(attr || 'property', key); m.setAttribute('content', val); head.appendChild(m); }
  // Organization / RealEstateAgent — every page
  ld({ "@context": "https://schema.org", "@type": "RealEstateAgent", "name": "Spring Real Estate", "url": origin + "/", "logo": origin + "/images/logo-ink.png", "image": origin + "/images/hero.jpg", "email": "info@springrealestate.com", "telephone": "+31302001020", "priceRange": "€€", "areaServed": ["Nederland", "España"], "address": { "@type": "PostalAddress", "streetAddress": "Stadhouderskade 12", "addressLocality": "Utrecht", "postalCode": "3531 BJ", "addressCountry": "NL" } });
  // WebSite + search action
  ld({ "@context": "https://schema.org", "@type": "WebSite", "name": "Spring Real Estate", "url": origin + "/", "potentialAction": { "@type": "SearchAction", "target": origin + "/listings.html?q={query}", "query-input": "required name=query" } });
  // Breadcrumbs from .crumbs
  const cr = document.querySelector('.crumbs');
  if (cr) {
    const parts = [...cr.childNodes].map(n => n.textContent).join('/').split('/').map(s => s.trim()).filter(s => s && s !== '·');
    const links = [...cr.querySelectorAll('a')];
    const items = parts.map((name, i) => { const o = { "@type": "ListItem", "position": i + 1, "name": name }; if (links[i]) o.item = new URL(links[i].getAttribute('href'), location.href).href; return o; });
    if (items.length) ld({ "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items });
  }
  // FAQPage from FAQ items
  const faqEls = [...document.querySelectorAll('.faq-list details, details.faq-item')];
  const faqs = faqEls.map(d => { const sum = d.querySelector('summary'); const ans = d.querySelector('.ans, .faq-a, p, div:not(:first-child)'); if (!sum) return null; const q = sum.textContent.replace(/\s*\+\s*$/, '').trim(); const a = (ans ? ans.textContent : '').trim(); return q && a ? { "@type": "Question", "name": q, "acceptedAnswer": { "@type": "Answer", "text": a } } : null; }).filter(Boolean);
  if (faqs.length) ld({ "@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faqs });
  // Open Graph / Twitter
  const desc = (document.querySelector('meta[name=description]') || {}).content || '';
  const img = document.querySelector('.hero img, .page-hero img, .media-tall img, .g-main img, .darkcard img');
  meta('og:title', document.title); meta('og:description', desc); meta('og:type', 'website');
  meta('og:site_name', 'Spring Real Estate'); meta('og:url', location.href);
  meta('og:image', img ? img.src : origin + '/images/hero.jpg');
  meta('twitter:card', 'summary_large_image', 'name'); meta('twitter:title', document.title, 'name'); meta('twitter:description', desc, 'name');
})();
