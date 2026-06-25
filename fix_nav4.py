import glob, os, re

ROOT = r'C:/Users/Gebruiker/spring-real-estate-concept'
files = glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True)

CHV = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>'

I_DOC  = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/></svg>'
I_DEAL = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 17l6-6 4 4 8-8"/><path d="M17 7h4v4"/></svg>'
I_CASE = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/><line x1="12" y1="12" x2="12" y2="16"/><line x1="10" y1="14" x2="14" y2="14"/></svg>'

# New Resources block: Cases first, then Transacties, then Algemeen
NEW_RES = f'''    <div class="has-drop"><button><span>Resources</span> {CHV}</button>
      <div class="drop">
        <a href="cases.html"><span class="d-ic">{I_CASE}</span><span><span class="d-t">Cases</span><span class="d-d">Resultaten voor onze klanten</span></span></a>
        <a href="resources.html"><span class="d-ic">{I_DEAL}</span><span><span class="d-t">Transacties</span><span class="d-d">Vastgoeddeals en marktdata</span></span></a>
        <a href="resources.html"><span class="d-ic">{I_DOC}</span><span><span class="d-t">Algemeen</span><span class="d-d">Analyses, trends en inzichten</span></span></a>
      </div>
    </div>'''

OLD_RES_PAT = re.compile(
    r'    <div class="has-drop"><button><span>Resources</span>.*?</div>\n    </div>',
    re.DOTALL
)

c = 0
for f in files:
    with open(f, encoding='utf-8') as fh:
        txt = fh.read()
    # 1. "Ons team" -> "Team" in nav button
    new = txt.replace('<button><span>Ons team</span>', '<button><span>Team</span>')
    # 2. Replace Resources block with new order
    new = OLD_RES_PAT.sub(NEW_RES, new)
    if new != txt:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(new)
        c += 1

print(f'Updated {c} files')
