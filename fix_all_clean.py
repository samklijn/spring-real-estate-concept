"""
fix_all_clean.py
=================
Herstelt alle HTML bestanden in één pass:

1. Fix mojibake (UTF-8 bytes die als CP1252 zijn ingelezen):
   Methode: lees als UTF-8, match aaneengesloten CP1252-bereik chars,
   encode terug naar CP1252 bytes, decode als UTF-8.

2. Pas talk-strip (Sam Klijn balk) toe vóór elke <footer> als nog niet aanwezig.

3. Verwijder grote CTA en talk-band secties.

4. Listings-specifieke wijzigingen:
   - Vervang groene zoekbalk door eenvoudige object-finder balk
   - Verwijder oude zoekform uit page-hero
   - Grijze locatiekaart (niet groen)

5. Homepage: grijze locatiekaart.

6. CSS versie -> v=22 (uitsluitend via Python, nooit PowerShell).

NOOIT PowerShell gebruiken voor HTML encoding!
"""
import os, glob, re

REPO = os.path.dirname(os.path.abspath(__file__))
VERSION = '22'

# ── 1. Mojibake-fix ─────────────────────────────────────────────────────────

# CP1252 speciale tekens boven U+00FF die in mojibake zitten
CP1252_EXTRAS = {
    '€', '‚', 'ƒ', '„', '…', '†', '‡',
    'ˆ', '‰', 'Š', '‹', 'Œ', 'Ž', '‘',
    '’', '“', '”', '•', '–', '—', '˜',
    '™', 'š', '›', 'œ', 'ž', 'Ÿ',
}

def is_cp1252_char(c):
    return '\x80' <= c <= '\xff' or c in CP1252_EXTRAS

def fix_mojibake(text):
    """Match aaneengesloten sequences van CP1252-bereik chars, decode ze correct."""
    result = []
    i = 0
    while i < len(text):
        if is_cp1252_char(text[i]):
            j = i + 1
            while j < len(text) and is_cp1252_char(text[j]):
                j += 1
            fragment = text[i:j]
            try:
                decoded = fragment.encode('cp1252').decode('utf-8')
                result.append(decoded)
            except (UnicodeEncodeError, UnicodeDecodeError):
                result.append(fragment)
            i = j
        else:
            result.append(text[i])
            i += 1
    return ''.join(result)

# ── 2. Talk-strip HTML ───────────────────────────────────────────────────────

TALK_STRIP = (
    '<section class="talk-strip"><div class="container">\n'
    '  <div class="talk-strip-inner">\n'
    '    <img src="images/team/sam.klijn.jpg" alt="Sam Klijn" class="ts-avatar">\n'
    '    <div class="ts-info">\n'
    '      <strong>Sam Klijn</strong>\n'
    '      <span>Partner Marketing &middot; Spring Real Estate</span>\n'
    '    </div>\n'
    '    <div class="ts-actions">\n'
    '      <a href="tel:+31302001020" class="ts-btn ts-btn--call">\n'
    '        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.4-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>\n'
    '        +31 30 200 10 20\n'
    '      </a>\n'
    '      <a href="https://wa.me/31302001020?text=Hoi%20Sam,%20ik%20heb%20een%20vraag" target="_blank" rel="noopener" class="ts-btn ts-btn--wa">\n'
    '        <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M.06 24l1.7-6.2A11.9 11.9 0 1 1 12 24a11.9 11.9 0 0 1-5.7-1.45L.06 24zM6.6 20.1l.37.22a9.9 9.9 0 0 0 5.05 1.38h.004a9.9 9.9 0 1 0-8.4-4.6l.24.38-1 3.67 3.74-.98zM17.5 14.3c-.15-.25-.55-.4-1.15-.7s-1.77-.87-2.04-.97-.47-.15-.67.15-.77.97-.94 1.17-.35.22-.65.07a8.13 8.13 0 0 1-2.4-1.48 9 9 0 0 1-1.66-2.06c-.17-.3 0-.46.13-.6s.3-.35.45-.52a2 2 0 0 0 .3-.5.55.55 0 0 0 0-.52c-.07-.15-.67-1.62-.92-2.22s-.5-.5-.67-.5h-.57a1.1 1.1 0 0 0-.8.37 3.35 3.35 0 0 0-1.04 2.5 5.8 5.8 0 0 0 1.22 3.08 13.3 13.3 0 0 0 5.1 4.5c.7.3 1.27.49 1.7.63a4.1 4.1 0 0 0 1.88.12c.57-.09 1.77-.72 2.02-1.42s.25-1.3.17-1.42z"/></svg>\n'
    '        WhatsApp\n'
    '      </a>\n'
    '      <a href="contact.html" class="ts-btn ts-btn--ghost">Plan gesprek</a>\n'
    '    </div>\n'
    '  </div>\n'
    '</div></section>\n'
)

# ── 3. Object-finder balk (listings.html) ────────────────────────────────────

