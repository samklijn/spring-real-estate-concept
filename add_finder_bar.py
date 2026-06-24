"""
add_finder_bar.py  (v2)
========================
- listings.html  → stap-voor-stap collapsible finder ("Vertel ons wat u zoekt")
- alle andere pagina's → simpele groene zoekbalk ("Waar bent u naar op zoek?")
- Verwijdert de eerder geplaatste finder-bar van niet-listings pagina's
- Bumpt CSS/JS versie naar v=24

NOOIT PowerShell voor HTML bestanden!
"""
import os, glob, re

REPO = os.path.dirname(os.path.abspath(__file__))
VERSION = '24'

# ── 1. Stap-voor-stap finder  (ALLEEN listings.html) ────────────────────────

LISTINGS_FINDER = '''\
<!-- FINDER BAR (listings) -->
<div class="finder-bar finder-bar--stepper" id="finderBar">
  <div class="container finder-bar-inner">
    <button class="fb-toggle" id="fbToggle" aria-expanded="false" aria-controls="fbPanel">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg>
      <span class="fb-label">Vertel ons wat u zoekt</span>
      <svg class="fb-chevron" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg>
    </button>
    <div class="fb-panel" id="fbPanel" hidden>
      <div class="fb-steps">
        <div class="fb-step fb-step--active" data-step="1">
          <span class="fb-step-num">1</span>
          <div class="fb-step-body">
            <p class="fb-step-q">Wat zoekt u?</p>
            <div class="fb-chips" id="fbTypeChips">
              <button class="fb-chip" data-val="kantoor">Kantoorruimte</button>
              <button class="fb-chip" data-val="bedrijf">Bedrijfsruimte</button>
              <button class="fb-chip" data-val="belegging">Belegging</button>
              <button class="fb-chip" data-val="woning">Woning</button>
            </div>
          </div>
        </div>
        <div class="fb-step" data-step="2">
          <span class="fb-step-num">2</span>
          <div class="fb-step-body">
            <p class="fb-step-q">Welke locatie?</p>
            <div class="fb-chips" id="fbLocChips">
              <button class="fb-chip" data-val="amsterdam">Amsterdam</button>
              <button class="fb-chip" data-val="utrecht">Utrecht</button>
              <button class="fb-chip" data-val="valencia">Valencia</button>
              <button class="fb-chip" data-val="estepona">Estepona</button>
            </div>
            <input type="text" class="fb-input" id="fbLocInput" placeholder="Of typ een locatie&hellip;">
          </div>
        </div>
        <div class="fb-step fb-step--opp" data-step="3">
          <span class="fb-step-num">3</span>
          <div class="fb-step-body">
            <p class="fb-step-q">Oppervlakte (m&sup2;)?</p>
            <div class="fb-range">
              <input type="number" class="fb-input fb-input--sm" placeholder="Min" min="0">
              <span class="fb-range-sep">&ndash;</span>
              <input type="number" class="fb-input fb-input--sm" placeholder="Max" min="0">
            </div>
          </div>
        </div>
      </div>
      <div class="fb-actions">
        <button class="fb-next" id="fbNext">Volgende <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg></button>
        <button class="fb-submit" id="fbSubmit" style="display:none">Zoek objecten <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg></button>
      </div>
    </div>
  </div>
</div>
<script>
(function(){
  var bar=document.getElementById('finderBar');
  if(!bar)return;
  var toggle=document.getElementById('fbToggle');
  var panel=document.getElementById('fbPanel');
  var nextBtn=document.getElementById('fbNext');
  var submitBtn=document.getElementById('fbSubmit');
  var steps=Array.prototype.slice.call(bar.querySelectorAll('.fb-step'));
  var current=0;
  toggle.addEventListener('click',function(){
    var open=panel.hidden;
    panel.hidden=!open;
    toggle.setAttribute('aria-expanded',String(open));
    bar.classList.toggle('fb--open',open);
    if(open){showStep(0);}
  });
  function hasOpp(){
    var tc=document.getElementById('fbTypeChips');
    var a=tc?tc.querySelector('.fb-chip.active'):null;
    var v=a?a.dataset.val:'';
    return v==='kantoor'||v==='bedrijf';
  }
  function showStep(i){
    steps.forEach(function(s,idx){s.classList.toggle('fb-step--active',idx===i);});
    current=i;
    var last=(i===steps.length-1)||(i===steps.length-2&&!hasOpp());
    nextBtn.style.display=last?'none':'inline-flex';
    submitBtn.style.display=last?'inline-flex':'none';
  }
  bar.querySelectorAll('.fb-chips').forEach(function(group){
    group.querySelectorAll('.fb-chip').forEach(function(btn){
      btn.addEventListener('click',function(){
        group.querySelectorAll('.fb-chip').forEach(function(b){b.classList.remove('active');});
        btn.classList.add('active');
      });
    });
  });
  nextBtn.addEventListener('click',function(){
    var next=current+1;
    if(next===steps.length-1&&!hasOpp()){submitBtn.click();return;}
    if(next<steps.length)showStep(next);
  });
  submitBtn.addEventListener('click',function(){window.location.href='listings.html';});
})();
</script>
'''

