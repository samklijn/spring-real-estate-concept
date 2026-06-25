import re, os, subprocess, glob

ROOT = r'C:/Users/Gebruiker/spring-real-estate-concept'
BROKEN = ['diensten.html', 'listing-detail.html', 'listings.html']

# Get correct nav from about.html
with open(os.path.join(ROOT, 'about.html'), encoding='utf-8') as f:
    about = f.read()
nav_m = re.search(r'<nav class="nav">(.*?)</nav>', about, re.DOTALL)
nav_inner = nav_m.group(1)
mm_m = re.search(r'<nav class="mm-nav">(.*?)</nav>', about, re.DOTALL)
mm_inner = mm_m.group(1) if mm_m else None

for fname in BROKEN:
    fpath = os.path.join(ROOT, fname)

    # Get old clean version from git
    result = subprocess.run(['git', 'show', f'1d553cf:{fname}'],
                            capture_output=True, encoding='utf-8', cwd=ROOT)
    old = result.stdout

    # Inject current nav into old version's header nav
    fixed = re.sub(r'<nav class="nav">.*?</nav>',
                   '<nav class="nav">' + nav_inner + '</nav>',
                   old, flags=re.DOTALL)
    if mm_inner:
        fixed = re.sub(r'<nav class="mm-nav">.*?</nav>',
                       '<nav class="mm-nav">' + mm_inner + '</nav>',
                       fixed, flags=re.DOTALL)

    # Update CSS version
    fixed = fixed.replace('styles.css?v=28', 'styles.css?v=30')

    # Keep page body content from CURRENT file (everything after </header>)
    with open(fpath, encoding='utf-8') as f:
        current = f.read()

    after_m_cur = re.search(r'</header>(.*)', current, re.DOTALL)
    after_m_fix = re.search(r'</header>(.*)', fixed, re.DOTALL)
    if after_m_cur and after_m_fix:
        fixed = fixed[:after_m_fix.start(1)] + after_m_cur.group(1)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(fixed)
    print(f'Fixed: {fname}')

print('Done')
