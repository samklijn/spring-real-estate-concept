"""
fix_lm_faq.py
- Lead magnet: compact donkere kaart (zelfde stijl als doelgroep-pagina's)
- FAQ: verplaatsen naar onderaan (na kennis, vóór gerelateerde diensten)
"""
import re, glob

def read(f):
    with open(f, encoding='utf-8') as fh: return fh.read()
def write(f, s):
    with open(f, 'w', encoding='utf-8') as fh: fh.write(s)

for fpath in sorted(glob.glob('unit-*.html')):
    src = read(fpath)

    # ── 1. Vervang lead-magnet door compacte donkere kaart ─────────────────
    lm_m = re.search(r'\n<section class="lead-magnet">.*?</section>', src, re.DOTALL)

    if lm_m:
        lm_src = lm_m.group(0)
        # Extraheer inhoud
        ey_m  = re.search(r'class="eyebrow">(.*?)<', lm_src)
        h2_m  = re.search(r'<h2>(.*?)</h2>', lm_src, re.DOTALL)
        p_m   = re.search(r'<p>(.*?)</p>', lm_src, re.DOTALL)
        btn_m = re.search(r'<button[^>]*>(.*?)</button>', lm_src)

        eyebrow  = ey_m.group(1)  if ey_m  else 'Gratis download'
        h2       = h2_m.group(1).strip() if h2_m  else ''
        p_text   = p_m.group(1).strip()  if p_m   else ''
        btn_text = btn_m.group(1)        if btn_m else 'Download gratis'

        new_lm = (
            '\n<section class="section--tight" id="download"><div class="container">\n'
            '  <div style="background:var(--ink);border-radius:16px;padding:36px 48px;'
            'display:grid;grid-template-columns:1fr auto;align-items:center;gap:40px;flex-wrap:wrap">\n'
            '    <div>\n'
            '      <span style="display:block;text-transform:uppercase;letter-spacing:.12em;'
            'font-size:.75rem;color:var(--green);margin-bottom:.5rem">' + eyebrow + '</span>\n'
            '      <h2 style="color:#fff;margin:0 0 .5rem;font-size:clamp(1.2rem,2.2vw,1.55rem);line-height:1.3">' + h2 + '</h2>\n'
            '      <p style="color:rgba(255,255,255,.6);margin:0;font-size:.94rem">' + p_text + '</p>\n'
            '    </div>\n'
            '    <form style="display:flex;flex-direction:column;gap:10px;min-width:220px" onsubmit="return false">\n'
            '      <input type="email" placeholder="Uw e-mailadres" style="padding:11px 15px;border-radius:8px;'
            'border:1px solid rgba(255,255,255,.18);background:rgba(255,255,255,.07);color:#fff;font-size:.94rem">\n'
            '      <button class="btn btn--primary" style="width:100%">' + btn_text + '</button>\n'
            '    </form>\n'
            '  </div>\n'
            '</div></section>'
        )
        src = src[:lm_m.start()] + new_lm + src[lm_m.end():]

    # ── 2. FAQ naar onderaan: na kennis, vóór laatste niet-talk-strip sectie ─
    # Verwijder FAQ uit huidige positie en bewaar
    faq_m = re.search(r'\n<section[^>]+id="faq"[^>]*>.*?</section>', src, re.DOTALL)
    if faq_m:
        faq_block = faq_m.group(0)
        src = src[:faq_m.start()] + src[faq_m.end():]

        # Voeg FAQ in vóór talk-strip
        ts_idx = src.find('\n<section class="talk-strip">')
        src = src[:ts_idx] + faq_block + '\n' + src[ts_idx:]

    write(fpath, src)
    print(f'  {fpath}: {len(src.splitlines())}L')

print('Klaar.')
