import re, os
ROOT = r'C:/Users/Gebruiker/spring-real-estate-concept'

def read(f):
    with open(ROOT+'/'+f, encoding='utf-8') as fh: return fh.read()

def write(f, s):
    with open(ROOT+'/'+f, 'w', encoding='utf-8') as fh: fh.write(s)
    print(f'  {f}: {len(s.splitlines())}L')

def after_hero(src, html):
    """Insert html right after the first </section> that closes page-hero"""
    i = src.index('<section class="page-hero"')
    after = src[i:]
    end = after.index('</section>') + len('</section>')
    pos = i + end
    return src[:pos] + '\n' + html + src[pos:]

def before_talkstrip(src, html):
    return src.replace('\n<section class="talk-strip">', html + '\n<section class="talk-strip">')

# ── Shared components ──────────────────────────────────────────────────────────

def BUTOC(links):
    inner = ''.join(f'<a href="#{slug}">{label}</a>' for slug, label in links)
    return f'<nav class="bu-toc"><div class="container">\n  {inner}\n</div></nav>'

REVIEWS = '''<section class="section" id="reviews" style="background:var(--green-tint)"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Reviews</span><h2 class="disp">Wat klanten <em>zeggen</em></h2></div></div>
  <div class="rev-grid">
    <div class="review"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>"Spring dacht echt mee en leverde sneller resultaat dan verwacht."</p><div class="who"><span class="av">JV</span><span><b>Jeroen V.</b><br><small>Scale-up, Utrecht</small></span></div></div>
    <div class="review"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>"Transparant, deskundig en datagedreven advies. Altijd bereikbaar."</p><div class="who"><span class="av">MK</span><span><b>Marit K.</b><br><small>Corporate vastgoed</small></span></div></div>
    <div class="review"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>"Een betrouwbare partner voor elk vastgoedvraagstuk."</p><div class="who"><span class="av">RG</span><span><b>Rafael G.</b><br><small>Investeerder</small></span></div></div>
  </div>
</div></section>'''

def LEAD_MAGNET(eyebrow, h2, p, btn):
    return f'''<section class="lead-magnet"><div class="container"><div class="lm-inner">
  <div class="lm-text"><span class="eyebrow">{eyebrow}</span><h2>{h2}</h2><p>{p}</p></div>
  <form class="lm-form" onsubmit="return false"><input type="email" placeholder="Uw e-mailadres"><button class="btn btn--primary btn--lg">{btn}</button></form>
</div></div></section>'''

def WERKWIJZE(steps):
    items = ''
    for i, (title, desc) in enumerate(steps, 1):
        items += f'\n    <div class="bu-step"><div class="n">{i}</div><h3>{title}</h3><p>{desc}</p></div>'
    return f'''<section class="section--soft" id="werkwijze"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Onze aanpak</span><h2 class="disp">Stap voor stap <em>resultaat</em></h2></div></div>
  <div class="bu-steps">{items}
  </div>
</div></section>'''

def AGENT(photo, name, role, email):
    return f'''<div class="agent"><div class="ph"><img src="images/team/{photo}" alt="{name}"></div><div class="body"><div class="name">{name}</div><div class="role">{role}</div><div class="socials"><a href="https://linkedin.com/company/spring-real-estate-nl" target="_blank" rel="noopener" aria-label="LinkedIn">in</a><a href="mailto:{email}" aria-label="E-mail">@</a></div></div></div>'''

def TEAM(agents):
    agents_html = '\n  '.join(AGENT(*a) for a in agents)
    return f'''<section class="section dark-sec" id="team"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow" style="color:var(--green-soft,#9DC76B)">Het team</span><h2 class="disp" style="color:#fff">Uw <em>experts</em></h2></div><a href="agents.html" class="btn btn--secondary">Heel het team</a></div>
  <div class="team-grid">
  {agents_html}
  </div>
</div></section>'''

def FAQ(title, items):
    details = ''
    for i, (q, a) in enumerate(items):
        open_attr = ' open' if i == 0 else ''
        details += f'\n      <details class="faq-item"{open_attr}><summary><span>{q}</span><span class="pl">+</span></summary><div class="ans">{a}</div></details>'
    return f'''<section class="section--soft" id="faq"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Veelgestelde vragen</span><h2 class="disp">FAQ: <em>{title}</em></h2></div></div>
  <div class="split">
    <div class="faq-list">{details}
    </div>
    <div class="aside-card aside-dark"><h3>Nog een vraag?</h3><p style="color:#bcbeb2;font-size:.94rem">Onze specialisten beantwoorden hem graag &#8212; vrijblijvend.</p><a href="contact.html" class="btn btn--primary" style="width:100%;margin-top:8px">Stel uw vraag</a><a href="tel:+31302001020" class="btn btn--ghost" style="width:100%;margin-top:10px;color:#fff;border-color:rgba(255,255,255,.3)">+31 30 200 10 20</a></div>
  </div>
</div></section>'''

