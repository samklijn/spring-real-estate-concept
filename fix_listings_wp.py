"""Voeg data-wp en data-wensen toe aan alle listing-cards."""

replacements = [
    # (uniek fragment in href, wp, wensen)
    ('mahler-tower-14e', '60', 'parkeren vergaderen lift receptie breeam'),
    ('wtc-amsterdam-tower-c', '8', 'receptie vergaderen lift'),
    ('gustav-mahlerplein-109', '30', 'parkeren vergaderen ov'),
    ('strawinskylaan-3051', '75', 'parkeren vergaderen lift breeam'),
    ('stationsplein-8', '50', 'ov vergaderen lift'),
    ('industrieweg-40', '0', 'parkeren'),
    ('oudegracht-187', '0', 'ov'),
    ('paseo-de-la-alameda', '12', 'receptie vergaderen'),
    ('avenida-del-puerto', '0', 'parkeren'),
    ('stadhouderskade-12', '0', 'parkeren vergaderen'),
    ('keizersgracht-210', '0', 'vergaderen lift ov'),
    ('croeselaan-28', '0', 'parkeren vergaderen lift breeam'),
    ('carrer-de-col', '0', 'vergaderen'),
    ('estepona-marina', '0', 'parkeren'),
]

with open('listings.html', encoding='utf-8') as f:
    src = f.read()

for slug, wp, wensen in replacements:
    # find the prop-card anchor containing this slug
    import re
    pat = r'(class="prop-card flisting" href="[^"]*' + re.escape(slug) + r'[^"]*"[^>]+)(data-avail="[^"]*")'
    def add_attrs(m):
        full = m.group(0)
        if 'data-wp=' in full:
            return full
        return m.group(1) + m.group(2) + f' data-wp="{wp}" data-wensen="{wensen}"'
    src = re.sub(pat, add_attrs, src)

with open('listings.html', 'w', encoding='utf-8') as f:
    f.write(src)

print('Klaar.')
