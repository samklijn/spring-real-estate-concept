"""
rebuild_bu_flow.py — maakt van alle 18 BU-pagina's één kloppend geheel

Fixes per pagina:
1. Bu-toc: verwijder #cijfers, voeg #download en #doelgroep toe
2. Doelgroep-sectie: sector-grid uitbreiden (nu 1 item → 5-6 per pagina)
3. Volgorde: werkwijze VOOR doelgroep (narratief: aanpak → hoe → voor wie)
4. FAQ VOOR gerelateerde diensten (bezwaren wegnemen vóór cross-sell)
"""
import re, glob

ROOT = r'C:/Users/Gebruiker/spring-real-estate-concept'

def read(f):
    with open(f, encoding='utf-8') as fh: return fh.read()
def write(f, s):
    with open(f, 'w', encoding='utf-8') as fh: fh.write(s)

CHKSVG = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M5 12l5 5L20 6"/></svg>'

def sector_html(items):
    return ''.join(
        f'<div class="sector">{CHKSVG} <span>{s}</span></div>'
        for s in items
    )

SECTORS = {
    'unit-aanhuur-kantoorruimte.html':        ['Scale-ups & groeiende bedrijven','MKB & ondernemers','Corporates','Non-profit & onderwijs','Overheid & semi-overheid','Tech & media'],
    'unit-aanverkoop-beleggingsvastgoed.html': ['Private beleggers','Institutionele partijen','Familie-kantoren','Vastgoedfondsen','Buitenlandse investeerders','Corporates'],
    'unit-asset-management.html':             ['Institutionele beleggers','Private beleggers','Familie-kantoren','Vastgoedfondsen','Buitenlandse partijen','Corporates'],
    'unit-commercieel-vastgoedbeheer.html':   ['Eigenaren & verhuurders','Beleggers','Projectontwikkelaars','Corporates','Institutionele partijen','VvE\'s'],
    'unit-design-build.html':                 ['Corporates','Scale-ups & tech','Zorgaanbieders','Non-profit & onderwijs','MKB','Retail & winkels'],
    'unit-financiele-administratie.html':     ['Beleggers','Eigenaren','VvE\'s','Projectontwikkelaars','Institutionele partijen'],
    'unit-grootzakelijke-taxaties.html':      ['Corporates','Overheden & gemeenten','Pensioenfondsen','Institutionele partijen','Banken & financiers'],
    'unit-herbouwwaarde-verzekering.html':    ['Eigenaren','Beleggers','VvE\'s','Corporates','Verzekeraars'],
    'unit-hr-advies.html':                    ['Vastgoedbedrijven','Beleggers','Projectontwikkelaars','Makelaars & adviseurs','Property managers'],
    'unit-recruitment-talent.html':           ['Vastgoedbedrijven','Beleggers','Makelaars & adviseurs','Projectontwikkelaars','Property managers'],
    'unit-residentieel-vastgoedbeheer.html':  ['Particuliere beleggers','Institutionele beleggers','Familie-kantoren','Projectontwikkelaars','Woningcorporaties'],
    'unit-serviced-offices.html':             ['Scale-ups & startups','ZZP & freelancers','Internationale bedrijven','Corporate satellietkantoren','MKB','Tijdelijke huisvesting'],
    'unit-strategic-advisory.html':           ['CFO\'s & directies','Projectontwikkelaars','Beleggers','Corporates','Gemeenten & overheden'],
    'unit-taxaties-beleggingsvastgoed.html':  ['Private beleggers','Institutionele partijen','Banken & financiers','Familie-kantoren','Vastgoedfondsen'],
    'unit-vastgoedadministratie.html':        ['Beleggers','Eigenaren','VvE\'s','Projectontwikkelaars','Institutionele partijen'],
    'unit-vastgoeddata-marktinzichten.html':  ['Beleggers','Projectontwikkelaars','Corporates','Gemeenten & overheden','Institutionele partijen'],
    'unit-vastgoedmarketing.html':            ['Eigenaren','Beleggers','Projectontwikkelaars','Institutionele partijen','Corporates'],
    'unit-verhuur-commercieel.html':          ['Kantoren','Logistiek & bedrijfsruimte','Retail & winkels','Zorgvastgoed','Residentieel','Hospitality'],
}

