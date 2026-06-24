/* Spring Real Estate — AI Search & Routing
   Eén taxonomie, twee voordeuren: de zoekbalk lost op naar dezelfde structuur
   als het klikgedeelte (5 categorieën). Client-side router: intent + entiteiten. */
(function () {
  const forms = [...document.querySelectorAll('form.search')];
  if (!forms.length) return;
  const IDX = window.SPRING_INDEX || { units: [], people: [], listings: [] };
  let lang = 'nl';
  try { lang = localStorage.getItem('spring-lang') || document.documentElement.lang || 'nl'; } catch (_) {}
  const L = (nl, en, es) => lang === 'en' ? en : lang === 'es' ? es : nl;
  const norm = s => (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');

  const CATS = [
    { key: 'objecten', label: L('Objecten', 'Properties', 'Inmuebles'), url: 'listings.html', kw: 'huur koop kopen huren pand object ruimte kantoor kantoorruimte bedrijfsruimte loods winkel retail belegging beleggingsobject te huur te koop m2 vierkante meter aanbod serviced office werkplek', ic: '<path d="M3 21h18M5 21V8l7-5 7 5v13M9 21v-6h6v6"/>' },
    { key: 'diensten', label: L('Diensten', 'Services', 'Servicios'), url: 'diensten.html', kw: 'dienst diensten taxatie taxeren taxateur beheer vastgoedbeheer verkopen verhuren verkoop verhuur marketing advies asset management herbouwwaarde verzekering aankoop strategisch administratie design build', ic: '<path d="M3 9l9-7 9 7v11a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/>' },
    { key: 'experts', label: L('Experts', 'Experts', 'Expertos'), url: 'agents.html', kw: 'expert experts specialist adviseur adviseurs team medewerker wie contactpersoon makelaar taxateur partner', ic: '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>' },
    { key: 'onderzoek', label: L('Onderzoek', 'Insights', 'Análisis'), url: 'resources.html', kw: 'markt trend trends blog artikel kennis onderzoek rapport begrip begrippen wat is uitleg case cases klantverhaal marktinzicht data', ic: '<path d="M3 3v18h18"/><path d="M7 14l3-4 3 2 4-6"/>' },
    { key: 'vacatures', label: L('Vacatures', 'Careers', 'Empleo'), url: 'vacatures.html', kw: 'vacature vacatures werken bij baan stage carriere job jobs solliciteren sollicitatie werk', ic: '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>' },
  ];
  const PAGES = [
    { n: L('Begrippen', 'Glossary', 'Glosario'), u: 'begrippen.html', kw: 'begrip begrippen jargon uitleg kk bar nar breeam erfpacht walt', cat: 'onderzoek' },
    { n: L('Klantverhalen & cases', 'Client cases', 'Casos'), u: 'cases.html', kw: 'case cases klantverhaal resultaat referentie', cat: 'onderzoek' },
    { n: L('Sectoren', 'Sectors', 'Sectores'), u: 'sectoren.html', kw: 'sector sectoren zorg logistiek retail kantoren residentieel hospitality', cat: 'diensten' },
    { n: 'About Us', u: 'about.html', kw: 'about over ons bedrijf missie geschiedenis', cat: 'diensten' },
    { n: 'Contact', u: 'contact.html', kw: 'contact bellen mailen afspraak', cat: 'diensten' },
  ];
  const DOEL = [
    { n: L('Gebruiker', 'User', 'Usuario'), u: 'doelgroep-gebruiker.html', kw: 'gebruiker kantoor werkplek huren ruimte zoeken' },
    { n: L('Eigenaar', 'Owner', 'Propietario'), u: 'doelgroep-eigenaar.html', kw: 'eigenaar verkopen verhuren rendement' },
    { n: L('Investeerder', 'Investor', 'Inversor'), u: 'doelgroep-investeerder.html', kw: 'investeerder beleggen belegging investeren rendement' },
    { n: L('Ontwikkelaar', 'Developer', 'Promotor'), u: 'doelgroep-ontwikkelaar.html', kw: 'ontwikkelaar ontwikkelen gebiedsontwikkeling acquisitie' },
  ];
  const LOC = [
    { n: 'Utrecht', u: 'locatie-utrecht.html', kw: 'utrecht hoofdkantoor' },
    { n: 'Amsterdam', u: 'locatie-amsterdam.html', kw: 'amsterdam zuidas' },
    { n: 'Valencia', u: 'locatie-valencia.html', kw: 'valencia spanje espana' },
    { n: 'Estepona', u: 'locatie-estepona.html', kw: 'estepona costa del sol spanje' },
  ];

  function intentCat(q) {
    const nq = norm(q); const toks = nq.split(/\s+/).filter(Boolean);
    let best = CATS[0], bestScore = 0;
    CATS.forEach(c => {
      const kw = norm(c.kw); let s = 0;
      toks.forEach(t => { if (t.length > 2 && kw.indexOf(t) >= 0) s++; });
      if (s > bestScore) { bestScore = s; best = c; }
    });
    if (bestScore === 0 && (/\b(amsterdam|utrecht|valencia|estepona|zuidas)\b/.test(nq) || /\d/.test(nq) || /m2|m²/.test(nq))) best = CATS[0];
    return { cat: best, score: bestScore };
  }

  function results(q) {
    const nq = norm(q); if (!nq) return [];
    const out = [];
    const hit = hay => norm(hay).indexOf(nq) >= 0;
    IDX.listings.forEach(x => { if (hit(x.n) || hit(x.city) || hit(x.loc) || hit(x.t) || hit(x.offer)) out.push({ t: x.n, s: x.city || '', u: x.u, c: 'objecten' }); });
    IDX.units.forEach(x => { if (hit(x.n) || hit(x.kw)) out.push({ t: x.n, s: L('Dienst', 'Service', 'Servicio'), u: x.u, c: 'diensten' }); });
    DOEL.forEach(x => { if (hit(x.n) || hit(x.kw)) out.push({ t: x.n, s: L('Doelgroep', 'Audience', 'Público'), u: x.u, c: 'diensten' }); });
    IDX.people.forEach(x => { if (hit(x.n) || hit(x.r)) out.push({ t: x.n, s: x.r, u: x.u, c: 'experts' }); });
    LOC.forEach(x => { if (hit(x.n) || hit(x.kw)) out.push({ t: x.n, s: L('Locatie', 'Location', 'Ubicación'), u: x.u, c: 'objecten' }); });
    PAGES.forEach(x => { if (hit(x.n) || hit(x.kw)) out.push({ t: x.n, s: '', u: x.u, c: x.cat }); });
    out.sort((a, b) => (norm(b.t).indexOf(nq) === 0 ? 1 : 0) - (norm(a.t).indexOf(nq) === 0 ? 1 : 0));
    return out.slice(0, 7);
  }

  const catIcon = key => { const c = CATS.find(x => x.key === key) || CATS[0]; return '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' + c.ic + '</svg>'; };
  const catChip = c => '<button type="button" class="ais-cat" data-url="' + c.url + '"><span class="ais-ic">' + catIcon(c.key) + '</span>' + c.label + '</button>';
  const esc = s => (s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

  forms.forEach(form => {
    const input = form.querySelector('input[type=text]') || form.querySelector('input'); if (!input) return;
    form.classList.add('ais-form');
    const panel = document.createElement('div'); panel.className = 'ais-panel'; form.appendChild(panel);
    function show(html) { panel.innerHTML = html; panel.classList.add('open'); }
    function hide() { panel.classList.remove('open'); }
    function destFor(q) { const r = results(q); if (r.length) return r[0].u; const c = intentCat(q).cat; return c.key === 'objecten' ? 'listings.html?q=' + encodeURIComponent(q) : c.url; }
    function render() {
      const q = input.value.trim();
      if (!q) { show('<div class="ais-h">' + L('Waar bent u naar op zoek?', 'What are you looking for?', '¿Qué buscas?') + '</div><div class="ais-cats">' + CATS.map(catChip).join('') + '</div>'); return; }
      const cat = intentCat(q).cat;
      const action = '<a class="ais-action" href="' + (cat.key === 'objecten' ? 'listings.html?q=' + encodeURIComponent(q) : cat.url) + '"><span class="ais-ic">' + catIcon(cat.key) + '</span><span class="ais-tx"><b>' + esc(q) + '</b><span class="ais-sub">' + L('Zoek in', 'Search in', 'Buscar en') + ' ' + cat.label + '</span></span><span class="ais-arr">&rarr;</span></a>';
      const rs = results(q);
      const rows = rs.map(r => '<a class="ais-row" href="' + r.u + '"><span class="ais-ic">' + catIcon(r.c) + '</span><span class="ais-tx"><b>' + esc(r.t) + '</b>' + (r.s ? '<span class="ais-sub">' + esc(r.s) + '</span>' : '') + '</span></a>').join('');
      show(action + (rows ? '<div class="ais-list">' + rows + '</div>' : ''));
    }
    input.addEventListener('focus', render);
    input.addEventListener('input', render);
    panel.addEventListener('mousedown', e => { const t = e.target.closest('.ais-cat'); if (t) { e.preventDefault(); location.href = t.dataset.url; } });
    form.addEventListener('submit', e => { e.preventDefault(); const q = input.value.trim(); if (q) location.href = destFor(q); });
    document.addEventListener('click', e => { if (!form.contains(e.target)) hide(); });
    input.addEventListener('keydown', e => { if (e.key === 'Escape') hide(); });
  });
})();
