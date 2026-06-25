import re, glob, os

ROOT = r'C:/Users/Gebruiker/spring-real-estate-concept'
CHV = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>'

# SVG icons
I_BUILD = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 3v18M15 9h3M15 13h3M15 17h3M6 9h1M6 13h1"/></svg>'
I_KEY   = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="7.5" cy="15.5" r="4.5"/><path d="M10.5 12.5L21 2M19 4l2 2M16 7l2 2"/></svg>'
I_DOC   = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/></svg>'
I_DEAL  = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 17l6-6 4 4 8-8"/><path d="M17 7h4v4"/></svg>'
I_CASE  = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/><line x1="12" y1="12" x2="12" y2="16"/><line x1="10" y1="14" x2="14" y2="14"/></svg>'
I_TEAM  = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></svg>'
I_WAVE  = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22C6.5 22 2 17.5 2 12S6.5 2 12 2s10 4.5 10 10-4.5 10-10 10z"/><path d="M12 8v4l3 3"/></svg>'
I_INFO  = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>'
I_MAP   = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/></svg>'

def di(ico, title, desc):
    return f'<a href="HREF"><span class="d-ic">{ico}</span><span><span class="d-t">{title}</span><span class="d-d">{desc}</span></span></a>'

NEW_AANBOD = f'''    <div class="has-drop"><button><span>Aanbod</span> {CHV}</button>
      <div class="drop">
        {di(I_BUILD,"Koopobjecten","Kantoor en bedrijfsruimte te koop").replace("HREF","listings.html")}
        {di(I_KEY,"Huurobjecten","Kantoor en bedrijfsruimte te huur").replace("HREF","listings.html")}
      </div>
    </div>'''

NEW_RESOURCES = f'''    <div class="has-drop"><button><span>Resources</span> {CHV}</button>
      <div class="drop">
        {di(I_DOC,"Alle resources","Analyses, trends en inzichten").replace("HREF","resources.html")}
        {di(I_DEAL,"Transacties","Vastgoeddeals en marktdata").replace("HREF","resources.html")}
        {di(I_CASE,"Cases","Resultaten voor onze klanten").replace("HREF","cases.html")}
      </div>
    </div>'''

NEW_TEAM = f'''    <div class="has-drop"><button><span>Ons team</span> {CHV}</button>
      <div class="drop">
        {di(I_TEAM,"Huidig team","100+ vastgoedspecialisten").replace("HREF","agents.html")}
        {di(I_WAVE,"Word jij onze nieuwe collega?","Bekijk vacatures").replace("HREF","vacatures.html")}
      </div>
    </div>'''

NEW_ABOUT = f'''    <div class="has-drop"><button><span>About</span> {CHV}</button>
      <div class="drop">
        {di(I_INFO,"Over Spring","Wie wij zijn en wat we doen").replace("HREF","about.html")}
        {di(I_MAP,"Onze locaties","Amsterdam, Utrecht &amp; Spanje").replace("HREF","locaties.html")}
      </div>
    </div>'''

NEW_NAV_TAIL = (
    NEW_AANBOD + '\n'
    + NEW_RESOURCES + '\n'
    + NEW_TEAM + '\n'
    '    <a href="vacatures.html">Vacatures</a>\n'
    + NEW_ABOUT + '\n'
    '  </nav>'
)

# Match from after Diensten closing through </nav>
NAV_PAT = re.compile(
    r'(      </div>\n    </div>\n)'
    r'.*?</nav>',
    re.DOTALL
)

files = glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True)
nav_count = 0
for f in files:
    with open(f, encoding='utf-8') as fh:
        txt = fh.read()
    new = NAV_PAT.sub(r'\1' + NEW_NAV_TAIL, txt)
    if new != txt:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(new)
        nav_count += 1

print(f'Nav updated: {nav_count} files')

# Fix stat: 40+ collega's -> 100+ in vacatures.html
vac = os.path.join(ROOT, 'vacatures.html')
with open(vac, encoding='utf-8') as f:
    txt = f.read()
txt = txt.replace(
    '<b style="font-size:2rem;font-weight:800;display:block;color:var(--green)">40+</b><span class="muted">collega&#39;s</span>',
    '<b style="font-size:2rem;font-weight:800;display:block;color:var(--green)">100+</b><span class="muted">collega\'s</span>'
)
with open(vac, 'w', encoding='utf-8') as f:
    f.write(txt)
print('Stat updated: 40+ -> 100+')

# CSS: fix Diensten dropdown overflow (shift right so it doesn't fall off-screen left)
# Also bump v29 -> v30
css_path = os.path.join(ROOT, 'css', 'styles.css')
with open(css_path, encoding='utf-8') as f:
    css = f.read()

# Add rule so first has-drop's .drop starts at left:0 instead of centered
FIX_CSS = '''
/* Diensten dropdown: align left edge to button instead of center to avoid overflow */
.nav .has-drop:first-child .drop{ left: 0; transform: translateY(8px); }
.nav .has-drop:first-child:hover .drop,
.nav .has-drop:first-child:focus-within .drop,
.nav .has-drop:first-child.click-open .drop{ transform: translateY(0); opacity:1; visibility:visible; }
'''

if 'has-drop:first-child .drop' not in css:
    # Insert before end of file or after last rule
    css = css.rstrip() + '\n' + FIX_CSS + '\n'

css = css.replace('styles.css?v=29', 'styles.css?v=30')  # in case it's in css
with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)
print('CSS updated')

# Bump v29 -> v30 in all html
css_count = 0
for f in files:
    with open(f, encoding='utf-8') as fh:
        txt = fh.read()
    new = txt.replace('styles.css?v=29', 'styles.css?v=30')
    if new != txt:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(new)
        css_count += 1
print(f'CSS version bumped in {css_count} files')
