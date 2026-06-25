import glob, os

ROOT = r'C:/Users/Gebruiker/spring-real-estate-concept'

# Simple string replacements: add data-i18n to nav spans
REPLACEMENTS = [
    # Nav buttons
    ('<button><span>Aanbod</span>',       '<button><span data-i18n="nav.aanbod">Aanbod</span>'),
    ('<button><span>Resources</span>',    '<button><span data-i18n="nav.resources">Resources</span>'),
    ('<button><span>Team</span>',         '<button><span data-i18n="nav.team">Team</span>'),
    ('<button><span>Vacatures</span>',    '<button><span data-i18n="nav.vacatures">Vacatures</span>'),
    ('<button><span>About</span>',        '<button><span data-i18n="nav.about">About</span>'),
    # Simple link
    ('<a href="vacatures.html">Vacatures</a>', '<a href="vacatures.html" data-i18n="nav.vacatures">Vacatures</a>'),
    # Aanbod dropdown items
    ('<span class="d-t">Koopobjecten</span>',                       '<span class="d-t" data-i18n="nav.koop">Koopobjecten</span>'),
    ('<span class="d-d">Kantoor en bedrijfsruimte te koop</span>',  '<span class="d-d" data-i18n="nav.koop.d">Kantoor en bedrijfsruimte te koop</span>'),
    ('<span class="d-t">Huurobjecten</span>',                       '<span class="d-t" data-i18n="nav.huur">Huurobjecten</span>'),
    ('<span class="d-d">Kantoor en bedrijfsruimte te huur</span>',  '<span class="d-d" data-i18n="nav.huur.d">Kantoor en bedrijfsruimte te huur</span>'),
    # Resources dropdown items
    ('<span class="d-t">Cases</span>',                              '<span class="d-t" data-i18n="nav.cases">Cases</span>'),
    ('<span class="d-d">Resultaten voor onze klanten</span>',       '<span class="d-d" data-i18n="nav.cases.d">Resultaten voor onze klanten</span>'),
    ('<span class="d-t">Transacties</span>',                        '<span class="d-t" data-i18n="nav.transacties">Transacties</span>'),
    ('<span class="d-d">Vastgoeddeals en marktdata</span>',         '<span class="d-d" data-i18n="nav.transacties.d">Vastgoeddeals en marktdata</span>'),
    ('<span class="d-t">Algemeen</span>',                           '<span class="d-t" data-i18n="nav.algemeen">Algemeen</span>'),
    ('<span class="d-d">Analyses, trends en inzichten</span>',      '<span class="d-d" data-i18n="nav.algemeen.d">Analyses, trends en inzichten</span>'),
    # Team dropdown items
    ('<span class="d-t">Huidig team</span>',                        '<span class="d-t" data-i18n="nav.huidig.team">Huidig team</span>'),
    ('<span class="d-d">100+ vastgoedspecialisten</span>',          '<span class="d-d" data-i18n="nav.huidig.team.d">100+ vastgoedspecialisten</span>'),
    ('<span class="d-t">Word jij onze nieuwe collega?</span>',      '<span class="d-t" data-i18n="nav.join">Word jij onze nieuwe collega?</span>'),
    ('<span class="d-d">Bekijk vacatures</span>',                   '<span class="d-d" data-i18n="nav.join.d">Bekijk vacatures</span>'),
    # About dropdown items
    ('<span class="d-t">Over Spring</span>',                        '<span class="d-t" data-i18n="nav.over.spring">Over Spring</span>'),
    ('<span class="d-d">Wie wij zijn en wat we doen</span>',        '<span class="d-d" data-i18n="nav.over.spring.d">Wie wij zijn en wat we doen</span>'),
    ('<span class="d-t">Onze locaties</span>',                      '<span class="d-t" data-i18n="nav.locaties">Onze locaties</span>'),
    ('<span class="d-d">Amsterdam, Utrecht &amp; Spanje</span>',    '<span class="d-d" data-i18n="nav.locaties.d">Amsterdam, Utrecht &amp; Spanje</span>'),
]

files = glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True)
count = 0
for f in files:
    with open(f, encoding='utf-8') as fh:
        txt = fh.read()
    new = txt
    for old, rep in REPLACEMENTS:
        new = new.replace(old, rep)
    if new != txt:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(new)
        count += 1

print(f'Updated {count} files with i18n nav attributes')