# ── Page definitions ───────────────────────────────────────────────────────────

pages = []

# 1. doelgroep-gebruiker.html
werkwijze_gebruiker = WERKWIJZE([
    ("Inventarisatie", "We brengen uw huisvestingswens in kaart: m², locatie, budget, tijdlijn en specifieke eisen aan de werkplek."),
    ("Marktverkenning", "Via SpringBase doorzoeken we het volledige aanbod — ook off-market objecten die niet op Funda staan."),
    ("Bezichtigingen &amp; advies", "We selecteren de beste opties en begeleiden alle bezichtigingen — met objectief advies over voor- en nadelen van elk pand."),
    ("Onderhandeling &amp; oplevering", "Spring onderhandelt namens u over huurprijs, incentives en contractvoorwaarden. Tot en met de sleuteloverdracht."),
])
team_gebruiker = TEAM([
    ("bas.sijbom.jpg", "Bas Sijbom", "Partner Agency", "bas.sijbom@springrealestate.com"),
    ("ivar.hillerstrom.jpg", "Ivar Hillerstrom", "Partner Agency", "ivar.hillerstrom@springrealestate.com"),
])
lm_gebruiker = LEAD_MAGNET("Gratis gids", "De complete kantoorzoekgids", "Alles wat u moet weten als kantoorhuurder — van zoekprofiel tot contractonderhandeling.", "Gids ontvangen")
faq_gebruiker = FAQ("kantoorgebruikers", [
    ("Hoe lang duurt een gemiddeld kantoorzoektraject?", "Afhankelijk van uw eisen en de markt: gemiddeld 4-12 weken. In krappe markten zoals Zuidas kan het langer duren — daarom werken we altijd met een parallelle off-market zoekstrategie."),
    ("Wat kost de begeleiding van Spring als huurder?", "In de meeste gevallen is onze dienstverlening voor de huurder kosteloos — Spring wordt door de verhuurder beloond. We zijn hier altijd transparant over."),
    ("Kan Spring ook helpen met de inrichting?", "Ja. Via Spring Design &amp; Build verzorgen we de volledige kantoorinrichting — van concept tot oplevering. Zo hoeft u maar één aanspreekpunt te hebben."),
])
pages.append({
    'file': 'doelgroep-gebruiker.html',
    'toc': BUTOC([('werkwijze','Aanpak'), ('team','Team'), ('reviews','Reviews'), ('faq','FAQ')]),
    'extra': '\n' + werkwijze_gebruiker + '\n' + team_gebruiker + '\n' + REVIEWS + '\n' + lm_gebruiker + '\n' + faq_gebruiker,
})

# 2. doelgroep-eigenaar.html
werkwijze_eigenaar = WERKWIJZE([
    ("Opname &amp; analyse", "We analyseren uw object grondig: technische staat, marktpositie, doelgroep en optimale huurprijs. Onderbouwd met actuele SpringBase-data."),
    ("Verhuurstrategie", "We stellen een maatwerkstrategie op: welke doelgroep past bij uw pand, welke aanpassingen maximaliseren de verhuurbaarheid?"),
    ("Marketing &amp; bezichtigingen", "Professionele fotografie, 3D-plattegronden, gerichte outreach en begeleiding van alle bezichtigingen — volledig ontzorgd."),
    ("Ondertekening &amp; nazorg", "We begeleiden de onderhandeling, opstelling van de huurovereenkomst en overdracht. Daarna blijven we beschikbaar voor vragen."),
])
team_eigenaar = TEAM([
    ("edgar.willems.jpg", "Edgar Willems", "Partner Agency", "edgar.willems@springrealestate.com"),
    ("rolf.vermeer.jpg", "Rolf Vermeer", "Partner Agency", "rolf.vermeer@springrealestate.com"),
])
lm_eigenaar = LEAD_MAGNET("Gratis verhuuradvies", "Wat is uw pand waard op de huurmarkt?", "Ontvang een gratis huurwaardeanalyse van uw object — inclusief marktpositionering en verhuurstrategie.", "Analyse aanvragen")
faq_eigenaar = FAQ("vastgoedeigenaren", [
    ("Wat is een realistische verhuurperiode voor mijn kantoor?", "Afhankelijk van locatie, staat en huurprijs: gemiddeld 6-12 weken. Spring haalt gemiddeld 6 weken doorlooptijd dankzij actieve huurdersdatabase en off-market netwerk."),
    ("Moet ik mijn pand aanpassen voor verhuur?", "Niet altijd. We adviseren u welke aanpassingen de meeste huurwaarde toevoegen versus de investeringskosten. Soms is een schoonmaak voldoende; soms is een herinrichting de sleutel."),
    ("Kan Spring ook het beheer overnemen na verhuur?", "Ja. Via Spring Asset Management en Property Management verzorgen wij het volledige beheer — van huurderscontact tot technisch onderhoud."),
])
pages.append({
    'file': 'doelgroep-eigenaar.html',
    'toc': BUTOC([('werkwijze','Aanpak'), ('team','Team'), ('reviews','Reviews'), ('faq','FAQ')]),
    'extra': '\n' + werkwijze_eigenaar + '\n' + team_eigenaar + '\n' + REVIEWS + '\n' + lm_eigenaar + '\n' + faq_eigenaar,
})

