#!/usr/bin/env python3
# rebuild_7pages.py — Spring Real Estate HTML rebuilder
# Rebuilds 7 HTML pages using extract_parts + shared components.

import os

ROOT = "C:/Users/Gebruiker/spring-real-estate-concept"

# ── Helper ────────────────────────────────────────────────────────────────────

def extract_parts(src):
    hero_start = src.index('<section class="page-hero"')
    after_hero = src[hero_start:]
    end = after_hero.index('</section>') + len('</section>')
    header = src[:hero_start + end].rstrip('\n') + '\n'
    footer = src[src.index('\n<section class="talk-strip">'):]
    return header, footer

# ── Shared components ─────────────────────────────────────────────────────────

LOGOS_BAND = '''
<section class="section section--tight" style="background:#F8F8F8;border-bottom:1px solid #E8E8E8">
  <div class="container">
    <p style="text-align:center;font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;color:#999;margin-bottom:18px">Vertrouwd door toonaangevende vastgoedpartijen</p>
    <div class="logo-band">
      <span>MERIN</span><span>a.s.r.</span><span>BPD</span><span>Vesteda</span><span>Heimstaden</span><span>Bouwinvest</span>
    </div>
  </div>
</section>'''

REVIEWS_SECTION = '''
<section class="section section--soft" id="reviews" style="background:var(--green-tint)">
  <div class="container">
    <div class="sec-head"><span class="eyebrow">Wat klanten zeggen</span><h2>Beoordelingen</h2></div>
    <div class="rev-grid">
      <div class="rev-card"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>"Spring dacht echt mee en leverde sneller resultaat dan verwacht."</p><strong>Jeroen V.</strong><span>Scale-ups</span></div>
      <div class="rev-card"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>"Transparant, deskundig en datagedreven advies. Altijd bereikbaar."</p><strong>Marit K.</strong><span>Corporate vastgoed</span></div>
      <div class="rev-card"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>"Een betrouwbare partner voor elk vastgoedvraagstuk."</p><strong>Rafael G.</strong><span>Investeerder</span></div>
    </div>
  </div>
</section>'''


def LEAD_MAGNET(eyebrow, h2, p, btn_text):
    return (
        '\n<section class="lead-magnet">\n'
        '  <div class="container">\n'
        '    <div class="lm-inner">\n'
        '      <div class="lm-text">\n'
        '        <span class="eyebrow">' + eyebrow + '</span>\n'
        '        <h2>' + h2 + '</h2>\n'
        '        <p>' + p + '</p>\n'
        '      </div>\n'
        '      <div class="lm-form">\n'
        '        <form>\n'
        '          <input type="email" placeholder="Uw e-mailadres" required>\n'
        '          <button type="submit" class="btn btn--primary btn--lg">' + btn_text + '</button>\n'
        '        </form>\n'
        '      </div>\n'
        '    </div>\n'
        '  </div>\n'
        '</section>'
    )


def CTA(h2, p):
    return (
        '\n<section class="section section--tight">\n'
        '  <div class="container">\n'
        '    <div class="cta">\n'
        '      <h2>' + h2 + '</h2>\n'
        '      <p>' + p + '</p>\n'
        '      <div class="cta-btns">\n'
        '        <a href="contact.html" class="btn btn--light btn--lg">Neem contact op</a>\n'
        '        <a href="listings.html" class="btn" style="background:rgba(255,255,255,.12);color:#fff;border:1px solid rgba(255,255,255,.3)">Bekijk aanbod</a>\n'
        '      </div>\n'
        '    </div>\n'
        '  </div>\n'
        '</section>'
    )


def FAQ_SECTION(title, faq_items):
    details_html = ''
    for q, a in faq_items:
        details_html += '        <details><summary>' + q + '</summary><p>' + a + '</p></details>\n'
    return (
        '\n<section class="section section--soft" id="faq">\n'
        '  <div class="container">\n'
        '    <div class="sec-head"><span class="eyebrow">Veelgestelde vragen</span><h2>FAQ <em>' + title + '</em></h2></div>\n'
        '    <div class="split">\n'
        '      <div class="faq-list">\n'
        + details_html +
        '      </div>\n'
        '      <aside class="aside-card aside-dark">\n'
        '        <h3>Nog een vraag?</h3>\n'
        '        <p>Onze adviseurs beantwoorden uw vraag persoonlijk.</p>\n'
        '        <a href="contact.html" class="btn btn--primary">Stel uw vraag</a>\n'
        '        <a href="tel:+31302272270" class="btn btn--ghost" style="margin-top:10px">+31 30 227 22 70</a>\n'
        '      </aside>\n'
        '    </div>\n'
        '  </div>\n'
        '</section>'
    )


def AGENT_CARD(photo, name, role, email):
    return (
        '  <div class="agent">\n'
        '    <div class="ph"><img src="img/' + photo + '" alt="' + name + '" loading="lazy"></div>\n'
        '    <div class="body">\n'
        '      <strong>' + name + '</strong>\n'
        '      <span>' + role + '</span>\n'
        '      <div class="socials">\n'
        '        <a href="https://linkedin.com/in/spring" aria-label="LinkedIn">in</a>\n'
        '        <a href="mailto:' + email + '" aria-label="E-mail">&#x2709;</a>\n'
        '      </div>\n'
        '    </div>\n'
        '  </div>\n'
    )


def TEAM_SECTION(agents_html, anchor='team'):
    return (
        '\n<section class="section dark-sec" id="' + anchor + '">\n'
        '  <div class="container">\n'
        '    <div class="sec-head">\n'
        '      <span class="eyebrow" style="color:var(--green-soft,#9DC76B)">Het team</span>\n'
        '      <h2 style="color:#fff">Uw <em>experts</em></h2>\n'
        '      <a href="agents.html" class="btn btn--secondary">Heel het team</a>\n'
        '    </div>\n'
        '    <div class="team-grid">' + agents_html + '</div>\n'
        '  </div>\n'
        '</section>'
    )


def STATS_GREEN(stats_list):
    n = len(stats_list)
    cells = ''
    for i, (num, lbl) in enumerate(stats_list):
        border = '' if i == n - 1 else 'border-right:1px solid #C5DFA0;'
        cells += (
            '      <div class="stat-cell" style="padding:24px 0;' + border + '">'
            '<b style="display:block;font-size:2rem;font-weight:800;color:var(--ink)">' + num + '</b>'
            '<small style="color:#555">' + lbl + '</small></div>\n'
        )
    return (
        '\n<section class="section section--tight" style="background:#EBF4D6;border-bottom:1px solid #C5DFA0">\n'
        '  <div class="container">\n'
        '    <div class="stats-band" style="display:grid;grid-template-columns:repeat(' + str(n) + ',1fr);text-align:center">\n'
        + cells +
        '    </div>\n'
        '  </div>\n'
        '</section>'
    )


