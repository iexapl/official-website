#!/usr/bin/env python3
"""
Fix nav menu across all 129 pages:
1. Replace menu text with homepage baseline
2. Set correct active class
3. Fix lang-switcher active
"""
import re
import os
import glob

BASE_DIR = "."

# Mapping of page filename -> which href basename should be active
# For dropdown items, the href basename equals the page filename
# For top-level triggers (default pages), we use the trigger's href
ACTIVE_MAP = {
    # Top-level pages
    "index.html": "index.html",
    "about.html": "about.html",
    "contact.html": "contact.html",
    # Service pages
    "service-software.html": "service-software.html",  # top trigger
    "service-ai.html": "service-ai.html",  # dropdown
    "service-modeling.html": "service-modeling.html",  # dropdown
    # Software product pages
    "product-software-hr.html": "product-software-hr.html",  # top trigger
    "product-software-bim.html": "product-software-bim.html",
    "product-software-blacklist.html": "product-software-blacklist.html",
    "product-software-budget.html": "product-software-budget.html",
    "product-software-dashboard.html": "product-software-dashboard.html",
    "product-software-ibms.html": "product-software-ibms.html",
    "product-software-info.html": "product-software-info.html",
    "product-software-inspection.html": "product-software-inspection.html",
    "product-software-warehouse.html": "product-software-warehouse.html",
    "product-software-workorder.html": "product-software-workorder.html",
    # Hardware product pages
    "product-hardware-camera.html": "product-hardware-camera.html",  # top trigger
    "product-hardware-adscreen.html": "product-hardware-adscreen.html",
    "product-hardware-attendance.html": "product-hardware-attendance.html",
    "product-hardware-drone.html": "product-hardware-drone.html",
    "product-hardware-edge.html": "product-hardware-edge.html",
    "product-hardware-gate.html": "product-hardware-gate.html",
    "product-hardware-gps.html": "product-hardware-gps.html",
    "product-hardware-led.html": "product-hardware-led.html",
    "product-hardware-oil.html": "product-hardware-oil.html",
    "product-hardware-passage.html": "product-hardware-passage.html",
    "product-hardware-splicing.html": "product-hardware-splicing.html",
    # Solution pages
    "solution-parking.html": "solution-parking.html",  # top trigger
    "solution-airport.html": "solution-airport.html",
    "solution-broadcast.html": "solution-broadcast.html",
    "solution-building.html": "solution-building.html",
    "solution-campus.html": "solution-campus.html",
    "solution-city.html": "solution-city.html",
    "solution-community.html": "solution-community.html",
    "solution-conference.html": "solution-conference.html",
    "solution-construction.html": "solution-construction.html",
    "solution-datacenter.html": "solution-datacenter.html",
    "solution-eagle.html": "solution-eagle.html",
    "solution-fire.html": "solution-fire.html",
    "solution-iptv.html": "solution-iptv.html",
    "solution-patrol.html": "solution-patrol.html",
    "solution-solar.html": "solution-solar.html",
    "solution-traffic.html": "solution-traffic.html",
}


def extract_baseline_nav(filepath):
    """Extract nav from homepage, keeping everything up to </nav>."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'(<nav class="nav">.*?</nav>)', content, re.DOTALL)
    if not m:
        raise ValueError(f"No nav found in {filepath}")
    return m.group(1)


def get_lang_switcher_from_page(filepath):
    """Extract the lang-switcher block from a page (to preserve hrefs)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'(<div class="lang-switcher".*?</div>\s*</nav>)', content, re.DOTALL)
    if not m:
        # fallback: try without the closing nav
        m = re.search(r'(<div class="lang-switcher".*?</div>)', content, re.DOTALL)
    return m.group(1) if m else None


