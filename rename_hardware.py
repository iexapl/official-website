#!/usr/bin/env python3
"""
Hardware product rename script.
Uses placeholder approach to avoid substring re-replacement issues.
"""
import os
import re
import json

# Replacement mappings per language: (old_text, new_text)
# Sorted by length (longest first) to handle substring cases.
# Includes both navigation names and product page title/h1 texts.
REPLACEMENTS = {
    "zh": [
        ("车辆偷油传感器", "车辆油耗与防偷油传感器"),
        ("车辆定位传感器", "车辆定位终端"),
        ("考勤设备", "考勤与门禁设备"),
        ("视频监控", "视频监控系统"),
        ("人行通道", "人行通道设备"),
        ("广告屏", "广告与信息显示屏"),
        ("拼接屏", "拼接屏系统"),
        ("户外LED屏", "户外 LED 大屏"),
    ],
    "en": [
        ("Attendance &amp; Access Control Equipment", "Attendance &amp; Access Control Equipment"),  # guard (already new)
        ("Attendance & Access Control Equipment", "Attendance & Access Control Equipment"),  # guard
        ("Attendance Devices", "Attendance &amp; Access Control Equipment"),
        ("Vehicle Fuel Consumption &amp; Anti-Theft Sensor", "Vehicle Fuel Consumption &amp; Anti-Theft Sensor"),  # guard
        ("Vehicle Fuel Theft Sensor", "Vehicle Fuel Consumption &amp; Anti-Theft Sensor"),
        ("Vehicle GPS Tracking Terminal", "Vehicle GPS Tracking Terminal"),  # guard
        ("Vehicle GPS Tracker", "Vehicle GPS Tracking Terminal"),
        ("Pedestrian Passage Equipment", "Pedestrian Passage Equipment"),  # guard
        ("Pedestrian Access", "Pedestrian Passage Equipment"),
        ("Advertising &amp; Information Display", "Advertising &amp; Information Display"),  # guard
        ("Advertising Screen", "Advertising &amp; Information Display"),
        ("Video Wall System", "Video Wall System"),  # guard
        ("Video Walls", "Video Wall System"),
        ("Video Wall", "Video Wall System"),
        ("Outdoor LED Display", "Outdoor LED Display"),  # guard (already new)
        ("LED Displays", "Outdoor LED Display"),
        ("CCTV System", "CCTV System"),  # guard
        ("CCTV", "CCTV System"),
        ("Attendance", "Attendance &amp; Access Control Equipment"),
        ("Fuel Sensor", "Vehicle Fuel Consumption &amp; Anti-Theft Sensor"),
        ("GPS Tracker", "Vehicle GPS Tracking Terminal"),
        ("Access Gates", "Pedestrian Passage Equipment"),
        ("Ad Screens", "Advertising &amp; Information Display"),
        ("Video Surveillance", "CCTV System"),
    ],
    "fr": [
        ("Équipements de Pointage et Contrôle d'Accès", "Équipements de Pointage et Contrôle d'Accès"),  # guard
        ("Appareils de Présence", "Équipements de Pointage et Contrôle d'Accès"),
        ("Pointage", "Équipements de Pointage et Contrôle d'Accès"),
        ("Capteur de Consommation et Anti-Vol de Carburant", "Capteur de Consommation et Anti-Vol de Carburant"),  # guard
        ("Capteur Antivol Carburant", "Capteur de Consommation et Anti-Vol de Carburant"),
        ("Capteur Carburant", "Capteur de Consommation et Anti-Vol de Carburant"),
        ("Terminal de Localisation GPS", "Terminal de Localisation GPS"),  # guard
        ("Traceur GPS Véhicule", "Terminal de Localisation GPS"),
        ("Traceur GPS", "Terminal de Localisation GPS"),
        ("Équipements de Passage Piéton", "Équipements de Passage Piéton"),  # guard
        ("Accès Piéton", "Équipements de Passage Piéton"),
        ("Contrôle d'Accès", "Équipements de Passage Piéton"),
        ("Écrans Publicitaires et d'Information", "Écrans Publicitaires et d'Information"),  # guard
        ("Écran Publicitaire", "Écrans Publicitaires et d'Information"),
        ("Écrans Pub", "Écrans Publicitaires et d'Information"),
        ("Système de Murs Vidéo", "Système de Murs Vidéo"),  # guard
        ("Mur d'Images", "Système de Murs Vidéo"),
        ("Murs Vidéo", "Système de Murs Vidéo"),
        ("Écrans LED Extérieurs", "Écrans LED Extérieurs"),  # guard
        ("Écran LED Extérieur", "Écrans LED Extérieurs"),
        ("Afficheurs LED", "Écrans LED Extérieurs"),
        ("Système de Vidéosurveillance", "Système de Vidéosurveillance"),  # guard
        ("Vidéosurveillance (CCTV)", "Système de Vidéosurveillance"),
        ("Vidéosurveillance", "Système de Vidéosurveillance"),
    ],
}


