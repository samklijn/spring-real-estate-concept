import re

ROOT = r'C:/Users/Gebruiker/spring-real-estate-concept'

# ── 1. index.html: fix homepage links ────────────────────────────────────────
with open(ROOT + '/index.html', encoding='utf-8') as f:
    idx = f.read()

# "Meer transacties" button: listings.html -> transacties.html
idx = idx.replace(
    '<a href="listings.html" class="btn btn--ghost" data-tr="1" data-en="More transactions" data-es="Más transacciones">Meer transacties</a>',
    '<a href="transacties.html" class="btn btn--ghost" data-tr="1" data-en="More transactions" data-es="Más transacciones">Meer transacties</a>'
)
# "Naar de blog" button + news-feature + news-row links: resources.html -> algemeen.html
idx = idx.replace(
    '<a href="resources.html" class="btn btn--ghost" data-tr="1" data-en="To the blog" data-es="Al blog">Naar de blog</a>',
    '<a href="algemeen.html" class="btn btn--ghost" data-tr="1" data-en="To the blog" data-es="Al blog">Naar de blog</a>'
)
idx = idx.replace('<a class="news-feature" href="resources.html">', '<a class="news-feature" href="algemeen.html">')
idx = re.sub(r'(<a class="news-row" href=")resources\.html(")', r'\1algemeen.html\2', idx)

with open(ROOT + '/index.html', 'w', encoding='utf-8') as f:
    f.write(idx)
print('index.html: homepage links updated')

# ── 2. cases.html: remove stats section ──────────────────────────────────────
with open(ROOT + '/cases.html', encoding='utf-8') as f:
    cas = f.read()

cas = re.sub(
    r'\n<!-- ============ STATS ============ -->\n<section class="section--tight section--soft">.*?</section>\n',
    '\n',
    cas, flags=re.DOTALL
)

with open(ROOT + '/cases.html', 'w', encoding='utf-8') as f:
    f.write(cas)
print('cases.html: stats section removed')

# ── 3. transacties.html: full upgrade ────────────────────────────────────────
with open(ROOT + '/transacties.html', encoding='utf-8') as f:
    tr = f.read()

# Keep header (up to and including page-hero closing </section>)
hero_end = tr.index('</section>', tr.index('<section class="page-hero">')) + len('</section>')
header_block = tr[:hero_end]

# Keep footer from talk-strip onwards
footer_start = tr.index('\n<section class="talk-strip">')
footer_block = tr[footer_start:]

