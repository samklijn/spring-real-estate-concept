import re, glob

def read(f):
    with open(f, encoding='utf-8') as fh: return fh.read()
def write(f, s):
    with open(f, 'w', encoding='utf-8') as fh: fh.write(s)

for fpath in sorted(glob.glob('unit-*.html')):
    src = read(fpath)

    # 1. Extraheer quote (em-tekst uit de compacte dark-ink sectie)
    quote_m = re.search(
        r'<section[^>]*style="background:var\(--ink\)"[^>]*><div class="container">.*?<em>(.*?)</em>.*?</section>',
        src, re.DOTALL
    )
    quote_text = quote_m.group(1).strip() if quote_m else ''

    # 2. Voeg quote in als blockquote-paragraaf in aanpak prose, na de laatste </p> vóór sluit-div
    if quote_text:
        insert = '\n    <p style="border-left:3px solid var(--green);padding-left:1rem;color:var(--ink);font-style:italic;margin-top:1.2rem">' + quote_text + '</p>'
        src = re.sub(
            r'(id="aanpak".*?<div class="prose">.*?)(</div>\s*<div class="media)',
            lambda m: m.group(1) + insert + m.group(2),
            src, flags=re.DOTALL, count=1
        )

    # 3. Verwijder cijfers sectie
    src = re.sub(r'\n<section[^>]+id="cijfers"[^>]*>.*?</section>', '', src, flags=re.DOTALL)

    # 4. Verwijder quote sectie
    src = re.sub(
        r'\n<section[^>]*style="background:var\(--ink\)"[^>]*>.*?</section>',
        '', src, flags=re.DOTALL
    )

    write(fpath, src)
    print(f'  {fpath}: {len(src.splitlines())}L')

print('Klaar.')
