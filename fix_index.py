import re, os

ROOT = r'C:/Users/Gebruiker/spring-real-estate-concept'

# Read the clean base (old nav structure, correct HTML)
with open(os.path.join(ROOT, 'index_base.html'), encoding='utf-8-sig') as f:
    base = f.read()

# Read the current about.html to grab the correct nav block
with open(os.path.join(ROOT, 'about.html'), encoding='utf-8') as f:
    about = f.read()

# Extract nav block from about.html (from <nav class="nav"> to </nav>)
nav_m = re.search(r'<nav class="nav">(.*?)</nav>', about, re.DOTALL)
if not nav_m:
    print('ERROR: could not find nav in about.html')
    exit(1)
nav_inner = nav_m.group(1)  # everything inside <nav>...</nav>

# Replace the nav in the base index with the current nav
fixed = re.sub(
    r'<nav class="nav">.*?</nav>',
    '<nav class="nav">' + nav_inner + '</nav>',
    base,
    flags=re.DOTALL
)

# Update CSS version to v30
fixed = fixed.replace('styles.css?v=28', 'styles.css?v=30')
fixed = fixed.replace('styles.css?v=29', 'styles.css?v=30')

# Also update mobile nav (mm-nav) to match - find it in about.html
mm_m = re.search(r'<nav class="mm-nav">(.*?)</nav>', about, re.DOTALL)
if mm_m:
    mm_inner = mm_m.group(1)
    fixed = re.sub(
        r'<nav class="mm-nav">.*?</nav>',
        '<nav class="mm-nav">' + mm_inner + '</nav>',
        fixed,
        flags=re.DOTALL
    )

with open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(fixed)

print('index.html restored and updated')