def STATS_DARK(eyebrow, h2, stats_list):
    n = len(stats_list)
    cells = ''
    for i, (num, lbl) in enumerate(stats_list):
        border = '' if i == n - 1 else 'border-right:1px solid rgba(255,255,255,.12);'
        cells += (
            '      <div style="padding:32px 0;' + border + '">'
            '<b style="display:block;font-size:2.2rem;font-weight:800;color:#fff">' + num + '</b>'
            '<span style="color:rgba(255,255,255,.65);font-size:.9rem">' + lbl + '</span></div>\n'
        )
    return (
        '\n<section class="section dark-sec" id="cijfers">\n'
        '  <div class="container">\n'
        '    <div class="sec-head">\n'
        '      <span class="eyebrow" style="color:var(--green-soft,#9DC76B)">' + eyebrow + '</span>\n'
        '      <h2 style="color:#fff">' + h2 + '</h2>\n'
        '    </div>\n'
        '    <div class="stats-band" style="display:grid;grid-template-columns:repeat(' + str(n) + ',1fr);text-align:center;border:1px solid rgba(255,255,255,.12);border-radius:12px">\n'
        + cells +
        '    </div>\n'
        '  </div>\n'
        '</section>'
    )


def WERKWIJZE(steps):
    steps_html = ''
    for i, (title, desc) in enumerate(steps, 1):
        steps_html += (
            '      <div class="bu-step">\n'
            '        <div class="n">' + str(i) + '</div>\n'
            '        <h3>' + title + '</h3>\n'
            '        <p>' + desc + '</p>\n'
            '      </div>\n'
        )
    return (
        '\n<section class="section section--soft" id="werkwijze">\n'
        '  <div class="container">\n'
        '    <div class="sec-head"><span class="eyebrow">Onze werkwijze</span><h2>Zo werken <em>wij</em></h2></div>\n'
        '    <div class="bu-steps">\n'
        + steps_html +
        '    </div>\n'
        '  </div>\n'
        '</section>'
    )


def BUTOC(*links):
    anchors = ''
    for anchor, label in links:
        anchors += '    <a href="#' + anchor + '">' + label + '</a>\n'
    return (
        '\n<nav class="bu-toc">\n'
        '  <div class="container">\n'
        + anchors +
        '  </div>\n'
        '</nav>'
    )


def LOC_MAP(bg_color, stroke, pin_color, city_name):
    return (
        '<div class="loc-map">\n'
        '  <svg viewBox="0 0 320 220" xmlns="http://www.w3.org/2000/svg">\n'
        '    <rect width="320" height="220" rx="12" fill="' + bg_color + '"/>\n'
        '    <line x1="0" y1="55" x2="320" y2="55" stroke="' + stroke + '" stroke-width="1" opacity=".4"/>\n'
        '    <line x1="0" y1="110" x2="320" y2="110" stroke="' + stroke + '" stroke-width="1" opacity=".4"/>\n'
        '    <line x1="0" y1="165" x2="320" y2="165" stroke="' + stroke + '" stroke-width="1" opacity=".4"/>\n'
        '    <line x1="80" y1="0" x2="80" y2="220" stroke="' + stroke + '" stroke-width="1" opacity=".4"/>\n'
        '    <line x1="160" y1="0" x2="160" y2="220" stroke="' + stroke + '" stroke-width="1" opacity=".4"/>\n'
        '    <line x1="240" y1="0" x2="240" y2="220" stroke="' + stroke + '" stroke-width="1" opacity=".4"/>\n'
        '    <path d="M0,110 Q80,90 160,110 Q240,130 320,110" stroke="' + stroke + '" stroke-width="3" fill="none" opacity=".6"/>\n'
        '    <path d="M160,0 Q140,110 160,220" stroke="' + stroke + '" stroke-width="3" fill="none" opacity=".6"/>\n'
        '    <circle cx="160" cy="100" r="14" fill="' + pin_color + '" opacity=".9"/>\n'
        '    <circle cx="160" cy="100" r="6" fill="#fff"/>\n'
        '    <text x="180" y="105" font-size="13" font-weight="700" fill="' + stroke + '">' + city_name + '</text>\n'
        '  </svg>\n'
        '</div>'
    )


def PROP_CARD(img, alt, badge, prop_type, location, price):
    return (
        '<div class="prop-card">\n'
        '  <div class="prop-img"><img src="img/' + img + '" alt="' + alt + '" loading="lazy" style="width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:8px 8px 0 0"></div>\n'
        '  <div class="prop-body">\n'
        '    <span class="badge">' + badge + '</span>\n'
        '    <h4>' + prop_type + '</h4>\n'
        '    <p class="prop-loc">' + location + '</p>\n'
        '    <strong class="prop-price">' + price + '</strong>\n'
        '  </div>\n'
        '</div>'
    )


def UNIT(url, label):
    return '<a href="' + url + '" class="unit"><span class="u-dot"></span>' + label + '</a>'


def CASE_CARD(cat, img, title, subtitle, kpi):
    return (
        '<div class="case" data-cat="' + cat + '">\n'
        '  <div class="case-img"><img src="img/' + img + '" alt="' + title + '" loading="lazy"></div>\n'
        '  <div class="case-body">\n'
        '    <strong class="case-kpi">' + kpi + '</strong>\n'
        '    <h3>' + title + '</h3>\n'
        '    <p>' + subtitle + '</p>\n'
        '  </div>\n'
        '</div>'
    )


def BLOG_CARD(cat_key, img, title, cat_label, meta):
    return (
        '<div class="blog-card" data-cat="' + cat_key + '">\n'
        '  <div class="blog-img"><img src="img/' + img + '" alt="' + title + '" loading="lazy" style="width:100%;aspect-ratio:16/9;object-fit:cover"></div>\n'
        '  <div class="blog-body">\n'
        '    <span class="cat-badge">' + cat_label + '</span>\n'
        '    <h3>' + title + '</h3>\n'
        '    <p class="blog-meta">' + meta + '</p>\n'
        '  </div>\n'
        '</div>'
    )


# ── Write helper ──────────────────────────────────────────────────────────────

