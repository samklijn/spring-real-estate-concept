import re

def read(f):
    with open(f, encoding='utf-8') as fh: return fh.read()
def write(f, s):
    with open(f, 'w', encoding='utf-8') as fh: fh.write(s)

def bu_dl(ey, h2, p, btn):
    return (
        '\n<section class="section--tight" id="download"><div class="container">\n'
        '  <div style="background:var(--ink);border-radius:16px;padding:36px 48px;'
        'display:grid;grid-template-columns:1fr auto;align-items:center;gap:40px;flex-wrap:wrap">\n'
        '    <div>\n'
        '      <span style="display:block;text-transform:uppercase;letter-spacing:.12em;font-size:.75rem;color:var(--green);margin-bottom:.5rem">' + ey + '</span>\n'
        '      <h2 style="color:#fff;margin:0 0 .5rem;font-size:clamp(1.2rem,2.2vw,1.6rem);line-height:1.3">' + h2 + '</h2>\n'
        '      <p style="color:rgba(255,255,255,.6);margin:0;font-size:.94rem">' + p + '</p>\n'
        '    </div>\n'
        '    <form style="display:flex;flex-direction:column;gap:10px;min-width:220px" onsubmit="return false">\n'
        '      <input type="email" placeholder="Uw e-mailadres" style="padding:11px 15px;border-radius:8px;border:1px solid rgba(255,255,255,.18);background:rgba(255,255,255,.07);color:#fff;font-size:.94rem">\n'
        '      <button class="btn btn--primary" style="width:100%">' + btn + '</button>\n'
        '    </form>\n'
        '  </div>\n'
        '</div></section>'
    )

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

P_LM  = re.compile(r'\n<section class="lead-magnet">.*?</section>', re.DOTALL)
P_SEC = lambda s: re.compile(r'\n<section[^>]+id="' + s + r'"[^>]*>.*?</section>', re.DOTALL)
P_CTA = re.compile(r'\n<section[^>]*>\s*\n?\s*<div class="container">\s*\n?\s*<div class="cta">.*?</section>', re.DOTALL)

# ── 1. listings.html ────────────────────────────────────────────────────────
print('listings.html')
src = read('listings.html')
src = P_LM.sub(bu_dl('Object niet gevonden?', 'Vraag naar ons <em>off-market aanbod</em>',
    'Het meeste vastgoed wordt nooit online gepubliceerd. Via SpringBase hebben we toegang tot off-market kantoren, bedrijfsruimten en beleggingsobjecten.',
    'Off-market aanbod opvragen'), src, count=1)
faq_items = (
    '\n      <details class="faq-item" open><summary><span>Hoe vind ik de juiste kantoorruimte in Amsterdam?</span><span class="pl">+</span></summary><div class="ans">Spring helpt u door het aanbod in Amsterdam heen. Onze specialisten kennen de Zuidas, het WTC en de Mahlerbuurt als geen ander.</div></details>'
    '\n      <details class="faq-item"><summary><span>Kan ik ook een kantoor huren in Utrecht?</span><span class="pl">+</span></summary><div class="ans">Ja, Spring is actief in het hart van Utrecht (Stationsgebied, Leidsche Rijn) en omgeving. Bekijk ons aanbod of bel ons voor actueel beschikbaar aanbod.</div></details>'
    '\n      <details class="faq-item"><summary><span>Wat is het verschil tussen huren en een serviced office?</span><span class="pl">+</span></summary><div class="ans">Bij een klassieke huur sluit u een direct huurcontract af. Bij een serviced office huurt u een flexibele werkplek inclusief diensten als receptie, schoonmaak en internet.</div></details>'
    '\n      <details class="faq-item"><summary><span>Helpt Spring ook bij vastgoed in Spanje?</span><span class="pl">+</span></summary><div class="ans">Ja. Spring Real Estate is actief in Valencia en Estepona. Wij begeleiden Nederlandse investeerders en bedrijven bij commercieel en residentieel vastgoed in Spanje.</div></details>\n    '
)
src = re.sub(r'\n<section class="section faq-band">.*?</section>', bu_faq('Veelgestelde vragen', 'Vragen over <em>ons aanbod</em>', faq_items), src, count=1, flags=re.DOTALL)
write('listings.html', src)
print('  OK')

# ── 2. cases.html ───────────────────────────────────────────────────────────
print('cases.html')
src = read('cases.html')
src = P_SEC('expertises').sub('', src, count=1)
src = P_SEC('werkwijze').sub('', src, count=1)
write('cases.html', src)
print('  OK')

# ── 3. transacties.html ─────────────────────────────────────────────────────
print('transacties.html')
src = read('transacties.html')
src = P_SEC('werkwijze').sub('', src, count=1)
src = src.replace('<section class="section section--soft" id="transacties">', '<section class="section section--tight" id="transacties">')

