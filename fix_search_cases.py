import re, os

ROOT = r'C:/Users/Gebruiker/spring-real-estate-concept'

# ── 1. CSS: search--light gets light-green background ────────────────────────
with open(ROOT + '/css/styles.css', encoding='utf-8') as f:
    css = f.read()

css = css.replace(
    '.search--light{ box-shadow:var(--shadow-soft); border:1px solid var(--line); margin-top:26px; }',
    '.search--light{ background:#EBF4D6; border:1px solid #C5DFA0; margin-top:20px; }'
)

with open(ROOT + '/css/styles.css', 'w', encoding='utf-8') as f:
    f.write(css)
print('styles.css: search--light updated to light green')


# ── helper: swap filter tabs above search form in page-hero ──────────────────
def swap_filter_above_search(src):
    """Move .team-filter div to be above the search form inside page-hero."""
    def replacer(m):
        block = m.group(0)
        # Find form and team-filter inside this hero
        form_m = re.search(r'(<form class="search[^"]*"[^>]*>.*?</form>)', block, re.DOTALL)
        filt_m = re.search(r'(<div class="team-filter"[^>]*>.*?</div>)', block, re.DOTALL)
        if not form_m or not filt_m:
            return block
        form_html = form_m.group(1)
        filt_html = filt_m.group(1)
        # Remove both from block
        block2 = block.replace(form_html, '').replace(filt_html, '')
        # Insert: filter then form, just before closing </div></section>
        block2 = re.sub(
            r'(\s*</div>\s*</section>\s*)$',
            '\n    ' + filt_html + '\n    ' + form_html + r'\1',
            block2
        )
        return block2
    return re.sub(
        r'<section class="page-hero">.*?</section>',
        replacer,
        src, flags=re.DOTALL
    )


# ── 2. resources.html: filter tabs above search ───────────────────────────────
with open(ROOT + '/resources.html', encoding='utf-8') as f:
    res = f.read()
res2 = swap_filter_above_search(res)
with open(ROOT + '/resources.html', 'w', encoding='utf-8') as f:
    f.write(res2)
changed = res2 != res
print(f'resources.html: {"filter above search" if changed else "no change"}')


# ── 3. algemeen.html: add filter tabs and put above search ───────────────────
with open(ROOT + '/algemeen.html', encoding='utf-8') as f:
    alg = f.read()

# Check if filter tabs exist in hero already
if 'team-filter' not in alg.split('</section>')[0]:
    # Add filter tabs right before the search form in hero
    alg = alg.replace(
        '    <form class="search search--light search--single" onsubmit="return false">',
        '''    <div class="team-filter">
      <a href="#" class="active" data-key="alle">Alle</a>
      <a href="#" data-key="marktinzicht">Marktinzicht</a>
      <a href="#" data-key="investeren">Investeren</a>
      <a href="#" data-key="huisvesting">Huisvesting</a>
      <a href="#" data-key="internationaal">Internationaal</a>
      <a href="#" data-key="taxaties">Taxaties</a>
    </div>
    <form class="search search--light search--single" onsubmit="return false">''',
        1
    )
else:
    alg = swap_filter_above_search(alg)

with open(ROOT + '/algemeen.html', 'w', encoding='utf-8') as f:
    f.write(alg)
print('algemeen.html: filter tabs above search')


# ── 4. cases.html: filter tabs above search + add spotlight ──────────────────
with open(ROOT + '/cases.html', encoding='utf-8') as f:
    cas = f.read()

# Swap filter above search in hero
cas = swap_filter_above_search(cas)

