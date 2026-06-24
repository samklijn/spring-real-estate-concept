# -*- coding: utf-8 -*-
"""Parse de 21-units docx-export (units_src.txt) -> units_content_v2.json met rijke prose."""
import re, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, 'build', 'units_src.txt'), encoding='utf-8').read().split('\n')

MAP = {1:"verhuur-commercieel",2:"aanhuur-kantoorruimte",3:"aanverkoop-beleggingsvastgoed",4:"serviced-offices",
       5:"taxaties-beleggingsvastgoed",6:"grootzakelijke-taxaties",7:"herbouwwaarde-verzekering",8:"vastgoeddata-marktinzichten",
       9:"asset-management",10:"commercieel-vastgoedbeheer",11:"residentieel-vastgoedbeheer",12:"design-build",
       13:"vastgoedadministratie",14:"financiele-administratie",15:"hr-advies",16:"recruitment-talent",
       17:"vastgoedmarketing",18:"strategic-advisory"}
LANGS = {'## Nederlands': 'nl', '## English': 'en', '## Español': 'es'}

def clean(s):
    return s.replace('&apos;', "'").replace('&quot;', '"').replace('&amp;', '&').strip()

SKIP = re.compile(r'^(URL-pad|SEO-?titel|SEO-?title|SEO-?título|Meta ?description|Meta ?descripci|Primair zoekwoord|Primary keyword|Palabra clave|H1|H2|Call-to-action|Llamada|Verder kijken|Further|Seguir|SEO-?check|Structured data|Datos estructurados|Betrokken personen|People involved|Personas|Doelgroep|Target|Público|Wat we doen|What we do|Qué hacemos|Lo que hacemos)', re.I)
def is_label(l):
    l = l.strip()
    return (not l) or bool(SKIP.match(l)) or l.startswith('/') or l.startswith('{') or l.startswith('↑') or l.startswith('→') or l.startswith('SEO')

# unit boundaries
idx = []
for i, l in enumerate(src):
    m = re.match(r'^## (\d+)\. (.+)$', l)
    if m: idx.append((i, int(m.group(1)), m.group(2).strip()))
idx.append((len(src), 999, ''))

out = {}
for k in range(len(idx) - 1):
    start, num, title = idx[k]; end = idx[k + 1][0]
    if num not in MAP: continue
    slug = MAP[num]; block = src[start:end]
    lsec = [(i, LANGS[l.strip()]) for i, l in enumerate(block) if l.strip() in LANGS]
    lsec.append((len(block), None))
    langdata = {}
    for j in range(len(lsec) - 1):
        s, lang = lsec[j]; e = lsec[j + 1][0]
        if lang is None: continue
        sec = block[s + 1:e]
        heads = [(i, clean(l[3:])) for i, l in enumerate(sec) if l.startswith('## ')]
        def after(rx):
            for i, l in enumerate(sec):
                if re.match(rx, l, re.I):
                    for n in range(i + 1, len(sec)):
                        if sec[n].strip(): return clean(sec[n])
            return ''
        d = {'meta_title': after(r'^SEO-?titel|^SEO-?title|^SEO-?título'),
             'meta_desc': after(r'^Meta ?description|^Meta ?descripci')}
        if not heads:
            langdata[lang] = d; continue
        d['h1'] = heads[0][1]
        tag = ''
        for n in range(heads[0][0] + 1, len(sec)):
            if sec[n].strip() and not is_label(sec[n]) and not sec[n].startswith('## '): tag = clean(sec[n]); break
        d['tagline'] = tag
        # intro
        if len(heads) >= 2:
            intro = []
            for n in range(heads[0][0] + 1, heads[1][0]):
                if 'eerste alinea' in sec[n] or re.match(r'^(Wat we doen|What we do|Qué hacemos|Lo que hacemos)', sec[n], re.I):
                    for m2 in range(n + 1, heads[1][0]):
                        if sec[m2].strip() and not is_label(sec[m2]) and not sec[m2].startswith('## '): intro.append(clean(sec[m2]))
                    break
            d['intro'] = ' '.join(intro) if intro else tag
            d['approach'] = [clean(x) for x in sec[heads[1][0] + 1:heads[2][0]] if x.strip() and not is_label(x) and not x.startswith('## ')] if len(heads) >= 3 else []
        if len(heads) >= 3:
            cta_i = None
            for n in range(heads[2][0] + 1, len(sec)):
                if re.match(r'^(Call-to-action|Llamada)', sec[n], re.I): cta_i = n; break
            usp_end = cta_i if cta_i else (heads[3][0] if len(heads) >= 4 else len(sec))
            d['usps'] = [clean(x) for x in sec[heads[2][0] + 1:usp_end] if x.strip() and not is_label(x) and not x.startswith('## ')]
            if cta_i:
                for n in range(cta_i + 1, len(sec)):
                    if sec[n].strip(): d['cta'] = clean(sec[n]); break
        if len(heads) >= 4:
            faq_end = len(sec)
            for n in range(heads[3][0] + 1, len(sec)):
                if re.match(r'^(Verder kijken|SEO-?check|SEO check|Structured data|Further|Seguir|Datos estructurados)', sec[n], re.I): faq_end = n; break
            qa = [clean(x) for x in sec[heads[3][0] + 1:faq_end] if x.strip() and not is_label(x) and not x.startswith('## ')]
            d['faq'] = [{'q': qa[n], 'a': qa[n + 1]} for n in range(0, len(qa) - 1, 2)]
        langdata[lang] = d
    out[slug] = langdata

json.dump(out, open(os.path.join(ROOT, 'build', 'units_content_v2.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('units parsed:', len(out))
s = out['verhuur-commercieel']['nl']
print('NL H1:', s.get('h1'))
print('NL tagline:', s.get('tagline'))
print('NL intro[:90]:', s.get('intro', '')[:90])
print('NL approach paras:', len(s.get('approach', [])), '| usps:', len(s.get('usps', [])), '| faq:', len(s.get('faq', [])))
e = out['asset-management']['en']
print('EN asset H1:', e.get('h1'), '| approach:', len(e.get('approach', [])), '| faq:', len(e.get('faq', [])))