# 3. doelgroep-investeerder.html
werkwijze_investeerder = WERKWIJZE([
    ("Beleggingsprofiel", "We definiëren samen uw beleggingsdoelen: risicoprofiel, gewenst rendement (BAR/NAR), looptijd en voorkeur voor asset type en locatie."),
    ("Marktscan &amp; selectie", "SpringBase scant real-time het volledige aanbod — inclusief off-market objecten. We selecteren alleen objecten die passen bij uw profiel."),
    ("Due diligence &amp; taxatie", "Onze RICS/NRVT-gecertificeerde taxateurs analyseren de waarde, het huurpotentieel en de risico's van elk object grondig."),
    ("Acquisitie &amp; beheer", "Na aankoop kunt u het beheer aan Spring overdragen — van huurincasso en administratie tot technisch onderhoud en herpositionering."),
])
team_investeerder = TEAM([
    ("ivar.hillerstrom.jpg", "Ivar Hillerstrom", "Partner Agency", "ivar.hillerstrom@springrealestate.com"),
    ("edgar.willems.jpg", "Edgar Willems", "Partner Agency", "edgar.willems@springrealestate.com"),
])
lm_investeerder = LEAD_MAGNET("Gratis beleggingsgids", "Beleggen in commercieel vastgoed in 2026", "BAR-rendementen, risicoanalyse en de beste markten — de complete gids voor beleggers van Spring Research.", "Gids ontvangen")
faq_investeerder = FAQ("beleggers", [
    ("Wat zijn huidige BAR-rendementen voor kantoren?", "Prime kantoren in Amsterdam (Zuidas) staan op circa 5,5%. Buiten de randstad liggen rendementen op 6,5-7,5%. Logistiek en lichtindustrieel scoort 6-7,5%. Actuele data via Spring Research."),
    ("Is beleggen in Spanje interessant voor Nederlandse investeerders?", "Ja. Valencia en Estepona bieden rendementen van 6-8% bij aankoopprijzen die 40-60% lager liggen dan vergelijkbare objecten in Amsterdam. Spring begeleidt het volledige traject vanuit Nederland."),
    ("Wat is het minimale investeringsbedrag bij Spring?", "Spring begeleidt transacties vanaf €500.000. Voor kleinere beleggers bieden we portefeuilleadvies en verwijzing naar geschikte fondsen."),
])
pages.append({
    'file': 'doelgroep-investeerder.html',
    'toc': BUTOC([('werkwijze','Aanpak'), ('team','Team'), ('reviews','Reviews'), ('faq','FAQ')]),
    'extra': '\n' + werkwijze_investeerder + '\n' + team_investeerder + '\n' + REVIEWS + '\n' + lm_investeerder + '\n' + faq_investeerder,
})