def fix_card(m):
    html = m.group(0)
    cat_m   = re.search(r'data-cat="([^"]+)"', html)
    img_m   = re.search(r'src="([^"]+)"[^>]*alt="([^"]+)"', html)
    title_m = re.search(r'<h3>(.*?)</h3>', html)
    meta_m  = re.search(r'<p class="blog-meta">(.*?)</p>', html)
    badge_m = re.search(r'<span class="cat-badge">(.*?)</span>', html)
    if not (cat_m and title_m and meta_m): return html
    return ('\n<a class="blog-card" href="#" data-cat="' + cat_m.group(1) + '">\n'
        '  <div class="ph"><img src="' + (img_m.group(1) if img_m else '') + '" alt="' + (img_m.group(2) if img_m else '') + '" loading="lazy"></div>\n'
        '  <div class="body"><span class="cat">' + (badge_m.group(1) if badge_m else '') + '</span>\n'
        '    <h3>' + title_m.group(1) + '</h3>\n'
        '    <p class="muted" style="font-size:.85rem;margin:.5rem 0 0">' + meta_m.group(1) + '</p>\n'
        '  </div>\n</a>')

src = re.sub(r'\n<div class="blog-card"[^>]*>.*?</div>\n</div>\n</div>', fix_card, src, flags=re.DOTALL)
write('transacties.html', src)
print('  OK')

# ── 4. agents.html ──────────────────────────────────────────────────────────
print('agents.html')
src = read('agents.html')
src = re.sub(r'\n<section class="section--soft"><div class="container">\s*<div class="sec-head">.*?Vragen over ons.*?</section>', '', src, count=1, flags=re.DOTALL)
src = P_LM.sub(bu_dl('Kennismaken?', 'Spreek direct met een <em>Spring-specialist</em>',
    'Onze adviseurs zijn beschikbaar voor een vrijblijvend kennismakingsgesprek — online of op kantoor in Utrecht of Amsterdam.',
    'Gesprek inplannen'), src, count=1)
src = src.replace('<section class="section--soft" id="faq">', '<section class="section--tight section--soft" id="faq">')
write('agents.html', src)
print('  OK')

# ── 5. vacatures.html ───────────────────────────────────────────────────────
print('vacatures.html')
src = read('vacatures.html')
src = src.replace('<div class="values-grid">', '<div class="usp-grid">')
src = re.sub(r'<div class="value"><div class="ic">.*?</div>', '<div class="usp">', src, flags=re.DOTALL)
src = re.sub(
    r'(<section class="section"><div class="container">\s*<div class="sec-head">.*?Arbeidsvoorwaarden)',
    lambda m: m.group(0).replace('<section class="section">', '<section class="section section--soft">'),
    src, count=1, flags=re.DOTALL
)
hero_pat = re.compile(r'\n<section class="section--tight"><div class="container">\s*<div class="hero-stats".*?</section>', re.DOTALL)
matches = list(hero_pat.finditer(src))
if len(matches) >= 2:
    m2 = matches[1]
    src = src[:m2.start()] + src[m2.end():]
    print('  dup stats removed')
faq_m = re.search(r'\n<section class="section--soft"><div class="container">\s*<div class="sec-head">.*?Vragen over.*?<div class="faq-list">(.*?)</div>\s*</div></section>', src, re.DOTALL)
if faq_m:
    src = src[:faq_m.start()] + bu_faq('Veelgestelde vragen', 'Vragen over <em>solliciteren</em>', faq_m.group(1), 'Direct contact?') + src[faq_m.end():]
    print('  faq split OK')
src = re.sub(r'\n<section class="section--tight"><div class="container"><div class="cta">.*?</section>', '', src, count=1, flags=re.DOTALL)
src = P_LM.sub(bu_dl('Open sollicitatie', 'Geen passende vacature? <em>We maken graag kennis</em>',
    'Spring groeit continu. Stuur uw open sollicitatie en we nemen contact op zodra er een passende rol beschikbaar is.',
    'Open sollicitatie sturen'), src, count=1)
write('vacatures.html', src)
print('  OK')

# ── 6. Locatie pages ────────────────────────────────────────────────────────
LOCATIES = [
    ('locatie-amsterdam.html', 'Gratis marktrapport', 'Amsterdam Vastgoedmarkt Q2 2026 — <em>actuele data</em>',
     'Actuele huurprijzen, BAR-rendementen en transactiedata voor Amsterdam en de Zuidas — van Spring Research.', 'Rapport ontvangen'),
    ('locatie-utrecht.html', 'Gratis marktrapport', 'Utrecht Vastgoedmarkt Q2 2026 — <em>actuele data</em>',
     'Actuele huurprijzen, leegstandscijfers en transactiedata voor Utrecht en het Stationsgebied.', 'Rapport ontvangen'),
    ('locatie-valencia.html', 'Gratis marktgids', 'Investeren in Valencia — <em>Spring Spain gids</em>',
     'Marktoverzicht, BAR-rendementen en praktische gids voor vastgoed in Valencia.', 'Gids ontvangen'),
    ('locatie-estepona.html', 'Gratis marktgids', 'Investeren in Estepona — <em>Spring Spain gids</em>',
     'Marktoverzicht en praktische gids voor vastgoed aan de Costa del Sol.', 'Gids ontvangen'),
]
for fname, ey, h2, p, btn in LOCATIES:
    print(fname)
    src = read(fname)
    src = P_SEC('faq').sub('', src, count=1)
    src = P_CTA.sub('', src, count=1)
    src = re.sub(r'\n<section class="section section--tight">\s*<div class="container">\s*<div class="cta">.*?</section>', '', src, count=1, flags=re.DOTALL)
    src = P_LM.sub(bu_dl(ey, h2, p, btn), src, count=1)
    write(fname, src)
    print('  OK')

print('\nAlles klaar.')
