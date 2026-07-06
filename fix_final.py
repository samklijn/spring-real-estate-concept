import re

def read(f):
    with open(f, encoding='utf-8') as fh: return fh.read()
def write(f, s):
    with open(f, 'w', encoding='utf-8') as fh: fh.write(s)

# ── 1. cases.html ────────────────────────────────────────────────────────────
print('cases.html')
src = read('cases.html')

# Merge quote into aanpak prose, remove resultaten section
OLD_AANPAK = '''        <a href="contact.html" class="btn btn--primary">Bespreek uw vraagstuk</a>
      </div>'''
NEW_AANPAK = '''        <blockquote style="border-left:3px solid var(--green);padding:.5rem 0 .5rem 1rem;margin:1.2rem 0;font-style:italic;color:var(--ink)">“Wij meten succes niet in deals, maar in de waarde die we toevoegen voor elke klant — bij elk project opnieuw.”<br><strong style="font-style:normal;font-size:.88rem;color:var(--green)">Ivar Hillerstrom — Managing Director</strong></blockquote>
        <a href="contact.html" class="btn btn--primary">Bespreek uw vraagstuk</a>
      </div>'''
src = src.replace(OLD_AANPAK, NEW_AANPAK, 1)

# Remove standalone resultaten section
src = re.sub(r'\n<section[^>]+id="resultaten"[^>]*>.*?</section>', '', src, count=1, flags=re.DOTALL)

# Uniform case-img sizing
src = src.replace('<div class="case-img"><img ', '<div class="case-img" style="aspect-ratio:4/3;overflow:hidden"><img style="width:100%;height:100%;object-fit:cover" ', )

write('cases.html', src)
print('  OK')

# ── 2. vacatures.html ────────────────────────────────────────────────────────
print('vacatures.html')
src = read('vacatures.html')

# Add missing </section> after usp-grid container
src = src.replace(
    '  </div>\n</div>\n\n<section class="section--tight section--tint">',
    '  </div>\n</div></section>\n\n<section class="section--tight section--tint">',
    1
)

write('vacatures.html', src)
print('  OK')

# ── 3. Locatie pages: remove FAQ link from toc, add BU FAQ ──────────────────

def bu_faq(ey, h2, items_html, aside='Nog een vraag?'):
    return (
        '\n<section class="section--tight section--soft" id="faq"><div class="container">\n'
        '  <div class="sec-head"><div class="t">\n'
        '    <span class="eyebrow">' + ey + '</span>\n'
        '    <h2 class="disp">' + h2 + '</h2>\n'
        '  </div></div>\n'
        '  <div class="split">\n'
        '    <div class="faq-list">' + items_html + '</div>\n'
        '    <div class="aside-card aside-dark">\n'
        '      <h3>' + aside + '</h3>\n'
        '      <p style="color:#bcbeb2;font-size:.94rem">Onze specialisten beantwoorden uw vraag persoonlijk.</p>\n'
        '      <a href="contact.html" class="btn btn--primary" style="width:100%;margin-top:8px">Neem contact op</a>\n'
        '      <a href="tel:+31302001020" class="btn btn--ghost" style="width:100%;margin-top:10px;color:#fff;border-color:rgba(255,255,255,.3)">+31 30 200 10 20</a>\n'
        '    </div>\n'
        '  </div>\n'
        '</div></section>'
    )

def faq_item(q, a, open_=False):
    op = ' open' if open_ else ''
    return ('\n      <details class="faq-item"' + op + '><summary><span>' + q + '</span><span class="pl">+</span></summary>'
            '<div class="ans">' + a + '</div></details>')