# 4. doelgroep-ontwikkelaar.html
werkwijze_ontwikkelaar = WERKWIJZE([
    ("Projectscan", "We analyseren uw ontwikkelproject: locatie, doelgroep, concurrentieanalyse en realistisch verhuur- of verkooppotentieel op basis van actuele marktdata."),
    ("Positionering &amp; programma", "We adviseren over het optimale programma: welk type huurder of koper past bij de locatie en hoe positioneert u zich ten opzichte van de concurrentie?"),
    ("Verhuurstrategie &amp; marketing", "Van BREEAM-communicatie tot gerichte campagnes voor eindgebruikers — Spring verzorgt de volledige verhuurmarketing en pre-let strategie."),
    ("Oplevering &amp; nazorg", "We begeleiden de overdracht, huurdersbegeleiding bij oplevering en blijven beschikbaar voor herpositionering of uitbreiding na ingebruikname."),
])
team_ontwikkelaar = TEAM([
    ("edgar.willems.jpg", "Edgar Willems", "Partner Agency", "edgar.willems@springrealestate.com"),
    ("rolf.vermeer.jpg", "Rolf Vermeer", "Partner Agency", "rolf.vermeer@springrealestate.com"),
])
lm_ontwikkelaar = LEAD_MAGNET("Gratis advies", "Pre-let strategie voor uw ontwikkelproject", "Ontvang een gratis projectscan — inclusief marktpositionering, doelgroepanalyse en verwacht huurpotentieel.", "Projectscan aanvragen")
faq_ontwikkelaar = FAQ("projectontwikkelaars", [
    ("Wanneer moet ik Spring inschakelen bij een nieuwbouwproject?", "Zo vroeg mogelijk — bij voorkeur al in de ontwerpfase. Zo kunnen we het programma en de plattegronden nog beïnvloeden op basis van wat huurders daadwerkelijk zoeken."),
    ("Wat is een realistisch pre-let percentage voor een nieuw kantoorpand?", "Banken vereisen doorgaans 30-50% pre-let voor financiering. Spring heeft een actieve database van huurders-in-oriëntatie waarmee we pre-let trajecten versnellen."),
    ("Begeleidt Spring ook transformatieprojecten?", "Ja. Van kantoor naar woningen, van logistiek naar mixed-use — Spring adviseert over haalbaarheid, bestemmingswijziging en verhuur-/verkoopstrategie na transformatie."),
])
pages.append({
    'file': 'doelgroep-ontwikkelaar.html',
    'toc': BUTOC([('werkwijze','Aanpak'), ('team','Team'), ('reviews','Reviews'), ('faq','FAQ')]),
    'extra': '\n' + werkwijze_ontwikkelaar + '\n' + team_ontwikkelaar + '\n' + REVIEWS + '\n' + lm_ontwikkelaar + '\n' + faq_ontwikkelaar,
})

# 5. contact.html
lm_contact = LEAD_MAGNET("Gratis intake", "Liever eerst een kennismakingsgesprek?", "Plan een vrijblijvend gesprek van 30 minuten met een van onze specialisten. Online of op kantoor.", "Afspraak inplannen")
pages.append({
    'file': 'contact.html',
    'toc': BUTOC([('contact','Contact'), ('team','Team'), ('faq','FAQ')]),
    'extra': '\n' + REVIEWS + '\n' + lm_contact,
})

# 6. agents.html
lm_agents = LEAD_MAGNET("Kennismaken?", "Spreek direct met een specialist", "Onze adviseurs zijn beschikbaar voor een vrijblijvend kennismakingsgesprek — online of op kantoor in Utrecht of Amsterdam.", "Gesprek inplannen")
faq_agents = FAQ("ons team", [
    ("Hoe kies ik de juiste Spring-specialist?", "Gebruik de filter hierboven om te zoeken op dienst, locatie of naam. U kunt ook contact opnemen via info@springrealestate.com — wij koppelen u dan aan de meest passende adviseur."),
    ("Werkt Spring ook met externe specialisten?", "Spring heeft een netwerk van vaste partners: notarissen, fiscalisten, architecten en bouwkundigen. Via ons één-loket-principe regelen we de coördinatie."),
    ("Zijn Spring-adviseurs gecertificeerd?", "Ja. Onze makelaars zijn NVM en VBO-gecertificeerd. Onze taxateurs zijn RICS en NRVT-gecertificeerd. Zie de profielpagina per adviseur voor specifieke kwalificaties."),
])
pages.append({
    'file': 'agents.html',
    'toc': BUTOC([('team','Het team'), ('reviews','Reviews'), ('faq','FAQ')]),
    'extra': '\n' + REVIEWS + '\n' + lm_agents + '\n' + faq_agents,
})

# 7. vacatures.html
lm_vacatures = LEAD_MAGNET("Open sollicitatie", "Geen passende vacature gevonden?", "Spring groeit continu. Stuur uw open sollicitatie en we nemen contact op zodra er een passende rol beschikbaar is.", "Open sollicitatie sturen")
pages.append({
    'file': 'vacatures.html',
    'toc': BUTOC([('vacatures','Vacatures'), ('werkwijze','Solliciteren'), ('team','Team'), ('faq','FAQ')]),
    'extra': '\n' + lm_vacatures,
})

