import re

def read(f):
    with open(f, encoding='utf-8') as fh: return fh.read()
def write(f, s):
    with open(f, 'w', encoding='utf-8') as fh: fh.write(s)

REVIEWS_BU = """
<section class="section" id="reviews" style="background:var(--green-tint)"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Reviews</span><h2 class="disp">Wat klanten <em>zeggen</em></h2></div></div>
  <div class="rev-grid">
    <div class="review"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>"Spring dacht echt mee en leverde sneller resultaat dan verwacht."</p><div class="who"><span class="av">JV</span><span><b>Jeroen V.</b><br><small>Scale-up, Utrecht</small></span></div></div>
    <div class="review"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>"Transparant, deskundig en datagedreven advies. Altijd bereikbaar."</p><div class="who"><span class="av">MK</span><span><b>Marit K.</b><br><small>Corporate vastgoed</small></span></div></div>
    <div class="review"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>"Een betrouwbare partner voor elk vastgoedvraagstuk."</p><div class="who"><span class="av">RG</span><span><b>Rafael G.</b><br><small>Investeerder</small></span></div></div>
  </div>
</div></section>"""

TEAM_BU = """
<section class="section dark-sec" id="team"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow" style="color:var(--green-soft,#9DC76B)">Het team</span><h2 class="disp" style="color:#fff">Uw <em>experts</em></h2></div><a href="agents.html" class="btn btn--secondary">Heel het team</a></div>
  <div class="team-grid">
  <div class="agent"><div class="ph"><img src="images/team/ivar.hillerstrom.jpg" alt="Ivar Hillerstrom" loading="lazy"></div><div class="body"><div class="name">Ivar Hillerstrom</div><div class="role">Managing Director</div><div class="socials"><a href="https://linkedin.com/company/spring-real-estate-nl" target="_blank" rel="noopener" aria-label="LinkedIn">in</a><a href="mailto:ivar.hillerstrom@springrealestate.com" aria-label="E-mail">@</a></div></div></div>
  <div class="agent"><div class="ph"><img src="images/team/edgar.willems.jpg" alt="Edgar Willems" loading="lazy"></div><div class="body"><div class="name">Edgar Willems</div><div class="role">Senior Adviseur</div><div class="socials"><a href="https://linkedin.com/company/spring-real-estate-nl" target="_blank" rel="noopener" aria-label="LinkedIn">in</a><a href="mailto:edgar.willems@springrealestate.com" aria-label="E-mail">@</a></div></div></div>
  </div>
</div></section>"""

PAGE_CONFIG = {
    'cases.html': {
        'lm_eyebrow': 'Gratis casegids',
        'lm_h2': 'Hoe Spring meetbaar resultaat levert — <em>in de praktijk</em>',
        'lm_p': 'Praktijkgids met aanpak, methodiek en bewezen cases — direct in uw inbox.',
        'lm_btn': 'Gids ontvangen',
        'faq_eyebrow': 'Veelgestelde vragen',
        'faq_h2': 'Vragen over <em>klantverhalen</em>',
        'faq_items': [
            ('In welke sectoren is Spring actief?', 'Spring werkt voor corporate gebruikers, scale-ups, institutionele investeerders en vastgoedeigenaren in kantoor, bedrijfsruimte en residentieel vastgoed.'),
            ('Hoe lang duurt een typisch traject?', 'Afhankelijk van de complexiteit varieert een verhuurtraject van 4 tot 12 weken. Herpositionering of investeringstrajecten kunnen 6–18 maanden duren.'),
            ('Werkt Spring ook voor internationale partijen?', 'Ja — via onze vestigingen in Amsterdam, Utrecht, Valencia en Estepona bedienen we zowel Nederlandse als internationale opdrachtgevers.'),
        ],
    },
    'transacties.html': {
        'lm_eyebrow': 'Gratis marktrapport',
        'lm_h2': 'Spring Marktrapport Q2 2026 — <em>actuele deals &amp; data</em>',
        'lm_p': 'Actuele transactieprijzen, BAR-rendementen en marktontwikkelingen per sector — samengesteld door Spring Research.',
        'lm_btn': 'Rapport ontvangen',
        'faq_eyebrow': 'Veelgestelde vragen',
        'faq_h2': 'Vragen over <em>transacties</em>',
        'faq_items': [
            ('Hoe verloopt een verkooptraject bij Spring?', 'We starten met een gratis marktwaardebepaling, gevolgd door een strategisch verkoopplan. Na akkoord nemen wij het volledige traject over, inclusief marketing, bezichtigingen en onderhandeling.'),
            ('Wat is de gemiddelde verkooptijd?', 'Afhankelijk van object en markt realiseren wij gemiddeld verkoop binnen 6 tot 14 weken na marktintroductie.'),
            ('Werkt Spring ook met buitenlandse investeerders?', 'Ja — Spring heeft een actief netwerk van Europese institutionele investeerders en family offices die actief zijn op de Nederlandse markt.'),
        ],
    },
    'algemeen.html': {
        'lm_eyebrow': 'Nieuwsbrief',
        'lm_h2': 'Marktinzichten direct <em>in uw inbox</em>',
        'lm_p': 'Elke maand: de belangrijkste vastgoedtrends, nieuwe analyses en exclusieve Spring-inzichten.',
        'lm_btn': 'Inschrijven',
        'faq_eyebrow': 'Veelgestelde vragen',
        'faq_h2': 'Vragen over <em>marktinzichten</em>',
        'faq_items': [
            ('Hoe vaak publiceert Spring nieuwe inzichten?', 'Spring publiceert wekelijks marktanalyses, maandelijks een uitgebreid marktrapport en elk kwartaal een verdiepend onderzoeksrapport via Spring Research.'),
            ('Kan ik mij aanmelden voor de nieuwsbrief?', 'Ja — via het aanmeldformulier op deze pagina ontvangt u automatisch onze nieuwste analyses, rapporten en marktberichten.'),
            ('Draagt Spring ook bij aan externe publicaties?', 'Onze specialisten schrijven regelmatig opiniestukken voor vakbladen zoals Vastgoedmarkt, PropertyNL en FD Vastgoed.'),
        ],
    },
}

