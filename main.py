import requests
from playwright.sync_api import sync_playwright

WEBHOOK_URL = "https://discord.com/api/webhooks/1469383829041975380/51UI7h8gILbV51o6AreYyRZTxeH3IjQ97KAGDlxKc7-qOLY3YHik0R-HCdskCoFCKIdm"

CLASSES = {
    "HUNTER":       {"icon": "🏹", "color": 0xABD473},
    "WARRIOR":      {"icon": "⚔️", "color": 0xC79C6E},
    "DEATH KNIGHT": {"icon": "💀", "color": 0xC41F3B},
    "MAGE":         {"icon": "❄️", "color": 0x3FC7EB},
    "DEMON HUNTER": {"icon": "😈", "color": 0xA330C9},
    "WARLOCK":      {"icon": "🔮", "color": 0x8787ED},
    "SHAMAN":       {"icon": "⚡", "color": 0x0070DE},
    "PALADIN":      {"icon": "🔨", "color": 0xF58CBA},
    "DRUID":        {"icon": "🌿", "color": 0xFF7D0A},
    "PRIEST":       {"icon": "✨", "color": 0xFFFFFF},
    "ROGUE":        {"icon": "🗡️", "color": 0xFFF569},
    "MONK":         {"icon": "🤜", "color": 0x00FF96},
    "EVOKER":       {"icon": "🐲", "color": 0x33937F}
}

# Correspondance texte du site → clé dans CLASSES
CLASS_MAP = {
    "death knight":  "DEATH KNIGHT",
    "demon hunter":  "DEMON HUNTER",
    "hunter":        "HUNTER",
    "warrior":       "WARRIOR",
    "mage":          "MAGE",
    "warlock":       "WARLOCK",
    "shaman":        "SHAMAN",
    "paladin":       "PALADIN",
    "druid":         "DRUID",
    "priest":        "PRIEST",
    "rogue":         "ROGUE",
    "monk":          "MONK",
    "evoker":        "EVOKER"
}

def scrape_murlok():
    """Scrape le Top 5 DPS M+ directement depuis murlok.io"""
    top_dps = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("📡 Chargement de murlok.io...")
        page.goto("https://murlok.io/meta/dps/m+", wait_until="networkidle", timeout=30000)

        # Attendre que les rankings soient chargés
        page.wait_for_selector("a[href*='/m+']", timeout=15000)

        # Récupérer les éléments du classement
        items = page.query_selector_all("a[href*='/m+']")

        rank = 1
        for item in items:
            if rank > 5:
                break

            text = item.inner_text().strip()
            lines = [l.strip() for l in text.split("\n") if l.strip()]

            # On cherche une ligne avec un score (nombre 4 chiffres)
            score = None
            name_parts = []
            for line in lines:
                if line.isdigit() and len(line) == 4:
                    score = line
                elif not line.isdigit():
                    name_parts.append(line)

            if not score:
                continue

            # Le nom complet ex: "Unholy Death Knight"
            full_name = " ".join(name_parts).replace(str(rank), "").strip()
            full_name_lower = full_name.lower()

            # Trouver la classe
            found_class = None
            found_spec = None
            for class_key in sorted(CLASS_MAP.keys(), key=len, reverse=True):
                if class_key in full_name_lower:
                    found_class = CLASS_MAP[class_key]
                    found_spec = full_name_lower.replace(class_key, "").strip().upper()
                    break

            if found_class and found_spec:
                top_dps.append({
                    "rank": str(rank),
                    "spec": found_spec,
                    "class": found_class,
                    "score": score
                })
                rank += 1

        browser.close()

    return top_dps


def send_meta():
    print("🔍 Scraping des données Murlok.io...")
    top_dps = scrape_murlok()

    if not top_dps:
        print("❌ Aucune donnée récupérée !")
        return

    print(f"✅ {len(top_dps)} specs récupérées")

    first_class = top_dps[0]["class"]
    embed_color = CLASSES[first_class]["color"]

    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]

    embed = {
        "title": "🏆 TOP 5 DPS M+ - MURLOK.IO",
        "color": embed_color,
        "description": "Classements **en temps réel** pour WoW: Midnight\n🔗 [Voir sur Murlok.io](https://murlok.io/meta/dps/m+)",
        "fields": [],
        "footer": {"text": "Données live • Murlok se met à jour toutes les 8h • Midnight 12.0"}
    }

    for i, item in enumerate(top_dps):
        c_info = CLASSES[item["class"]]
        embed["fields"].append({
            "name": f"{medals[i]} {c_info['icon']} {item['spec']} {item['class']}",
            "value": f"📈 Score : `{item['score']}`",
            "inline": False
        })

    response = requests.post(WEBHOOK_URL, json={"embeds": [embed]})

    if response.status_code == 204:
        print("✅ Message Discord envoyé avec succès !")
    else:
        print(f"❌ Erreur Discord : {response.status_code} - {response.text}")


if __name__ == "__main__":
    send_meta()
