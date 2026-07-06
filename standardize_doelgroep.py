"""
standardize_doelgroep.py  — uniforme layout voor alle 4 doelgroep-pagina's

Doelstructuur (na CTA):
  [testimonials]  →  compact-dark-lead-magnet  →  FAQ-split (+ aside-card)
  →  team  →  reviews  →  talk-strip…

Aanpak per pagina:
- Deel HTML op bij talk-strip: HEAD (alles t/m reviews) + TAIL
- Herbouw alles tussen einde-CTA en talk-strip
- Gebruiker krijgt testimonials en FAQ erbij; lead-magnet naar compact-dark
"""
import re

ROOT = r'C:/Users/Gebruiker/spring-real-estate-concept'

def read(f):
    with open(ROOT + '/' + f, encoding='utf-8') as fh: return fh.read()
def write(f, s):
    with open(ROOT + '/' + f, 'w', encoding='utf-8') as fh: fh.write(s)
    print(f'  {f}: {len(s.splitlines())}L')

# ── helpers ────────────────────────────────────────────────────────────────────

def extract_section(src, pattern):
    """Geeft de eerste sectie die overeenkomt met pattern (re-patroon op openers)."""
    m = re.search(pattern + r'.*?</section>', src, re.DOTALL)
    return m.group(0).strip() if m else ''

def compact_lm(eyebrow, h2, p, btn, btn_extra=''):
    be = f';{btn_extra}' if btn_extra else ''
    return (
        '<section class="section--tight" id="download"><div class="container">\n'
        '  <div style="background:var(--ink);border-radius:16px;padding:36px 48px;'
        'display:grid;grid-template-columns:1fr auto;align-items:center;gap:40px;flex-wrap:wrap">\n'
        '    <div>\n'
        f'      <span style="display:block;text-transform:uppercase;letter-spacing:.12em;font-size:.75rem;color:var(--green);margin-bottom:.5rem">{eyebrow}</span>\n'
        f'      <h2 style="color:#fff;margin:0 0 .5rem;font-size:clamp(1.2rem,2.2vw,1.6rem);line-height:1.3">{h2}</h2>\n'
        f'      <p style="color:rgba(255,255,255,.6);margin:0;font-size:.94rem">{p}</p>\n'
        '    </div>\n'
        '    <form style="display:flex;flex-direction:column;gap:10px;min-width:220px" onsubmit="return false">\n'
        '      <input type="email" placeholder="Uw e-mailadres" style="padding:11px 15px;border-radius:8px;border:1px solid rgba(255,255,255,.18);background:rgba(255,255,255,.07);color:#fff;font-size:.94rem">\n'
        f'      <button class="btn btn--primary" style="width:100%{be}">{btn}</button>\n'
        '    </form>\n'
        '  </div>\n'
        '</div></section>'
    )

ASIDE = (
    '<div class="aside-card aside-dark">\n'
    '      <h3>Neem contact op</h3>\n'
    '      <p style="color:#bcbeb2;font-size:.94rem">Onze specialisten beantwoorden uw vraag persoonlijk — vrijblijvend.</p>\n'
    '      <a href="contact.html" class="btn btn--primary" style="width:100%;margin-top:8px">Neem contact op</a>\n'
    '      <a href="tel:+31302001020" class="btn btn--ghost" style="width:100%;margin-top:10px;color:#fff;border-color:rgba(255,255,255,.3)">+31 30 200 10 20</a>\n'
    '    </div>'
)

def faq_split(title_em, items):
    items_html = ''.join(items)
    return (
        '<section class="section--tight section--soft" id="faq"><div class="container">\n'
        '  <div class="sec-head"><div class="t">\n'
        '    <span class="eyebrow">Veelgestelde vragen</span>\n'
        f'    <h2 class="disp">Vragen als <em>{title_em}</em></h2>\n'
        '  </div></div>\n'
        '  <div class="split">\n'
        f'    <div class="faq-list">{items_html}</div>\n'
        f'    {ASIDE}\n'
        '  </div>\n'
        '</div></section>'
    )

def fi(q, a, open_=False):
    op = ' open' if open_ else ''
    return (f'<details class="faq-item"{op}><summary><span>{q}</span>'
            f'<span class="pl">+</span></summary><div class="ans">{a}</div></details>')

# ── Content-definitie per pagina ───────────────────────────────────────────────