# 8. locaties.html
lm_locaties = LEAD_MAGNET("Vestigingskeuze", "Welke Spring-vestiging past bij uw vraag?", "Onze adviseurs helpen u bepalen welk kantoor het beste uw vraagstuk kan begeleiden — in Nederland of Spanje.", "Neem contact op")
faq_locaties = FAQ("onze vestigingen", [
    ("Wat is het verschil tussen de vestigingen Utrecht en Amsterdam?", "Utrecht is ons hoofdkantoor met alle 18 business units onder één dak. Amsterdam is gespecialiseerd in de Zuidas-markt en internationale bedrijven. Voor de meeste vraagstukken kunt u bij beide terecht."),
    ("Helpt Spring ook in andere Nederlandse steden?", "Ja. Vanuit Utrecht en Amsterdam bedienen we heel Nederland. We hebben actieve netwerken in Rotterdam, Den Haag, Eindhoven en de G10-steden."),
    ("Wat doet Spring in Spanje?", "Via onze vestigingen in Valencia en Estepona begeleiden we Nederlandse investeerders bij aankoop, verhuur en beheer van vastgoed in Spanje. Volledig Nederlandstalig."),
])
pages.append({
    'file': 'locaties.html',
    'toc': BUTOC([('locaties','Locaties'), ('reviews','Reviews'), ('faq','FAQ')]),
    'extra': '\n' + REVIEWS + '\n' + lm_locaties + '\n' + faq_locaties,
})

# 9. listings.html — no TOC, only lead-magnet before talk-strip
lm_listings = LEAD_MAGNET("Object niet gevonden?", "Vraag naar ons off-market aanbod", "Het meeste vastgoed wordt nooit online gepubliceerd. Via SpringBase hebben we toegang tot off-market kantoren, bedrijfsruimten en beleggingsobjecten.", "Off-market aanbod opvragen")
pages.append({
    'file': 'listings.html',
    'toc': None,
    'extra': '\n' + lm_listings,
})

# ── Process each page ──────────────────────────────────────────────────────────

for page in pages:
    f = page['file']
    fpath = ROOT + '/' + f
    if not os.path.exists(fpath):
        print(f'  SKIP {f}: file not found')
        continue

    src = read(f)
    added = []

    # Insert bu-toc after hero (skip if already present)
    if page['toc'] is not None:
        if 'bu-toc' in src:
            print(f'  {f}: bu-toc already present, skipping TOC insert')
        else:
            try:
                src = after_hero(src, page['toc'])
                added.append('bu-toc')
            except ValueError as e:
                print(f'  {f}: could not insert bu-toc -- {e}')

    # Append extra sections before talk-strip (guard per component)
    if '\n<section class="talk-strip">' not in src:
        print(f'  {f}: talk-strip not found, skipping extra sections')
    else:
        extra_to_add = page['extra']
        # Guard against duplicate reviews
        if 'id="reviews"' in src and 'id="reviews"' in extra_to_add:
            extra_to_add = re.sub(r'<section[^>]*id="reviews"[^>]*>.*?</section>', '', extra_to_add, flags=re.DOTALL)
            print(f'  {f}: reviews already present, skipped')
        # Guard against duplicate lead-magnet
        if 'class="lead-magnet"' in src and 'class="lead-magnet"' in extra_to_add:
            extra_to_add = re.sub(r'<section class="lead-magnet">.*?</section>', '', extra_to_add, flags=re.DOTALL)
            print(f'  {f}: lead-magnet already present, skipped')
        # Guard against duplicate werkwijze
        if 'id="werkwijze"' in src and 'id="werkwijze"' in extra_to_add:
            extra_to_add = re.sub(r'<section[^>]*id="werkwijze"[^>]*>.*?</section>', '', extra_to_add, flags=re.DOTALL)
            print(f'  {f}: werkwijze already present, skipped')
        # Guard against duplicate team
        if 'id="team"' in src and 'id="team"' in extra_to_add:
            extra_to_add = re.sub(r'<section[^>]*id="team"[^>]*>.*?</section>', '', extra_to_add, flags=re.DOTALL)
            print(f'  {f}: team already present, skipped')
        # Guard against duplicate faq
        if 'id="faq"' in src and 'id="faq"' in extra_to_add:
            extra_to_add = re.sub(r'<section[^>]*id="faq"[^>]*>.*?</section>', '', extra_to_add, flags=re.DOTALL)
            print(f'  {f}: faq already present, skipped')

        if extra_to_add.strip():
            src = before_talkstrip(src, extra_to_add)
            added.append('extra sections')

    if added:
        write(f, src)
        print(f'  {f}: added {", ".join(added)}')
    else:
        print(f'  {f}: nothing to add (all sections already present)')

print('\nDone.')
