import re, glob

def read(f):
    with open(f, encoding='utf-8') as fh: return fh.read()
def write(f, s):
    with open(f, 'w', encoding='utf-8') as fh: fh.write(s)

ROOT = 'C:/Users/Gebruiker/spring-real-estate-concept'

# ══════════════════════════════════════════════════════════════════════════════
# index.html
# ══════════════════════════════════════════════════════════════════════════════
print('index.html...')
src = read(f'{ROOT}/index.html')

# 1. Hero: remove hero-stats (getallen weg)
src = re.sub(
    r'\n    <div class="hero-stats hero-stats--openai">.*?</div>\n  </div>',
    '\n  </div>',
    src, count=1, flags=re.DOTALL
)

# 2. Hero input: add id for JS placeholder rotation
src = src.replace(
    'placeholder="Zoek een object, locatie of dienst…" aria-label="Zoeken"',
    'placeholder="Zoek een object, locatie of dienst…" aria-label="Zoeken" id="heroInput" autocomplete="off"',
    1
)

# 3. Doelgroepen: add Financierder as 5th card
OLD_ONTWIKKELAAR_CARD = '<a class="kat-card" href="doelgroep-ontwikkelaar.html" id="ontwikkelaar">'
FINANCIER_CARD = '\n        <a class="kat-card" href="doelgroep-financier.html" id="financier"><img src="images/photo-2.jpg" alt=""><span class="ktag">05 &mdash; Financier</span><span class="kbody"><h3>Financier</h3><p>Ik wil vastgoed financieren of taxeren</p></span><span class="karr"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></a>'

# find end of ontwikkelaar card
ow_start = src.find(OLD_ONTWIKKELAAR_CARD)
if ow_start > 0:
    # find closing </a> after it
    ow_end = src.find('</a>', ow_start) + 4
    src = src[:ow_end] + FINANCIER_CARD + src[ow_end:]
    print('  Financierder card added')

# 4. Extract logos-band HTML so we can reinsert it later
logos_match = re.search(r'\n<!-- ============ CLIENT LOGOS.*?-->\n<section class="logos-band">.*?</section>', src, re.DOTALL)
logos_html = logos_match.group(0) if logos_match else ''
if logos_html:
    src = src.replace(logos_html, '', 1)
    print('  logos-band extracted')

# 5. Remove unwanted sections
sections_removed = []
patterns = [
    ('Kernwaarden/USPs', r'\n<!-- ============ USPs.*?-->\n<section class="section">\s*<div class="container">\s*<div class="sec-head">.*?</section>'),
    ('Locaties/map', r'\n<!-- ============ LOCATIONS.*?-->\n<section class="section dark-sec" id="diensten">.*?</section>'),
    ('Bewezen aanpak', r'\n<!-- ============ PROVEN.*?-->\n<section class="section">.*?</section>'),
    ('Team', r'\n<!-- ============ TEAM.*?-->\n<section class="section dark-sec">.*?</section>'),
    ('Reviews', r'\n<!-- ============ REVIEWS.*?-->\n<section class="section">.*?</section>'),
    ('Business units', r'\n<!-- ============ BUSINESS UNITS.*?-->\n<section class="section dark-sec">.*?</section>'),
    ('Uitgelicht aanbod', r'\n<!-- ============ UITGELICHT AANBOD.*?-->\n<section class="section--tight">.*?</section>'),
    ('Recente transacties', r'\n<!-- ============ RECENTE TRANSACTIES.*?-->\n<section class="section--tight">.*?</section>'),
    ('Resources/nieuws', r'\n<!-- ============ RESOURCES.*?-->\n<section class="section">.*?</section>'),
]
for name, pat in patterns:
    new_src = re.sub(pat, '', src, count=1, flags=re.DOTALL)
    if new_src != src:
        src = new_src
        sections_removed.append(name)
    else:
        print(f'  MISS: {name}')
print(f'  Removed: {", ".join(sections_removed)}')

# 6. Insert logos-band after audience/doelgroepen section
if logos_html:
    audience_comment = '<!-- ============ AUDIENCE'
    audience_pos = src.find(audience_comment)
    if audience_pos > 0:
        section_end = src.find('</section>', audience_pos) + 10
        src = src[:section_end] + '\n' + logos_html + src[section_end:]
        print('  logos-band inserted after doelgroepen')

# 7. Remove talk-strip
src = re.sub(r'\n<section class="talk-strip">.*?</section>', '', src, count=1, flags=re.DOTALL)

# 8. Remove floating bel-knop
src = re.sub(r'\n<!-- Floating bel-knop -->\n<a[^>]*class="float-cta"[^>]*>.*?</a>', '', src, count=1, flags=re.DOTALL)