def write_page(filename, content):
    path = os.path.join(ROOT, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    lines = content.count('\n')
    print(filename + ': ' + str(lines) + 'L')


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — cases.html
# ═══════════════════════════════════════════════════════════════════════════════

def build_cases():
    path = os.path.join(ROOT, 'cases.html')
    with open(path, 'r', encoding='utf-8') as f:
        src = f.read()
    header, footer = extract_parts(src)

    toc = BUTOC(
        ('aanpak', 'Aanpak'),
        ('resultaten', 'Resultaten'),
        ('cases', 'Cases'),
        ('team', 'Team'),
        ('reviews', 'Reviews'),
        ('faq', 'FAQ'),
    )

    stats_green = STATS_GREEN([
        ('1.500+', 'Succesvolle cases'),
        ('98%', 'Klanttevredenheid'),
        ('€1,2 mld', 'Vastgoed begeleid'),
        ('15+', 'Jaar ervaring'),
    ])

    aanpak_section = '''
<section class="section section--tight" id="aanpak">
  <div class="container">
    <div class="two-col">
      <div class="prose">
        <span class="eyebrow">Onze aanpak</span>
        <h2>Resultaten die <em>voor zich spreken</em></h2>
        <p>Spring Real Estate combineert diepgaande marktkennis met een datagedreven aanpak. Van complexe herpositioneringen tot grootschalige verhuurtrajecten — wij leveren meetbaar resultaat voor eigenaren, gebruikers en investeerders.</p>
        <p>Onze aanpak is altijd maatwerk: we analyseren uw vraagstuk grondig, bouwen een concreet plan en begeleiden het volledige traject. Transparant, betrokken en resultaatgericht.</p>
        <a href="contact.html" class="btn btn--primary">Bespreek uw vraagstuk</a>
      </div>
      <div class="media-tall">
        <img src="img/photo-2.jpg" alt="Spring aanpak" loading="lazy" style="width:100%;height:100%;object-fit:cover;border-radius:12px">
      </div>
    </div>
  </div>
</section>'''

    expertises_section = '''
<section class="section section--soft" id="expertises">
  <div class="container">
    <div class="sec-head"><span class="eyebrow">Wat wij doen</span><h2>Onze <em>expertises</em></h2></div>
    <div class="usp-grid">
      <div class="usp"><h3>Verhuur &amp; acquisitie</h3><p>Van marktanalyse tot contractondertekening — wij begeleiden het volledige verhuurproces.</p></div>
      <div class="usp"><h3>Aan- en verkoop</h3><p>Strategisch advies en begeleiding bij aankoop of verkoop van commercieel vastgoed.</p></div>
      <div class="usp"><h3>Asset management</h3><p>Optimalisatie van vastgoedportefeuilles met focus op bezettingsgraad en rendement.</p></div>
      <div class="usp"><h3>Design &amp; Build</h3><p>Integrale kantoorinrichting van concept tot oplevering — volledig ontzorgd.</p></div>
      <div class="usp"><h3>Herpositionering</h3><p>Strategische herpositionering van kantoor- en bedrijfspanden voor maximale waardecreatie.</p></div>
      <div class="usp"><h3>Investeringsadvies</h3><p>Diepgaand rendements- en risicoadvies voor institutionele en particuliere investeerders.</p></div>
    </div>
  </div>
</section>'''

    quote_section = '''
<section class="section" style="text-align:center;background:#fff" id="resultaten">
  <div class="container" style="max-width:760px">
    <p style="font-size:1.35rem;font-style:italic;color:var(--ink);line-height:1.6">"Wij meten succes niet in deals, maar in de waarde die we toevoegen voor elke klant — bij elk project opnieuw."</p>
    <strong style="color:var(--green);display:block;margin-top:16px">Ivar Hillerstrom — Managing Director Spring Real Estate</strong>
  </div>
</section>'''

    stats_dark = STATS_DARK(
        'Bewezen resultaat',
        'Elk project, een <em>meetbaar verschil</em>',
        [
            ('+18%', 'gem. rendement herpositionering'),
            ('6 wkn', 'gem. doorlooptijd verhuur'),
            ('98%', 'bezettingsgraad na traject'),
            ('4,8/5', 'klantscore Google'),
        ]
    )

    werkwijze = WERKWIJZE([
        ('Intake &amp; analyse', 'We brengen uw vraagstuk scherp in kaart samen met doelstellingen en context.'),
        ('Strategie &amp; aanpak', 'Datagedreven advies en concreet plan van aanpak — onderbouwd met SpringBase marktdata.'),
        ('Uitvoering', 'We begeleiden het volledige traject: onderhandelen, co\xf6rdineren en communiceren.'),
        ('Oplevering &amp; nazorg', 'Resultaat opgeleverd, met evaluatie. Zo leren we samen van elk project.'),
    ])

    cases_items = (
        CASE_CARD('verhuur', 'photo-1.jpg', 'Zuidas kantoor 1.250 m\xb2', 'Verhuur aan internationale tech-firma binnen 4 weken', '+22% boven markthuur') + '\n' +
        CASE_CARD('asset management', 'photo-2.jpg', 'Herpositionering Utrecht Science Park', 'Van 45% naar 97% bezetting in 18 maanden', '97% bezetting') + '\n' +
        CASE_CARD('verhuur', 'hero.jpg', 'Kantoorcomplex Rotterdam', 'Multinationale huurder gevonden voor 3.800 m\xb2', '3.800 m\xb2 verhuurd') + '\n' +
        CASE_CARD('investments', 'photo-1.jpg', 'Investeringsportefeuille Amsterdam', 'Acquisitie en optimalisatie €85 mln portefeuille', '€85 mln AUM') + '\n' +
        CASE_CARD('design & build', 'photo-2.jpg', 'Design &amp; Build hoofdkantoor', 'Volledig ontzorgd kantoorconcept voor 400 medewerkers', '4.200 m\xb2 ingericht') + '\n' +
        CASE_CARD('verhuur', 'hero.jpg', 'Verhuur flex-hub Den Haag', 'Verhuur van flexibele werkplekken in Den Haag Centraal', '850 m\xb2 flex')
    )

    cases_section = (
        '\n<section class="section section--tight" id="cases">\n'
        '  <div class="container">\n'
        '    <div class="sec-head"><span class="eyebrow">Recente projecten</span><h2>Onze <em>cases</em></h2></div>\n'
        '    <div class="case-grid">\n'
        + cases_items + '\n'
        '    </div>\n'
        '  </div>\n'
        '</section>'
    )

    agents_html = (
        AGENT_CARD('ivar.hillerstrom.jpg', 'Ivar Hillerstrom', 'Managing Director', 'ivar@springrealestate.com') +
        AGENT_CARD('edgar.willems.jpg', 'Edgar Willems', 'Senior Adviseur', 'edgar@springrealestate.com')
    )
    team = TEAM_SECTION(agents_html)

    lead = LEAD_MAGNET(
        'Gratis whitepaper',
        'Hoe Spring meetbaar resultaat levert',
        'Praktijkgids met aanpak, methodiek en bewezen cases — direct in uw inbox.',
        'Download gratis'
    )

    faq = FAQ_SECTION('klantverhalen', [
        ('In welke sectoren is Spring actief?', 'Spring werkt voor corporate gebruikers, scale-ups, institutionele investeerders en vastgoedeigenaren in kantoor, bedrijfsruimte en residentieel vastgoed.'),
        ('Hoe lang duurt een typisch traject?', 'Afhankelijk van de complexiteit varieert een verhuurtraject van 4 tot 12 weken. Herpositionering of investeringstrajecten kunnen 6–18 maanden duren.'),
        ('Werkt Spring ook voor internationale partijen?', 'Ja — via onze vestigingen in Amsterdam, Utrecht, Valencia en Estepona bedienen we zowel Nederlandse als internationale opdrachtgevers.'),
    ])

    cta = CTA(
        'Wil ook zulke resultaten bereiken?',
        'Vertel ons uw vraagstuk — onze adviseurs denken vanaf dag \xe9\xe9n met u mee.'
    )

    body = (
        toc + stats_green + aanpak_section + expertises_section +
        quote_section + stats_dark + werkwijze + cases_section +
        team + REVIEWS_SECTION + lead + faq + cta
    )

    write_page('cases.html', header + body + footer)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — transacties.html
# ═══════════════════════════════════════════════════════════════════════════════

def build_transacties():
    path = os.path.join(ROOT, 'transacties.html')
    with open(path, 'r', encoding='utf-8') as f:
        src = f.read()
    header, footer = extract_parts(src)

    # Insert filter tabs before <form class="search
    filter_tabs = (
        '    <div class="team-filter" style="margin-top:20px">\n'
        '      <a href="#" class="active" data-key="alle">Alle</a>\n'
        '      <a href="#" data-key="verhuur">Verhuur</a>\n'
        '      <a href="#" data-key="verkoop">Verkoop</a>\n'
        '      <a href="#" data-key="investering">Investering</a>\n'
        '      <a href="#" data-key="design &amp; build">Design &amp; Build</a>\n'
        '    </div>\n'
    )
    header = header.replace('<form class="search', filter_tabs + '    <form class="search', 1)

    toc = BUTOC(
        ('aanpak', 'Aanpak'),
        ('cijfers', 'Cijfers'),
        ('transacties', 'Transacties'),
        ('team', 'Team'),
        ('reviews', 'Reviews'),
        ('faq', 'FAQ'),
    )

    spotlight = '''
<section class="section section--tight" id="aanpak">
  <div class="container">
    <div class="two-col">
      <div class="prose">
        <span class="eyebrow">Deal in de spotlight</span>
        <span class="badge" style="background:var(--green-tint);color:var(--green);margin-bottom:12px;display:inline-block">Verhuur</span>
        <h2>Verhuur Zuidas-kantoor <br><em>1.250 m&#178; aan internationale tech-firma</em></h2>
        <p>Spring begeleidde de verhuur van een premium kantoorruimte op de Zuidas aan een snel groeiende Europese tech-onderneming. Het traject werd afgerond binnen vier weken na marktintroductie.</p>
        <ul>
          <li>Huurprijs 22% boven benchmark huurprijsniveau Zuidas</li>
          <li>Volledig ontzorgd traject van zoekopdracht tot sleuteloverdracht</li>
          <li>Juridische en commerci\xeble begeleiding inbegrepen</li>
          <li>Huurder gevonden via SpringBase netwerk zonder externe marketing</li>
        </ul>
        <a href="contact.html" class="btn btn--primary">Bespreek uw vastgoed</a>
      </div>
      <div class="media-tall">
        <img src="img/photo-1.jpg" alt="Zuidas kantoor" loading="lazy" style="width:100%;height:100%;object-fit:cover;border-radius:12px">
      </div>
    </div>
  </div>
</section>'''

    stats_dark = STATS_DARK(
        'Spring in cijfers',
        'Bewezen <em>track record</em>',
        [
            ('€450M+', 'Transactiewaarde'),
            ('1.500+', 'Deals begeleid'),
            ('4', 'Vestigingen NL &amp; ES'),
            ('15+', 'Jaar marktervaring'),
        ]
    )

    werkwijze = WERKWIJZE([
        ('Opdracht &amp; briefing', 'We analyseren uw object, uw doelstellingen en de marktpositie — voor een scherp geformuleerde opdrachtomschrijving.'),
        ('Marktintroductie', 'Gerichte outreach via ons netwerk en SpringBase, aangevuld met gerichte marketing op relevante platforms.'),
        ('Onderhandeling', 'We voeren de onderhandelingen namens u: transparant, doelgericht en met focus op de best haalbare voorwaarden.'),
        ('Afronding &amp; nazorg', 'Juridische begeleiding tot en met de notari\xeble akte of huurovereenkomst, met nazorg na oplevering.'),
    ])

    blog_items = (
        BLOG_CARD('verhuur', 'photo-1.jpg', 'Kantoor 1.250 m\xb2 Zuidas verhuurd', 'Verhuur', 'Mei 2026 • Amsterdam') + '\n' +
        BLOG_CARD('verkoop', 'photo-2.jpg', 'Verkoop bedrijfspand Westpoort €4,8 mln', 'Verkoop', 'April 2026 • Amsterdam') + '\n' +
        BLOG_CARD('investering', 'hero.jpg', 'Acquisitie portefeuille Utrecht €32 mln', 'Investering', 'Maart 2026 • Utrecht') + '\n' +
        BLOG_CARD('verhuur', 'photo-1.jpg', 'Verhuur flex-kantoor Rotterdam 620 m\xb2', 'Verhuur', 'Februari 2026 • Rotterdam') + '\n' +
        BLOG_CARD('design & build', 'photo-2.jpg', 'Design &amp; Build inrichting 400 werkplekken', 'Design &amp; Build', 'Januari 2026 • Amsterdam') + '\n' +
        BLOG_CARD('investering', 'hero.jpg', 'Sale &amp; leaseback transactie €18 mln', 'Investering', 'December 2025 • Utrecht')
    )

    transacties_section = (
        '\n<section class="section section--soft" id="transacties">\n'
        '  <div class="container">\n'
        '    <div class="sec-head"><span class="eyebrow">Recente transacties</span><h2>Actueel <em>dealoverzicht</em></h2></div>\n'
        '    <div class="blog-grid">\n'
        + blog_items + '\n'
        '    </div>\n'
        '  </div>\n'
        '</section>'
    )

    lead = LEAD_MAGNET(
        'Gratis download',
        'Spring Marktrapport Q2 2026',
        'Actuele transactieprijzen, BAR-rendementen en marktontwikkelingen per sector — samengesteld door Spring Research.',
        'Rapport ontvangen'
    )

    agents_html = (
        AGENT_CARD('ivar.hillerstrom.jpg', 'Ivar Hillerstrom', 'Managing Director', 'ivar@springrealestate.com') +
        AGENT_CARD('edgar.willems.jpg', 'Edgar Willems', 'Senior Adviseur', 'edgar@springrealestate.com')
    )
    team = TEAM_SECTION(agents_html)

    faq = FAQ_SECTION('transacties', [
        ('Hoe verloopt een verkooptraject bij Spring?', 'We starten met een gratis marktwaardebepaling, gevolgd door een strategisch verkoopplan. Na akkoord nemen wij het volledige traject over, inclusief marketing, bezichtigingen en onderhandeling.'),
        ('Wat is de gemiddelde verkooptijd?', 'Afhankelijk van object en markt realiseren wij gemiddeld verkoop binnen 6 tot 14 weken na marktintroductie.'),
        ('Werkt Spring ook met buitenlandse investeerders?', 'Ja — Spring heeft een actief netwerk van Europese institutionele investeerders en family offices die actief zijn op de Nederlandse markt.'),
    ])

    cta = CTA(
        'Benieuwd wat uw vastgoed waard is?',
        'Vraag een vrijblijvende taxatie of marktanalyse aan bij onze specialisten.'
    )

    body = (
        toc + spotlight + stats_dark + werkwijze +
        transacties_section + lead + team + REVIEWS_SECTION + faq + cta
    )

    write_page('transacties.html', header + body + footer)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — algemeen.html
# ═══════════════════════════════════════════════════════════════════════════════

def build_algemeen():
    path = os.path.join(ROOT, 'algemeen.html')
    with open(path, 'r', encoding='utf-8') as f:
        src = f.read()
    header, footer = extract_parts(src)

    # Find end of hero to locate existing body
    hero_start = src.index('<section class="page-hero"')
    after_hero = src[hero_start:]
    hero_end_offset = after_hero.index('</section>') + len('</section>')
    end_of_hero = hero_start + hero_end_offset

    existing_body = src[end_of_hero: src.index('\n<section class="talk-strip">')]

    # Add id attributes to key sections
    existing_body = existing_body.replace(
        '<section class="section section--tight section--soft"',
        '<section class="section section--tight section--soft" id="uitgelicht"',
        1
    )
    existing_body = existing_body.replace(
        '<section style="background:var(--ink)',
        '<section id="podcast" style="background:var(--ink)',
        1
    )
    existing_body = existing_body.replace(
        '<section class="section filterable"',
        '<section class="section filterable" id="artikelen"',
        1
    )

    toc = BUTOC(
        ('uitgelicht', 'Uitgelicht'),
        ('podcast', 'Podcast'),
        ('artikelen', 'Artikelen'),
        ('team', 'Team'),
        ('reviews', 'Reviews'),
        ('faq', 'FAQ'),
    )

    agents_html = (
        AGENT_CARD('ivar.hillerstrom.jpg', 'Ivar Hillerstrom', 'Managing Director', 'ivar@springrealestate.com') +
        AGENT_CARD('edgar.willems.jpg', 'Edgar Willems', 'Senior Adviseur', 'edgar@springrealestate.com')
    )
    team = TEAM_SECTION(agents_html)

    faq = FAQ_SECTION('marktinzichten', [
        ('Hoe vaak publiceert Spring nieuwe inzichten?', 'Spring publiceert wekelijks marktanalyses, maandelijks een uitgebreid marktrapport en elk kwartaal een verdiepend onderzoeksrapport via Spring Research.'),
        ('Kan ik mij aanmelden voor de nieuwsbrief?', 'Ja — via het aanmeldformulier op deze pagina ontvangt u automatisch onze nieuwste analyses, rapporten en marktberichten.'),
        ('Draagt Spring ook bij aan externe publicaties?', 'Onze specialisten schrijven regelmatig opiniestukken voor vakbladen zoals Vastgoedmarkt, PropertyNL en FD Vastgoed.'),
    ])

    cta = CTA(
        'Meer weten over een specifiek onderwerp?',
        'Onze specialisten beantwoorden uw vragen en sturen u de relevante rapporten toe.'
    )

    body = toc + existing_body + team + REVIEWS_SECTION + faq + cta

    write_page('algemeen.html', header + body + footer)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGES 4-7 — Location pages
# ═══════════════════════════════════════════════════════════════════════════════

def build_location_page(filename, city_config):
    path = os.path.join(ROOT, filename)
    with open(path, 'r', encoding='utf-8') as f:
        src = f.read()
    header, footer = extract_parts(src)

    cfg = city_config

    toc = BUTOC(
        ('markt', 'Markt'),
        ('diensten', 'Diensten'),
        ('team', 'Team'),
        ('aanbod', 'Aanbod'),
        ('faq', 'FAQ'),
    )

    # Market section with stat cards
    stat_cards = ''
    for num, lbl, sub in cfg['market_stats']:
        stat_cards += (
            '<div class="stat-card" style="background:#fff;border-radius:10px;padding:20px;box-shadow:0 2px 8px rgba(0,0,0,.06)">'
            '<b style="font-size:1.8rem;font-weight:800;color:var(--ink)">' + num + '</b>'
            '<span style="display:block;color:#555;font-size:.85rem">' + lbl + '</span>'
            '<small style="color:#888">' + sub + '</small>'
            '</div>\n'
        )

    markt_section = (
        '\n<section class="section section--tight" id="markt">\n'
        '  <div class="container">\n'
        '    <span class="eyebrow">' + cfg['markt_eyebrow'] + '</span>\n'
        '    <h2>' + cfg['markt_h2'] + '</h2>\n'
        '    <div class="two-col" style="margin-top:32px">\n'
        '      <div class="stat-cards-grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:16px">\n'
        + stat_cards +
        '      </div>\n'
        '      <div class="prose">\n'
        '        <p>' + cfg['markt_p1'] + '</p>\n'
        '        <p>' + cfg['markt_p2'] + '</p>\n'
        '      </div>\n'
        '    </div>\n'
        '  </div>\n'
        '</section>'
    )

    # Vestiging section with loc-map
    loc_map = LOC_MAP(cfg['map_bg'], cfg['map_stroke'], cfg['map_pin'], cfg['map_city'])
    pop_stats = ''
    for num, lbl in cfg['pop_stats']:
        pop_stats += (
            '<div class="stat-pop" style="display:flex;align-items:center;gap:12px;margin-bottom:10px">'
            '<b style="font-size:1.4rem;font-weight:800;min-width:48px">' + num + '</b>'
            '<span style="color:#555;font-size:.9rem">' + lbl + '</span>'
            '</div>\n'
        )

    vestiging_section = (
        '\n<section class="section section--tight">\n'
        '  <div class="container">\n'
        '    <div class="two-col">\n'
        '      <div class="prose">\n'
        '        <span class="eyebrow">Over onze vestiging</span>\n'
        '        <h2>' + cfg['vestiging_h2'] + '</h2>\n'
        '        <p>' + cfg['vestiging_p'] + '</p>\n'
        '        <div style="margin-top:20px">\n'
        + pop_stats +
        '        </div>\n'
        '      </div>\n'
        '      <div>\n'
        + loc_map + '\n'
        '      </div>\n'
        '    </div>\n'
        '  </div>\n'
        '</section>'
    )

    # Diensten
    units_html = ''
    for url, label in cfg['diensten']:
        units_html += '      ' + UNIT(url, label) + '\n'

    diensten_section = (
        '\n<section class="section section--tight section--soft" id="diensten">\n'
        '  <div class="container">\n'
        '    <div class="sec-head"><span class="eyebrow">Wat wij doen</span><h2>Onze <em>diensten</em> in ' + cfg['city_name'] + '</h2></div>\n'
        '    <div class="units-grid">\n'
        + units_html +
        '    </div>\n'
        '  </div>\n'
        '</section>'
    )

    # Kantoorimpressie
    impressie_section = (
        '\n<section class="section section--tight">\n'
        '  <div class="container">\n'
        '    <div class="sec-head"><span class="eyebrow">Kantoorindruk</span><h2>Onze <em>locatie</em></h2></div>\n'
        '    <div class="cards-grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px">\n'
        '      <img src="img/photo-1.jpg" alt="Kantoor ' + cfg['city_name'] + '" loading="lazy" style="width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:10px">\n'
        '      <img src="img/photo-2.jpg" alt="Kantoor ' + cfg['city_name'] + '" loading="lazy" style="width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:10px">\n'
        '      <img src="img/hero.jpg" alt="Kantoor ' + cfg['city_name'] + '" loading="lazy" style="width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:10px">\n'
        '    </div>\n'
        '  </div>\n'
        '</section>'
    )

    stats_dark = STATS_DARK(cfg['stats_eyebrow'], cfg['stats_h2'], cfg['stats_list'])

    # Team section (dark)
    team_agents = ''
    for photo, name, role in cfg['agents']:
        team_agents += AGENT_CARD(photo, name, role, name.lower().replace(' ', '.') + '@springrealestate.com')

    team_section = (
        '\n<section class="section dark-sec" id="team">\n'
        '  <div class="container">\n'
        '    <div class="sec-head">\n'
        '      <span class="eyebrow" style="color:var(--green-soft,#9DC76B)">Ons team in ' + cfg['city_name'] + '</span>\n'
        '      <h2 style="color:#fff">Uw <em>lokale experts</em></h2>\n'
        '      <a href="agents.html" class="btn btn--secondary">Heel het team</a>\n'
        '    </div>\n'
        '    <div class="team-grid">' + team_agents + '</div>\n'
        '  </div>\n'
        '</section>'
    )

    lead = LEAD_MAGNET(cfg['lead_eyebrow'], cfg['lead_h2'], cfg['lead_p'], cfg['lead_btn'])

    # Aanbod
    prop_cards = ''
    for pc in cfg['prop_cards']:
        prop_cards += PROP_CARD(pc[0], pc[1], pc[2], pc[3], pc[4], pc[5]) + '\n'

    aanbod_section = (
        '\n<section class="section section--tight" id="aanbod">\n'
        '  <div class="container">\n'
        '    <div class="sec-head"><span class="eyebrow">Beschikbaar aanbod</span><h2>Actueel <em>aanbod</em> in ' + cfg['city_name'] + '</h2></div>\n'
        '    <div style="margin-bottom:24px"><a href="listings.html" class="btn btn--ghost">Heel het aanbod bekijken</a></div>\n'
        '    <div class="cards-grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px">\n'
        + prop_cards +
        '    </div>\n'
        '  </div>\n'
        '</section>'
    )

    faq = FAQ_SECTION(cfg['city_name'], cfg['faq_items'])
    cta = CTA(cfg['cta_h2'], cfg['cta_p'])

    body = (
        toc + LOGOS_BAND + markt_section + vestiging_section +
        diensten_section + impressie_section + stats_dark +
        team_section + REVIEWS_SECTION + lead + aanbod_section + faq + cta
    )

    write_page(filename, header + body + footer)


# ── City configurations ───────────────────────────────────────────────────────

UTRECHT_CONFIG = {
    'city_name': 'Utrecht',
    'markt_eyebrow': 'De Utrechtse vastgoedmarkt',
    'markt_h2': 'Utrecht: dynamisch <em>centrum</em> van Nederland',
    'markt_p1': 'Utrecht is na Amsterdam de meest gevraagde kantoormarkt van Nederland. De ligging in het hart van het land, uitstekende infrastructuur en een groeiende kenniseconomie maken Utrecht tot een magneet voor nationale en internationale bedrijven.',
    'markt_p2': 'Spring Real Estate is al meer dan 15 jaar actief in de regio Utrecht en begeleidt jaarlijks tientallen transacties in kantoor, bedrijfsruimte en residentieel vastgoed.',
    'market_stats': [
        ('€195/m\xb2', 'Prime huur Stationsgebied', 'per jaar'),
        ('4,8%', 'BAR kantoorbelegging', 'gemiddeld 2026'),
        ('94%', 'Bezettingsgraad prime', 'Utrecht Centrum'),
    ],
    'vestiging_h2': 'Spring Utrecht: <em>hart van</em> de regio',
    'vestiging_p': 'Onze Utrechtse vestiging aan de Stadhouderskade is het kloppende hart voor vastgoedadvies in de regio. Met 18 business units en 40+ specialisten zijn we de meest complete vastgoedadviseur in Utrecht.',
    'pop_stats': [
        ('18', 'business units'),
        ('40+', 'specialisten'),
        ('15+', 'jaar regio'),
    ],
    'map_bg': '#E8F0D8',
    'map_stroke': '#7CA73F',
    'map_pin': '#7CA73F',
    'map_city': 'Utrecht',
    'diensten': [
        ('doelgroep-gebruiker.html', 'Kantoorhuur &amp; aquisitie'),
        ('doelgroep-eigenaar.html', 'Kantoorverkoop'),
        ('doelgroep-investeerder.html', 'Investeringsadvies'),
        ('doelgroep-ontwikkelaar.html', 'Projectontwikkeling'),
        ('listings.html', 'Asset management'),
        ('listings.html', 'Design &amp; Build'),
        ('listings.html', 'Herpositionering'),
        ('listings.html', 'Duurzaamheidsadvies'),
    ],
    'stats_eyebrow': 'Utrecht in cijfers',
    'stats_h2': 'Bewezen <em>aanwezigheid</em> in de regio',
    'stats_list': [
        ('200+', 'transacties in Utrecht'),
        ('8', 'objecten beschikbaar'),
        ('15+', 'jaar marktkennis'),
        ('18', 'business units'),
    ],
    'agents': [
        ('bas.sijbom.jpg', 'Bas Sijbom LLM', 'Directeur Utrecht'),
        ('rolf.vermeer.jpg', 'ir. Rolf Vermeer', 'Senior Adviseur'),
        ('willemjan.schouten.jpg', 'Willem Jan Schouten', 'Adviseur Beleggingen'),
    ],
    'lead_eyebrow': 'Gratis marktrapport',
    'lead_h2': 'Utrecht Vastgoedmarkt Q2 2026',
    'lead_p': 'Actuele huurprijzen, leegstandscijfers en transactiedata voor de regio Utrecht — van Spring Research.',
    'lead_btn': 'Rapport ontvangen',
    'prop_cards': [
        ('photo-1.jpg', 'Kantoor Stationsgebied', 'Huur', 'Kantoor', 'Utrecht Stationsgebied', '€195/m\xb2/jr'),
        ('photo-2.jpg', 'Bedrijfsruimte Leidsche Rijn', 'Huur', 'Bedrijfsruimte', 'Utrecht Leidsche Rijn', '€140/m\xb2/jr'),
        ('hero.jpg', 'Kantoorvilla Science Park', 'Koop', 'Kantoor', 'Utrecht Science Park', '€3,2 mln'),
    ],
    'faq_items': [
        ('Hoe zijn de huurprijzen in Utrecht?', 'Prime kantoorhuur in het Stationsgebied ligt rond €195 per m\xb2 per jaar. Buiten de pieklocaties zijn huurprijzen van €140–€165/m\xb2/jr gangbaar.'),
        ('Wat zijn de parkeernormen in Utrecht?', 'In Utrecht Centrum geldt een beperkte parkeernorm van 1 op 250 m\xb2. Buiten de ring zijn normen van 1 op 80 tot 1 op 125 m\xb2 gebruikelijk.'),
        ('Hoe snel kan Spring een object presenteren?', 'Na ontvangst van uw opdracht presenteren wij binnen 5 werkdagen een longlist van geschikte objecten in de regio Utrecht.'),
    ],
    'cta_h2': 'Vastgoed zoeken of adviseren in Utrecht?',
    'cta_p': 'Onze Utrechtse specialisten staan klaar — van eerste vraag tot oplevering.',
}

AMSTERDAM_CONFIG = {
    'city_name': 'Amsterdam',
    'markt_eyebrow': 'De Amsterdamse vastgoedmarkt',
    'markt_h2': 'Amsterdam Zuidas: <em>Europees</em> toptopgebied',
    'markt_p1': 'Amsterdam is de meest liquide en internationale kantorenmarkt van Nederland. De Zuidas fungeert als Europees financieel centrum en trekt multinationals, financiële instellingen en internationale advocatenkantoren.',
    'markt_p2': 'Spring Real Estate Amsterdam begeleidt transacties voor de meest veeleisende gebruikers en investeerders, van boutique offices tot grootschalige corporate relocaties.',
    'market_stats': [
        ('€485/m\xb2', 'Prime huur Zuidas', 'per jaar'),
        ('3,8%', 'BAR kantoorbelegging', 'Zuidas 2026'),
        ('96%', 'Bezettingsgraad prime', 'Amsterdam Zuidas'),
    ],
    'vestiging_h2': 'Spring Amsterdam: <em>in het hart van</em> de Zuidas',
    'vestiging_p': 'Ons Amsterdamse kantoor aan de Gustav Mahlerplein is de uitvalsbasis voor alle Randstad-transacties. Met direct toegang tot het internationale netwerk van Spring bedienen we de meest veeleisende klanten.',
    'pop_stats': [
        ('24', 'business units'),
        ('60+', 'specialisten'),
        ('20+', 'jaar aanwezig'),
    ],
    'map_bg': '#FFE8E0',
    'map_stroke': '#D4603A',
    'map_pin': '#D4603A',
    'map_city': 'Amsterdam Zuidas',
    'diensten': [
        ('doelgroep-gebruiker.html', 'Corporate kantoorhuur'),
        ('doelgroep-eigenaar.html', 'Institutioneel vastgoed'),
        ('doelgroep-investeerder.html', 'Investeringsadvies'),
        ('doelgroep-ontwikkelaar.html', 'Gebiedsontwikkeling'),
        ('listings.html', 'Asset management'),
        ('listings.html', 'Design &amp; Build'),
    ],
    'stats_eyebrow': 'Amsterdam in cijfers',
    'stats_h2': 'Bewezen <em>marktleiderschap</em> in de hoofdstad',
    'stats_list': [
        ('500+', 'transacties in Amsterdam'),
        ('12', 'objecten beschikbaar'),
        ('20+', 'jaar marktkennis'),
        ('€1,2 mrd', 'transactiewaarde'),
    ],
    'agents': [
        ('ivar.hillerstrom.jpg', 'Ivar Hillerstrom', 'Managing Director'),
        ('edgar.willems.jpg', 'Edgar Willems', 'Senior Adviseur'),
    ],
    'lead_eyebrow': 'Gratis marktrapport',
    'lead_h2': 'Amsterdam Vastgoedmarkt Q2 2026',
    'lead_p': 'Actuele huurprijzen, BAR-rendementen en transactiedata voor Amsterdam en de Zuidas — van Spring Research.',
    'lead_btn': 'Rapport ontvangen',
    'prop_cards': [
        ('photo-1.jpg', 'Kantoor Zuidas', 'Huur', 'Kantoor', 'Amsterdam Zuidas', '€485/m\xb2/jr'),
        ('photo-2.jpg', 'Boutique office Oud-Zuid', 'Huur', 'Kantoor', 'Amsterdam Oud-Zuid', '€320/m\xb2/jr'),
        ('hero.jpg', 'Beleggingsobject Centrum', 'Koop', 'Gemengd object', 'Amsterdam Centrum', '€8,5 mln'),
    ],
    'faq_items': [
        ('Wat zijn de huurprijzen op de Zuidas?', 'Prime huurprijzen op de Zuidas liggen in 2026 tussen €450 en €510 per m\xb2 per jaar voor A-grade kantoorruimte.'),
        ('Hoe snel vind ik een huurder voor mijn Amsterdams pand?', 'Afhankelijk van locatie en kwaliteit realiseren wij gemiddeld verhuur binnen 8 weken via ons directe netwerk.'),
        ('Heeft Spring ook aanbod buiten de Zuidas?', 'Ja — wij hebben aanbod in alle deelgebieden van Amsterdam: Centrum, West, Oost, Noord en het Havengebied.'),
    ],
    'cta_h2': 'Vastgoed zoeken of adviseren in Amsterdam?',
    'cta_p': 'Onze Amsterdamse specialisten staan klaar — van strategie tot oplevering.',
}

VALENCIA_CONFIG = {
    'city_name': 'Valencia',
    'markt_eyebrow': 'De Valencia vastgoedmarkt',
    'markt_h2': 'Valencia: <em>opkomende</em> Europese vastgoedmarkt',
    'markt_p1': 'Valencia is uitgegroeid tot een van de meest dynamische vastgoedmarkten van Zuid-Europa. Lage kosten ten opzichte van Madrid en Barcelona, gecombineerd met uitstekende infrastructuur en kwaliteit van leven, trekken internationale bedrijven en investeerders aan.',
    'markt_p2': 'Spring Valencia begeleidt Nederlandse en internationale klanten bij kantoorhuur, -koop en investeringen in de Valencian Community.',
    'market_stats': [
        ('€185/m\xb2', 'Prime huur Valencia CBD', 'per jaar'),
        ('5,2%', 'Aanvangsrendement', 'kantoor 2026'),
        ('88%', 'Bezettingsgraad prime', 'Valencia Centrum'),
    ],
    'vestiging_h2': 'Spring Valencia: <em>uw brug</em> naar Spanje',
    'vestiging_p': 'Onze Valenciaanse vestiging biedt Nederlandse en Belgische klanten directe toegang tot de Spaanse vastgoedmarkt. Volledig tweetalig team met lokale marktkennis en Nederlandse zakelijke cultuur.',
    'pop_stats': [
        ('8', 'specialisten'),
        ('5+', 'jaar aanwezig'),
        ('100+', 'transacties ES'),
    ],
    'map_bg': '#E8C4A0',
    'map_stroke': '#C4956A',
    'map_pin': '#C4956A',
    'map_city': 'Valencia',
    'diensten': [
        ('doelgroep-gebruiker.html', 'Kantoorhuur Valencia'),
        ('doelgroep-eigenaar.html', 'Vastgoedverkoop Spanje'),
        ('doelgroep-investeerder.html', 'Investeringsadvies ES'),
        ('doelgroep-ontwikkelaar.html', 'Projectbegeleiding'),
        ('listings.html', 'Belastingadvies &amp; structurering'),
        ('listings.html', 'Relocation services'),
    ],
    'stats_eyebrow': 'Valencia in cijfers',
    'stats_h2': 'Spring <em>actief</em> in Valencia',
    'stats_list': [
        ('100+', 'transacties in Spanje'),
        ('5', 'objecten beschikbaar'),
        ('5+', 'jaar marktkennis'),
        ('8', 'lokale specialisten'),
    ],
    'agents': [
        ('bas.sijbom.jpg', 'Carlos Mart\xednez', 'Directeur Valencia'),
        ('rolf.vermeer.jpg', 'Petra van den Berg', 'Senior Adviseur'),
    ],
    'lead_eyebrow': 'Gratis gids',
    'lead_h2': 'Investeren in Spaans vastgoed 2026',
    'lead_p': 'Alles over belastingstructuren, aanvangsrendementen en hotspots in Valencia — samengesteld door Spring Research.',
    'lead_btn': 'Gids ontvangen',
    'prop_cards': [
        ('photo-1.jpg', 'Kantoor Valencia CBD', 'Huur', 'Kantoor', 'Valencia Centro', '€185/m\xb2/jr'),
        ('photo-2.jpg', 'Beleggingspand Valencia', 'Koop', 'Gemengd object', 'Valencia Ruzafa', '€2,4 mln'),
        ('hero.jpg', 'Showroom/kantoor Quatre Carreres', 'Huur', 'Bedrijfsruimte', 'Valencia Quatre Carreres', '€95/m\xb2/jr'),
    ],
    'faq_items': [
        ('Welke belastingen betaal ik bij koop in Spanje?', 'Bij aankoop van bestaand Spaans vastgoed betaalt u 10% ITP (overdrachtsbelasting) in de Valencian Community plus notaris- en registratiekosten van ca. 1,5%.'),
        ('Kan Spring ook helpen met Spaanse vergunningen?', 'Ja — ons lokale team begeleidt u bij vergunningsaanvragen, bestemmingsplannen en contact met gemeentelijke instanties.'),
        ('Is er vraag naar kantoorruimte in Valencia?', 'Absoluut. Valencia kent een groeiende tech- en startupscene en trekt steeds meer internationale bedrijven die betaalbare, kwalitatieve kantoorruimte zoeken.'),
    ],
    'cta_h2': 'Investeren of werken in Valencia?',
    'cta_p': 'Onze Valenciaanse specialisten helpen u van eerste ori\xebntatie tot sleuteloverdracht.',
}

ESTEPONA_CONFIG = {
    'city_name': 'Estepona',
    'markt_eyebrow': 'De Costa del Sol vastgoedmarkt',
    'markt_h2': 'Estepona: <em>luxe</em> aan de Costa del Sol',
    'markt_p1': 'Estepona is uitgegroeid tot het meest exclusieve segment van de Costa del Sol — het alternatief voor Marbella, met minder drukte en meer authenticiteit. Ultra-luxe residenties, golfresorts en boutique commercieel vastgoed trekken internationaal vermogende ko pers.',
    'markt_p2': 'Spring Estepona bedient een select cli\xebnteel van vermogende particulieren, family offices en projectontwikkelaars die het beste van de Costa del Sol zoeken.',
    'market_stats': [
        ('€6.500/m\xb2', 'Gem. koopprijs luxe', 'Estepona Golden Mile'),
        ('6,8%', 'Bruto huurrendement', 'luxe vakantieverhuur'),
        ('32%', 'Waardestijging', 'afgelopen 3 jaar'),
    ],
    'vestiging_h2': 'Spring Estepona: <em>uw partner</em> aan de Costa del Sol',
    'vestiging_p': 'Onze vestiging in Estepona bedient vermogende Nederlandse en internationale kl\xebanten die op zoek zijn naar premium vastgoed aan de Costa del Sol. Persoonlijk, discreet en met diepgaande lokale marktkennis.',
    'pop_stats': [
        ('6', 'specialisten'),
        ('3+', 'jaar aanwezig'),
        ('50+', 'luxe transacties'),
    ],
    'map_bg': '#B8D4E8',
    'map_stroke': '#5B9EC9',
    'map_pin': '#5B9EC9',
    'map_city': 'Estepona',
    'diensten': [
        ('doelgroep-gebruiker.html', 'Luxe woningen'),
        ('doelgroep-eigenaar.html', 'Exclusieve verkoop'),
        ('doelgroep-investeerder.html', 'Beleggingsvastgoed'),
        ('doelgroep-ontwikkelaar.html', 'Nieuwbouwprojecten'),
        ('listings.html', 'Vakantieverhuur beheer'),
    ],
    'stats_eyebrow': 'Estepona in cijfers',
    'stats_h2': 'Spring <em>actief</em> aan de Costa del Sol',
    'stats_list': [
        ('50+', 'luxe transacties'),
        ('4', 'objecten beschikbaar'),
        ('3+', 'jaar aanwezig'),
        ('€6.500/m\xb2', 'gem. transactieprijs'),
    ],
    'agents': [
        ('bas.sijbom.jpg', 'Miguel Fern\xe1ndez', 'Directeur Estepona'),
        ('rolf.vermeer.jpg', 'Sophie de Vries', 'Senior Adviseur'),
    ],
    'lead_eyebrow': 'Gratis gids',
    'lead_h2': 'Luxe vastgoed Costa del Sol 2026',
    'lead_p': 'Alles over toplocaties, koopprijzen, rendement en juridische aspecten van luxevastgoed in Estepona en omgeving.',
    'lead_btn': 'Gids ontvangen',
    'prop_cards': [
        ('photo-1.jpg', 'Villa Estepona Golden Mile', 'Koop', 'Luxe villa', 'Estepona Golden Mile', '€3,8 mln'),
        ('photo-2.jpg', 'Penthouse zeezicht', 'Koop', 'Penthouse', 'Estepona Centro', '€1,95 mln'),
        ('hero.jpg', 'Appartement golfresort', 'Koop', 'Appartement', 'Estepona Golf', '€895.000'),
    ],
    'faq_items': [
        ('Kan ik als Nederlander vastgoed kopen in Estepona?', 'Ja — EU-burgers kunnen vrijelijk Spaans vastgoed aankopen. Spring begeleidt u bij het NIE-nummer, notariaat en financieringsstructuur.'),
        ('Wat is het huurrendement in Estepona?', 'Luxe vakantieverhuur in Estepona genereert bruto rendementen van 5–8%, afhankelijk van locatie, bezetting en object.'),
        ('Hoe lang duurt een aankooptraject?', 'Een standaard aankooptraject duurt 8–12 weken van bezichtiging tot notari\xeble overdracht, mits financiering en documenten op orde zijn.'),
    ],
    'cta_h2': 'Droomt u van vastgoed aan de Costa del Sol?',
    'cta_p': 'Spring Estepona begeleidt u discreet en persoonlijk bij uw zoektocht naar het perfecte object.',
}


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print('=== Spring Real Estate — rebuild_7pages.py ===')
    build_cases()
    build_transacties()
    build_algemeen()
    build_location_page('locatie-utrecht.html', UTRECHT_CONFIG)
    build_location_page('locatie-amsterdam.html', AMSTERDAM_CONFIG)
    build_location_page('locatie-valencia.html', VALENCIA_CONFIG)
    build_location_page('locatie-estepona.html', ESTEPONA_CONFIG)
    print('=== Done — 7 pages written ===')


if __name__ == '__main__':
    main()
