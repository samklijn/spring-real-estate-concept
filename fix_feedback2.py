import re, glob, shutil

ROOT = 'C:/Users/Gebruiker/spring-real-estate-concept'

def read(f):
    with open(f, encoding='utf-8') as fh: return fh.read()
def write(f, s):
    with open(f, 'w', encoding='utf-8') as fh: fh.write(s)

# ══════════════════════════════════════════════════════════════════════════════
# 1. Verwijder topbar van ALLE pagina's
# ══════════════════════════════════════════════════════════════════════════════
print('1. Topbar verwijderen van alle paginas...')
pages = glob.glob(f'{ROOT}/*.html')
topbar_removed = 0
for fname in pages:
    with open(fname, encoding='utf-8') as fh: src = fh.read()
    if 'class="topbar"' in src:
        new = re.sub(r'\n?<div class="topbar">.*?</div>\n?', '\n', src, count=1, flags=re.DOTALL)
        write(fname, new)
        topbar_removed += 1
print(f'   Topbar verwijderd van {topbar_removed} paginas')

# ══════════════════════════════════════════════════════════════════════════════
# 2. Nav: maak Aanbod, Resources, Team, About direct klikbaar
# ══════════════════════════════════════════════════════════════════════════════
print('2. Nav knoppen klikbaar maken...')

NAV_REPLACEMENTS = [
    # Aanbod button -> a href
    (
        '<div class="has-drop"><button><span data-i18n="nav.aanbod">Aanbod</span>',
        '<div class="has-drop"><a href="listings.html" class="nav-btn-link"><span data-i18n="nav.aanbod">Aanbod</span>'
    ),
    # Resources button -> a href
    (
        '<div class="has-drop"><button><span data-i18n="nav.resources">Resources</span>',
        '<div class="has-drop"><a href="resources.html" class="nav-btn-link"><span data-i18n="nav.resources">Resources</span>'
    ),
    # Team button -> a href
    (
        '<div class="has-drop"><button><span data-i18n="nav.team">Team</span>',
        '<div class="has-drop"><a href="agents.html" class="nav-btn-link"><span data-i18n="nav.team">Team</span>'
    ),
    # About button -> a href
    (
        '<div class="has-drop"><button><span data-i18n="nav.about">About</span>',
        '<div class="has-drop"><a href="about.html" class="nav-btn-link"><span data-i18n="nav.about">About</span>'
    ),
]
# Also fix the closing </button> -> </a> for each
NAV_CLOSE_OLD = ' <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button>'
NAV_CLOSE_NEW = ' <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></a>'

nav_updated = 0
for fname in pages:
    with open(fname, encoding='utf-8') as fh: src = fh.read()
    orig = src
    for old, new in NAV_REPLACEMENTS:
        src = src.replace(old, new, 1)
    # Fix closing tags: replace </button> after nav-btn-link openings
    # Count how many nav-btn-link anchors exist to replace same number of </button>
    count = src.count('class="nav-btn-link"')
    # Replace first `count` occurrences of the svg+button close pattern
    replaced = 0
    pos = 0
    while replaced < count and pos < len(src):
        idx = src.find(NAV_CLOSE_OLD, pos)
        if idx == -1: break
        src = src[:idx] + NAV_CLOSE_NEW + src[idx+len(NAV_CLOSE_OLD):]
        pos = idx + len(NAV_CLOSE_NEW)
        replaced += 1
    if src != orig:
        write(fname, src)
        nav_updated += 1
print(f'   {nav_updated} paginas nav bijgewerkt')

# ══════════════════════════════════════════════════════════════════════════════
# 3. Kernwaarden onder hero toevoegen op index.html
# ══════════════════════════════════════════════════════════════════════════════
print('3. Kernwaarden strip onder hero...')
src = read(f'{ROOT}/index.html')

KERNWAARDEN_HTML = '''
<section class="section--tight kw-strip" style="background:var(--ink);border-top:1px solid rgba(255,255,255,.08)">
  <div class="container">
    <div class="kw-row">
      <div class="kw-item">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--green-soft)" stroke-width="2"><path d="M12 2l8 4v6c0 5-3.5 8-8 10-4.5-2-8-5-8-10V6z"/><path d="M9 12l2 2 4-4"/></svg>
        <span><strong>Trusted Advisor</strong><span class="kw-sub">Helder, eerlijk advies dat werkt</span></span>
      </div>
      <div class="kw-item">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--green-soft)" stroke-width="2"><path d="M13 2L3 14h7l-1 8 10-12h-7z"/></svg>
        <span><strong>Work Hard, Play Hard</strong><span class="kw-sub">Energie en resultaat gaan samen</span></span>
      </div>
      <div class="kw-item">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--green-soft)" stroke-width="2"><path d="M3 17l6-6 4 4 8-8M21 7v6M21 7h-6"/></svg>
        <span><strong>Every Step We Grow</strong><span class="kw-sub">Elke dag beter, voor onze klanten</span></span>
      </div>
      <div class="kw-item">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--green-soft)" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
        <span><strong>Let&rsquo;s Go</strong><span class="kw-sub">Proactief, van idee tot resultaat</span></span>
      </div>
      <div class="kw-item">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--green-soft)" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13A4 4 0 0 1 16 11"/></svg>
        <span><strong>All-in, All Together</strong><span class="kw-sub">Als &eacute;&eacute;n team, voor u</span></span>
      </div>
    </div>
  </div>
</section>'''

