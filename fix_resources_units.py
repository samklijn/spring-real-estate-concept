import re, os

ROOT = r'C:/Users/Gebruiker/spring-real-estate-concept'

# ═══════════════════════════════════════════════════════════════════════════
# 1. CSS — download-card strakker + layout-variety hulpklassen
# ═══════════════════════════════════════════════════════════════════════════
with open(ROOT + '/css/styles.css', encoding='utf-8') as f:
    css = f.read()

EXTRA_CSS = '''
/* ── download-card als full-bleed lead magnet ─────────────────────────── */
.lead-magnet{
  background:linear-gradient(135deg,var(--green) 0%,#5a8a2e 100%);
  color:#fff; padding:56px 0;
}
.lead-magnet .lm-inner{
  display:flex; align-items:center; justify-content:space-between;
  gap:2rem; flex-wrap:wrap;
}
.lead-magnet .lm-text .eyebrow{ color:rgba(255,255,255,.65); }
.lead-magnet .lm-text h2{ color:#fff; margin:.3rem 0 .5rem; font-size:clamp(1.3rem,2.5vw,1.9rem); }
.lead-magnet .lm-text p{ color:rgba(255,255,255,.8); max-width:48ch; font-size:.95rem; }
.lead-magnet .lm-form{ display:flex; gap:10px; flex-wrap:wrap; }
.lead-magnet .lm-form input[type=email]{
  flex:1; min-width:220px; border:0; border-radius:var(--r-pill);
  padding:12px 20px; font-family:inherit; font-size:.95rem; color:var(--ink);
}
.lead-magnet .lm-form .btn{ white-space:nowrap; background:#fff; color:var(--green); font-weight:700; }
.lead-magnet .lm-form .btn:hover{ background:var(--green-tint); }
@media(max-width:720px){
  .lead-magnet .lm-inner{ flex-direction:column; }
  .lead-magnet .lm-form{ width:100%; }
  .lead-magnet .lm-form input[type=email]{ width:100%; }
}
'''

if '.lead-magnet{' not in css:
    css += '\n' + EXTRA_CSS
    with open(ROOT + '/css/styles.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print('styles.css: lead-magnet CSS toegevoegd')
else:
    print('styles.css: lead-magnet al aanwezig')


# ═══════════════════════════════════════════════════════════════════════════
# 2. Unit pages — lead magnet terug + layout afwisseling
# ═══════════════════════════════════════════════════════════════════════════
UNIT_FILES = sorted([f for f in os.listdir(ROOT) if f.startswith('unit-') and f.endswith('.html')])

def get_h1_text(src):
    m = re.search(r'<h1[^>]*>(.+?)</h1>', src, re.DOTALL)
    if not m: return 'Spring Real Estate'
    return re.sub(r'<[^>]+>', '', m.group(1)).strip()

def fix_unit_page(src, unit_h1):
    # a) Voeg lead magnet toe voor de FAQ sectie
    LM = f'''
<!-- ── LEAD MAGNET ──────────────────────────────────────────────────── -->
<section class="lead-magnet">
<div class="container">
  <div class="lm-inner">
    <div class="lm-text">
      <span class="eyebrow">Gratis download</span>
      <h2>Whitepaper: {unit_h1}</h2>
      <p>Ontvang onze praktische gids direct in uw inbox — inclusief marktcijfers en aanpaktips.</p>
    </div>
    <form class="lm-form" onsubmit="return false">
      <input type="email" placeholder="Uw e-mailadres">
      <button class="btn btn--primary btn--lg">Download gratis</button>
    </form>
  </div>
</div>
</section>

'''
    # Voeg in vóór FAQ sectie (als die er nog niet in staat)
    if 'lead-magnet' not in src and 'id="faq"' in src:
        src = src.replace('\n<section class="section--soft" id="faq">', LM + '<section class="section--soft" id="faq">')

    # b) Expertises sectie: voeg section--soft toe voor visuele afwisseling
    src = src.replace(
        '<section class="section" id="expertises">',
        '<section class="section section--soft" id="expertises">'
    )

    # c) Reviews sectie: geef gekleurde achtergrond (green-tint)
    src = src.replace(
        '<section class="section" id="reviews">',
        '<section class="section" id="reviews" style="background:var(--green-tint)">'
    )

    return src

total = 0
for fname in UNIT_FILES:
    path = os.path.join(ROOT, fname)
    with open(path, encoding='utf-8') as f:
        src = f.read()
    h1 = get_h1_text(src)
    new = fix_unit_page(src, h1)
    if new != src:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new)
        print(f'  {fname}: bijgewerkt ({len(new.splitlines())}L)')
        total += 1
    else:
        print(f'  {fname}: geen wijzigingen')
print(f'Unit pages bijgewerkt: {total}/{len(UNIT_FILES)}')


# ═══════════════════════════════════════════════════════════════════════════
# 3. cases.html — stats band + spotlight case + betere cards
# ═══════════════════════════════════════════════════════════════════════════
with open(ROOT + '/cases.html', encoding='utf-8') as f:
    cas = f.read()

