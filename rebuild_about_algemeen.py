import subprocess, re

ROOT = r'C:/Users/Gebruiker/spring-real-estate-concept'

# ── 1. ABOUT.HTML — restore content + add locaties + fix ─────────────────────
# Get the last clean version (before our about fix, which is commit aa649e9)
result = subprocess.run(['git', 'show', 'aa649e9:about.html'],
                        capture_output=True, encoding='utf-8', cwd=ROOT)
old = result.stdout
lines = old.splitlines(keepends=True)

# Lines 1-167: clean content (header → page-hero → all sections → two-col closing)
# Line 168+: nav injection
# Lines 198-201: misplaced scripts
# Line 203+: correct talk-strip/footer/mobile-menu/scripts

top = ''.join(lines[:167])   # everything up to (not including) nav injection

# Close the section--soft properly (two-col div already closed, just need container + section)
top += '  </div>\n</section>\n'

# Locaties section — 4 clickable city cards
locaties = '''
<!-- locaties -->
<section class="section">
<div class="container">
  <div class="sec-head"><div class="t">
    <span class="eyebrow">Onze vestigingen</span>
    <h2 class="disp">Lokaal verankerd, <em>internationaal aanwezig</em></h2>
  </div></div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1.5rem;margin-top:2rem">

    <a href="locatie-utrecht.html" style="text-decoration:none;color:inherit">
    <div style="border:1px solid #e5e8e0;border-radius:12px;padding:1.75rem;transition:box-shadow .2s" onmouseover="this.style.boxShadow='0 4px 20px rgba(0,0,0,.08)'" onmouseout="this.style.boxShadow='none'">
      <div style="font-size:1.5rem;margin-bottom:.75rem">&#127475;&#127473;</div>
      <h3 style="margin:0 0 4px;font-size:1.1rem">Utrecht</h3>
      <p style="color:#7a7f74;font-size:.85rem;margin:0 0 1rem">Hoofdkantoor &middot; Croeselaan 28</p>
      <ul style="list-style:none;padding:0;margin:0 0 1.25rem;display:grid;gap:6px;font-size:.85rem">
        <li style="display:flex;gap:8px"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4" style="flex-shrink:0;margin-top:2px"><path d="M5 12l5 5L20 6"/></svg>Full-service vastgoedadvies</li>
        <li style="display:flex;gap:8px"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4" style="flex-shrink:0;margin-top:2px"><path d="M5 12l5 5L20 6"/></svg>18 business units</li>
        <li style="display:flex;gap:8px"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4" style="flex-shrink:0;margin-top:2px"><path d="M5 12l5 5L20 6"/></svg>Commercieel &amp; residentieel</li>
      </ul>
      <span style="color:var(--green);font-size:.85rem;font-weight:600">Bekijk vestiging &#8594;</span>
    </div>
    </a>

    <a href="locatie-amsterdam.html" style="text-decoration:none;color:inherit">
    <div style="border:1px solid #e5e8e0;border-radius:12px;padding:1.75rem;transition:box-shadow .2s" onmouseover="this.style.boxShadow='0 4px 20px rgba(0,0,0,.08)'" onmouseout="this.style.boxShadow='none'">
      <div style="font-size:1.5rem;margin-bottom:.75rem">&#127475;&#127473;</div>
      <h3 style="margin:0 0 4px;font-size:1.1rem">Amsterdam</h3>
      <p style="color:#7a7f74;font-size:.85rem;margin:0 0 1rem">Regionale vestiging &middot; Zuidas</p>
      <ul style="list-style:none;padding:0;margin:0 0 1.25rem;display:grid;gap:6px;font-size:.85rem">
        <li style="display:flex;gap:8px"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4" style="flex-shrink:0;margin-top:2px"><path d="M5 12l5 5L20 6"/></svg>Kantoor- &amp; bedrijfsruimte</li>
        <li style="display:flex;gap:8px"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4" style="flex-shrink:0;margin-top:2px"><path d="M5 12l5 5L20 6"/></svg>Zuidas-specialist</li>
        <li style="display:flex;gap:8px"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4" style="flex-shrink:0;margin-top:2px"><path d="M5 12l5 5L20 6"/></svg>Investment &amp; beleggingen</li>
      </ul>
      <span style="color:var(--green);font-size:.85rem;font-weight:600">Bekijk vestiging &#8594;</span>
    </div>
    </a>

    <a href="locatie-valencia.html" style="text-decoration:none;color:inherit">
    <div style="border:1px solid #e5e8e0;border-radius:12px;padding:1.75rem;transition:box-shadow .2s" onmouseover="this.style.boxShadow='0 4px 20px rgba(0,0,0,.08)'" onmouseout="this.style.boxShadow='none'">
      <div style="font-size:1.5rem;margin-bottom:.75rem">&#127466;&#127480;</div>
      <h3 style="margin:0 0 4px;font-size:1.1rem">Valencia</h3>
      <p style="color:#7a7f74;font-size:.85rem;margin:0 0 1rem">Internationale vestiging &middot; Spanje</p>
      <ul style="list-style:none;padding:0;margin:0 0 1.25rem;display:grid;gap:6px;font-size:.85rem">
        <li style="display:flex;gap:8px"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4" style="flex-shrink:0;margin-top:2px"><path d="M5 12l5 5L20 6"/></svg>Residentieel &amp; commercieel</li>
        <li style="display:flex;gap:8px"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4" style="flex-shrink:0;margin-top:2px"><path d="M5 12l5 5L20 6"/></svg>NL-expats &amp; investeerders</li>
        <li style="display:flex;gap:8px"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4" style="flex-shrink:0;margin-top:2px"><path d="M5 12l5 5L20 6"/></svg>Fiscaal advies &amp; begeleiding</li>
      </ul>
      <span style="color:var(--green);font-size:.85rem;font-weight:600">Bekijk vestiging &#8594;</span>
    </div>
    </a>

    <a href="locatie-estepona.html" style="text-decoration:none;color:inherit">
    <div style="border:1px solid #e5e8e0;border-radius:12px;padding:1.75rem;transition:box-shadow .2s" onmouseover="this.style.boxShadow='0 4px 20px rgba(0,0,0,.08)'" onmouseout="this.style.boxShadow='none'">
      <div style="font-size:1.5rem;margin-bottom:.75rem">&#127466;&#127480;</div>
      <h3 style="margin:0 0 4px;font-size:1.1rem">Estepona</h3>
      <p style="color:#7a7f74;font-size:.85rem;margin:0 0 1rem">Internationale vestiging &middot; Costa del Sol</p>
      <ul style="list-style:none;padding:0;margin:0 0 1.25rem;display:grid;gap:6px;font-size:.85rem">
        <li style="display:flex;gap:8px"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4" style="flex-shrink:0;margin-top:2px"><path d="M5 12l5 5L20 6"/></svg>Luxe residentieel vastgoed</li>
        <li style="display:flex;gap:8px"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4" style="flex-shrink:0;margin-top:2px"><path d="M5 12l5 5L20 6"/></svg>Costa del Sol-specialist</li>
        <li style="display:flex;gap:8px"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4" style="flex-shrink:0;margin-top:2px"><path d="M5 12l5 5L20 6"/></svg>Verhuur &amp; belegging</li>
      </ul>
      <span style="color:var(--green);font-size:.85rem;font-weight:600">Bekijk vestiging &#8594;</span>
    </div>
    </a>

  </div>
</div>
</section>
'''