# Insert after hero section, before audience section
INSERT_BEFORE = '\n<!-- ============ VASTGOEDZOEKER'
src = src.replace(INSERT_BEFORE, KERNWAARDEN_HTML + INSERT_BEFORE, 1)
write(f'{ROOT}/index.html', src)
print('   Kernwaarden strip toegevoegd')

# ══════════════════════════════════════════════════════════════════════════════
# 4. CSS voor kernwaarden strip + kw-row
# ══════════════════════════════════════════════════════════════════════════════
print('4. CSS toevoegen...')
css = read(f'{ROOT}/css/styles.css')
if '.kw-strip' not in css:
    css += '''

/* ── Kernwaarden strip ──────────────────────────────────────────── */
.kw-strip{ padding:20px 0; }
.kw-row{
  display:flex; flex-wrap:wrap; gap:8px 32px;
  justify-content:space-between; align-items:center;
}
.kw-item{
  display:flex; align-items:center; gap:10px;
  color:rgba(255,255,255,.75); font-size:.875rem;
}
.kw-item strong{ display:block; color:#fff; font-size:.88rem; line-height:1.2; }
.kw-sub{ display:block; color:rgba(255,255,255,.45); font-size:.78rem; margin-top:1px; }
@media(max-width:768px){
  .kw-row{ gap:16px 24px; }
  .kw-item{ flex:1 1 calc(50% - 24px); }
}
@media(max-width:480px){
  .kw-item{ flex:1 1 100%; }
}
'''
    write(f'{ROOT}/css/styles.css', css)
    print('   CSS updated')

# ══════════════════════════════════════════════════════════════════════════════
# 5. Maak doelgroep-financier.html (kopie van investeerder als basis)
# ══════════════════════════════════════════════════════════════════════════════
print('5. doelgroep-financier.html aanmaken...')
base = read(f'{ROOT}/doelgroep-investeerder.html')

# Adapt for Financier
fin = base
fin = fin.replace('<title>Spring Real Estate &mdash; Voor de investeerder', '<title>Spring Real Estate &mdash; Voor de financier')
fin = fin.replace('Voor de <em>investeerder</em>', 'Voor de <em>financier</em>')
fin = fin.replace('Investeerder', 'Financier')
fin = fin.replace('investeerder', 'financier')
fin = fin.replace('doelgroep-investeerder', 'doelgroep-financier')
fin = fin.replace('Ik wil investeren in vastgoed', 'Ik wil vastgoed financieren of taxeren')
fin = fin.replace('Voor de investeerder', 'Voor de financier')
# Update hero title
fin = re.sub(
    r'<h1[^>]*>.*?</h1>',
    '<h1>Vastgoed <em>financieren</em> &amp; taxeren</h1>',
    fin, count=1, flags=re.DOTALL
)
# Update lead text
fin = re.sub(
    r'(<p class="hero-sub"[^>]*>)[^<]*</p>',
    r'\1Spring begeleidt financiers, banken en taxateurs bij commercieel en residentieel vastgoed &mdash; met gecertificeerde expertise (RICS, NRVT) en actuele marktdata.</p>',
    fin, count=1
)
write(f'{ROOT}/doelgroep-financier.html', fin)
print('   doelgroep-financier.html aangemaakt')

# ══════════════════════════════════════════════════════════════════════════════
# 6. Zoekbalk placeholder JS verbeteren (al op index, maar ook
#    controleren of het id heroInput correct staat)
# ══════════════════════════════════════════════════════════════════════════════
print('6. Zoekbalk placeholder check...')
src = read(f'{ROOT}/index.html')
if 'id="heroInput"' in src and 'heroInput' in src:
    print('   Rotating placeholders al aanwezig OK')
else:
    src = src.replace(
        'aria-label="Zoeken"',
        'aria-label="Zoeken" id="heroInput" autocomplete="off"',
        1
    )
    print('   heroInput id toegevoegd')
    write(f'{ROOT}/index.html', src)

print('\nAlles klaar!')