# 9. Footer: Locaties -> Kantoorgebieden + address + Sectoren + Financierder
src = src.replace(
    '<h4 data-i18n="foot.locaties">Locaties</h4>',
    '<h4>Kantoorgebieden</h4>',
    1
)
src = src.replace(
    '<li><a href="locatie-estepona.html">Estepona (ES)</a></li>\n    </ul></div>',
    '<li><a href="locatie-estepona.html">Estepona (ES)</a></li>\n      <li style="margin-top:12px;color:#a9ab9f;font-size:.85rem"><strong style="color:#d1d4cb">Spring Real Estate</strong><br>Croeselaan 28, 3521 CA Utrecht</li>\n    </ul></div>',
    1
)
# Add Financierder to footer doelgroepen list
src = src.replace(
    '<li><a href="doelgroep-ontwikkelaar.html" data-i18n="dd.ontwikkelaar">Ontwikkelaar</a></li>\n    </ul></div>',
    '<li><a href="doelgroep-ontwikkelaar.html" data-i18n="dd.ontwikkelaar">Ontwikkelaar</a></li>\n      <li><a href="doelgroep-financier.html">Financier</a></li>\n    </ul></div>',
    1
)
# Add Sectoren + Alle diensten to navigation list
src = src.replace(
    '<li><a href="sectoren.html">Sectoren</a></li>',
    '<li><a href="sectoren.html">Sectoren</a></li>\n      <li><a href="diensten.html">Alle oplossingen</a></li>',
    1
)

# 10. Rotating search placeholders JS
PLACEHOLDER_JS = '''<script>
(function(){
  var el=document.getElementById('heroInput');
  if(!el)return;
  var hints=[
    'Ik zoek een kantoor van 500m² in Amsterdam…',
    'Hoe verhuur ik mijn bedrijfspand het snelst?',
    'Wat levert mijn vastgoed op als belegging?',
    'Design & Build voor ons nieuwe hoofdkantoor…',
    'Taxatie van mijn commercieel pand aanvragen…',
    'Kantoorruimte huren in Utrecht Stationsgebied…',
  ];
  var i=0;
  setInterval(function(){ i=(i+1)%hints.length; el.setAttribute('placeholder',hints[i]); }, 3200);
})();
</script>'''
src = src.replace('</body>', PLACEHOLDER_JS + '\n</body>', 1)

write(f'{ROOT}/index.html', src)
print('index.html DONE\n')

# ══════════════════════════════════════════════════════════════════════════════
# All pages: rename Diensten->Oplossingen, add Financierder to dropdown,
# remove talk-strip + float-cta
# ══════════════════════════════════════════════════════════════════════════════
print('All pages nav updates...')

FINANCIER_NAV = '        <a href="doelgroep-financier.html"><span class="d-ic"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3h18v4H3zM3 10h18v4H3zM3 17h18v4H3z"/></svg></span><span><span class="d-t">Financier</span><span class="d-d">Ik wil vastgoed financieren of taxeren</span></span></a>'

pages = glob.glob(f'{ROOT}/*.html')
nav_updated = 0
for fname in pages:
    try:
        with open(fname, encoding='utf-8') as fh: txt = fh.read()
        orig = txt

        # Rename Diensten -> Oplossingen in nav button
        txt = txt.replace('>Diensten<', '>Oplossingen<', 1)

        # Add Financierder to nav dropdown (after Ontwikkelaar link)
        OLD_END = 'Ik wil ontwikkelen of optimaliseren</span></span></a>\n      </div>'
        NEW_END = 'Ik wil ontwikkelen of optimaliseren</span></span></a>\n' + FINANCIER_NAV + '\n      </div>'
        if OLD_END in txt and FINANCIER_NAV not in txt:
            txt = txt.replace(OLD_END, NEW_END, 1)

        # Remove talk-strip
        if 'class="talk-strip"' in txt:
            txt = re.sub(r'\n<section class="talk-strip">.*?</section>', '', txt, count=1, flags=re.DOTALL)

        # Remove float-cta
        if 'float-cta' in txt:
            txt = re.sub(r'\n<!-- Floating bel-knop -->\n<a[^>]*float-cta[^>]*>.*?</a>', '', txt, count=1, flags=re.DOTALL)
            txt = re.sub(r'\n<a[^>]*float-cta[^>]*>.*?</a>', '', txt, count=1, flags=re.DOTALL)

        if txt != orig:
            with open(fname, 'w', encoding='utf-8') as fh: fh.write(txt)
            nav_updated += 1
    except Exception as e:
        print(f'  ERR {fname}: {e}')

print(f'Nav: {nav_updated} pages updated\n')

# ══════════════════════════════════════════════════════════════════════════════
# CSS: kat-grid 5 columns
# ══════════════════════════════════════════════════════════════════════════════
print('CSS...')
css_path = f'{ROOT}/css/styles.css'
css = read(css_path)
if 'kat-grid--five' not in css:
    css += '''

/* ── 5-doelgroepen kat-grid ──────────────────────────────────── */
@media(min-width:1100px){ .kat-grid{ grid-template-columns:repeat(5,1fr); } }
@media(min-width:600px) and (max-width:1099px){ .kat-grid{ grid-template-columns:repeat(3,1fr); } }
/* placeholder so selector is unique */ .kat-grid--five{ display:none; }
'''
    write(css_path, css)
    print('CSS updated')

print('\nKlaar!')
