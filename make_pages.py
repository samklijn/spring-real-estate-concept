import re

ROOT = r'C:/Users/Gebruiker/spring-real-estate-concept'

with open(ROOT + '/resources.html', encoding='utf-8') as f:
    res = f.read()

header_end = res.index('</header>') + len('</header>')
header = res[:header_end]

footer_start = res.index('\n<section class="talk-strip">')
footer = res[footer_start:]

SEARCH_FORM = '''    <form class="search search--light search--single" onsubmit="return false">
      <label class="seg"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg>
        <input type="text" placeholder="Zoek…" aria-label="Zoeken"></label>
      <button class="search-btn"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg> Zoeken</button>
    </form>'''

def make_page(title_nl, slug, eyebrow, h1_html, lead_nl, content):
    page = header
    page = page.replace('<title>Resources &amp; marktinzichten — Spring Real Estate</title>',
                        f'<title>{title_nl} — Spring Real Estate</title>')
    page = page.replace('<meta name="description" content="Blog, marktinzichten en kennis over commercieel vastgoed van Spring Real Estate.">',
                        f'<meta name="description" content="{title_nl} - Spring Real Estate.">')
    hero = f'''

<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="index.html">Home</a> / <a href="resources.html">Resources</a> / {eyebrow}</div>
    <span class="eyebrow">{eyebrow}</span>
    <h1>{h1_html}</h1>
    <p class="lead">{lead_nl}</p>
{SEARCH_FORM}
  </div>
</section>

{content}
'''
    full = page + hero + footer
    with open(ROOT + f'/{slug}.html', 'w', encoding='utf-8') as f:
        f.write(full)
    print(f'{slug}.html: {len(full.splitlines())} lines')

# ── transacties.html ──────────────────────────────────────────────────────────
transacties = '''<section class="section">
<div class="container">
  <div class="sec-head"><div class="t">
    <span class="eyebrow">Recente transacties</span>
    <h2 class="disp">Vastgoeddeals &amp; <em>marktdata</em></h2>
  </div></div>
  <div class="blog-grid">
    <a class="blog-card" href="resources.html">
      <div class="ph"><img src="images/photo-1.jpg" alt="Zuidas kantoor"></div>
      <div class="body"><span class="cat">Verhuur</span>
        <h3>Verhuur Zuidas-kantoor 1.250 m² aan internationale tech-firma</h3>
        <p class="muted" style="font-size:.9rem">Amsterdam &middot; Q1 2026 &middot; €720/m²/jaar</p>
      </div>
    </a>
    <a class="blog-card" href="resources.html">
      <div class="ph"><img src="images/photo-2.jpg" alt="Utrecht belegging"></div>
      <div class="body"><span class="cat">Verkoop</span>
        <h3>Verkoop beleggingsobject Utrecht &mdash; €4,9 mln k.k. bij 6,2% BAR</h3>
        <p class="muted" style="font-size:.9rem">Utrecht &middot; Q4 2025 &middot; Belegging</p>
      </div>
    </a>
    <a class="blog-card" href="resources.html">
      <div class="ph"><img src="images/hero.jpg" alt="Kantoorpand"></div>
      <div class="body"><span class="cat">Verhuur</span>
        <h3>Herpositionering kantoorpand levert turn-key verhuur in 3 weken op</h3>
        <p class="muted" style="font-size:.9rem">Utrecht &middot; Q3 2025 &middot; Asset management</p>
      </div>
    </a>
    <a class="blog-card" href="resources.html">
      <div class="ph"><img src="images/photo-1.jpg" alt="Valencia"></div>
      <div class="body"><span class="cat">Investering</span>
        <h3>Aankoop beleggingsobject Valencia &mdash; €3,8 mln bij 7,1% BAR</h3>
        <p class="muted" style="font-size:.9rem">Valencia &middot; Q2 2025 &middot; Spanje</p>
      </div>
    </a>
    <a class="blog-card" href="resources.html">
      <div class="ph"><img src="images/photo-2.jpg" alt="Logistiek"></div>
      <div class="body"><span class="cat">Design &amp; Build</span>
        <h3>Build-to-suit logistiek 12.000 m² opgeleverd in Tilburg</h3>
        <p class="muted" style="font-size:.9rem">Tilburg &middot; Q1 2025 &middot; Logistiek</p>
      </div>
    </a>
    <a class="blog-card" href="resources.html">
      <div class="ph"><img src="images/hero.jpg" alt="Portefeuille"></div>
      <div class="body"><span class="cat">Verkoop</span>
        <h3>Portefeuille van 3 Utrechtse kantoorpanden verkocht &mdash; €8,9 mln</h3>
        <p class="muted" style="font-size:.9rem">Utrecht &middot; Q4 2024 &middot; Portefeuille</p>
      </div>
    </a>
  </div>
</div>
</section>

<section class="section--tight" style="background:var(--green)">
<div class="container"><div class="cta" style="text-align:center;padding:3rem 0">
  <h2 style="color:#fff">Benieuwd wat uw vastgoed waard is?</h2>
  <p style="color:rgba(255,255,255,.85);max-width:520px;margin:.75rem auto 1.5rem">Vraag een vrijblijvende taxatie aan bij onze specialisten.</p>
  <div class="btns">
    <a href="contact.html" class="btn btn--light btn--lg">Taxatie aanvragen</a>
    <a href="listings.html" class="btn btn--lg" style="background:rgba(255,255,255,.16);color:#fff;border-color:rgba(255,255,255,.4)">Bekijk aanbod</a>
  </div>
</div></div>
</section>
'''

