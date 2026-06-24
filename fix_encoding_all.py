"""
fix_encoding_all.py
Mojibake = UTF-8 bytes opgeslagen als latin-1, dan opnieuw als UTF-8 gelezen.
Resultaat: elke UTF-8 multibyte sequence is als losse latin-1 tekens opgeslagen.
Fix: encode de mojibake string terug naar latin-1 bytes, decode dan als UTF-8.
"""
import os, glob, re

REPO = os.path.dirname(os.path.abspath(__file__))

def decode_mojibake(text):
    """
    Zoek naar aaneengesloten reeksen van latin-1 special chars (0x80-0xFF)
    die samen geldige UTF-8 vormen, en vervang ze door de juiste unicode.
    """
    # Patroon: 1 of meer opeenvolgende chars in bereik U+0080..U+00FF
    pattern = re.compile(r'[\x80-\xFF]+')

    def try_fix(m):
        fragment = m.group(0)
        try:
            fixed = fragment.encode('latin-1').decode('utf-8')
            return fixed
        except (UnicodeDecodeError, UnicodeEncodeError):
            return fragment  # niet aan te passen, laat staan

    return pattern.sub(try_fix, text)

def fix_file(path):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    fixed = decode_mojibake(content)
    # Verwijder ook BOM
    fixed = fixed.lstrip('﻿')
    if fixed != content:
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(fixed)
        return True
    return False

html_files = glob.glob(os.path.join(REPO, '*.html'))
fixed_count = 0
for path in sorted(html_files):
    if fix_file(path):
        fixed_count += 1
        print(f'  Gecorrigeerd: {os.path.basename(path)}')

print(f'\nKlaar. {fixed_count}/{len(html_files)} bestanden bijgewerkt.')
