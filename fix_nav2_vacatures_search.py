import re, glob, os

ROOT = r'C:/Users/Gebruiker/spring-real-estate-concept'
CHV = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>'

# Icons
ICO_BUILDING = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 3v18M15 9h3M15 13h3M15 17h3M6 9h1M6 13h1"/></svg>'
ICO_PIN      = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="10" r="3"/><path d="M12 21s-7-5.5-7-11a7 7 0 0 1 14 0c0 5.5-7 11-7 11z"/></svg>'

# New nav block: Aanbod dropdown with icons + simple links for the rest
NEW_NAV_TAIL = f'''    <div class="has-drop"><button><span>Aanbod</span> {CHV}</button>
      <div class="drop">
        <a href="listings.html"><span class="d-ic">{ICO_BUILDING}</span><span><span class="d-t">Alle objecten</span><span class="d-d">Kantoor, bedrijf en belegging</span></span></a>
        <a href="locatie-amsterdam.html"><span class="d-ic">{ICO_PIN}</span><span><span class="d-t">Amsterdam</span><span class="d-d">7 objecten beschikbaar</span></span></a>
        <a href="locatie-utrecht.html"><span class="d-ic">{ICO_PIN}</span><span><span class="d-t">Utrecht</span><span class="d-d">5 objecten beschikbaar</span></span></a>
        <a href="locatie-valencia.html"><span class="d-ic">{ICO_PIN}</span><span><span class="d-t">Valencia &amp; Estepona</span><span class="d-d">4 objecten beschikbaar</span></span></a>
      </div>
    </div>
    <a href="agents.html">Ons team</a>
    <a href="about.html">About</a>
    <a href="resources.html">Resources</a>
    <a href="vacatures.html">Vacatures</a>
  </nav>'''

# Match from the new Aanbod dropdown (or old) through </nav>
# This pattern matches everything from the first has-drop after Diensten to </nav>
NAV_PAT = re.compile(
    r'(      </div>\n    </div>\n)'          # end of Diensten has-drop
    r'    <div class="has-drop">.*?</nav>',  # everything through </nav>
    re.DOTALL
)

SEARCH_FORM = '''    <form class="search search--light search--single" onsubmit="return false">
      <label class="seg"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg>
        <input type="text" placeholder="Zoek een object, locatie of dienst&hellip;" aria-label="Zoeken"></label>
      <button class="search-btn"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg> Zoeken</button>
    </form>'''

SKIP_SEARCH = {'contact.html','cookies.html','privacy.html','voorwaarden.html','listings.html',
               'index.html','404.html','listing-detail.html'}

files = glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True)
nav_count = search_count = 0

for f in files:
    fname = os.path.basename(f)
    with open(f, encoding='utf-8') as fh:
        txt = fh.read()
    changed = False

    # 1. Fix nav
    new_txt = NAV_PAT.sub(r'\1' + NEW_NAV_TAIL, txt)
    if new_txt != txt:
        txt = new_txt
        nav_count += 1
        changed = True

    # 2. Add search--light to page-hero if missing and not in skip list
    if fname not in SKIP_SEARCH and 'page-hero' in txt and 'search--light' not in txt:
        # Insert before </div></section> that closes the page-hero container
        txt = txt.replace('  </div>\n</section>\n\n<section', SEARCH_FORM + '\n  </div>\n</section>\n\n<section', 1)
        search_count += 1
        changed = True

    if changed:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(txt)

print(f'Nav updated: {nav_count} files')
print(f'Search added: {search_count} files')

# --- Fix vacatures.html section order ---
vac_file = os.path.join(ROOT, 'vacatures.html')
with open(vac_file, encoding='utf-8') as f:
    txt = f.read()

# Extract sections by finding them all
def extract_section(txt, marker):
    m = re.search(r'(<section[^>]*' + re.escape(marker) + r'[^>]*>[\s\S]*?</section>)\n', txt)
    return m

# Current order (after previous fix):
# hero | vacatures | hero-stats | two-col-intro | arbeidsvoorwaarden | sollicitatieproces | quotes | FAQ | CTA | talk-strip

# Extract vacatures section (id="vacatures")
m_vac = re.search(r'\n(<section[^>]*id="vacatures"[^>]*>[\s\S]*?</section>)\n', txt)
m_stats = re.search(r'\n(<section[^>]*section--tight[^>]*>[\s\S]*?hero-stats[\s\S]*?</section>)\n', txt)
m_intro = re.search(r'\n(<section[^>]*section--soft[^>]*><div class="container"><div class="two-col">[\s\S]*?</section>)\n', txt)
m_vw    = re.search(r'\n(<section[^>]*class="section"[^>]*><div class="container">\n  <div class="sec-head">[\s\S]*?arbeidsvoorwaarden[\s\S]*?</section>)\n', txt)

if all([m_vac, m_stats, m_intro]):
    vac_sec   = m_vac.group(1)
    stats_sec = m_stats.group(1) if m_stats else ''
    intro_sec = m_intro.group(1)

    # Remove all three from current positions
    txt2 = txt
    for m in [m_vac, m_stats, m_intro]:
        if m:
            txt2 = txt2.replace('\n' + m.group(1) + '\n', '\n', 1)

    # Insert after page-hero: stats → intro → vacatures
    insert = '\n' + stats_sec + '\n\n' + intro_sec + '\n\n' + vac_sec + '\n'
    txt2 = re.sub(r'(</section>\n)(\n<section)', insert + r'\2', txt2, count=1)

    with open(vac_file, 'w', encoding='utf-8') as f:
        f.write(txt2)
    print('Vacatures page reordered: hero → stats → intro → vacatures → rest')
else:
    print('Could not fully reorder vacatures — missing sections')

# --- CSS version bump v28 -> v29 ---
css_count = 0
for f in files:
    with open(f, encoding='utf-8') as fh:
        txt = fh.read()
    new = txt.replace('styles.css?v=28', 'styles.css?v=29')
    if new != txt:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(new)
        css_count += 1
print(f'CSS version bumped in {css_count} files')
