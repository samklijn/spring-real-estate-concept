content = open('index.html', encoding='utf-8').read()
# Remove BOM
if content.startswith('﻿'):
    content = content[1:]
# Fix remaining mojibake - build pairs from utf-8 -> cp1252 -> bad pattern
import unicodedata
fixes = []
# Known remaining issues
pairs = [
    ('¿', None),  # ¿
    ('Á', None),  # Á (Ámsterdam)
]
# Auto-generate mojibake patterns
for correct_char, _ in pairs:
    try:
        bad = correct_char.encode('utf-8').decode('cp1252')
        fixes.append((bad, correct_char))
    except Exception as e:
        print(f'Skipping {repr(correct_char)}: {e}')

# Sort longest first
fixes.sort(key=lambda x: -len(x[0]))
for bad, good in fixes:
    if bad in content:
        count = content.count(bad)
        content = content.replace(bad, good)
        print(f'Fixed {repr(bad)} -> {repr(good)}: {count}x')

# Also fix Ámsterdam specifically (the Á case where 0x81 is dropped)
# U+00C1 = UTF-8 C3 81. In CP1252, 0x81 is undefined so it becomes Ã + nothing
# The result in the file would be Ã followed by the next char 'm'
# This is tricky - let's check for the specific pattern
if 'Ãmster' in content:
    content = content.replace('Ãmster', 'Ámster')
    print('Fixed Ãmster -> Ámster')

open('index.html', 'w', encoding='utf-8', newline='').write(content)
print('Done')
