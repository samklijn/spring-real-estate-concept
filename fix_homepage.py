import re

def read(f):
    with open(f, encoding='utf-8') as fh: return fh.read()
def write(f, s):
    with open(f, 'w', encoding='utf-8') as fh: fh.write(s)

# ── index.html ───────────────────────────────────────────────────────────────
src = read('index.html')

# 1. Remove topbar
src = re.sub(r'\n<!-- ============ TOP BAR.*?-->\n<div class="topbar">.*?</div>\n', '\n', src, count=1, flags=re.DOTALL)

# 2. Remove trust-strip
src = re.sub(r'\n<div class="trust-strip">.*?</div>\n', '\n', src, count=1, flags=re.DOTALL)

# 3. Header: add class header--dark, swap logo to white
src = src.replace('<header class="header">', '<header class="header header--dark">', 1)
src = src.replace('images/logo-ink.png', 'images/logo-white.png', 1)

# 4. Diensten nav: change <button> to <a href="#diensten"> so clicking navigates
OLD_DIENSTEN_BTN = '<div class="has-drop"><button><span data-i18n="nav.diensten">Diensten</span> <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button>'
NEW_DIENSTEN_BTN = '<div class="has-drop"><a href="#diensten" class="nav-btn-link"><span data-i18n="nav.diensten">Diensten</span> <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></a>'
src = src.replace(OLD_DIENSTEN_BTN, NEW_DIENSTEN_BTN, 1)

# 5. Redesign hero section to OpenAI-style
OLD_HERO = src[src.find('<section class="hero">'):src.find('</section>', src.find('<section class="hero">')) + 10]

NEW_HERO = '''<section class="hero hero--openai">
  <div class="hero-bg" id="heroBg">
    <img src="images/hero.jpg" alt="Commercieel vastgoed" class="is-active">
    <img src="images/photo-1.jpg" alt="" loading="lazy">
    <img src="images/photo-2.jpg" alt="" loading="lazy">
  </div>
  <div class="container hero-openai-inner">
    <span class="hero-eyebrow-sm">Spring Real Estate &mdash; Powered by People. Backed by Tech.</span>
    <h1 class="hero-openai-h1" data-tr="1" data-en="How can we <em>help you?</em>" data-es="&iquest;En qu&eacute; podemos <em>ayudarle?</em>">Hoe kunnen wij u <em>helpen?</em></h1>
    <form class="search hero-search hero-search--lg" onsubmit="return false">
      <label class="seg"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg>
        <input type="text" placeholder="Zoek een object, locatie of dienst&hellip;" aria-label="Zoeken"></label>
      <button class="search-btn">Zoeken</button>
    </form>
    <div class="hero-chips">
      <a href="listings.html" class="hero-chip">Kantoor zoeken</a>
      <a href="doelgroep-eigenaar.html" class="hero-chip">Vastgoed verhuren</a>
      <a href="doelgroep-investeerder.html" class="hero-chip">Investeren in vastgoed</a>
      <a href="doelgroep-gebruiker.html" class="hero-chip">Design &amp; Build</a>
      <a href="#diensten" class="hero-chip">Alle diensten</a>
    </div>
    <div class="hero-stats hero-stats--openai">
      <div class="s"><b>18</b><span data-tr="1" data-en="business units" data-es="unidades de negocio">business units</span></div>
      <div class="s"><b>4</b><span data-tr="1" data-en="locations NL &amp; ES" data-es="ubicaciones NL y ES">locaties NL &amp; ES</span></div>
      <div class="s"><b>&euro;1,2 mld</b><span data-tr="1" data-en="real estate under management" data-es="inmuebles bajo gesti&oacute;n">vastgoed onder beheer</span></div>
      <div class="s"><b>15+</b><span data-tr="1" data-en="years of experience" data-es="a&ntilde;os de experiencia">jaar ervaring</span></div>
    </div>
  </div>
</section>'''

src = src.replace(OLD_HERO, NEW_HERO, 1)

# 6. Add id="diensten" to the 18 BU section
src = src.replace(
    '<section class="section dark-sec">\n  <div class="container">\n    <div class="sec-head">\n      <div class="t">\n        <span class="eyebrow" style="color:var(--green-soft)"',
    '<section class="section dark-sec" id="diensten">\n  <div class="container">\n    <div class="sec-head">\n      <div class="t">\n        <span class="eyebrow" style="color:var(--green-soft)"',
    1
)

write('index.html', src)
print('index.html OK')

# ── css/styles.css — append new rules ────────────────────────────────────────
css = read('css/styles.css')

