# -*- coding: utf-8 -*-
"""Parse Spring_Websiteteksten_21_units (NL/EN/ES) -> units_content.json
Each language block has exactly 4 '## ' content headings in order:
H1, approach, why-choose, FAQ. We segment positionally so it works per language."""
import re, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_assets", "teksten.txt")
OUT = os.path.join(ROOT, "build", "units_content.json")

lines = open(SRC, encoding="utf-8").read().split("\n")

def is_junk(l):
    s = l.strip()
    return (not s) or s.startswith("<w:") or s.startswith("{") or s.startswith('"@') \
        or s.startswith("SEO-check") or s.startswith("Structured data") \
        or s.startswith("URL-pad") or s.startswith("SEO-titel") or s.startswith("Meta desc") \
        or s.startswith("Primair zoekwoord") or s.startswith("H1") or s.startswith("H2")

# split into unit blocks
units = {}
idx = [i for i,l in enumerate(lines) if re.match(r'^## \d+\. ', l)]
idx.append(len(lines))
for k in range(len(idx)-1):
    blk = lines[idx[k]:idx[k+1]]
    num = int(re.match(r'^## (\d+)\.', blk[0]).group(1))
    title = blk[0].split(". ",1)[1].strip()
    # involved people (before first '## Nederlands')
    people = []
    try:
        pstart = next(i for i,l in enumerate(blk) if l.strip()=="Betrokken personen")
        pend = next(i for i,l in enumerate(blk) if l.strip().startswith("## Nederlands"))
        for l in blk[pstart+1:pend]:
            s=l.strip()
            if s and "—" in s:
                people.append(s)
    except StopIteration:
        pass
    # language sub-blocks
    langmarks = [(i,l.strip()) for i,l in enumerate(blk) if re.match(r'^## (Nederlands|English|Espa)', l)]
    langmarks.append((len(blk), "END"))
    langs = {}
    namemap = {"Nederlands":"nl","English":"en","Espa":"es"}
    for li in range(len(langmarks)-1):
        start, label = langmarks[li]
        end = langmarks[li+1][0]
        code = next(v for kk,v in namemap.items() if label.startswith("## "+kk))
        sub = blk[start+1:end]
        # find the 4 content '## ' headings
        heads = [i for i,l in enumerate(sub) if l.startswith("## ")]
        if len(heads) < 4:
            continue
        def seg(a,b): return sub[a+1:b]
        # H1 segment
        h1 = sub[heads[0]][3:].strip()
        h1seg = seg(heads[0], heads[1])
        tagline = next((l.strip() for l in h1seg if not is_junk(l)), "")
        # intro = line after 'eerste alinea)'
        intro = ""
        for i,l in enumerate(h1seg):
            if "eerste alinea)" in l:
                rest = [x.strip() for x in h1seg[i+1:] if not is_junk(x)]
                intro = rest[0] if rest else ""
                break
        # approach
        approach = [l.strip() for l in seg(heads[1],heads[2]) if not is_junk(l)]
        # why-choose -> usps + cta
        why = [l.strip() for l in seg(heads[2],heads[3]) if not is_junk(l)]
        usps=[]; cta=""
        ctamark = None
        for i,l in enumerate(why):
            if l.lower().startswith(("call-to-action","call to action","llamada")):
                ctamark = i; break
        # 'Call-to-action' label may itself be filtered? it's not junk. find it in raw seg
        rawwhy = seg(heads[2],heads[3])
        cidx = next((i for i,l in enumerate(rawwhy) if l.strip().lower().startswith(("call-to-action","call to action","llamada"))), None)
        if cidx is not None:
            usps = [l.strip() for l in rawwhy[:cidx] if not is_junk(l)]
            after = [l.strip() for l in rawwhy[cidx+1:] if not is_junk(l)]
            cta = after[0] if after else ""
        else:
            usps = why
        # FAQ
        faqseg = sub[heads[3]+1:]
        faq=[]; qa=[]
        stop = ("Verder kijken","SEO-check","Structured data","Further","Más","Ver más","Verder")
        clean=[]
        for l in faqseg:
            s=l.strip()
            if s.startswith(stop): break
            if is_junk(l): continue
            clean.append(s)
        for i in range(0,len(clean)-1,2):
            faq.append({"q":clean[i],"a":clean[i+1]})
        langs[code] = {"h1":h1,"tagline":tagline,"intro":intro,
                       "approach":approach,"usps":usps,"cta":cta,"faq":faq}
    units[num] = {"title":title,"people":people,"langs":langs}

json.dump(units, open(OUT,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("parsed", len(units), "units ->", OUT)
# quick sanity
u=units[1]["langs"]["nl"]
print("U01 H1:", u["h1"])
print("U01 tagline:", u["tagline"])
print("U01 usps:", len(u["usps"]), "| faq:", len(u["faq"]), "| approach paras:", len(u["approach"]))
print("U01 people:", units[1]["people"])
