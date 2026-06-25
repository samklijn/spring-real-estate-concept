import glob, re, subprocess, os

ROOT = r'C:/Users/Gebruiker/spring-real-estate-concept'
files = glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True)
broken = []
for f in files:
    with open(f, encoding='utf-8') as fh:
        txt = fh.read()
    tb = re.search(r'<div class="topbar">.*?</div>\n</div>', txt, re.DOTALL)
    if tb and 'has-drop' in tb.group(0):
        broken.append(os.path.basename(f))

print(len(broken), 'broken files:')
for b in broken:
    print(' ', b)