NEW_CSS = '''

/* ── header--dark (zwarte navigatiebalk) ───────────────────────── */
.header--dark{
  background:var(--ink);
  border-bottom-color:rgba(255,255,255,.08);
}
.header--dark .nav > a,
.header--dark .has-drop > a.nav-btn-link,
.header--dark .has-drop > button{ color:rgba(255,255,255,.85); }
.header--dark .nav > a:hover,
.header--dark .has-drop > a.nav-btn-link:hover,
.header--dark .has-drop > button:hover{ color:#fff; }
.header--dark .h-search{ background:rgba(255,255,255,.1); border-color:rgba(255,255,255,.2); color:#fff; }
.header--dark .h-search:hover{ border-color:var(--green); }
.header--dark .h-lang button{ color:rgba(255,255,255,.55); }
.header--dark .h-lang button.active{ background:rgba(255,255,255,.12); color:#fff; }
.header--dark.scrolled{ background:var(--ink); box-shadow:0 4px 24px rgba(0,0,0,.35); }
.header--dark .btn--primary{ background:var(--green); color:#fff; }

/* nav-btn-link: same look as the old button */
.has-drop > a.nav-btn-link{
  text-decoration:none; font-size:.98rem; font-weight:600;
  display:inline-flex; align-items:center; gap:6px; padding:8px 0;
}

/* ── hero--openai (OpenAI-stijl hero) ──────────────────────────── */
.hero--openai{ min-height:100svh; display:flex; align-items:center; }
.hero--openai .hero-bg img{ filter:brightness(.22) saturate(.5); }
.hero--openai .hero-bg::after{
  background:linear-gradient(180deg,rgba(4,6,4,.6) 0%,rgba(4,6,4,.5) 50%,rgba(4,6,4,.8) 100%);
}
.hero-openai-inner{
  display:flex; flex-direction:column; align-items:center; text-align:center;
  padding-top:80px; padding-bottom:80px; width:100%;
}
.hero-eyebrow-sm{
  font-size:.78rem; letter-spacing:.14em; text-transform:uppercase;
  color:var(--green-soft); margin-bottom:1.2rem; opacity:.85;
}
.hero-openai-h1{
  font-size:clamp(2.4rem,6vw,4.4rem); font-weight:800; line-height:1.12;
  color:#fff; margin:0 0 2rem; max-width:760px;
}
.hero-openai-h1 em{ color:var(--green-soft); font-style:normal; }

/* bigger centered search bar */
.hero-search--lg{
  max-width:680px; width:100%;
  background:rgba(255,255,255,.1); border:1px solid rgba(255,255,255,.25);
  padding:6px 6px 6px 22px; border-radius:var(--r-pill);
  backdrop-filter:blur(10px);
}
.hero-search--lg input{
  font-size:1.05rem; color:#fff; flex:1;
}
.hero-search--lg input::placeholder{ color:rgba(255,255,255,.5); }
.hero-search--lg .search-btn{
  background:var(--green); color:#fff; border:0; border-radius:var(--r-pill);
  padding:12px 26px; font-size:.96rem; font-weight:700; cursor:pointer; white-space:nowrap;
}
.hero-search--lg .search-btn:hover{ background:var(--green-bright,#8abb45); }
.hero-search--lg svg{ color:#fff; opacity:.6; flex-shrink:0; }

/* quick-suggestion chips */
.hero-chips{
  display:flex; flex-wrap:wrap; gap:10px; justify-content:center; margin-top:22px;
}
.hero-chip{
  padding:8px 18px; border-radius:var(--r-pill);
  border:1px solid rgba(255,255,255,.22); color:rgba(255,255,255,.78);
  font-size:.875rem; font-weight:500; text-decoration:none; background:rgba(255,255,255,.07);
  transition:border-color .18s, background .18s, color .18s;
}
.hero-chip:hover{ border-color:var(--green); color:#fff; background:rgba(124,167,63,.15); }

/* stats row below chips */
.hero-stats--openai{
  margin-top:60px; display:flex; gap:clamp(28px,5vw,64px);
  flex-wrap:wrap; justify-content:center;
  border-top:1px solid rgba(255,255,255,.1); padding-top:32px; width:100%; max-width:680px;
}
.hero-stats--openai .s b{ font-size:1.6rem; }

@media(max-width:600px){
  .hero-openai-h1{ font-size:2.2rem; }
  .hero-search--lg{ padding:4px 4px 4px 16px; }
}
'''

if '/* ── header--dark' not in css:
    css += NEW_CSS
    write('css/styles.css', css)
    print('styles.css OK')
else:
    print('styles.css — already patched, skipping')
