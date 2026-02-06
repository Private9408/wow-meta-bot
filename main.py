import requests

# Ton URL de Webhook Discord
WEBHOOK_URL = "https://discord.com/api/webhooks/1469383829041975380/51UI7h8gILbV51o6AreYyRZTxeH3IjQ97KAGDlxKc7-qOLY3YHik0R-HCdskCoFCKIdm"

def send_meta():
    # Dictionnaire de toutes les classes avec icônes et couleurs
    CLASSES = {
        "HUNTER": {"icon": "🏹", "color": 0xABD473},
        "WARRIOR": {"icon": "⚔️", "color": 0xC79C6E},
        "DEATH KNIGHT": {"icon": "💀", "color": 0xC41F3B},
        "MAGE": {"icon": "❄️", "color": 0x3FC7EB},
        "DEMON HUNTER": {"icon": "😈", "color": 0xA330C9},
        "WARLOCK": {"icon": "🔮", "color": 0x8787ED},
        "SHAMAN": {"icon": "⚡", "color": 0x0070DE},
        "PALADIN": {"icon": "🔨", "color": 0xF58CBA},
        "DRUID": {"icon": "🌿", "color": 0xFF7D0A},
        "PRIEST": {"icon": "✨", "color": 0xFFFFFF},
        "ROGUE": {"icon": "🗡️", "color": 0xFFF569},
        "MONK": {"icon": "🤜", "color": 0x00FF96},
        "EVOKER": {"icon": "🐲", "color": 0x33937F}
    }

    # Liste du Top DPS (Modifie les noms et scores ici quand ça change sur Murlok)
    top_dps = [
        {"rank": "1", "spec": "SURVIVAL", "class": "HUNTER", "score": "4127"},
        {"rank": "2", "spec": "FURY", "class": "WARRIOR", "score": "4124"},
        {"rank": "3", "spec": "UNHOLY", "class": "DEATH KNIGHT", "score": "4118"},
        {"rank": "4", "spec": "FROST", "class": "MAGE", "score": "4111"},
        {"rank": "5", "spec": "DEVOURER", "class": "DEMON HUNTER", "score": "4092"}
    ]

    # Récupération de la couleur de la classe n°1 pour le bord du message
    first_class = top_dps[0]["class"]
    embed_color = CLASSES[first_class]["color"]

    embed = {
        "title": "🏆 TOP 5 DPS M+ - MURLOK.IO",
        "color": embed_color,
        "description": "Classements actuels pour World of Warcraft: Midnight",
        "fields": [],
        "footer": {"text": "Actualisé via GitHub Actions • Midnight 12.0"}
    }

    for item in top_dps:
        c_info = CLASSES[item["class"]]
        embed["fields"].append({
            "name": f"{item['rank']}. {c_info['icon']} {item['spec']} {item['class']}",
            "value": f"📈 Score : `{item['score']}`",
            "inline": False
        })

    # Envoi au Discord
    response = requests.post(WEBHOOK_URL, json={"embeds": [embed]})
    
    if response.status_code == 204:
        print("Message envoyé avec succès !")
    else:
        print(f"Erreur : {response.status_code}")

if __name__ == "__main__":
    send_meta()
