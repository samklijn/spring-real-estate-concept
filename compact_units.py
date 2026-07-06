"""
compact_units.py — maak unit pages visueel compacter zonder content te verwijderen:
1. Sector-grid sectie + quote-panel sectie → samenvoegen in één compacte sectie
2. Reviews: section → section section--tight (minder whitespace)
3. Werkwijze: section--soft → section--tight section--soft
4. FAQ: section--soft → section--tight section--soft
5. Kennis: section--tight blijft, maar cert-row + blog-grid inline compacter
"""

import re, os

ROOT = r'C:/Users/Gebruiker/spring-real-estate-concept'
UNIT_FILES = sorted(f for f in os.listdir(ROOT) if f.startswith('unit-') and f.endswith('.html'))

def compact(src):
    changed = []

    # 1. Tighter reviews padding
    old = '<section class="section" id="reviews" style="background:var(--green-tint)">'
    new = '<section class="section section--tight" id="reviews" style="background:var(--green-tint)">'
    if old in src:
        src = src.replace(old, new)
        changed.append('reviews tight')

    # 2. Werkwijze tighter
    old = '<section class="section--soft" id="werkwijze">'
    new = '<section class="section--tight section--soft" id="werkwijze">'
    if old in src:
        src = src.replace(old, new)
        changed.append('werkwijze tight')

    # 3. FAQ tighter
    old = '<section class="section--soft" id="faq">'
    new = '<section class="section--tight section--soft" id="faq">'
    if old in src:
        src = src.replace(old, new)
        changed.append('faq tight')

    # 4. Merge sector-grid + quote-panel into one compact two-col section
    # Pattern: <section class="section--tight"><div class="container">
    #   <div class="sec-head">...<span class="eyebrow">Sectoren...
    #   <div class="sector-grid">...</div>
    # </div></section>
    # <section class="section--tight"><div class="container">
    #   <div class="panel" ...>quote</div>
    # </div></section>
    sector_pat = re.compile(
        r'(<section class="section--tight"><div class="container">\s*'
        r'<div class="sec-head">.*?Sectoren.*?</div>\s*'
        r'<div class="sector-grid">.*?</div>\s*'
        r'</div></section>)\s*'
        r'(<section class="section--tight"><div class="container">\s*'
        r'<div class="panel"[^>]*>.*?</div>\s*'
        r'</div></section>)',
        re.DOTALL
    )
    def merge_sector_quote(m):
        sector_block = m.group(1)
        quote_block = m.group(2)
        # Extract sector-grid inner HTML
        sector_inner = re.search(
            r'(<div class="sec-head">.*?</div>\s*<div class="sector-grid">.*?</div>)',
            sector_block, re.DOTALL)
        # Extract quote inner HTML
        quote_inner = re.search(r'<div class="panel"[^>]*>(.*?)</div>', quote_block, re.DOTALL)
        if not sector_inner or not quote_inner:
            return m.group(0)
        return (
            '\n<section class="section--tight"><div class="container">'
            '<div class="two-col two-col--60-40" style="align-items:center;gap:40px">'
            '<div>' + sector_inner.group(1) + '</div>'
            '<div class="panel" style="background:var(--green-tint);border-radius:12px;padding:28px 32px">'
            + quote_inner.group(1) +
            '</div>'
            '</div>'
            '</div></section>'
        )
    new_src, n = sector_pat.subn(merge_sector_quote, src)
    if n:
        src = new_src
        changed.append('sector+quote merged')

    return src, changed

total = 0
for fname in UNIT_FILES:
    path = os.path.join(ROOT, fname)
    with open(path, encoding='utf-8') as f:
        src = f.read()
    new_src, changes = compact(src)
    if changes:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_src)
        print(f'  {fname}: {len(new_src.splitlines())}L — {", ".join(changes)}')
        total += 1
    else:
        print(f'  {fname}: geen wijzigingen')

print(f'\nUnit pages aangepast: {total}/{len(UNIT_FILES)}')