# ── 2. Simpele groene zoekbalk (alle andere pagina's) ───────────────────────

SIMPLE_SEARCH_BAR = '''\
<!-- ZOEKBALK -->
<div class="site-search-bar">
  <div class="container">
    <form class="ssb-form" onsubmit="return false">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg>
      <input type="text" class="ssb-input" placeholder="Waar bent u naar op zoek?" aria-label="Zoeken">
      <button type="submit" class="ssb-btn">Zoeken</button>
    </form>
  </div>
</div>
'''

# ── Verwerking ───────────────────────────────────────────────────────────────

def remove_old_finder(text):
    """Verwijder eerder geplaatste finder-bar of zoekbalk."""
    # Verwijder finder-bar blok (met script tag erna)
    text = re.sub(
        r'<!-- FINDER BAR.*?</script>\n',
        '', text, flags=re.DOTALL
    )
    # Verwijder site-search-bar blok
    text = re.sub(
        r'<!-- ZOEKBALK -->\n<div class="site-search-bar">.*?</div>\n',
        '', text, flags=re.DOTALL
    )
    # Verwijder oude vf-bar of obj-finder-bar
    text = re.sub(r'<div class="vf-bar">.*?</div>\s*\n', '', text, flags=re.DOTALL)
    text = re.sub(r'<div class="obj-finder-bar">.*?</div>\s*\n', '', text, flags=re.DOTALL)
    return text

def process(path):
    fname = os.path.basename(path)

    with open(path, 'rb') as f:
        raw = f.read()
    if raw.startswith(b'\xef\xbb\xbf'):
        raw = raw[3:]
    text = raw.decode('utf-8', errors='replace')

    # Verwijder alle eerder geplaatste zoekbalken
    text = remove_old_finder(text)

    # Voeg de juiste balk toe na </header>
    if '</header>' in text:
        if fname == 'listings.html':
            text = text.replace('</header>', '</header>\n' + LISTINGS_FINDER, 1)
        else:
            text = text.replace('</header>', '</header>\n' + SIMPLE_SEARCH_BAR, 1)

    # CSS/JS versie bumpen
    text = re.sub(r'\?v=\d+', f'?v={VERSION}', text)

    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)

html_files = glob.glob(os.path.join(REPO, '*.html'))
print(f'Verwerken {len(html_files)} bestanden...')
for path in sorted(html_files):
    process(path)

# Controle
with open(os.path.join(REPO, 'listings.html'), encoding='utf-8') as f:
    s = f.read()
print('finder-bar--stepper in listings.html:', 'finder-bar--stepper' in s)
print('site-search-bar in listings.html:    ', 'site-search-bar' in s)

with open(os.path.join(REPO, 'index.html'), encoding='utf-8') as f:
    s2 = f.read()
print('site-search-bar in index.html:       ', 'site-search-bar' in s2)
print('finder-bar in index.html:            ', 'finder-bar--stepper' in s2)

print('\nKlaar!')
