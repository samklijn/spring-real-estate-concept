"""
fix_all_pages.py
- Verwijder grote CTA-sectie + talk-band van alle pagina's
- Voeg talk-strip (compacte Sam Klijn balk) toe boven footer op alle pagina's
- Voeg groene zoekbalk toe bovenaan listings.html
- Update CSS: nav-zoekicoon als popup, grijs avatar placeholder
"""
import re, os, glob

REPO = os.path.dirname(os.path.abspath(__file__))

TALK_STRIP = '''<section class="talk-strip"><div class="container">
  <div class="talk-strip-inner">
    <img src="images/team/sam.klijn.jpg" alt="Sam Klijn" class="ts-avatar">
    <div class="ts-info">
      <strong>Sam Klijn</strong>
      <span>Partner Marketing &middot; Spring Real Estate</span>
    </div>
    <div class="ts-actions">
      <a href="tel:+31302001020" class="ts-btn ts-btn--call">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.4-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>
        +31 30 200 10 20
      </a>
      <a href="https://wa.me/31302001020?text=Hoi%20Sam,%20ik%20heb%20een%20vraag" target="_blank" rel="noopener" class="ts-btn ts-btn--wa">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M.06 24l1.7-6.2A11.9 11.9 0 1 1 12 24a11.9 11.9 0 0 1-5.7-1.45L.06 24zM6.6 20.1l.37.22a9.9 9.9 0 0 0 5.05 1.38h.004a9.9 9.9 0 1 0-8.4-4.6l.24.38-1 3.67 3.74-.98zM17.5 14.3c-.15-.25-.55-.4-1.15-.7s-1.77-.87-2.04-.97-.47-.15-.67.15-.77.97-.94 1.17-.35.22-.65.07a8.13 8.13 0 0 1-2.4-1.48 9 9 0 0 1-1.66-2.06c-.17-.3 0-.46.13-.6s.3-.35.45-.52a2 2 0 0 0 .3-.5.55.55 0 0 0 0-.52c-.07-.15-.67-1.62-.92-2.22s-.5-.5-.67-.5h-.57a1.1 1.1 0 0 0-.8.37 3.35 3.35 0 0 0-1.04 2.5 5.8 5.8 0 0 0 1.22 3.08 13.3 13.3 0 0 0 5.1 4.5c.7.3 1.27.49 1.7.63a4.1 4.1 0 0 0 1.88.12c.57-.09 1.77-.72 2.02-1.42s.25-1.3.17-1.42z"/></svg>
        WhatsApp
      </a>
      <a href="contact.html" class="ts-btn ts-btn--ghost">Plan gesprek</a>
    </div>
  </div>
</div></section>
'''

# Groene zoekbalk voor listings.html (boven de kaart)
LISTINGS_SEARCH_BAR = '''<!-- ============ GROENE ZOEKBALK ============ -->
<div class="listings-hero-search">
  <div class="container">
    <form class="lhs-form" onsubmit="return false;">
      <svg class="lhs-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg>
      <input id="lhsInput" type="text" class="lhs-input" placeholder="Zoek op locatie, type of oppervlakte&hellip;" aria-label="Zoeken in het aanbod">
      <button type="button" class="lhs-btn" onclick="document.getElementById('lhsInput').focus()">Zoeken</button>
    </form>
    <div class="lhs-tags">
      <button class="lhs-tag active" data-seg="all">Alle</button>
      <button class="lhs-tag" data-seg="huur">Te huur</button>
      <button class="lhs-tag" data-seg="koop">Te koop</button>
    </div>
  </div>
</div>
'''

def process_file(path):
    with open(path, encoding='utf-8') as f:
        html = f.read()

    original = html
    filename = os.path.basename(path)

    # 1. Verwijder grote talk-band sectie (Praat met een adviseur kaart)
    html = re.sub(
        r'<section class="section talk-band">.*?</section>',
        '', html, flags=re.DOTALL
    )

    # 2. Verwijder grote CTA sectie (div.cta met btns "Neem contact op")
    # Patroon: <section ... id="contact">...<div class="cta">...</section>
    html = re.sub(
        r'<section[^>]*id="contact"[^>]*>\s*<div class="container">\s*<div class="cta">.*?</div></div></section>',
        '', html, flags=re.DOTALL
    )

    # Ook de losse cta-sectie op index.html (zonder id="contact")
    html = re.sub(
        r'<!-- ============ CTA ============ -->\s*<section class="section--tight">\s*<div class="container">\s*<div class="cta">.*?</div>\s*</div>\s*</section>',
        '', html, flags=re.DOTALL
    )

    # 3. Voeg talk-strip toe voor <footer als die er nog niet in zit
    if 'talk-strip' not in html and '<footer' in html:
        html = html.replace('<footer class="footer">', TALK_STRIP + '\n<footer class="footer">', 1)

    # 4. Listings.html: voeg groene zoekbalk in vóór de locatiekaart
    if filename == 'listings.html':
        if 'listings-hero-search' not in html:
            html = html.replace(
                '<!-- ============ LOCATIEKAART ============ -->',
                LISTINGS_SEARCH_BAR + '\n<!-- ============ LOCATIEKAART ============ -->'
            )

    if html != original:
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(html)
        print(f'  Bijgewerkt: {filename}')
    else:
        print(f'  Ongewijzigd: {filename}')


# Alle HTML bestanden verwerken
html_files = glob.glob(os.path.join(REPO, '*.html'))
print(f'Verwerken {len(html_files)} bestanden...')
for path in sorted(html_files):
    process_file(path)

print('\nKlaar.')
