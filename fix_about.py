ROOT = r'C:/Users/Gebruiker/spring-real-estate-concept'

with open(ROOT + '/about.html', encoding='utf-8') as f:
    src = f.read()

# Keep everything up to and including the closing </ul> of the checks list
# inside section--soft (ends at line 165 closing </ul>, then </div></div>)
# We cut just before the injected has-drop at "    <div class=\"has-drop\">"
cut_at = src.index('\n    <div class="has-drop"><button><span data-i18n="nav.aanbod">')
top = src[:cut_at]

# Close the two-col, container, and section properly
top += '\n    </div>\n  </div>\n</section>\n'

# Add locaties section — 4 clickable city blocks
locaties = '''
<!-- locaties op about -->
<section class="section">
<div class="container">
  <div class="sec-head"><div class="t">
    <span class="eyebrow">Onze vestigingen</span>
    <h2 class="disp">Lokaal verankerd, <em>internationaal aanwezig</em></h2>
  </div></div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1.5rem;margin-top:2rem">

    <a href="locatie-utrecht.html" style="text-decoration:none;color:inherit">
    <div style="border:1px solid #e5e8e0;border-radius:12px;padding:1.75rem;transition:box-shadow .2s" onmouseover="this.style.boxShadow='0 4px 20px rgba(0,0,0,.08)'" onmouseout="this.style.boxShadow='none'">
      <div style="font-size:1.5rem;margin-bottom:.75rem">🇳🇱</div>
      <h3 style="margin:0 0 4px;font-size:1.1rem">Utrecht</h3>
      <p style="color:#7a7f74;font-size:.85rem;margin:0 0 1rem">Hoofdkantoor &middot; Croeselaan 28</p>
      <ul style="list-style:none;padding:0;margin:0 0 1.25rem;display:grid;gap:6px;font-size:.85rem">
        <li style="display:flex;gap:8px"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4" style="flex-shrink:0;margin-top:2px"><path d="M5 12l5 5L20 6"/></svg>Full-service vastgoedadvies</li>
        <li style="display:flex;gap:8px"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4" style="flex-shrink:0;margin-top:2px"><path d="M5 12l5 5L20 6"/></svg>Commercieel &amp; residentieel</li>
        <li style="display:flex;gap:8px"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4" style="flex-shrink:0;margin-top:2px"><path d="M5 12l5 5L20 6"/></svg>18 business units</li>
      </ul>
      <span style="color:var(--green);font-size:.85rem;font-weight:600">Bekijk vestiging &rarr;</span>
    </div>
    </a>

    <a href="locatie-amsterdam.html" style="text-decoration:none;color:inherit">
    <div style="border:1px solid #e5e8e0;border-radius:12px;padding:1.75rem;transition:box-shadow .2s" onmouseover="this.style.boxShadow='0 4px 20px rgba(0,0,0,.08)'" onmouseout="this.style.boxShadow='none'">
      <div style="font-size:1.5rem;margin-bottom:.75rem">🇳🇱</div>
      <h3 style="margin:0 0 4px;font-size:1.1rem">Amsterdam</h3>
      <p style="color:#7a7f74;font-size:.85rem;margin:0 0 1rem">Regionale vestiging &middot; Zuidas</p>
      <ul style="list-style:none;padding:0;margin:0 0 1.25rem;display:grid;gap:6px;font-size:.85rem">
        <li style="display:flex;gap:8px"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4" style="flex-shrink:0;margin-top:2px"><path d="M5 12l5 5L20 6"/></svg>Kantoor- &amp; bedrijfsruimte</li>
        <li style="display:flex;gap:8px"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4" style="flex-shrink:0;margin-top:2px"><path d="M5 12l5 5L20 6"/></svg>Zuidas-specialist</li>
        <li style="display:flex;gap:8px"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4" style="flex-shrink:0;margin-top:2px"><path d="M5 12l5 5L20 6"/></svg>Investment &amp; beleggingen</li>
      </ul>
      <span style="color:var(--green);font-size:.85rem;font-weight:600">Bekijk vestiging &rarr;</span>
    </div>
    </a>

    <a href="locatie-valencia.html" style="text-decoration:none;color:inherit">
    <div style="border:1px solid #e5e8e0;border-radius:12px;padding:1.75rem;transition:box-shadow .2s" onmouseover="this.style.boxShadow='0 4px 20px rgba(0,0,0,.08)'" onmouseout="this.style.boxShadow='none'">
      <div style="font-size:1.5rem;margin-bottom:.75rem">🇪🇸</div>
      <h3 style="margin:0 0 4px;font-size:1.1rem">Valencia</h3>
      <p style="color:#7a7f74;font-size:.85rem;margin:0 0 1rem">Internationale vestiging &middot; Spanje</p>
      <ul style="list-style:none;padding:0;margin:0 0 1.25rem;display:grid;gap:6px;font-size:.85rem">
        <li style="display:flex;gap:8px"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4" style="flex-shrink:0;margin-top:2px"><path d="M5 12l5 5L20 6"/></svg>Residentieel &amp; commercieel</li>
        <li style="display:flex;gap:8px"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4" style="flex-shrink:0;margin-top:2px"><path d="M5 12l5 5L20 6"/></svg>NL-expats &amp; investeerders</li>
        <li style="display:flex;gap:8px"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4" style="flex-shrink:0;margin-top:2px"><path d="M5 12l5 5L20 6"/></svg>Fiscaal advies &amp; begeleiding</li>
      </ul>
      <span style="color:var(--green);font-size:.85rem;font-weight:600">Bekijk vestiging &rarr;</span>
    </div>
    </a>

    <a href="locatie-estepona.html" style="text-decoration:none;color:inherit">
    <div style="border:1px solid #e5e8e0;border-radius:12px;padding:1.75rem;transition:box-shadow .2s" onmouseover="this.style.boxShadow='0 4px 20px rgba(0,0,0,.08)'" onmouseout="this.style.boxShadow='none'">
      <div style="font-size:1.5rem;margin-bottom:.75rem">🇪🇸</div>
      <h3 style="margin:0 0 4px;font-size:1.1rem">Estepona</h3>
      <p style="color:#7a7f74;font-size:.85rem;margin:0 0 1rem">Internationale vestiging &middot; Costa del Sol</p>
      <ul style="list-style:none;padding:0;margin:0 0 1.25rem;display:grid;gap:6px;font-size:.85rem">
        <li style="display:flex;gap:8px"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4" style="flex-shrink:0;margin-top:2px"><path d="M5 12l5 5L20 6"/></svg>Luxe residentieel vastgoed</li>
        <li style="display:flex;gap:8px"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4" style="flex-shrink:0;margin-top:2px"><path d="M5 12l5 5L20 6"/></svg>Costa del Sol-specialist</li>
        <li style="display:flex;gap:8px"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.4" style="flex-shrink:0;margin-top:2px"><path d="M5 12l5 5L20 6"/></svg>Verhuur &amp; belegging</li>
      </ul>
      <span style="color:var(--green);font-size:.85rem;font-weight:600">Bekijk vestiging &rarr;</span>
    </div>
    </a>

  </div>
</div>
</section>
'''

# Find talk-strip in original (skip the misplaced scripts at lines 198-201)
talk_start = src.index('\n<section class="talk-strip">', cut_at)
bottom = src[talk_start:]

new_about = top + locaties + bottom

with open(ROOT + '/about.html', 'w', encoding='utf-8') as f:
    f.write(new_about)

print(f'about.html: nav injection removed, 4 clickable location cards added ({len(new_about.splitlines())}L)')