def build_nav_for_page(baseline_nav, page_path, lang):
    """Build corrected nav for a specific page."""
    basename = os.path.basename(page_path)
    active_href = ACTIVE_MAP.get(basename)
    if not active_href:
        raise ValueError(f"No active mapping for {basename}")

    # Split baseline into menu part and lang-switcher part
    # The baseline lang-switcher always points to index.html
    # We need to rebuild it for the current page

    # Extract menu items from baseline (everything inside nav before lang-switcher)
    menu_match = re.search(r'<nav class="nav">(.*?)(?:<div class="lang-switcher".*)', baseline_nav, re.DOTALL)
    if not menu_match:
        raise ValueError("Could not split baseline nav")
    menu_part = menu_match.group(1)

    # Remove all existing active classes from menu part
    menu_part = re.sub(r'\sclass="([^"]*)active([^"]*)"',
                       lambda m: f' class="{m.group(1).strip()}{m.group(2).strip()}"'.strip() if (m.group(1).strip() or m.group(2).strip()) else '',
                       menu_part)
    menu_part = re.sub(r'class="\s*"', '', menu_part)
    menu_part = menu_part.replace('  ', ' ')

    # Add active to the correct element
    # Strategy: find the exact href and add active class
    # We need to handle two cases:
    # 1. Simple <a href="...">
    # 2. Already has some class

    # Find the tag with href="active_href" in menu_part
    # We want to match <a href="active_href"> or <a href="active_href" class="...">
    # But NOT match partial hrefs

    def add_active_to_href(text, href):
        # Match <a href="exact_href"> or <a href="exact_href" class="...">
        # or <a class="..." href="exact_href">
        pattern = r'(<a\s+[^>]*href="' + re.escape(href) + r'"[^>]*?)>'

        def repl(m):
            tag = m.group(1)
            if 'class=' in tag:
                # Add active to existing class
                tag = re.sub(r'class="([^"]*)"', lambda c: f'class="{c.group(1)} active"', tag)
            else:
                tag += ' class="active"'
            return tag + '>'

        return re.sub(pattern, repl, text, count=1)

    menu_part = add_active_to_href(menu_part, active_href)

    # Build lang-switcher: hrefs should point to same page in other languages
    # For zh/page.html: ../zh/page.html, ../en/page.html, ../fr/page.html
    # The lang-switcher in the baseline has ../zh/index.html etc.
    # We need to replace "index.html" with the current basename

    current_basename = basename
    if lang == "zh":
        zh_active, en_active, fr_active = ' class="active"', '', ''
    elif lang == "en":
        zh_active, en_active, fr_active = '', ' class="active"', ''
    elif lang == "fr":
        zh_active, en_active, fr_active = '', '', ' class="active"'
    else:
        zh_active = en_active = fr_active = ''

    lang_switcher = f'''      <div class="lang-switcher" style="display:flex;align-items:center;gap:8px;margin-left:auto;padding-left:16px;border-left:1px solid rgba(255,255,255,0.2);font-size:0.9rem;">
        <a href="../zh/{current_basename}"{zh_active}>中</a>
        <a href="../en/{current_basename}"{en_active}>EN</a>
        <a href="../fr/{current_basename}"{fr_active}>FR</a>
      </div>
    </nav>'''

    return f'<nav class="nav">\n{menu_part}{lang_switcher}'


def main():
    # Extract baselines
    baselines = {
        "zh": extract_baseline_nav("zh/index.html"),
        "en": extract_baseline_nav("en/index.html"),
        "fr": extract_baseline_nav("fr/index.html"),
    }

    # Also handle root index.html
    # The root index.html probably redirects or is the Chinese homepage
    # Let's check its current nav
    root_nav = None
    if os.path.exists("index.html"):
        with open("index.html", 'r', encoding='utf-8') as f:
            root_content = f.read()
        if '<nav class="nav">' in root_content:
            root_nav = extract_baseline_nav("index.html")

    pages_fixed = 0

    for lang in ["zh", "en", "fr"]:
        baseline = baselines[lang]
        html_files = sorted(glob.glob(f"{lang}/*.html"))

        for filepath in html_files:
            basename = os.path.basename(filepath)

            if basename == "index.html":
                # For homepages, we just need to ensure lang-switcher is correct
                # and there's exactly one active on the home link
                # Let's still rebuild to be safe
                new_nav = build_nav_for_page(baseline, filepath, lang)
            else:
                new_nav = build_nav_for_page(baseline, filepath, lang)

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            old_nav_match = re.search(r'<nav class="nav">.*?</nav>', content, re.DOTALL)
            if not old_nav_match:
                print(f"SKIP: no nav in {filepath}")
                continue

            old_nav = old_nav_match.group(0)
            if old_nav == new_nav:
                print(f"SKIP: no change needed for {filepath}")
                continue

            new_content = content.replace(old_nav, new_nav)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            pages_fixed += 1
            print(f"FIXED: {filepath}")

    print(f"\nTotal pages fixed: {pages_fixed}")


if __name__ == "__main__":
    main()