def get_all_html_files():
    files = []
    for root, dirs, filenames in os.walk('.'):
        if '.git' in root:
            continue
        for fname in filenames:
            if fname.endswith('.html'):
                files.append(os.path.join(root, fname))
    return sorted(files)


def apply_replacements(content, replacements):
    """Apply replacements using placeholder approach to avoid substring issues."""
    changes = []
    new_content = content
    placeholders = {}

    # Phase 1: Replace old texts with unique placeholders
    for i, (old_text, new_text) in enumerate(replacements):
        if old_text == new_text:
            continue
        count = new_content.count(old_text)
        if count > 0:
            placeholder = f"__HW_RENAME_PLACEHOLDER_{i:03d}__"
            placeholders[placeholder] = new_text
            changes.append({
                "old": old_text,
                "new": new_text,
                "count": count,
            })
            new_content = new_content.replace(old_text, placeholder)

    # Phase 2: Replace placeholders with new texts
    for placeholder, new_text in placeholders.items():
        new_content = new_content.replace(placeholder, new_text)

    return new_content, changes


def main():
    all_files = get_all_html_files()
    print(f"Found {len(all_files)} HTML files")

    total_changes = []
    files_modified = 0

    for filepath in all_files:
        if filepath.startswith('./zh/'):
            lang = 'zh'
        elif filepath.startswith('./en/'):
            lang = 'en'
        elif filepath.startswith('./fr/'):
            lang = 'fr'
        elif filepath == './index.html':
            continue
        else:
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = content
        file_changes = []

        if lang in REPLACEMENTS:
            new_content, file_changes = apply_replacements(new_content, REPLACEMENTS[lang])

        if file_changes:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            files_modified += 1
            total_changes.append({
                "file": filepath,
                "changes": file_changes,
            })
            print(f"Modified: {filepath}")
            for c in file_changes:
                print(f"  '{c['old']}' -> '{c['new']}' ({c['count']} occurrences)")

    print(f"\nTotal files modified: {files_modified}")

    with open('rename_report.json', 'w', encoding='utf-8') as f:
        json.dump(total_changes, f, ensure_ascii=False, indent=2)

    # Verification
    print("\n=== Verification: checking for remaining old names ===")
    old_names_by_lang = {
        "zh": ["视频监控", "考勤设备", "车辆偷油传感器", "车辆定位传感器", "人行通道", "广告屏", "拼接屏", "户外LED屏"],
        "en": ["Attendance", "Fuel Sensor", "GPS Tracker", "Access Gates", "Ad Screens", "Video Walls", "LED Displays", "Video Surveillance", "Attendance Devices", "Vehicle Fuel Theft Sensor", "Vehicle GPS Tracker", "Pedestrian Access", "Advertising Screen", "Video Wall"],
        "fr": ["Pointage", "Capteur Carburant", "Traceur GPS", "Contrôle d'Accès", "Écrans Pub", "Murs Vidéo", "Afficheurs LED", "Vidéosurveillance", "Appareils de Présence", "Capteur Antivol Carburant", "Traceur GPS Véhicule", "Accès Piéton", "Écran Publicitaire", "Mur d'Images", "Écran LED Extérieur"],
    }

    remaining = []
    for filepath in all_files:
        if filepath == './index.html':
            continue
        if filepath.startswith('./zh/'):
            lang = 'zh'
        elif filepath.startswith('./en/'):
            lang = 'en'
        elif filepath.startswith('./fr/'):
            lang = 'fr'
        else:
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        for old_name in old_names_by_lang[lang]:
            count = content.count(old_name)
            if count > 0:
                idx = 0
                while True:
                    idx = content.find(old_name, idx)
                    if idx == -1:
                        break
                    start = max(0, idx - 40)
                    end = min(len(content), idx + len(old_name) + 40)
                    context = content[start:end].replace('\n', ' ')
                    remaining.append({
                        "file": filepath,
                        "old_name": old_name,
                        "context": context,
                    })
                    idx += len(old_name)

    # Special check for CCTV (English): count "CCTV" not followed by " System"
    for filepath in all_files:
        if filepath.startswith('./en/'):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            pattern = re.compile(r'CCTV(?! System)')
            matches = list(pattern.finditer(content))
            for m in matches:
                start = max(0, m.start() - 30)
                end = min(len(content), m.end() + 30)
                context = content[start:end].replace('\n', ' ')
                remaining.append({
                    "file": filepath,
                    "old_name": "CCTV",
                    "context": context,
                })

    if remaining:
        print(f"WARNING: Found {len(remaining)} remaining old name occurrences:")
        for r in remaining[:60]:
            print(f"  {r['file']}: '{r['old_name']}' in ...{r['context']}...")
        if len(remaining) > 60:
            print(f"  ... and {len(remaining) - 60} more")
    else:
        print("PASS: No remaining old name occurrences found!")

    with open('remaining_report.json', 'w', encoding='utf-8') as f:
        json.dump(remaining, f, ensure_ascii=False, indent=2)

    return total_changes, remaining


if __name__ == '__main__':
    main()