TESTIMONIALS_GEBRUIKER = (
    '<section class="section--soft"><div class="container">\n'
    '  <div class="sec-head"><div class="t">\n'
    '    <span class="eyebrow">Wat gebruikers zeggen</span>\n'
    '    <h2 class="disp">Gebruikers over <em>Spring</em></h2>\n'
    '  </div></div>\n'
    '  <div class="rev-grid">\n'
    '    <div class="review"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>\n'
    '      <p>"Spring vond binnen drie weken een kantoor dat precies paste bij onze groeiplannen. Zonder Spring hadden we maanden gezocht."</p>\n'
    '      <div class="who"><span class="av">LH</span><span><b>Lisa Hoekstra</b><br><span class="muted">CEO, scale-up · Amsterdam</span></span></div>\n'
    '    </div>\n'
    '    <div class="review"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>\n'
    '      <p>"Ze onderhandelden een huurkorting en drie maanden huurvrij die wij nooit zelf hadden gekregen. Absoluut de moeite waard."</p>\n'
    '      <div class="who"><span class="av">TK</span><span><b>Thomas Kleijn</b><br><span class="muted">CFO, middelgroot bedrijf · Utrecht</span></span></div>\n'
    '    </div>\n'
    '    <div class="review"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>\n'
    '      <p>"Van kantoorzoektocht tot sleuteloverdracht in acht weken — inclusief volledige inrichting via Spring Design &amp; Build."</p>\n'
    '      <div class="who"><span class="av">MB</span><span><b>Marloes B.</b><br><span class="muted">Directeur, adviesbureau · Rotterdam</span></span></div>\n'
    '    </div>\n'
    '  </div>\n'
    '</div></section>'
)

PAGES = {
    'doelgroep-gebruiker.html': {
        'testimonials': TESTIMONIALS_GEBRUIKER,
        'lm': compact_lm(
            'Gratis kantoorzoekgids',
            'Vind uw ideale kantoor — <em>sneller dan u denkt</em>',
            'Van zoekprofiel tot sleuteloverdracht. Inclusief checklist, huurprijsoverzicht en onderhandeltips.',
            'Gids ontvangen'
        ),
        'faq': faq_split('kantoorgebruiker', [
            fi('Hoe lang duurt een gemiddeld kantoorzoektraject?',
               'Gemiddeld 4–12 weken, afhankelijk van uw eisen en de markt. In krappe markten werken we parallel met een off-market zoekstrategie via SpringBase.', True),
            fi('Wat kost de begeleiding als huurder?',
               'In de meeste gevallen is onze dienstverlening voor de huurder kosteloos — Spring wordt door de verhuurder beloond. We zijn hier altijd transparant over.'),
            fi('Kan Spring ook helpen met de inrichting?',
               'Ja. Via Spring Design & Build verzorgen we de volledige kantoorinrichting van concept tot oplevering. Eén aanspreekpunt voor het hele traject.'),
            fi('Werkt Spring ook in Spanje?',
               'Ja. Via onze vestigingen in Valencia en Estepona helpen we Nederlandse bedrijven die ook kantoorruimte in Spanje zoeken.'),
        ]),
    },
    'doelgroep-eigenaar.html': {
        'lm': compact_lm(
            'Gratis verhuurwaarde-analyse',
            'Wat brengt uw pand op? <em>Direct inzicht.</em>',
            'Onderbouwde marktanalyse inclusief huurprijsbenchmark, doelgroepadvies en verhuurstrategie op maat.',
            'Analyse aanvragen'
        ),
        'faq': faq_split('eigenaar', [
            fi('Wat is de waarde van mijn object?',
               'Onze RICS-gecertificeerde taxateurs bepalen een onderbouwde marktwaarde op basis van actuele transactiedata, locatieanalyse en objectkenmerken. U ontvangt een gevalideerd rapport dat direct bruikbaar is voor financiers.', True),
            fi('Hoe lang duurt een verhuurtraject gemiddeld?',
               'In de Amsterdamse kantorenmarkt zijn courante objecten gemiddeld binnen 3–6 maanden verhuurd. Spring werkt actief en direct — wij benaderen potentiële huurders proactief.'),
            fi('Werken jullie ook buiten Nederland?',
               'Ja. Via onze vestigingen in Valencia en Estepona begeleiden we ook verkoop en verhuur van commercieel vastgoed in Spanje. Eén aanspreekpunt voor NL én ES.'),
            fi('Wat kost een taxatie of verhuurtraject?',
               'We werken op maat — tarieven zijn afhankelijk van het type object en de gevraagde dienst. Neem contact op voor een vrijblijvende offerte.'),
        ]),
    },
    'doelgroep-investeerder.html': {
        'lm': compact_lm(
            'Exclusief voor beleggers',
            'Spring Beleggingsscan — <em>gratis en vrijblijvend</em>',
            'Persoonlijke scan met actuele BAR-rendementen, marktkansen en een selectie van passende objecten.',
            'Beleggingsscan ontvangen',
            'background:#F4BD2A;color:#1a1a2e;border-color:#F4BD2A'
        ),
        'faq': faq_split('investeerder', [
            fi('Welke BAR kan ik verwachten in Amsterdam?',
               "In Amsterdam Zuidas liggen prime kantoren op een BAR van 4,5–5,8%. Buiten de A-locaties en in logistiek zijn BAR's van 5,5–7,5% haalbaar. Spring Research voorziet u van actuele benchmarks.", True),
            fi('Helpen jullie ook bij de financiering?',
               'We begeleiden het acquisitietraject volledig inclusief due diligence en taxatierapporten bruikbaar voor financiers. Voor financiering werken we samen met erkende vastgoedfinanciers.'),
            fi('Kunnen jullie de portefeuille na aankoop beheren?',
               'Ja. Via Spring Asset Management en Property Management regelen we het volledige beheer — van huurincasso en onderhoud tot rapportage en ESG-monitoring.'),
            fi('Investeren in Spanje: waar moet ik op letten?',
               'Spanje kent eigen belastingregels, due-diligence-processen en ruimtelijke ordening. Onze teams in Valencia en Estepona begeleiden u van zoektocht tot notariële overdracht.'),
        ]),
    },
    'doelgroep-ontwikkelaar.html': {
        'lm': compact_lm(
            'Gratis projectscan',
            'Is uw locatie verhuurbaar? <em>Wij analyseren het gratis.</em>',
            'Doelgroepanalyse, concurrentiescan en pre-let strategie-advies voor uw ontwikkellocatie.',
            'Projectscan aanvragen'
        ),
        'faq': faq_split('ontwikkelaar', [
            fi('Kunnen jullie al vroeg in het traject adviseren?',
               'Absoluut. Wij adviseren het liefst vanaf de haalbaarheidsfase — zo sturen we op de juiste mix van functies, huurprijzen en afzetbaarheid. Vroeg instappen bespaart u tijd en geld.', True),
            fi('Doen jullie verhuuradvies voor nieuwbouwprojecten?',
               'Ja. Via Spring Agency verzorgen we de verhuurbegeleiding van nieuwbouw en transformatieprojecten — van strategie en marketing tot huurdersakkoord.'),
            fi('Hoe snel kunnen jullie een haalbaarheidsrapport opleveren?',
               "Een first-look haalbaarheidsanalyse leveren wij doorgaans binnen twee weken. Een uitgebreid rapport met marktanalyse en financiële scenario's volgt binnen vier tot zes weken."),
            fi('Zijn jullie ook actief bij projecten in Spanje?',
               'Ja. Via onze Spaanse vestigingen begeleiden we ontwikkelaars bij locatieanalyse, vergunningtrajecten en verkoopstrategie in Valencia en op de Costa del Sol.'),
        ]),
    },
}

