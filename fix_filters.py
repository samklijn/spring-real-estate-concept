import re

def move_filter_to_hero(filepath, search_placeholder):
    with open(filepath, encoding='utf-8') as f:
        txt = f.read()

    # Extract the team-filter div
    m = re.search(r'(<div class="team-filter">[\s\S]*?</div>)', txt)
    if not m:
        print(f'No team-filter found in {filepath}')
        return
    team_filter_html = m.group(1)

    # Insert team-filter into page-hero, before the <form class="search
    # Find the form in the hero and insert before it
    hero_form_pat = r'(<form class="search search--light search--single")'
    replacement = team_filter_html + '\n  \\1'
    txt2 = re.sub(hero_form_pat, replacement, txt, count=1)

    # Remove original team-filter from filterable section (now duplicated)
    # It appears twice now; remove the second occurrence
    first_pos = txt2.find(team_filter_html)
    second_pos = txt2.find(team_filter_html, first_pos + 1)
    if second_pos != -1:
        txt2 = txt2[:second_pos] + txt2[second_pos + len(team_filter_html):]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(txt2)
    print(f'Done: {filepath}')

move_filter_to_hero(r'C:/Users/Gebruiker/spring-real-estate-concept/agents.html', 'expert')
move_filter_to_hero(r'C:/Users/Gebruiker/spring-real-estate-concept/resources.html', 'marktinzichten')
