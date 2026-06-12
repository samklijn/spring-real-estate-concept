# -*- coding: utf-8 -*-
"""Idempotent: voeg Fraunces toe aan de Google-Fonts link op elke HTML-pagina."""
import glob, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = 'family=Raleway:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,500&display=swap'
NEW = 'family=Raleway:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,500&family=Fraunces:ital,opsz,wght@1,9..144,400;1,9..144,500&display=swap'
n = 0
for f in glob.glob(os.path.join(ROOT, '*.html')):
    s = open(f, encoding='utf-8').read()
    if OLD in s:
        open(f, 'w', encoding='utf-8').write(s.replace(OLD, NEW))
        n += 1
print('updated', n, 'pages with Fraunces')