make_page(
    'Transacties',
    'transacties',
    'Transacties',
    'Vastgoeddeals &amp; <em style="color:var(--green);font-style:italic;font-weight:500">marktdata</em>',
    'Actuele deals, marktcijfers en vastgoeddata direct van de Spring-specialisten.',
    transacties
)

# ── algemeen.html ─────────────────────────────────────────────────────────────
algemeen = '''<section class="section filterable">
<div class="container">
  <div class="sec-head"><div class="t">
    <span class="eyebrow">Analyses &amp; trends</span>
    <h2 class="disp">Markt<em>inzichten</em> van onze specialisten</h2>
  </div>
  <div class="team-filter" style="margin-top:20px">
    <a href="#" class="active" data-key="alle">Alle</a>
    <a href="#" data-key="marktinzicht">Marktinzicht</a>
    <a href="#" data-key="investeren">Investeren</a>
    <a href="#" data-key="huisvesting">Huisvesting</a>
    <a href="#" data-key="internationaal">Internationaal</a>
    <a href="#" data-key="taxaties">Taxaties</a>
  </div>
  </div>
  <div class="blog-grid">
    <a class="blog-card" href="resources.html" data-cat="marktinzicht">
      <div class="ph"><img src="images/photo-1.jpg" alt="Kantoormarkt"></div>
      <div class="body"><span class="cat">Marktinzicht</span>
        <h3>Kantoormarkt Randstad Q1 2026: aanbod daalt, huurprijzen stijgen verder</h3>
        <p class="muted" style="font-size:.9rem">Spring Research &middot; april 2026</p>
      </div>
    </a>
    <a class="blog-card" href="resources.html" data-cat="investeren">
      <div class="ph"><img src="images/photo-2.jpg" alt="Spanje investering"></div>
      <div class="body"><span class="cat">Investeren</span>
        <h3>Waarom beleggers nu instappen in commercieel vastgoed in Spanje</h3>
        <p class="muted" style="font-size:.9rem">Spring Research &middot; maart 2026</p>
      </div>
    </a>
    <a class="blog-card" href="resources.html" data-cat="huisvesting">
      <div class="ph"><img src="images/hero.jpg" alt="Kantoor"></div>
      <div class="body"><span class="cat">Huisvesting</span>
        <h3>Flexibel vs. traditioneel kantoor: de kosten-batenanalyse voor 2026</h3>
        <p class="muted" style="font-size:.9rem">Spring Insights &middot; februari 2026</p>
      </div>
    </a>
    <a class="blog-card" href="resources.html" data-cat="marktinzicht">
      <div class="ph"><img src="images/photo-1.jpg" alt="Zuidas"></div>
      <div class="body"><span class="cat">Marktinzicht</span>
        <h3>Zuidas 2026: leegstand op historisch laagste punt, huurprijzen recordhoog</h3>
        <p class="muted" style="font-size:.9rem">Spring Research &middot; januari 2026</p>
      </div>
    </a>
    <a class="blog-card" href="resources.html" data-cat="internationaal">
      <div class="ph"><img src="images/photo-2.jpg" alt="Valencia"></div>
      <div class="body"><span class="cat">Internationaal</span>
        <h3>Valencia als vestigingslocatie: fiscale voordelen &amp; vastgoedkansen</h3>
        <p class="muted" style="font-size:.9rem">Spring Spain &middot; december 2025</p>
      </div>
    </a>
    <a class="blog-card" href="resources.html" data-cat="taxaties">
      <div class="ph"><img src="images/hero.jpg" alt="Taxatie"></div>
      <div class="body"><span class="cat">Taxaties</span>
        <h3>Hoe bepalen taxateurs de waarde van een kantoorpand in 2026?</h3>
        <p class="muted" style="font-size:.9rem">Spring Insights &middot; november 2025</p>
      </div>
    </a>
  </div>
</div>
</section>
'''

make_page(
    'Algemeen',
    'algemeen',
    'Algemeen',
    'Analyses, trends &amp; <em style="color:var(--green);font-style:italic;font-weight:500">inzichten</em>',
    'Diepgaande analyses, marktontwikkelingen en praktische inzichten over commercieel vastgoed.',
    algemeen
)

print('Done.')