# Insert spotlight case between </section> (hero end) and <!-- CASES -->
SPOTLIGHT = '''
<!-- ── SPOTLIGHT CASE ─────────────────────────────────────────────── -->
<section class="section--tight section--soft">
<div class="container">
  <span class="eyebrow">Uitgelichte case</span>
  <div class="two-col" style="align-items:center;gap:3rem;margin-top:1.5rem">
    <div class="media-tall" style="border-radius:12px;overflow:hidden">
      <img src="images/photo-1.jpg" alt="Herpositionering kantoor" style="width:100%;height:100%;object-fit:cover">
    </div>
    <div class="prose">
      <span class="cat" style="background:var(--green);color:#fff;padding:4px 12px;border-radius:20px;font-size:.8rem;font-weight:600;display:inline-block;margin-bottom:16px">Asset management · Amsterdam</span>
      <h2 class="disp" style="font-size:1.8rem">Herpositionering levert<br><em>+18% rendement</em> op in 14 maanden</h2>
      <p style="color:#555;margin:.75rem 0 1.25rem">Een belegger met een leegstaand kantoorpand vroeg Spring om een strategie. Van zoekprofiel tot verhuurde meters: Spring begeleidde het volledige traject — van duurzame renovatie tot turn-key verhuur aan een tech-scale-up.</p>
      <ul style="list-style:none;padding:0;display:grid;gap:8px;margin-bottom:1.5rem">
        <li style="display:flex;gap:10px;align-items:center"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4"><path d="M5 12l5 5L20 6"/></svg> <strong>Resultaat:</strong>&nbsp;+18% rendement YoY</li>
        <li style="display:flex;gap:10px;align-items:center"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4"><path d="M5 12l5 5L20 6"/></svg> <strong>Bezetting:</strong>&nbsp;van 0% naar 98% in 14 maanden</li>
        <li style="display:flex;gap:10px;align-items:center"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4"><path d="M5 12l5 5L20 6"/></svg> <strong>Aanpak:</strong>&nbsp;herpositionering + duurzame renovatie</li>
        <li style="display:flex;gap:10px;align-items:center"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4"><path d="M5 12l5 5L20 6"/></svg> <strong>Doorlooptijd:</strong>&nbsp;14 maanden van plan tot volledige verhuur</li>
      </ul>
      <a href="contact.html" class="btn btn--primary">Soortgelijke case bespreken</a>
    </div>
  </div>
</div>
</section>

'''

# Insert after the closing </section> of page-hero
cas = cas.replace(
    '</div></section>\n\n<!-- ============ CASES',
    '</div></section>\n' + SPOTLIGHT + '<!-- ============ CASES'
)

with open(ROOT + '/cases.html', 'w', encoding='utf-8') as f:
    f.write(cas)
print(f'cases.html: spotlight added + filter above search ({len(cas.splitlines())}L)')


# ── 5. transacties.html: lighten the dark stats band ─────────────────────────
with open(ROOT + '/transacties.html', encoding='utf-8') as f:
    tr = f.read()

# Replace dark stats band with light green version
tr = re.sub(
    r'<section class="section--tight" style="background:var\(--ink\);color:#fff">.*?</section>',
    '''<section class="section--tight" style="background:#EBF4D6;border-bottom:1px solid #C5DFA0">
<div class="container">
  <div class="grid" style="grid-template-columns:repeat(4,1fr);gap:0;text-align:center">
    <div style="border-right:1px solid #C5DFA0;padding:1.5rem 0">
      <b style="font-size:2rem;font-weight:800;color:var(--ink)">€450M+</b>
      <span style="display:block;font-size:.85rem;color:var(--ink-soft);margin-top:4px">Transactiewaarde</span>
    </div>
    <div style="border-right:1px solid #C5DFA0;padding:1.5rem 0">
      <b style="font-size:2rem;font-weight:800;color:var(--ink)">1.500+</b>
      <span style="display:block;font-size:.85rem;color:var(--ink-soft);margin-top:4px">Deals begeleid</span>
    </div>
    <div style="border-right:1px solid #C5DFA0;padding:1.5rem 0">
      <b style="font-size:2rem;font-weight:800;color:var(--ink)">4</b>
      <span style="display:block;font-size:.85rem;color:var(--ink-soft);margin-top:4px">Vestigingen</span>
    </div>
    <div style="padding:1.5rem 0">
      <b style="font-size:2rem;font-weight:800;color:var(--ink)">15+</b>
      <span style="display:block;font-size:.85rem;color:var(--ink-soft);margin-top:4px">Jaar marktervaring</span>
    </div>
  </div>
</div>
</section>''',
    tr, flags=re.DOTALL
)

with open(ROOT + '/transacties.html', 'w', encoding='utf-8') as f:
    f.write(tr)
print('transacties.html: stats band lightened')

print('\nDone.')
