import requests

# Ton URL de Webhook Discord
WEBHOOK_URL = "https://discord.com/api/webhooks/1469392325775069266/sIVDwFyieKtZcGGSS7asyCHv5pIzcsur9dy_i5-GfanQkFtVSHcYHlmo_28_m5G59voC"

def send_heal_meta():
    # Dictionnaire de TOUTES les classes Heal (au cas où le top change)
    CLASSES = {
        "SHAMAN": {"icon": "🌊", "color": 0x0070DE},   # Restauration
        "EVOKER": {"icon": "🐲", "color": 0x33937F},   # Préservation
        "PRIEST": {"icon": "✨", "color": 0xFFFFFF},   # Discipline / Sacré
        "DRUID": {"icon": "🌿", "color": 0xFF7D0A},    # Restauration
        "MONK": {"icon": "🍃", "color": 0x00FF96},     # Tisse-brume
        "PALADIN": {"icon": "🔨", "color": 0xF58CBA}   # Sacré
    }

    # Top 5 Heal actuel (Modifie ici selon Murlok.io)
    top_heal = [
        {"rank": "1", "spec": "RESTORATION", "class": "SHAMAN", "score": "4205"},
        {"rank": "2", "spec": "PRESERVATION", "class": "EVOKER", "score": "4188"},
        {"rank": "3", "spec": "DISCIPLINE", "class": "PRIEST", "score": "4150"},
        {"rank": "4", "spec": "RESTORATION", "class": "DRUID", "score": "4110"},
        {"rank": "5", "spec": "MISTWEAVER", "class": "MONK", "score": "4095"}
    ]

    # Couleur dynamique basée sur le n°1
    first_class_color = CLASSES[top_heal[0]["class"]]["color"]

    embed = {
        "title": "🌿 TOP 5 HEALERS M+ - MURLOK.IO",
        "color": first_class_color,
        "description": "Classement des soigneurs (Top 50 mondial)",
        "fields": [],
        "footer": {"text": "Mis à jour via GitHub Actions • Midnight"}
    }

    for item in top_heal:
        # On récupère les infos de la classe (icône/couleur)
        c_info = CLASSES.get(item["class"], {"icon": "🏥", "color": 0x2f3136})
        
        embed["fields"].append({
            "name": f"{item['rank']}. {c_info['icon']} {item['spec']} {item['class']}",
            "value": f"💚 Score : `{item['score']}`",
            "inline": False
        })

    requests.post(WEBHOOK_URL, json={"embeds": [embed]})

if __name__ == "__main__":
    send_heal_meta()
