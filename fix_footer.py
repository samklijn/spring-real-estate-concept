import re, os, subprocess, glob

ROOT = r'C:/Users/Gebruiker/spring-real-estate-concept'

# Get correct mm-nav from about.html (current, correctly structured nav)
with open(os.path.join(ROOT, 'about.html'), encoding='utf-8') as f:
    about = f.read()
mm_m = re.search(r'<nav class="mm-nav">(.*?)</nav>', about, re.DOTALL)
mm_inner = mm_m.group(1) if mm_m else ''

files = glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True)
fixed = 0

for fpath in files:
    fname = os.path.basename(fpath)

    with open(fpath, encoding='utf-8') as f:
        current = f.read()

    # Get old clean version from git
    result = subprocess.run(['git', 'show', f'1d553cf:{fname}'],
                            capture_output=True, encoding='utf-8', cwd=ROOT)
    if result.returncode != 0 or not result.stdout.strip():
        continue
    old = result.stdout

    # Extract footer block from old version
    # Marker: <section class="talk-strip"> or <footer if no talk-strip
    foot_m = re.search(r'(<section class="talk-strip">.*)', old, re.DOTALL)
    if not foot_m:
        foot_m = re.search(r'(<footer class="footer">.*)', old, re.DOTALL)
    if not foot_m:
        continue
    old_footer_block = foot_m.group(1)

    # Update mm-nav inside footer block with current nav
    old_footer_block = re.sub(
        r'<nav class="mm-nav">.*?</nav>',
        '<nav class="mm-nav">' + mm_inner + '</nav>',
        old_footer_block, flags=re.DOTALL
    )

    # Update script/CSS versions
    old_footer_block = old_footer_block.replace('styles.css?v=28', 'styles.css?v=30')
    old_footer_block = old_footer_block.replace('?v=26', '?v=30')

    # Find where the footer block starts in CURRENT file
    # Use the same marker, but current file may be broken — find by talk-strip or footer
    cur_foot_m = re.search(r'<section class="talk-strip">', current)
    if not cur_foot_m:
        cur_foot_m = re.search(r'<footer class="footer">', current)
    if not cur_foot_m:
        # No footer marker found — append footer to end before </body>
        new = current.replace('</body>', '\n' + old_footer_block + '\n</body>', 1)
    else:
        # Replace everything from footer marker to end with old footer block
        new = current[:cur_foot_m.start()] + old_footer_block

    if new != current:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new)
        fixed += 1

print(f'Footer restored on {fixed} pages')