new_body = '''

<!-- ── STATS BAND ─────────────────────────────────────────────────── -->
<section class="section--tight" style="background:var(--ink);color:#fff">
<div class="container">
  <div class="stats-band" style="background:transparent;border:none;padding:0">
    <div class="grid" style="grid-template-columns:repeat(4,1fr);gap:0;text-align:center">
      <div style="border-right:1px solid rgba(255,255,255,.12);padding:1.5rem 0">
        <b style="font-size:2rem;font-weight:800;color:#fff">€450M+</b>
        <span style="display:block;font-size:.85rem;color:rgba(255,255,255,.6);margin-top:4px">Transactiewaarde</span>
      </div>
      <div style="border-right:1px solid rgba(255,255,255,.12);padding:1.5rem 0">
        <b style="font-size:2rem;font-weight:800;color:#fff">1.500+</b>
        <span style="display:block;font-size:.85rem;color:rgba(255,255,255,.6);margin-top:4px">Deals begeleid</span>
      </div>
      <div style="border-right:1px solid rgba(255,255,255,.12);padding:1.5rem 0">
        <b style="font-size:2rem;font-weight:800;color:#fff">4</b>
        <span style="display:block;font-size:.85rem;color:rgba(255,255,255,.6);margin-top:4px">Vestigingen</span>
      </div>
      <div style="padding:1.5rem 0">
        <b style="font-size:2rem;font-weight:800;color:#fff">15+</b>
        <span style="display:block;font-size:.85rem;color:rgba(255,255,255,.6);margin-top:4px">Jaar marktervaring</span>
      </div>
    </div>
  </div>
</div>
</section>

<!-- ── SPOTLIGHT DEAL ──────────────────────────────────────────────── -->
<section class="section--tight section--soft">
<div class="container">
  <span class="eyebrow">Uitgelichte deal</span>
  <div class="two-col" style="align-items:center;gap:3rem;margin-top:1.5rem">
    <div class="media-tall" style="border-radius:12px;overflow:hidden">
      <img src="images/photo-1.jpg" alt="Zuidas kantoor" style="width:100%;height:100%;object-fit:cover">
    </div>
    <div class="prose">
      <span class="cat" style="background:var(--green);color:#fff;padding:4px 12px;border-radius:20px;font-size:.8rem;font-weight:600;display:inline-block;margin-bottom:16px">Verhuur · Q1 2026</span>
      <h2 class="disp" style="font-size:1.8rem">Verhuur Zuidas-kantoor<br><em>1.250 m²</em> aan internationale tech-firma</h2>
      <p style="color:#555;margin:.75rem 0 1.25rem">Een multinational zocht snel én discreet een representatief Zuidas-kantoor. Spring begeleidde het volledige traject: van zoekprofiel tot sleuteloverdracht in minder dan 6 weken.</p>
      <ul style="list-style:none;padding:0;display:grid;gap:8px;margin-bottom:1.5rem">
        <li style="display:flex;gap:10px;align-items:center"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4"><path d="M5 12l5 5L20 6"/></svg> <strong>Locatie:</strong>&nbsp;Amsterdam Zuidas</li>
        <li style="display:flex;gap:10px;align-items:center"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4"><path d="M5 12l5 5L20 6"/></svg> <strong>Huurprijs:</strong>&nbsp;€720 /m²/jaar</li>
        <li style="display:flex;gap:10px;align-items:center"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4"><path d="M5 12l5 5L20 6"/></svg> <strong>Looptijd:</strong>&nbsp;5 jaar vast + 2 optiejaren</li>
        <li style="display:flex;gap:10px;align-items:center"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4"><path d="M5 12l5 5L20 6"/></svg> <strong>Doorlooptijd:</strong>&nbsp;6 weken van zoekprofiel tot sleutels</li>
      </ul>
      <a href="contact.html" class="btn btn--primary">Soortgelijke deal bespreken</a>
    </div>
  </div>
</div>
</section>

<!-- ── DEAL GRID ───────────────────────────────────────────────────── -->
<section class="section filterable">
<div class="container">
  <div class="sec-head"><div class="t">
    <span class="eyebrow">Recente transacties</span>
    <h2 class="disp">Alle <em>deals</em> op een rij</h2>
  </div>
  <div class="team-filter">
    <a href="#" class="active" data-key="alle">Alle</a>
    <a href="#" data-key="verhuur">Verhuur</a>
    <a href="#" data-key="verkoop">Verkoop</a>
    <a href="#" data-key="investering">Investering</a>
    <a href="#" data-key="design &amp; build">Design &amp; Build</a>
  </div>
  </div>

  <div class="blog-grid" style="margin-top:2rem">
    <a class="blog-card" href="#" data-cat="verkoop">
      <div class="ph"><img src="images/photo-2.jpg" alt="Utrecht belegging"></div>
      <div class="body">
        <span class="cat">Verkoop</span>
        <h3>Beleggingsobject Utrecht &mdash; €4,9 mln k.k. bij 6,2% BAR</h3>
        <p class="muted" style="font-size:.85rem;margin:.5rem 0 0">Utrecht &middot; Q4 2025 &middot; Kantoor / Belegging</p>
      </div>
    </a>
    <a class="blog-card" href="#" data-cat="verhuur">
      <div class="ph"><img src="images/hero.jpg" alt="Kantoorpand Utrecht"></div>
      <div class="body">
        <span class="cat">Verhuur</span>
        <h3>Turn-key verhuur 820 m² kantoor na herpositionering</h3>
        <p class="muted" style="font-size:.85rem;margin:.5rem 0 0">Utrecht &middot; Q3 2025 &middot; Asset management</p>
      </div>
    </a>
    <a class="blog-card" href="#" data-cat="investering">
      <div class="ph"><img src="images/photo-1.jpg" alt="Valencia investering"></div>
      <div class="body">
        <span class="cat">Investering</span>
        <h3>Aankoop beleggingsobject Valencia &mdash; €3,8 mln bij 7,1% BAR</h3>
        <p class="muted" style="font-size:.85rem;margin:.5rem 0 0">Valencia &middot; Q2 2025 &middot; Spanje</p>
      </div>
    </a>
    <a class="blog-card" href="#" data-cat="design &amp; build">
      <div class="ph"><img src="images/photo-2.jpg" alt="Logistiek Tilburg"></div>
      <div class="body">
        <span class="cat">Design &amp; Build</span>
        <h3>Build-to-suit logistiek 12.000 m² opgeleverd in Tilburg</h3>
        <p class="muted" style="font-size:.85rem;margin:.5rem 0 0">Tilburg &middot; Q1 2025 &middot; Logistiek</p>
      </div>
    </a>
    <a class="blog-card" href="#" data-cat="verkoop">
      <div class="ph"><img src="images/hero.jpg" alt="Portefeuille Utrecht"></div>
      <div class="body">
        <span class="cat">Verkoop</span>
        <h3>Portefeuille 3 kantoorpanden Utrecht &mdash; €8,9 mln</h3>
        <p class="muted" style="font-size:.85rem;margin:.5rem 0 0">Utrecht &middot; Q4 2024 &middot; Portefeuille</p>
      </div>
    </a>
    <a class="blog-card" href="#" data-cat="verhuur">
      <div class="ph"><img src="images/photo-1.jpg" alt="Kantoor Amsterdam"></div>
      <div class="body">
        <span class="cat">Verhuur</span>
        <h3>Verhuur 2.800 m² kantoor aan Europees hoofdkantoor</h3>
        <p class="muted" style="font-size:.85rem;margin:.5rem 0 0">Amsterdam &middot; Q3 2024 &middot; €695/m²/jaar</p>
      </div>
    </a>
  </div>
</div>
</section>

<!-- ── CTA ─────────────────────────────────────────────────────────── -->
<section class="section--tight"><div class="container"><div class="cta">
  <h2>Benieuwd wat uw vastgoed waard is?</h2>
  <p>Vraag een vrijblijvende taxatie of marktanalyse aan bij onze specialisten.</p>
  <div class="btns">
    <a href="contact.html" class="btn btn--light btn--lg">Taxatie aanvragen</a>
    <a href="listings.html" class="btn btn--lg" style="background:rgba(255,255,255,.16);color:#fff;border-color:rgba(255,255,255,.4)">Bekijk aanbod</a>
  </div>
</div></div></section>
'''

new_tr = header_block + new_body + footer_block
with open(ROOT + '/transacties.html', 'w', encoding='utf-8') as f:
    f.write(new_tr)
print(f'transacties.html: upgraded ({len(new_tr.splitlines())}L)')

print('Done.')