# ── Verwerk elke pagina ────────────────────────────────────────────────────────

for fname, cfg in PAGES.items():
    src = read(fname)

    # Splits bij talk-strip (alles erna bewaren we ongewijzigd)
    ts_idx = src.find('\n<section class="talk-strip">')
    if ts_idx == -1:
        print(f'  FOUT: talk-strip niet gevonden in {fname}'); continue
    tail  = src[ts_idx:]       # talk-strip + footer + scripts
    front = src[:ts_idx]       # alles ervóór

    # Extraheer bestaande team-sectie
    team_m = re.search(r'\n<section class="section dark-sec" id="team">.*?</section>', front, re.DOTALL)
    team = team_m.group(0) if team_m else ''

    # Extraheer bestaande reviews-sectie
    rev_m = re.search(r'\n<section class="section" id="reviews"[^>]*>.*?</section>', front, re.DOTALL)
    reviews = rev_m.group(0) if rev_m else ''

    # Snij front af bij het einde van de CTA-sectie
    # CTA is de section--tight met class="cta" erin
    cta_m = re.search(
        r'<section class="section--tight"><div class="container"><div class="cta">.*?</section>',
        front, re.DOTALL
    )
    if cta_m:
        front = front[:cta_m.end()]
    else:
        # Fallback: snij af vóór team of vóór de eerste "testimonials"
        print(f'  WAARSCHUWING: CTA niet gevonden in {fname}, probeer fallback')
        idx = team_m.start() if team_m else ts_idx
        front = front[:idx]

    # Bepaal testimonials-blok
    testimonials = cfg.get('testimonials', '')
    if not testimonials:
        # Voor eigenaar/investeerder/ontwikkelaar: sectie--soft ZONDER faq-list direct na CTA
        after_cta = src[cta_m.end():ts_idx] if cta_m else ''
        t_m = re.search(r'\n<section class="section--soft"><div class="container">\s*<div class="sec-head">.*?</div>\s*<div class="rev-grid">.*?</section>', after_cta, re.DOTALL)
        if t_m:
            testimonials = t_m.group(0)

    # Herbouw het lichaam
    new_body = (
        front.rstrip() + '\n\n' +
        (testimonials.strip() + '\n\n' if testimonials else '') +
        cfg['lm'].strip() + '\n' +
        cfg['faq'].strip() + '\n' +
        team + '\n' +
        reviews
    )

    write(fname, new_body + tail)

print('\nKlaar.')
