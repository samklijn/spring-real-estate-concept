"""
reorder_units.py  v2  — CRO-volgorde + split sector/quote voor alle 18 BU-pagina's

Splits de pagina in 3 vaste zones:
  HEADER  = alles t/m </nav> van bu-toc
  CONTENT = alles tussen bu-toc en talk-strip  (hier herschikken we)
  TAIL    = talk-strip + footer + scripts

CRO-volgorde in CONTENT:
  Logos → Cijfers → Aanpak → Expertises → Voor wie (sector) → Werkwijze
  → Cases → Quote (donkere break) → Team → Reviews → Lead magnet
  → FAQ → Kennis → Spanje (optioneel) → Gerelateerde diensten
"""
import re, glob

ROOT = r'C:/Users/Gebruiker/spring-real-estate-concept'

def read(f):
    with open(f, encoding='utf-8') as fh: return fh.read()
def write(f, s):
    with open(f, 'w', encoding='utf-8') as fh: fh.write(s)

def pull_id(content, sid):
    """Haal sectie met id=sid uit content; return (sectie, rest)."""
    m = re.search(r'\n<section[^>]+id="' + sid + r'"[^>]*>.*?</section>', content, re.DOTALL)
    if m:
        return m.group(0), content[:m.start()] + content[m.end():]
    return '', content

def pull_pattern(content, pattern):
    """Haal eerste match van pattern uit content; return (match, rest)."""
    m = re.search(pattern, content, re.DOTALL)
    if m:
        return m.group(0), content[:m.start()] + content[m.end():]
    return '', content

for fpath in sorted(glob.glob(ROOT + '/unit-*.html')):
    fname = fpath.split('\\')[-1].split('/')[-1]
    src = read(fpath)

    # ── Splits in 3 zones ───────────────────────────────────────────────────
    # HEADER eindigt na de </nav> van bu-toc (niet de header-nav)
    toc_end = re.search(r'<nav class="bu-toc">.*?</nav>\s*\n', src, re.DOTALL)
    if not toc_end:
        print(f'  SKIP (geen bu-toc): {fname}'); continue

    # TAIL begint bij talk-strip
    ts_start = src.find('\n<section class="talk-strip">')
    if ts_start == -1:
        print(f'  SKIP (geen talk-strip): {fname}'); continue

    header  = src[:toc_end.end()]
    content = src[toc_end.end():ts_start]
    tail    = src[ts_start:]

    # ── Split gecombineerde sector+quote sectie ─────────────────────────────
    combo_m = re.search(
        r'\n<section class="section--tight"><div class="container">'
        r'<div class="two-col two-col--60-40"[^>]*>(.*?)</section>',
        content, re.DOTALL
    )
    new_quote_sec = ''
    if combo_m:
        inner = combo_m.group(1)

        sec_head_m = re.search(r'<div class="sec-head">.*?</div></div>', inner, re.DOTALL)
        sec_head   = sec_head_m.group(0) if sec_head_m else ''

        grid_m    = re.search(r'<div class="(?:sector|units)-grid">.*?</div>', inner, re.DOTALL)
        grid_html = grid_m.group(0) if grid_m else ''

        panel_m   = re.search(r'<div class="panel"[^>]*>(.*?)</div>\s*</div></div>', inner, re.DOTALL)
        panel_inner = panel_m.group(1) if panel_m else ''

        # Sector-sectie (standalone, lichtgroen)
        new_sector = (
            '\n<section class="section--tight" id="doelgroep"><div class="container">'
            '\n  <div class="sec-head">' + sec_head + '</div>'
            '\n  ' + grid_html +
            '\n</div></section>'
        )

        # Quote-sectie (donker, als break)
        if panel_inner.strip():
            new_quote_sec = (
                '\n<section class="section dark-sec"><div class="container">'
                '\n  <div class="center" style="max-width:68ch;margin:0 auto;text-align:center">'
                '\n' + re.sub(r'style="', 'style="color:#fff;', panel_inner.strip()) +
                '\n  </div>'
                '\n</div></section>'
            )

        content = content[:combo_m.start()] + new_sector + content[combo_m.end():]

    # ── Trek secties eruit ───────────────────────────────────────────────────
    logos_txt,   content = pull_pattern(content, r'\n?<section class="logos-band">.*?</section>')
    cijfers_txt, content = pull_id(content, 'cijfers')
    aanpak_txt,  content = pull_id(content, 'aanpak')
    exp_txt,     content = pull_id(content, 'expertises')
    doelg_txt,   content = pull_id(content, 'doelgroep')
    werk_txt,    content = pull_id(content, 'werkwijze')
    cases_txt,   content = pull_id(content, 'cases')
    team_txt,    content = pull_id(content, 'team')
    rev_txt,     content = pull_id(content, 'reviews')
    faq_txt,     content = pull_id(content, 'faq')
    kennis_txt,  content = pull_id(content, 'kennis')
    espana_txt,  content = pull_id(content, 'espana')

    # Lead magnet (geen standaard id)
    lm_txt, content = pull_pattern(content, r'\n(?:<!-- ── LEAD MAGNET.*?-->)?\n*<section class="lead-magnet">.*?</section>')

    # Wat overblijft in content = gerelateerde diensten + eventuele kleine secties
    leftover = content.strip()

    # ── Herbouw CONTENT in CRO-volgorde ─────────────────────────────────────
    parts = [p for p in [
        logos_txt,
        cijfers_txt,
        aanpak_txt,
        exp_txt,
        doelg_txt,
        werk_txt,
        cases_txt,
        new_quote_sec,
        team_txt,
        rev_txt,
        lm_txt,
        faq_txt,
        kennis_txt,
        espana_txt,
        '\n' + leftover if leftover else '',
    ] if p and p.strip()]

    new_src = header + '\n'.join(parts) + '\n' + tail
    write(fpath, new_src)
    print(f'  {fname}: {len(new_src.splitlines())}L')

print('\nKlaar.')
