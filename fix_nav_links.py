import os, re, glob

ROOT = r'C:/Users/Gebruiker/spring-real-estate-concept'

files = glob.glob(ROOT + '/*.html')
updated = 0

for path in files:
    with open(path, encoding='utf-8') as f:
        src = f.read()

    orig = src

    # Fix Transacties nav link: href="resources.html" right before nav.transacties span
    # Pattern: <a href="resources.html"><span ...>...<span ... data-i18n="nav.transacties">
    src = re.sub(
        r'(<a href=")resources\.html("><span class="d-ic">(?:[^<]|<(?!/a>))*?data-i18n="nav\.transacties")',
        r'\1transacties.html\2',
        src
    )

    # Fix Algemeen nav link similarly
    src = re.sub(
        r'(<a href=")resources\.html("><span class="d-ic">(?:[^<]|<(?!/a>))*?data-i18n="nav\.algemeen")',
        r'\1algemeen.html\2',
        src
    )

    if src != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(src)
        updated += 1

print(f'Updated {updated} files out of {len(files)}')