# talk-strip + footer + mobile-menu + scripts — skip lines 168-201 (injection + stray scripts)
# Line 203 = talk-strip (0-indexed: 202)
bottom = ''.join(lines[202:])

about = top + locaties + bottom
with open(ROOT + '/about.html', 'w', encoding='utf-8') as f:
    f.write(about)
print(f'about.html: restored ({len(about.splitlines())}L, has-drop count in body: {about.count("has-drop")})')


# ── 2. ALGEMEEN.HTML — premium rebuild with podcast ──────────────────────────
# Read the header + footer from resources.html
with open(ROOT + '/resources.html', encoding='utf-8') as f:
    res = f.read()

header_end = res.index('</header>') + len('</header>')
header = res[:header_end]
footer_start = res.index('\n<section class="talk-strip">')
footer = res[footer_start:]

PODCAST_SVG = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polygon points="10 8 16 12 10 16 10 8"/></svg>'
MIC_SVG = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 10a7 7 0 0 0 14 0M12 19v3M8 22h8"/></svg>'
ARTICLE_SVG = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/></svg>'

body = '''

<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="index.html">Home</a> / <a href="resources.html">Resources</a> / Algemeen</div>
    <span class="eyebrow">Analyses &amp; inzichten</span>
    <h1>Markt<em style="color:var(--green);font-style:italic;font-weight:500">inzichten</em> &amp; kennisdeling</h1>
    <p class="lead">Diepgaande analyses, marktontwikkelingen en praktische inzichten — door de Spring-specialisten.</p>
    <div class="team-filter">
      <a href="#" class="active" data-key="alle">Alle</a>
      <a href="#" data-key="marktinzicht">Marktinzicht</a>
      <a href="#" data-key="investeren">Investeren</a>
      <a href="#" data-key="podcast">Podcast</a>
      <a href="#" data-key="huisvesting">Huisvesting</a>
      <a href="#" data-key="internationaal">Internationaal</a>
    </div>
    <form class="search search--light search--single" onsubmit="return false">
      <label class="seg">''' + MIC_SVG.replace('22','22').replace('rect','rect') + '''<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg>
        <input type="text" placeholder="Zoek analyses, podcasts of inzichten&hellip;" aria-label="Zoeken"></label>
      <button class="search-btn"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg> Zoeken</button>
    </form>
  </div>
</section>

<!-- UITGELICHT -->
<section class="section--tight section--soft">
<div class="container">
  <span class="eyebrow">Uitgelicht</span>
  <div class="two-col" style="align-items:center;gap:3rem;margin-top:1.5rem">
    <div class="media-tall" style="border-radius:12px;overflow:hidden;position:relative">
      <img src="images/photo-1.jpg" alt="Kantoormarkt analyse" style="width:100%;height:100%;object-fit:cover">
      <div style="position:absolute;bottom:16px;left:16px;background:var(--green);color:#fff;padding:6px 14px;border-radius:20px;font-size:.8rem;font-weight:600">Marktinzicht &middot; april 2026</div>
    </div>
    <div class="prose">
      <h2 class="disp" style="font-size:1.8rem">Kantoormarkt Randstad Q1 2026: aanbod daalt, huurprijzen stijgen naar <em>recordniveau</em></h2>
      <p style="color:#555;margin:.75rem 0 1.25rem">De leegstand op de Amsterdamse Zuidas staat op het laagste punt in 15 jaar. Tegelijkertijd trekken huurprijzen in Utrecht en Den Haag aan. Spring Research analyseert de kerncijfers en geeft een vooruitzicht voor het jaar.</p>
      <ul style="list-style:none;padding:0;display:grid;gap:8px;margin-bottom:1.5rem">
        <li style="display:flex;gap:10px;align-items:flex-start"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4" style="flex-shrink:0;margin-top:3px"><path d="M5 12l5 5L20 6"/></svg>Leegstand Amsterdam: historisch dieptepunt van 4,2%</li>
        <li style="display:flex;gap:10px;align-items:flex-start"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4" style="flex-shrink:0;margin-top:3px"><path d="M5 12l5 5L20 6"/></svg>Huurprijzen Utrecht +9% YoY — vraag overstijgt aanbod</li>
        <li style="display:flex;gap:10px;align-items:flex-start"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4" style="flex-shrink:0;margin-top:3px"><path d="M5 12l5 5L20 6"/></svg>Verwachting: BAR-rendementen dalen verder naar 5,5% gemiddeld</li>
      </ul>
      <a href="resources.html" class="btn btn--primary">Lees het volledige rapport</a>
    </div>
  </div>
</div>
</section>

<!-- PODCAST -->
<section class="section" style="background:var(--ink);color:#fff">
<div class="container">
  <div class="sec-head"><div class="t">
    <span class="eyebrow" style="color:var(--green-soft)">Spring Podcast</span>
    <h2 class="disp disp--light">De vastgoedpodcast voor <em>professionals</em></h2>
  </div></div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1.5rem;margin-top:2rem">

    <div style="background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);border-radius:12px;padding:1.5rem" data-cat="podcast">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:1rem">
        <div style="width:48px;height:48px;background:var(--green);border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0">''' + PODCAST_SVG + '''</div>
        <div><p style="margin:0;font-size:.75rem;color:rgba(255,255,255,.5);letter-spacing:.1em;text-transform:uppercase">Aflevering 24 &middot; 38 min</p></div>
      </div>
      <h3 style="font-size:1rem;margin:0 0 .5rem;color:#fff">De Zuidas in 2026: wat drijft huurprijzen naar recordhoogtes?</h3>
      <p style="font-size:.85rem;color:rgba(255,255,255,.6);margin:0 0 1.25rem">Met Jan de Vries (Head of Research) en Mia Smit (Leasing Director)</p>
      <a href="#" style="display:inline-flex;align-items:center;gap:8px;color:var(--green-soft);font-size:.85rem;font-weight:600;text-decoration:none">''' + PODCAST_SVG + ''' Beluister aflevering</a>
    </div>

    <div style="background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);border-radius:12px;padding:1.5rem" data-cat="podcast">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:1rem">
        <div style="width:48px;height:48px;background:var(--green);border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0">''' + PODCAST_SVG + '''</div>
        <div><p style="margin:0;font-size:.75rem;color:rgba(255,255,255,.5);letter-spacing:.1em;text-transform:uppercase">Aflevering 23 &middot; 42 min</p></div>
      </div>
      <h3 style="font-size:1rem;margin:0 0 .5rem;color:#fff">Beleggen in Spanje: kansen en valkuilen voor Nederlandse investeerders</h3>
      <p style="font-size:.85rem;color:rgba(255,255,255,.6);margin:0 0 1.25rem">Met Carlos Moreno (Spring Spain) en Petra Laan (Investments)</p>
      <a href="#" style="display:inline-flex;align-items:center;gap:8px;color:var(--green-soft);font-size:.85rem;font-weight:600;text-decoration:none">''' + PODCAST_SVG + ''' Beluister aflevering</a>
    </div>

    <div style="background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);border-radius:12px;padding:1.5rem" data-cat="podcast">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:1rem">
        <div style="width:48px;height:48px;background:var(--green);border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0">''' + PODCAST_SVG + '''</div>
        <div><p style="margin:0;font-size:.75rem;color:rgba(255,255,255,.5);letter-spacing:.1em;text-transform:uppercase">Aflevering 22 &middot; 31 min</p></div>
      </div>
      <h3 style="font-size:1rem;margin:0 0 .5rem;color:#fff">Duurzaamheid als waardedrijver: BREEAM-impact op huurprijs en rendement</h3>
      <p style="font-size:.85rem;color:rgba(255,255,255,.6);margin:0 0 1.25rem">Met Sophie Groot (Sustainability Lead) en Erik Bakker (Asset Management)</p>
      <a href="#" style="display:inline-flex;align-items:center;gap:8px;color:var(--green-soft);font-size:.85rem;font-weight:600;text-decoration:none">''' + PODCAST_SVG + ''' Beluister aflevering</a>
    </div>

  </div>
  <div style="margin-top:2rem;text-align:center">
    <a href="#" class="btn btn--secondary">Alle afleveringen bekijken</a>
  </div>
</div>
</section>

<!-- ARTIKELEN GRID -->
<section class="section filterable">
<div class="container">
  <div class="sec-head"><div class="t">
    <span class="eyebrow">Analyses &amp; artikelen</span>
    <h2 class="disp">Recente <em>inzichten</em></h2>
  </div></div>

  <div class="blog-grid" style="margin-top:2rem">
    <a class="blog-card" href="resources.html" data-cat="investeren">
      <div class="ph"><img src="images/photo-2.jpg" alt="Spanje vastgoed"></div>
      <div class="body"><span class="cat">Investeren</span>
        <h3>Waarom beleggers nu instappen in commercieel vastgoed in Spanje</h3>
        <p class="muted" style="font-size:.85rem;margin:.5rem 0 0">Spring Research &middot; maart 2026</p>
      </div>
    </a>
    <a class="blog-card" href="resources.html" data-cat="huisvesting">
      <div class="ph"><img src="images/hero.jpg" alt="Kantoor flexibel"></div>
      <div class="body"><span class="cat">Huisvesting</span>
        <h3>Flexibel vs. traditioneel kantoor: de kosten-batenanalyse voor 2026</h3>
        <p class="muted" style="font-size:.85rem;margin:.5rem 0 0">Spring Insights &middot; februari 2026</p>
      </div>
    </a>
    <a class="blog-card" href="resources.html" data-cat="marktinzicht">
      <div class="ph"><img src="images/photo-1.jpg" alt="Zuidas"></div>
      <div class="body"><span class="cat">Marktinzicht</span>
        <h3>Zuidas 2026: leegstand op historisch laagste punt, huurprijzen recordhoog</h3>
        <p class="muted" style="font-size:.85rem;margin:.5rem 0 0">Spring Research &middot; januari 2026</p>
      </div>
    </a>
    <a class="blog-card" href="resources.html" data-cat="internationaal">
      <div class="ph"><img src="images/photo-2.jpg" alt="Valencia"></div>
      <div class="body"><span class="cat">Internationaal</span>
        <h3>Valencia als vestigingslocatie: fiscale voordelen &amp; vastgoedkansen</h3>
        <p class="muted" style="font-size:.85rem;margin:.5rem 0 0">Spring Spain &middot; december 2025</p>
      </div>
    </a>
    <a class="blog-card" href="resources.html" data-cat="investeren">
      <div class="ph"><img src="images/hero.jpg" alt="Belegging"></div>
      <div class="body"><span class="cat">Investeren</span>
        <h3>Beleggen in commercieel vastgoed: 5 lessen van ervaren investeerders</h3>
        <p class="muted" style="font-size:.85rem;margin:.5rem 0 0">Spring Research &middot; november 2025</p>
      </div>
    </a>
    <a class="blog-card" href="resources.html" data-cat="huisvesting">
      <div class="ph"><img src="images/photo-1.jpg" alt="Taxatie"></div>
      <div class="body"><span class="cat">Huisvesting</span>
        <h3>Hoe bepalen taxateurs de waarde van een kantoorpand in 2026?</h3>
        <p class="muted" style="font-size:.85rem;margin:.5rem 0 0">Spring Insights &middot; oktober 2025</p>
      </div>
    </a>
  </div>
</div>
</section>
'''

algemeen = header + body + footer
with open(ROOT + '/algemeen.html', 'w', encoding='utf-8') as f:
    f.write(algemeen)
print(f'algemeen.html: rebuilt with podcast ({len(algemeen.splitlines())}L)')

# ── 3. CSS: search--light sits neatly inside page-hero tint ──────────────────
# The page-hero already has background var(--green-tint). The search bar should
# blend in — keep light green but ensure no extra margin-top that breaks the flow
with open(ROOT + '/css/styles.css', encoding='utf-8') as f:
    css = f.read()

# Make sure search--light inside page-hero looks clean (no white box feeling)
if '.page-hero .search--light' not in css:
    css = css.replace(
        '.page-hero .team-filter a.active, .page-hero .team-filter a:hover{ background:var(--green); color:#fff; border-color:var(--green); }',
        '.page-hero .team-filter a.active, .page-hero .team-filter a:hover{ background:var(--green); color:#fff; border-color:var(--green); }\n.page-hero .search--light{ background:rgba(255,255,255,.6); border-color:rgba(0,0,0,.12); }'
    )
    with open(ROOT + '/css/styles.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print('styles.css: page-hero search--light refined')
else:
    print('styles.css: already has page-hero search rule')

print('\nDone.')