CASES_INSERT = '''
<!-- ── STATS BAND ─────────────────────────────────────────────────── -->
<section class="section--tight" style="background:#EBF4D6;border-bottom:1px solid #C5DFA0">
<div class="container">
  <div class="grid" style="grid-template-columns:repeat(4,1fr);gap:0;text-align:center">
    <div style="border-right:1px solid #C5DFA0;padding:1.5rem 0">
      <b style="font-size:2rem;font-weight:800;color:var(--ink)">1.500+</b>
      <span style="display:block;font-size:.85rem;color:var(--ink-soft);margin-top:4px">Succesvolle cases</span>
    </div>
    <div style="border-right:1px solid #C5DFA0;padding:1.5rem 0">
      <b style="font-size:2rem;font-weight:800;color:var(--ink)">98%</b>
      <span style="display:block;font-size:.85rem;color:var(--ink-soft);margin-top:4px">Klanttevredenheid</span>
    </div>
    <div style="border-right:1px solid #C5DFA0;padding:1.5rem 0">
      <b style="font-size:2rem;font-weight:800;color:var(--ink)">€1,2 mld</b>
      <span style="display:block;font-size:.85rem;color:var(--ink-soft);margin-top:4px">Vastgoed begeleid</span>
    </div>
    <div style="padding:1.5rem 0">
      <b style="font-size:2rem;font-weight:800;color:var(--ink)">15+</b>
      <span style="display:block;font-size:.85rem;color:var(--ink-soft);margin-top:4px">Jaar ervaring</span>
    </div>
  </div>
</div>
</section>

<!-- ── SPOTLIGHT CASE ─────────────────────────────────────────────── -->
<section class="section--tight section--soft">
<div class="container">
  <span class="eyebrow">Uitgelichte case</span>
  <div class="two-col" style="align-items:center;gap:3rem;margin-top:1.5rem">
    <div class="media-tall" style="border-radius:12px;overflow:hidden">
      <img src="images/photo-1.jpg" alt="Herpositionering kantoor" style="width:100%;height:100%;object-fit:cover">
    </div>
    <div class="prose">
      <span class="cat" style="background:var(--green);color:#fff;padding:4px 12px;border-radius:20px;font-size:.8rem;font-weight:600;display:inline-block;margin-bottom:16px">Asset management · Amsterdam</span>
      <h2 class="disp" style="font-size:1.8rem">Herpositionering levert <em>+18% rendement</em> op in 14 maanden</h2>
      <p style="color:#555;margin:.75rem 0 1.25rem">Een belegger met een leegstaand kantoorpand vroeg Spring om een strategie. Van zoekprofiel tot verhuurde meters: Spring begeleidde het volledige traject — van duurzame renovatie tot turn-key verhuur aan een tech-scale-up.</p>
      <ul style="list-style:none;padding:0;display:grid;gap:8px;margin-bottom:1.5rem">
        <li style="display:flex;gap:10px;align-items:center"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4"><path d="M5 12l5 5L20 6"/></svg><strong>Resultaat:</strong>&nbsp;+18% rendement YoY</li>
        <li style="display:flex;gap:10px;align-items:center"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4"><path d="M5 12l5 5L20 6"/></svg><strong>Bezetting:</strong>&nbsp;van 0% naar 98% in 14 maanden</li>
        <li style="display:flex;gap:10px;align-items:center"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4"><path d="M5 12l5 5L20 6"/></svg><strong>Aanpak:</strong>&nbsp;herpositionering + duurzame renovatie</li>
        <li style="display:flex;gap:10px;align-items:center"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4"><path d="M5 12l5 5L20 6"/></svg><strong>Doorlooptijd:</strong>&nbsp;14 maanden van plan tot volledige verhuur</li>
      </ul>
      <a href="contact.html" class="btn btn--primary">Soortgelijke case bespreken</a>
    </div>
  </div>
</div>
</section>

<!-- ── STATISTIEKEN KLANTEN ───────────────────────────────────────── -->
<section class="section dark-sec">
<div class="container">
  <div class="center" style="max-width:700px;margin:0 auto 36px">
    <span class="eyebrow" style="color:var(--green-soft)">Bewezen resultaat</span>
    <h2 class="disp disp--light">Elk project, een <em>meetbaar verschil</em></h2>
  </div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1.5rem">
    <div style="background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);border-radius:12px;padding:1.75rem;text-align:center">
      <div style="font-size:2.2rem;font-weight:800;color:var(--green-soft)">+18%</div>
      <p style="color:rgba(255,255,255,.7);font-size:.9rem;margin:.5rem 0 0">Gemiddeld rendement<br>na herpositionering</p>
    </div>
    <div style="background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);border-radius:12px;padding:1.75rem;text-align:center">
      <div style="font-size:2.2rem;font-weight:800;color:var(--green-soft)">6 wkn</div>
      <p style="color:rgba(255,255,255,.7);font-size:.9rem;margin:.5rem 0 0">Gemiddelde doorlooptijd<br>verhuurtraject</p>
    </div>
    <div style="background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);border-radius:12px;padding:1.75rem;text-align:center">
      <div style="font-size:2.2rem;font-weight:800;color:var(--green-soft)">98%</div>
      <p style="color:rgba(255,255,255,.7);font-size:.9rem;margin:.5rem 0 0">Bezettingsgraad na<br>Spring-traject</p>
    </div>
    <div style="background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);border-radius:12px;padding:1.75rem;text-align:center">
      <div style="font-size:2.2rem;font-weight:800;color:var(--green-soft)">4,8/5</div>
      <p style="color:rgba(255,255,255,.7);font-size:.9rem;margin:.5rem 0 0">Klantscore<br>Google reviews</p>
    </div>
  </div>
</div>
</section>

'''

