"""
fix_flow.py — achtergrond-flow en kleine bugs op alle BU-pagina's

Fixes:
1. Verwijder overgebleven logos-row/logos-cap sectie (geen logos-band class)
2. Voeg section--soft toe aan kennis (was WIT, moet LICHTGROEN)
3. Herstel dubbele sec-head in doelgroep-sectie
4. Gerelateerde diensten: voeg section--soft toe zodat flow klopt
   (download WIT → kennis LG → gerelateerde diensten WIT → faq LG)
   → gerelateerde diensten blijft WIT, het ritme klopt al
"""
import re, glob

def read(f):
    with open(f, encoding='utf-8') as fh: return fh.read()
def write(f, s):
    with open(f, 'w', encoding='utf-8') as fh: fh.write(s)

for fpath in sorted(glob.glob('unit-*.html')):
    src = read(fpath)

    # 1. Verwijder logos-row sectie (section--tight met logos-cap erin)
    src = re.sub(
        r'\n<section class="section--tight"><div class="container">\s*<div class="logos-cap">.*?</section>',
        '', src, flags=re.DOTALL
    )

    # 2. Kennis: section--tight → section--tight section--soft
    src = src.replace(
        '<section class="section--tight" id="kennis">',
        '<section class="section--tight section--soft" id="kennis">'
    )

    # 3. Fix dubbele sec-head in doelgroep
    src = re.sub(
        r'(<section[^>]+id="doelgroep"[^>]*><div class="container">\s*)<div class="sec-head"><div class="sec-head">',
        r'\1<div class="sec-head">',
        src
    )
    # ook de bijbehorende extra sluit-div
    src = re.sub(
        r'(id="doelgroep".*?<div class="sec-head"><div class="t">.*?</div></div>)</div>',
        r'\1',
        src, flags=re.DOTALL, count=1
    )

    # 4. Gerelateerde diensten krijgt subtiele lichtgrijze tint voor scheiding
    #    (section--tight blijft, voeg geen soft toe — FAQ (soft) volgt al)

    write(fpath, src)
    print(f'  {fpath}: {len(src.splitlines())}L')

print('Klaar.')
