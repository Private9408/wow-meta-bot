import requests

# REMPLACE ICI PAR TON TROISIÈME WEBHOOK POUR LE TANK
WEBHOOK_URL_TANK = "https://discord.com/api/webhooks/1469393187918577837/E0F3yfHs-nHfhCCdulOdUjK-jOPT-5vZxi8u3tlupH_ZT5jiIQwgut2nGolgmN70PS4g"

def send_tank_meta():
    # Dictionnaire de TOUTES les classes Tank (Midnight)
    CLASSES = {
        "DEATH KNIGHT": {"icon": "💀", "color": 0xC41F3B}, # Sang
        "PALADIN": {"icon": "🔨", "color": 0xF58CBA},      # Protection
        "WARRIOR": {"icon": "🛡️", "color": 0xC79C6E},      # Protection
        "DRUID": {"icon": "🐻", "color": 0xFF7D0A},       # Gardien
        "MONK": {"icon": "🍺", "color": 0x00FF96},        # Maître brasseur
        "DEMON HUNTER": {"icon": "🔥", "color": 0xA330C9}  # Vengeance
    }

    # Données actuelles (Murlok.io)
    top_tank = [
        {"rank": "1", "spec": "BLOOD", "class": "DEATH KNIGHT", "score": "4250"},
        {"rank": "2", "spec": "PROTECTION", "class": "PALADIN", "score": "4190"},
        {"rank": "3", "spec": "VENGEANCE", "class": "DEMON HUNTER", "score": "4165"},
        {"rank": "4", "spec": "GUARDIAN", "class": "DRUID", "score": "4120"},
        {"rank": "5", "spec": "PROTECTION", "class": "WARRIOR", "score": "4090"}
    ]

    # Couleur dynamique basée sur le n°1
    first_class_color = CLASSES[top_tank[0]["class"]]["color"]

    embed = {
        "title": "🛡️ TOP 5 TANKS M+ - MURLOK.IO",
        "color": first_class_color,
        "description": "Les remparts les plus solides (Top 50 mondial)",
        "fields": [],
        "footer": {"text": "Mis à jour via GitHub Actions • Midnight"}
    }

    for item in top_tank:
        c_info = CLASSES.get(item["class"], {"icon": "🛡️", "color": 0x2f3136})
        
        embed["fields"].append({
            "name": f"{item['rank']}. {c_info['icon']} {item['spec']} {item['class']}",
            "value": f"🛡️ Score : `{item['score']}`",
            "inline": False
        })

    requests.post(WEBHOOK_URL_TANK, json={"embeds": [embed]})

if __name__ == "__main__":
    send_tank_meta()