# Verwijder bestaande spotlight als die er al in zit (door vorige run)
cas = re.sub(r'\n<!-- ── SPOTLIGHT CASE.*?</section>\n', '\n', cas, flags=re.DOTALL)
cas = re.sub(r'\n<!-- ── STATS BAND.*?</section>\n', '\n', cas, flags=re.DOTALL)
cas = re.sub(r'\n<!-- ── STATISTIEKEN KLANTEN.*?</section>\n', '\n', cas, flags=re.DOTALL)

# Voeg in na hero (voor eerste ============ comment)
cas = re.sub(
    r'(\n</div></section>\n+)(<!-- ============ CASES)',
    r'\1' + CASES_INSERT + r'\2',
    cas
)

with open(ROOT + '/cases.html', 'w', encoding='utf-8') as f:
    f.write(cas)
print(f'cases.html: stats + spotlight + dark stats ({len(cas.splitlines())}L)')


# ═══════════════════════════════════════════════════════════════════════════
# 4. transacties.html — marktrapport lead magnet toevoegen
# ═══════════════════════════════════════════════════════════════════════════
with open(ROOT + '/transacties.html', encoding='utf-8') as f:
    tr = f.read()

TR_LM = '''
<!-- ── MARKTRAPPORT ──────────────────────────────────────────────── -->
<section class="lead-magnet">
<div class="container">
  <div class="lm-inner">
    <div class="lm-text">
      <span class="eyebrow">Gratis download</span>
      <h2>Spring Marktrapport Q2 2026</h2>
      <p>Actuele transactieprijzen, BAR-rendementen en marktontwikkelingen per sector — samengesteld door Spring Research.</p>
    </div>
    <form class="lm-form" onsubmit="return false">
      <input type="email" placeholder="Uw e-mailadres">
      <button class="btn btn--primary btn--lg">Rapport ontvangen</button>
    </form>
  </div>
</div>
</section>

'''

# Voeg in na spotlight deal, voor deal grid
if 'lead-magnet' not in tr:
    tr = tr.replace(
        '\n<!-- ── DEAL GRID',
        TR_LM + '<!-- ── DEAL GRID'
    )
    with open(ROOT + '/transacties.html', 'w', encoding='utf-8') as f:
        f.write(tr)
    print(f'transacties.html: marktrapport lead magnet toegevoegd ({len(tr.splitlines())}L)')
else:
    print('transacties.html: lead magnet al aanwezig')


# ═══════════════════════════════════════════════════════════════════════════
# 5. algemeen.html — newsletter sectie + betere artikel grid heading
# ═══════════════════════════════════════════════════════════════════════════
with open(ROOT + '/algemeen.html', encoding='utf-8') as f:
    alg = f.read()

ALG_NL = '''
<!-- ── NIEUWSBRIEF BAND ──────────────────────────────────────────── -->
<section class="lead-magnet">
<div class="container">
  <div class="lm-inner">
    <div class="lm-text">
      <span class="eyebrow">Nieuwsbrief</span>
      <h2>Marktinzichten direct in uw inbox</h2>
      <p>Elke maand: de belangrijkste vastgoedtrends, nieuwe analyses en exclusieve Spring-inzichten. Geen spam, altijd uitschrijfbaar.</p>
    </div>
    <form class="lm-form" onsubmit="return false">
      <input type="email" placeholder="Uw e-mailadres">
      <button class="btn btn--primary btn--lg">Inschrijven</button>
    </form>
  </div>
</div>
</section>

'''

# Voeg in vóór de talk-strip
if 'lead-magnet' not in alg:
    alg = alg.replace(
        '\n<section class="talk-strip">',
        ALG_NL + '<section class="talk-strip">'
    )
    with open(ROOT + '/algemeen.html', 'w', encoding='utf-8') as f:
        f.write(alg)
    print(f'algemeen.html: nieuwsbrief lead magnet toegevoegd ({len(alg.splitlines())}L)')
else:
    print('algemeen.html: lead magnet al aanwezig')

print('\nKlaar.')
