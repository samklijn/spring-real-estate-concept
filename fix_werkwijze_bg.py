import glob

def read(f):
    with open(f, encoding='utf-8') as fh: return fh.read()
def write(f, s):
    with open(f, 'w', encoding='utf-8') as fh: fh.write(s)

for fpath in sorted(glob.glob('unit-*.html')):
    if 'herbouwwaarde' in fpath:
        continue
    src = read(fpath)
    new = src.replace(
        '<section class="section--tight section--soft" id="werkwijze">',
        '<section class="section--tight" id="werkwijze">'
    )
    if new != src:
        write(fpath, new)
        print(f'  {fpath}: OK')
    else:
        print(f'  {fpath}: geen match')