OBJ_FINDER_BAR = (
    '<!-- ============ OBJECT FINDER BALK ============ -->\n'
    '<div class="obj-finder-bar">\n'
    '  <div class="container obj-finder-inner">\n'
    '    <div class="ofb-left">\n'
    '      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg>\n'
    '      <span><strong>Vind uw real estate object</strong> &mdash; 16 objecten in Utrecht, Amsterdam &amp; Valencia</span>\n'
    '    </div>\n'
    '    <div class="ofb-tags">\n'
    '      <span class="ofb-tag">Kantoorruimte</span>\n'
    '      <span class="ofb-tag">Bedrijfsruimte</span>\n'
    '      <span class="ofb-tag">Belegging</span>\n'
    '    </div>\n'
    '  </div>\n'
    '</div>\n'
)

# ── 4. Kaart: groen -> grijs ─────────────────────────────────────────────────

MAP_COLOR_FIXES = [
    ('rgba(124,167,63,.07)', 'rgba(100,100,100,.06)'),
    ('rgba(124,167,63,.1)',  'rgba(100,100,100,.09)'),
    ('rgba(124,167,63,.12)', 'rgba(100,100,100,.09)'),
    ('rgba(124,167,63,.22)', 'rgba(100,100,100,.18)'),
    ('rgba(124,167,63,.25)', 'rgba(100,100,100,.18)'),
    ('rgba(124,167,63,.3)',  'rgba(100,100,100,.22)'),
    ('rgba(124,167,63,.35)', 'rgba(100,100,100,.28)'),
    ('fill="#7CA73F"',       'fill="#888"'),
    ('fill="#89B647"',       'fill="#aaa"'),
]

# ── Hoofd-verwerking ─────────────────────────────────────────────────────────

def process(path):
    fname = os.path.basename(path)

    with open(path, 'rb') as f:
        raw = f.read()
    if raw.startswith(b'\xef\xbb\xbf'):
        raw = raw[3:]  # strip BOM

    text = raw.decode('utf-8', errors='replace')

    # 1. Mojibake fix
    text = fix_mojibake(text)

    # 2. Talk-strip vóór footer (als nog niet aanwezig)
    if 'talk-strip' not in text and '<footer class="footer">' in text:
        text = text.replace('<footer class="footer">', TALK_STRIP + '<footer class="footer">', 1)

    # 3. Verwijder grote talk-band
    text = re.sub(r'<section class="section talk-band">.*?</section>', '', text, flags=re.DOTALL)

    # 4. Verwijder grote CTA sectie (id="contact" met div.cta)
    text = re.sub(
        r'<section[^>]*id="contact"[^>]*>\s*<div class="container">\s*<div class="cta">.*?</div></div></section>',
        '', text, flags=re.DOTALL
    )
    # Ook de homepage CTA zonder id
    text = re.sub(
        r'<!-- ={8,} CTA ={8,} -->\s*<section class="section--tight">\s*<div class="container">\s*<div class="cta">.*?</div>\s*</div>\s*</section>',
        '', text, flags=re.DOTALL
    )

    # 5. Listings-specifiek
    if fname == 'listings.html':
        # Verwijder oude zoekform uit page-hero
        text = re.sub(r'<form class="search search--light[^"]*"[^>]*>.*?</form>', '', text, flags=re.DOTALL)

        # Vervang groene lhs zoekbalk door object-finder balk
        text = re.sub(
            r'<!-- ={8,} GROENE ZOEKBALK ={8,} -->.*?</div>\n',
            OBJ_FINDER_BAR,
            text, flags=re.DOTALL, count=1
        )
        # Als er geen groene balk was, voeg finder balk toe vóór locatiekaart
        if 'obj-finder-bar' not in text and '<!-- ============ LOCATIEKAART ============ -->' in text:
            text = text.replace(
                '<!-- ============ LOCATIEKAART ============ -->',
                OBJ_FINDER_BAR + '\n<!-- ============ LOCATIEKAART ============ -->'
            )

        # Grijze kaart in listings
        for bad, good in MAP_COLOR_FIXES:
            text = text.replace(bad, good)

    # 6. Homepage: grijze kaart
    if fname == 'index.html':
        for bad, good in MAP_COLOR_FIXES:
            text = text.replace(bad, good)

    # 7. CSS/JS versie bumpen
    text = re.sub(r'\?v=\d+', f'?v={VERSION}', text)

    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)

html_files = glob.glob(os.path.join(REPO, '*.html'))
print(f'Verwerken {len(html_files)} bestanden...')
for path in sorted(html_files):
    process(path)

# Controleer het resultaat
with open(os.path.join(REPO, 'listings.html'), encoding='utf-8') as f:
    sample = f.read()

idx = sample.find('Partner Marketing')
print('\n--- Controle ---')
print('Partner Marketing:', repr(sample[idx:idx+35]))
idx2 = sample.find('kwartaal')
print('Scarcity notice: ', repr(sample[idx2:idx2+55]))
idx3 = sample.find('Vind uw real estate')
print('Finder balk:     ', repr(sample[idx3:idx3+50]) if idx3>=0 else 'NIET GEVONDEN')

# Tel resterende mojibake
bad_count = len(re.findall(r'[\xc0-\xff][\x80-\xbf]', sample.encode('latin-1', errors='replace').decode('latin-1')))
print(f'Resterende latin-1 sequences: {bad_count}')

print('\nKlaar. Gebruik NOOIT PowerShell voor HTML bestanden!')