def balanced_div_end(text, start):
    """Geeft positie NA het sluitende </div> van het div dat op 'start' begint."""
    pos = start + 4  # skip '<div'
    depth = 1
    while depth > 0 and pos < len(text):
        o = text.find('<div', pos)
        c = text.find('</div>', pos)
        if c == -1:
            break
        if o != -1 and o < c:
            depth += 1
            pos = o + 4
        else:
            depth -= 1
            pos = c + 6
    return pos  # points to char after last </div>

def replace_sector_grid(src, fname):
    """Vervangt de sector-grid inhoud in de doelgroep-sectie."""
    sectors = SECTORS.get(fname, ['Corporates', 'Beleggers', 'Projectontwikkelaars', 'MKB', 'Overheid'])
    new_grid = '<div class="sector-grid">' + sector_html(sectors) + '</div>'

    # Vind de doelgroep sectie
    doelg_m = re.search(r'<section[^>]+id="doelgroep"[^>]*>', src)
    if not doelg_m:
        return src

    # Vind sector-grid binnen de doelgroep sectie (start zoeken na sectie-open)
    grid_idx = src.find('<div class="sector-grid">', doelg_m.start())
    if grid_idx == -1:
        return src

    grid_end = balanced_div_end(src, grid_idx)
    return src[:grid_idx] + new_grid + src[grid_end:]

NEW_TOC = '''<nav class="bu-toc"><div class="container">
  <a href="#aanpak">Aanpak</a><a href="#expertises">Expertises</a><a href="#werkwijze">Zo werken wij</a><a href="#doelgroep">Voor wie</a><a href="#cases">Cases</a><a href="#team">Team</a><a href="#reviews">Reviews</a><a href="#download">Download</a><a href="#faq">FAQ</a><a href="#kennis">Kennis</a>
</div></nav>'''

for fpath in sorted(glob.glob(ROOT + '/unit-*.html')):
    fname = fpath.split('\\')[-1].split('/')[-1]
    src = read(fpath)
    orig_len = len(src)

    # 1. Bu-toc vervangen
    src = re.sub(r'<nav class="bu-toc">.*?</nav>', NEW_TOC, src, flags=re.DOTALL)

    # 2. Sector-grid uitbreiden
    src = replace_sector_grid(src, fname)

    # 3. Volgorde: werkwijze VOOR doelgroep (als doelgroep nu eerder staat)
    werk_m  = re.search(r'\n<section[^>]+id="werkwijze"[^>]*>.*?</section>', src, re.DOTALL)
    doelg_m = re.search(r'\n<section[^>]+id="doelgroep"[^>]*>.*?</section>', src, re.DOTALL)
    if werk_m and doelg_m and werk_m.start() > doelg_m.start():
        werk  = werk_m.group(0)
        doelg = doelg_m.group(0)
        mid   = src[doelg_m.end():werk_m.start()]
        src   = src[:doelg_m.start()] + werk + mid + doelg + src[werk_m.end():]

    # 4. FAQ VOOR gerelateerde diensten (als FAQ nu later staat)
    faq_m  = re.search(r'\n<section[^>]+id="faq"[^>]*>.*?</section>', src, re.DOTALL)
    grel_m = re.search(
        r'\n<section[^>]*><div class="container">\s*<div class="sec-head">.*?Gerelateerde diensten.*?</section>',
        src, re.DOTALL
    )
    if faq_m and grel_m and faq_m.start() > grel_m.start():
        faq  = faq_m.group(0)
        grel = grel_m.group(0)
        mid  = src[grel_m.end():faq_m.start()]
        src  = src[:grel_m.start()] + faq + mid + grel + src[faq_m.end():]

    write(fpath, src)
    delta = len(src) - orig_len
    print(f'  {fname}: {len(src.splitlines())}L  ({delta:+d} chars)')

print('\nKlaar.')
