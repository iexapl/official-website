#!/usr/bin/env python3
"""
Verify that old hardware product names have been replaced.
Excludes cases where the old name is a substring of ANY new name.
"""
import os

# Map: language -> list of (old_name, new_name)
NAME_PAIRS = {
    "zh": [
        ("视频监控", "视频监控系统"),
        ("考勤设备", "考勤与门禁设备"),
        ("车辆偷油传感器", "车辆油耗与防偷油传感器"),
        ("车辆定位传感器", "车辆定位终端"),
        ("人行通道", "人行通道设备"),
        ("广告屏", "广告与信息显示屏"),
        ("拼接屏", "拼接屏系统"),
        ("户外LED屏", "户外 LED 大屏"),
    ],
    "en": [
        ("CCTV", "CCTV System"),
        ("Attendance", "Attendance &amp; Access Control Equipment"),
        ("Fuel Sensor", "Vehicle Fuel Consumption &amp; Anti-Theft Sensor"),
        ("GPS Tracker", "Vehicle GPS Tracking Terminal"),
        ("Access Gates", "Pedestrian Passage Equipment"),
        ("Ad Screens", "Advertising &amp; Information Display"),
        ("Video Walls", "Video Wall System"),
        ("LED Displays", "Outdoor LED Display"),
        ("Video Surveillance", "CCTV System"),
        ("Attendance Devices", "Attendance &amp; Access Control Equipment"),
        ("Vehicle Fuel Theft Sensor", "Vehicle Fuel Consumption &amp; Anti-Theft Sensor"),
        ("Vehicle GPS Tracker", "Vehicle GPS Tracking Terminal"),
        ("Pedestrian Access", "Pedestrian Passage Equipment"),
        ("Advertising Screen", "Advertising &amp; Information Display"),
        ("Video Wall", "Video Wall System"),
    ],
    "fr": [
        ("Vidéosurveillance (CCTV)", "Système de Vidéosurveillance"),
        ("Vidéosurveillance", "Système de Vidéosurveillance"),
        ("Pointage", "Équipements de Pointage et Contrôle d'Accès"),
        ("Capteur Carburant", "Capteur de Consommation et Anti-Vol de Carburant"),
        ("Traceur GPS", "Terminal de Localisation GPS"),
        ("Contrôle d'Accès", "Équipements de Passage Piéton"),
        ("Écrans Pub", "Écrans Publicitaires et d'Information"),
        ("Murs Vidéo", "Système de Murs Vidéo"),
        ("Afficheurs LED", "Écrans LED Extérieurs"),
        ("Appareils de Présence", "Équipements de Pointage et Contrôle d'Accès"),
        ("Capteur Antivol Carburant", "Capteur de Consommation et Anti-Vol de Carburant"),
        ("Traceur GPS Véhicule", "Terminal de Localisation GPS"),
        ("Accès Piéton", "Équipements de Passage Piéton"),
        ("Écran Publicitaire", "Écrans Publicitaires et d'Information"),
        ("Mur d'Images", "Système de Murs Vidéo"),
        ("Écran LED Extérieur", "Écrans LED Extérieurs"),
    ],
}


def get_all_new_names(lang):
    return [new_name for _, new_name in NAME_PAIRS.get(lang, [])]


def is_inside_any_new_name(content, old_start, old_end, all_new_names):
    for new_name in all_new_names:
        idx = 0
        while True:
            idx = content.find(new_name, idx)
            if idx == -1:
                break
            new_start = idx
            new_end = idx + len(new_name)
            if old_start < new_end and old_end > new_start:
                return True
            idx += 1
    return False


def find_actual_occurrences(content, old_name, all_new_names):
    results = []
    idx = 0
    while True:
        idx = content.find(old_name, idx)
        if idx == -1:
            break
        old_start = idx
        old_end = idx + len(old_name)
        if not is_inside_any_new_name(content, old_start, old_end, all_new_names):
            start = max(0, old_start - 40)
            end = min(len(content), old_end + 40)
            context = content[start:end].replace('\n', ' ')
            results.append((old_start, context))
        idx += 1
    return results


def main():
    all_files = []
    for root, dirs, filenames in os.walk('.'):
        if '.git' in root:
            continue
        for fname in filenames:
            if fname.endswith('.html'):
                all_files.append(os.path.join(root, fname))

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

        all_new_names = get_all_new_names(lang)
        checked_old = set()

        for old_name, _ in NAME_PAIRS.get(lang, []):
            if old_name in checked_old:
                continue
            checked_old.add(old_name)
            occurrences = find_actual_occurrences(content, old_name, all_new_names)
            for idx, context in occurrences:
                remaining.append({
                    "file": filepath,
                    "old_name": old_name,
                    "context": context,
                })

    if remaining:
        print(f"WARNING: Found {len(remaining)} remaining old name occurrences:")
        for r in remaining[:100]:
            print(f"  {r['file']}: '{r['old_name']}' in ...{r['context']}...")
        if len(remaining) > 100:
            print(f"  ... and {len(remaining) - 100} more")
    else:
        print("PASS: No remaining old name occurrences found!")

    return remaining


if __name__ == '__main__':
    main()
