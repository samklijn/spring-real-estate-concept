"""
fix_encoding_final.py
Herstelt alle HTML bestanden:
1. Leest ruwe bytes
2. Probeert eerst als UTF-8 te decoderen
3. Als er mojibake in zit: encode latin-1 -> decode UTF-8 per substring
4. Bumpt CSS versie naar v=22
5. Schrijft terug als UTF-8 zonder BOM

NOOIT meer PowerShell gebruiken voor bestanden met speciale tekens!
"""
import os, glob, re

REPO = os.path.dirname(os.path.abspath(__file__))
TARGET_VERSION = '22'

def fix_mojibake(text):
    """
    Vervangt aaneengesloten sequences van latin-1 upper bytes (U+0080..U+00FF)
    plus CP1252 'special' hoger-unicode tekens die vaak samen voorkomen in mojibake.
    """
    # CP1252 speciale chars die in mojibake zitten (boven U+00FF)
    # worden apart afgevangen via directe string replace
    direct_fixes = [
        # Volgorde: langste sequenties eerst
        ('â€”', '—'),  # â€" -> — (em dash)  [E2 80 9D in CP1252 = "]
        ('â€œ', '“'),  # â€œ -> " (left dbl quote) [9C=œ]
        ('â€˜', '‘'),  # â€˜ -> ' (left sgl quote) [98=˜]
        ('â€™', '’'),  # â€™ -> ' (right sgl quote) [99=™]
        ('â€“', '–'),  # â€" -> – (en dash) [93="]
        ('â€\xa6', '…'),    # â€¦ -> … (ellipsis) [A6]
        ('â€ˆ', '†'),  # â€  -> † [86=ˆ] -- dagger
        ('â†’', '→'),  # â†' -> → [E2 86 92]
        ('â†”', '↓'),  # â†" -> ↓ [E2 86 93]
        ('â…\xac', '€'),    # â‚¬ -> € [E2 82 AC]
        # Bij dubbel-encoded: eerst ontdubbelen
        ('ÃƒÂ\xb7', '\xb7'),  # Ã‚· -> ·
        ('Ã‚Â\xac', '€'), # Ã‚¬ -> €
    ]

    for bad, good in direct_fixes:
        text = text.replace(bad, good)

    # Dan de 0x80-0xFF single-byte mojibake aanpakken
    def try_decode_latin1(m):
        fragment = m.group(0)
        try:
            return fragment.encode('latin-1').decode('utf-8')
        except Exception:
            return fragment

    text = re.sub(r'[\x80-\xff]+', try_decode_latin1, text)
    return text

def process_file(path):
    # Lees altijd als raw bytes
    with open(path, 'rb') as f:
        raw = f.read()

    # Strip UTF-8 BOM als aanwezig
    if raw.startswith(b'\xef\xbb\xbf'):
        raw = raw[3:]

    # Decodeer als UTF-8
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        # Probeer latin-1 als fallback
        text = raw.decode('latin-1')

    # Fix mojibake
    fixed = fix_mojibake(text)

    # Bump CSS/JS versie
    fixed = re.sub(r'\?v=\d+', f'?v={TARGET_VERSION}', fixed)

    # Schrijf terug als UTF-8 zonder BOM, Unix newlines
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(fixed)

html_files = glob.glob(os.path.join(REPO, '*.html'))
print(f'Verwerken {len(html_files)} bestanden...')
for path in sorted(html_files):
    process_file(path)

# Controleer listings.html na fix
with open(os.path.join(REPO, 'listings.html'), encoding='utf-8') as f:
    sample = f.read()
idx = sample.find('Partner Marketing')
print('\nSample na fix:', repr(sample[idx:idx+30]))
idx2 = sample.find('kwartaal')
print('Scarcity na fix:', repr(sample[idx2:idx2+35]))

print('\nKlaar. Alle bestanden gefixed en versie naar v=22 gebracht.')