def make_lm_faq(cfg):
    items = []
    for i, (q, a) in enumerate(cfg['faq_items']):
        open_attr = ' open' if i == 0 else ''
        items.append(
            f'      <details class="faq-item"{open_attr}>'
            f'<summary><span>{q}</span><span class="pl">+</span></summary>'
            f'<div class="ans">{a}</div></details>'
        )
    items_html = '\n'.join(items)
    return f"""
<section class="section--tight" id="download"><div class="container">
  <div style="background:var(--ink);border-radius:16px;padding:36px 48px;display:grid;grid-template-columns:1fr auto;align-items:center;gap:40px;flex-wrap:wrap">
    <div>
      <span style="display:block;text-transform:uppercase;letter-spacing:.12em;font-size:.75rem;color:var(--green);margin-bottom:.5rem">{cfg['lm_eyebrow']}</span>
      <h2 style="color:#fff;margin:0 0 .5rem;font-size:clamp(1.2rem,2.2vw,1.6rem);line-height:1.3">{cfg['lm_h2']}</h2>
      <p style="color:rgba(255,255,255,.6);margin:0;font-size:.94rem">{cfg['lm_p']}</p>
    </div>
    <form style="display:flex;flex-direction:column;gap:10px;min-width:220px" onsubmit="return false">
      <input type="email" placeholder="Uw e-mailadres" style="padding:11px 15px;border-radius:8px;border:1px solid rgba(255,255,255,.18);background:rgba(255,255,255,.07);color:#fff;font-size:.94rem">
      <button class="btn btn--primary" style="width:100%">{cfg['lm_btn']}</button>
    </form>
  </div>
</div></section>
<section class="section--tight section--soft" id="faq"><div class="container">
  <div class="sec-head"><div class="t">
    <span class="eyebrow">{cfg['faq_eyebrow']}</span>
    <h2 class="disp">{cfg['faq_h2']}</h2>
  </div></div>
  <div class="split">
    <div class="faq-list">
{items_html}
    </div>
    <div class="aside-card aside-dark">
      <h3>Nog een vraag?</h3>
      <p style="color:#bcbeb2;font-size:.94rem">Onze specialisten beantwoorden uw vraag persoonlijk — vrijblijvend.</p>
      <a href="contact.html" class="btn btn--primary" style="width:100%;margin-top:8px">Neem contact op</a>
      <a href="tel:+31302001020" class="btn btn--ghost" style="width:100%;margin-top:10px;color:#fff;border-color:rgba(255,255,255,.3)">+31 30 200 10 20</a>
    </div>
  </div>
</div></section>"""

P_REVIEWS = re.compile(r'\n<section[^>]+id="reviews"[^>]*>.*?</section>', re.DOTALL)
P_TEAM    = re.compile(r'\n<section[^>]+id="team"[^>]*>.*?</section>', re.DOTALL)
P_LM      = re.compile(r'\n<section class="lead-magnet">.*?</section>', re.DOTALL)
P_LM2     = re.compile(r'\n<section class="section--tight" id="download">.*?</section>', re.DOTALL)
P_FAQ     = re.compile(r'\n<section[^>]+id="faq"[^>]*>.*?</section>', re.DOTALL)
P_CTA     = re.compile(r'\n<section class="section section--tight">\s*\n\s*<div class="container">\s*\n\s*<div class="cta">.*?</section>', re.DOTALL)
# Nieuwsbrief sectie in algemeen (lead-magnet variant)
P_NL      = re.compile(r'\n<!-- ── NIEUWSBRIEF BAND.*?</section>', re.DOTALL)

for fname, cfg in PAGE_CONFIG.items():
    src = read(fname)

    # Reviews
    m = P_REVIEWS.search(src)
    if m:
        src = P_REVIEWS.sub(REVIEWS_BU, src, count=1)
        print(f'{fname}: reviews OK')

    # Team
    m = P_TEAM.search(src)
    if m:
        src = P_TEAM.sub(TEAM_BU, src, count=1)
        print(f'{fname}: team OK')

    # Lead magnet (verwijder huidig blok, dan faq vervangen door lm+faq)
    new_lm_faq = make_lm_faq(cfg)
    src = P_NL.sub('', src)   # verwijder nieuwsbrief-band in algemeen
    src = P_LM.sub('', src)   # verwijder lead-magnet sectie
    src = P_LM2.sub('', src)  # verwijder al bestaand download blok

    # FAQ vervangen door lm+faq combo
    if P_FAQ.search(src):
        src = P_FAQ.sub(new_lm_faq, src, count=1)
        print(f'{fname}: faq+lead-magnet OK')

    # CTA sectie verwijderen
    src = P_CTA.sub('', src)

    write(fname, src)
    print(f'{fname}: klaar')

print('\nAlles klaar.')