LOCATIES = {
    'locatie-amsterdam.html': {
        'ey': 'Veelgestelde vragen',
        'h2': 'Vragen over <em>Amsterdam</em>',
        'aside': 'Vraag stellen?',
        'items': [
            ('Wat zijn de huurprijzen op de Zuidas?',
             'Prime huurprijzen op de Zuidas liggen in 2026 tussen €450 en €510 per m² per jaar voor A-grade kantoorruimte. Spring Research houdt deze data continu bij.',
             True),
            ('Hoe snel vind ik een huurder voor mijn Amsterdams pand?',
             'Afhankelijk van locatie en kwaliteit realiseren wij gemiddeld verhuur binnen 8 weken via ons directe netwerk van huurders en gebruikers.'),
            ('Heeft Spring ook aanbod buiten de Zuidas?',
             'Ja — wij hebben aanbod in alle deelgebieden van Amsterdam: Centrum, West, Oost, Noord en het Havengebied. Neem contact op voor actueel aanbod.'),
            ('Begeleidt Spring ook vastgoedbeleggingen in Amsterdam?',
             'Zeker. Onze investment-afdeling adviseert bij aan- en verkoop van beleggingspanden in Amsterdam, inclusief waarderingsadvies en due diligence.'),
        ]
    },
    'locatie-utrecht.html': {
        'ey': 'Veelgestelde vragen',
        'h2': 'Vragen over <em>Utrecht</em>',
        'aside': 'Vraag stellen?',
        'items': [
            ('Wat kost kantoorruimte in het Stationsgebied Utrecht?',
             'Kantoorruimte in het Stationsgebied Utrecht varieert in 2026 van €260 tot €320 per m² per jaar, afhankelijk van kwaliteit en verdieping.',
             True),
            ('Is er aanbod in Leidsche Rijn of Papendorp?',
             'Ja, Spring is actief in alle kantoorclusters rondom Utrecht, waaronder Leidsche Rijn Centrum, Papendorp en het Stationsgebied. Vraag naar actueel beschikbaar aanbod.'),
            ('Helpt Spring ook bij verhuur buiten de Randstad?',
             'Onze expertise ligt primair in Utrecht, Amsterdam en de Randstad. Voor locaties buiten deze regio’s schakelen we ons netwerk in.'),
            ('Kan ik ook een bedrijfspand kopen via Spring in Utrecht?',
             'Ja — Spring begeleidt zowel huurders als kopers van commercieel vastgoed in Utrecht. Onze investment-specialisten adviseren bij aan- en verkoop.'),
        ]
    },
    'locatie-valencia.html': {
        'ey': 'Veelgestelde vragen',
        'h2': 'Vragen over <em>Valencia</em>',
        'aside': 'Vraag stellen?',
        'items': [
            ('Wat zijn de rendementen op vastgoed in Valencia?',
             'Commercieel vastgoed in Valencia levert in 2026 doorgaans een bruto aanvangsrendement (BAR) van 5,5–7,5%, afhankelijk van locatie en type object.',
             True),
            ('Is Valencia interessant voor Nederlandse investeerders?',
             'Ja — Valencia biedt aantrekkelijke instapprijzen, groeiende vraag en een stabiel huurklimaat. Spring Spain begeleidt Nederlandse investeerders van A tot Z.'),
            ('Hoe werkt het aankoopproces in Spanje?',
             'Het aankoopproces in Spanje verloopt via een Nota Simple (eigendomsoverzicht), koopcompromis en notarieel transport. Spring Spain begeleidt elk stap.'),
            ('Zijn er belastingvoordelen voor investeerders in Spanje?',
             'Spanje kent gunstige belastingverdragen met Nederland. Spring works samen met lokale fiscalisten om uw structuur optimaal in te richten.'),
        ]
    },
    'locatie-estepona.html': {
        'ey': 'Veelgestelde vragen',
        'h2': 'Vragen over <em>Estepona</em>',
        'aside': 'Vraag stellen?',
        'items': [
            ('Wat maakt Estepona interessant voor vastgoedinvesteerders?',
             'Estepona is een van de snelstgroeiende kustgemeenten aan de Costa del Sol, met toenemende vraag naar residentieel en commercieel vastgoed en solide prijsgroei.',
             True),
            ('Welk rendement kan ik verwachten op een vakantiewoning in Estepona?',
             'Toeristisch verhuur in Estepona levert doorgaans 5–8% bruto rendement, afhankelijk van bezettingsgraad en object. Spring Spain adviseert op basis van actuele marktdata.'),
            ('Begeleidt Spring ook de aankoop van grond in Estepona?',
             'Ja, Spring Spain heeft ervaring met projectontwikkeling en grondverwerving aan de Costa del Sol. Wij zorgen voor lokale due diligence en juridische begeleiding.'),
            ('Hoe lang duurt het aankoopproces in Spanje gemiddeld?',
             'Gemiddeld 6–10 weken van eerste bezichtiging tot notariële overdracht, mits financiering en documentatie op orde zijn.'),
        ]
    },
}

for fname, cfg in LOCATIES.items():
    print(fname)
    src = read(fname)

    # Remove <a href="#faq">FAQ</a> from bu-toc
    src = re.sub(r'\s*<a href="#faq">FAQ</a>', '', src)

    # Build FAQ html
    items_html = ''.join(faq_item(q, a, *([True] if i == 0 else [])) for i, (q, a, *_) in enumerate(cfg['items']))
    faq_block = bu_faq(cfg['ey'], cfg['h2'], items_html + '\n    ', cfg['aside'])

    # Insert FAQ before the download section
    dl_pat = re.compile(r'\n<section class="section--tight" id="download">')
    m = dl_pat.search(src)
    if m:
        src = src[:m.start()] + faq_block + src[m.start():]
        print('  FAQ inserted before download')
    else:
        print('  WARNING: download section not found')

    write(fname, src)
    print('  OK')

print('\nKlaar.')
