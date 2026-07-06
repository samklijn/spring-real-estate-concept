"""
fix_order_only.py — corrigeert alleen de volgorde van secties op BU-pagina's.

Gewenste volgorde:
aanpak → expertises → werkwijze → doelgroep → cases → team → reviews → download → kennis → faq → gerelateerde → talk-strip
"""
import re, glob

ROOT = r'C:/Users/Gebruiker/spring-real-estate-concept'

def read(f):
    with open(f, encoding='utf-8') as fh: return fh.read()
def write(f, s):
    with open(f, 'w', encoding='utf-8') as fh: fh.write(s)

def extract(src, pattern):
    """Haal eerste match op en geef (match_str, src_zonder_match)."""
    m = re.search(pattern, src, re.DOTALL)
    if m:
        return m.group(0), src[:m.start()] + src[m.end():]
    return None, src

def insert_before(src, block, anchor):
    """Voeg block in net vóór anchor-string."""
    idx = src.find(anchor)
    if idx == -1:
        return src
    return src[:idx] + block + '\n' + src[idx:]

# Patronen voor secties (liberal: werkt ongeacht classes)
P_WERKWIJZE = r'\n<section[^>]+id="werkwijze"[^>]*>.*?</section>'
P_DOELGROEP = r'\n<section[^>]+id="doelgroep"[^>]*>.*?</section>'
P_FAQ       = r'\n<section[^>]+id="faq"[^>]*>.*?</section>'
TALK_STRIP  = '\n<section class="talk-strip">'

for fpath in sorted(glob.glob(ROOT + '/unit-*.html')):
    fname = fpath.split('\\')[-1].split('/')[-1]
    if fname == 'unit-herbouwwaarde-verzekering.html':
        continue  # unieke pagina, geen standaard-secties
    src = read(fpath)

    # ── Stap 1: haal werkwijze en doelgroep eruit, zet werkwijze vóór doelgroep ─
    werk_m  = re.search(P_WERKWIJZE, src, re.DOTALL)
    doelg_m = re.search(P_DOELGROEP, src, re.DOTALL)

    if werk_m and doelg_m and werk_m.start() > doelg_m.start():
        # doelgroep staat vóór werkwijze → swap
        werk  = werk_m.group(0)
        doelg = doelg_m.group(0)
        mid   = src[doelg_m.end():werk_m.start()]
        src   = src[:doelg_m.start()] + werk + mid + doelg + src[werk_m.end():]

    # ── Stap 2: haal FAQ eruit, zet hem vóór talk-strip (na kennis/gerelateerde) ─
    faq_block, src = extract(src, P_FAQ)
    if faq_block:
        src = insert_before(src, faq_block, TALK_STRIP)

    write(fpath, src)
    print(f'  {fname}: OK')

print('\nKlaar.')
