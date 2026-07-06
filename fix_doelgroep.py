"""
fix_doelgroep.py
1. Alle 4 doelgroep-pagina's: verwijder werkwijze-sectie + FAQ-sectie(s) toegevoegd door upgrade script
2. doelgroep-gebruiker: voeg stats-band toe na bu-toc (zoals de andere 3)
3. Alle 4: vervang lead-magnet door unieke versie per pagina
"""
import re, os

ROOT = r'C:/Users/Gebruiker/spring-real-estate-concept'

def read(f):
    with open(ROOT + '/' + f, encoding='utf-8') as fh:
        return fh.read()

def write(f, s):
    with open(ROOT + '/' + f, 'w', encoding='utf-8') as fh:
        fh.write(s)
    print(f'  {f}: {len(s.splitlines())}L')

def remove_section_by_id(src, section_id):
    """Verwijder ALLE secties met id=section_id."""
    pattern = re.compile(
        r'\n<section[^>]+id=["\']' + re.escape(section_id) + r'["\'][^>]*>.*?</section>',
        re.DOTALL
    )
    return pattern.sub('', src)

def remove_werkwijze(src):
    """Verwijder section--soft id=werkwijze (de toegevoegde aanpak-sectie)."""
    return remove_section_by_id(src, 'werkwijze')

def replace_lead_magnet(src, new_lm_html):
    """Vervang de volledige lead-magnet sectie."""
    pattern = re.compile(r'<section class="lead-magnet">.*?</section>', re.DOTALL)
    # ook wrapper-variant: section--tight > container > div.lead-magnet
    pattern2 = re.compile(
        r'<section class="section--tight"><div class="container"><div class="lead-magnet">.*?</div></div></section>',
        re.DOTALL
    )
    new, n = pattern.subn(new_lm_html, src)
    if not n:
        new, n = pattern2.subn(new_lm_html, src)
    return new, n

# ── Unieke lead-magnet HTML per pagina ───────────────────────────────────────

LM_GEBRUIKER = '''<section class="lead-magnet" style="background:linear-gradient(135deg,#3a7d2c 0%,#7CA73F 60%,#5a9b32 100%)">
<div class="container"><div class="lm-inner">
  <div class="lm-text">
    <span class="eyebrow">Gratis kantoorzoekgids</span>
    <h2>Vind het perfecte kantoor — <em>zonder gedoe</em></h2>
    <p>Onze praktische gids helpt u van zoekprofiel tot sleuteloverdracht. Inclusief checklist, huurprijsoverzicht en onderhandeltips.</p>
  </div>
  <form class="lm-form" onsubmit="return false">
    <input type="email" placeholder="Uw e-mailadres">
    <button class="btn btn--primary btn--lg">Gids ontvangen</button>
  </form>
</div></div></section>'''

LM_EIGENAAR = '''<section class="lead-magnet" style="background:linear-gradient(135deg,#1a3a5c 0%,#2d6a9f 60%,#1e4f7a 100%)">
<div class="container"><div class="lm-inner">
  <div class="lm-text">
    <span class="eyebrow">Gratis verhuurwaarde-analyse</span>
    <h2>Wat is uw pand waard op de <em>huurmarkt?</em></h2>
    <p>Ontvang een onderbouwde marktanalyse van uw object — inclusief huurprijsbenchmark, doelgroepadvies en verhuurstrategie op maat.</p>
  </div>
  <form class="lm-form" onsubmit="return false">
    <input type="email" placeholder="Uw e-mailadres">
    <button class="btn btn--primary btn--lg" style="background:#fff;color:#1a3a5c">Analyse aanvragen</button>
  </form>
</div></div></section>'''

LM_INVESTEERDER = '''<section class="lead-magnet" style="background:linear-gradient(135deg,#2c1a4a 0%,#5a3d8a 60%,#3d2466 100%)">
<div class="container"><div class="lm-inner">
  <div class="lm-text">
    <span class="eyebrow">Exclusief voor beleggers</span>
    <h2>Spring Beleggingsscan — <em>gratis en vrijblijvend</em></h2>
    <p>Ontvang een persoonlijke scan van uw beleggingsprofiel met actuele BAR-rendementen, marktkansen en een selectie van passende objecten uit onze database.</p>
  </div>
  <form class="lm-form" onsubmit="return false">
    <input type="email" placeholder="Uw e-mailadres">
    <button class="btn btn--primary btn--lg" style="background:#F4BD2A;color:#1a1a2e;border-color:#F4BD2A">Beleggingsscan ontvangen</button>
  </form>
</div></div></section>'''

LM_ONTWIKKELAAR = '''<section class="lead-magnet" style="background:linear-gradient(135deg,#3a2010 0%,#8B4513 60%,#5c3010 100%)">
<div class="container"><div class="lm-inner">
  <div class="lm-text">
    <span class="eyebrow">Gratis voor projectontwikkelaars</span>
    <h2>Projectscan: is uw locatie <em>verhuurbaar?</em></h2>
    <p>Spring analyseert uw ontwikkellocatie gratis — inclusief doelgroepanalyse, concurrentiescan, verwacht huurpotentieel en pre-let strategie-advies.</p>
  </div>
  <form class="lm-form" onsubmit="return false">
    <input type="email" placeholder="Uw e-mailadres">
    <button class="btn btn--primary btn--lg" style="background:#fff;color:#3a2010">Projectscan aanvragen</button>
  </form>
</div></div></section>'''

# ── Stats-band voor doelgroep-gebruiker (ontbreekt) ──────────────────────────

STATS_GEBRUIKER = '''
<section class="section--tight section--soft"><div class="container">
  <div class="stats-band"><div class="grid">
    <div><b>500+</b><span>kantoorgebruikers begeleid</span></div>
    <div><b>6&nbsp;wkn</b><span>gem. doorlooptijd aanhuur</span></div>
    <div><b>98%</b><span>klanttevredenheid</span></div>
    <div><b>Off-market</b><span>aanbod via SpringBase</span></div>
  </div></div>
</div></section>'''

# ── Pas pagina's aan ──────────────────────────────────────────────────────────

pages = [
    ('doelgroep-gebruiker.html',    LM_GEBRUIKER,    True),
    ('doelgroep-eigenaar.html',     LM_EIGENAAR,     False),
    ('doelgroep-investeerder.html', LM_INVESTEERDER, False),
    ('doelgroep-ontwikkelaar.html', LM_ONTWIKKELAAR, False),
]

for fname, lm_html, add_stats in pages:
    src = read(fname)

    # 1. Verwijder werkwijze sectie
    src = remove_werkwijze(src)

    # 2. Verwijder FAQ sectie(s)
    src = remove_section_by_id(src, 'faq')

    # 3. Voeg stats-band toe na bu-toc (alleen gebruiker)
    if add_stats and STATS_GEBRUIKER.strip() not in src:
        src = src.replace(
            '\n<section class="section--tight section--soft"',
            STATS_GEBRUIKER + '\n<section class="section--tight section--soft"',
            1  # alleen de eerste
        )
        # Als die class er niet is, insert na </nav> van bu-toc
        if STATS_GEBRUIKER.strip() not in src:
            src = src.replace(
                '</nav>\n',
                '</nav>\n' + STATS_GEBRUIKER + '\n',
                1
            )

    # 4. Vervang lead-magnet
    src, n = replace_lead_magnet(src, lm_html)
    if not n:
        print(f'  WAARSCHUWING: lead-magnet niet gevonden in {fname}')

    write(fname, src)

print('\nKlaar.')
