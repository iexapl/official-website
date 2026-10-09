#!/usr/bin/env python3
"""
Verify nav fix across all 129 pages.
"""
import re
import os
import glob


def normalize_nav(nav_html):
    """Remove class attributes and normalize whitespace for comparison."""
    # Remove all class="..." attributes
    text = re.sub(r'\s*class="[^"]*"', '', nav_html)
    # Normalize whitespace
    text = re.sub(r'>\s+<', '><', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text


def extract_menu_part(nav_html):
    """Return nav content before lang-switcher."""
    parts = nav_html.split('<div class="lang-switcher"')
    return parts[0] + '</nav>' if len(parts) > 1 else nav_html


def verify():
    errors = []
    passed = 0
    failed = 0

    for lang in ["zh", "en", "fr"]:
        # Load baseline from homepage
        with open(f"{lang}/index.html", 'r', encoding='utf-8') as f:
            baseline_content = f.read()
        baseline_nav_match = re.search(r'<nav class="nav">.*?</nav>', baseline_content, re.DOTALL)
        if not baseline_nav_match:
            errors.append(f"FAIL: {lang}/index.html has no nav")
            failed += 1
            continue
        baseline_nav = baseline_nav_match.group(0)
        baseline_menu = extract_menu_part(baseline_nav)
        baseline_normalized = normalize_nav(baseline_menu)

        html_files = sorted(glob.glob(f"{lang}/*.html"))
        for filepath in html_files:
            basename = os.path.basename(filepath)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            nav_match = re.search(r'<nav class="nav">.*?</nav>', content, re.DOTALL)
            if not nav_match:
                errors.append(f"FAIL: {filepath} - no nav found")
                failed += 1
                continue

            nav = nav_match.group(0)
            menu_part = extract_menu_part(nav)
            menu_normalized = normalize_nav(menu_part)

            # Assertion a: menu matches baseline
            if menu_normalized != baseline_normalized:
                errors.append(f"FAIL: {filepath} - menu does not match baseline")
                # Show first diff
                if len(menu_normalized) != len(baseline_normalized):
                    errors.append(f"  length diff: baseline={len(baseline_normalized)} page={len(menu_normalized)}")
                failed += 1
                continue

            # Assertion b: exactly one active in menu, href basename == current page filename
            # Find all tags with class="...active..." in menu_part
            active_tags = re.findall(r'<a[^>]*class="[^"]*active[^"]*"[^>]*href="([^"]+)"[^>]*>', menu_part)
            # Also check class after href
            active_tags += re.findall(r'<a[^>]*href="([^"]+)"[^>]*class="[^"]*active[^"]*"[^>]*>', menu_part)

            if len(active_tags) != 1:
                errors.append(f"FAIL: {filepath} - expected 1 menu active, found {len(active_tags)}: {active_tags}")
                failed += 1
                continue

            active_href = os.path.basename(active_tags[0])
            if active_href != basename:
                errors.append(f"FAIL: {filepath} - active href basename '{active_href}' != page '{basename}'")
                failed += 1
                continue

            # Assertion c: exactly one active in lang-switcher, and it's current lang
            lang_part = nav.split('<div class="lang-switcher"')[1] if '<div class="lang-switcher"' in nav else ''
            lang_actives = re.findall(r'<a[^>]*class="[^"]*active[^"]*"[^>]*>([^<]+)</a>', lang_part)

            if len(lang_actives) != 1:
                errors.append(f"FAIL: {filepath} - expected 1 lang active, found {len(lang_actives)}: {lang_actives}")
                failed += 1
                continue

            expected_lang = {"zh": "中", "en": "EN", "fr": "FR"}[lang]
            if lang_actives[0] != expected_lang:
                errors.append(f"FAIL: {filepath} - lang active '{lang_actives[0]}' != expected '{expected_lang}'")
                failed += 1
                continue

            errors.append(f"PASS: {filepath}")
            passed += 1

    # Also check root index.html if it has nav
    if os.path.exists("index.html"):
        with open("index.html", 'r', encoding='utf-8') as f:
            content = f.read()
        if '<nav class="nav">' in content:
            nav_match = re.search(r'<nav class="nav">.*?</nav>', content, re.DOTALL)
            if nav_match:
                nav = nav_match.group(0)
                menu_part = extract_menu_part(nav)
                menu_normalized = normalize_nav(menu_part)
                # Compare to zh baseline (root index is Chinese)
                with open("zh/index.html", 'r', encoding='utf-8') as f:
                    baseline = f.read()
                baseline_nav = re.search(r'<nav class="nav">.*?</nav>', baseline, re.DOTALL).group(0)
                baseline_menu = extract_menu_part(baseline_nav)
                baseline_normalized = normalize_nav(baseline_menu)
                if menu_normalized == baseline_normalized:
                    active_tags = re.findall(r'<a[^>]*class="[^"]*active[^"]*"[^>]*href="([^"]+)"[^>]*>', menu_part)
                    active_tags += re.findall(r'<a[^>]*href="([^"]+)"[^>]*class="[^"]*active[^"]*"[^>]*>', menu_part)
                    if len(active_tags) == 1 and os.path.basename(active_tags[0]) == "index.html":
                        errors.append("PASS: index.html")
                        passed += 1
                    else:
                        errors.append(f"FAIL: index.html - active issue: {active_tags}")
                        failed += 1
                else:
                    errors.append("FAIL: index.html - menu does not match zh baseline")
                    failed += 1

    print(f"\n{'='*60}")
    print(f"RESULTS: {passed} passed, {failed} failed")
    print(f"{'='*60}\n")
    for msg in errors:
        print(msg)

    return failed == 0


if __name__ == "__main__":
    ok = verify()
    exit(0 if ok else 1)
