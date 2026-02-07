import requests

# --- CONFIGURATION MANUELLE DU PATCH ---
# Change ces informations à chaque nouveau patch
VERSION = "26.3"
PATCH_URL = f"https://www.leagueoflegends.com/fr-fr/news/game-updates/patch-{VERSION.replace('.', '-')}-notes/"

# Résumé rapide des changements (À modifier à chaque patch)
BUFFS = "Aatrox, Cho'Gath, Corki, Lux"
NERFS = "Ezreal, Karma, Maokai"
SKINS = "Porcelaine (Kindred, Graves, Darius)"
NOTE_CLE = "Ajustements majeurs sur les objets de support et équilibrage de l'ARAM."

# URL de l'image de garde (Bannière du patch)
PATCH_IMAGE = "https://images.contentstack.io/v3/assets/blt731b4148e173d051/blt7e727e57c6179471/65b056801289133c99f9c733/013124_LoL_Patch_26_3_Notes_Banner.jpg"

# Ton URL Webhook LoL
WEBHOOK_URL = "https://discord.com/api/webhooks/1469458508977279079/YL4KeSwJKfv9OtnkTk9traXj8itFPxpBNb8ZO-4TMkfneO1HjYBL3_rZ9tHZnOzk-XFO"

def send_detailed_patch():
    embed = {
        "title": f"🛠️ NOTES DE PATCH {VERSION}",
        "url": PATCH_URL,
        "color": 16743424, # Orange League of Legends
        "description": f"La mise à jour **{VERSION}** est arrivée ! Voici un résumé des changements importants sur la Faille.",
        "fields": [
            {
                "name": "📈 Buffs (Champions & Items)",
                "value": BUFFS,
                "inline": True
            },
            {
                "name": "📉 Nerfs (Champions & Items)",
                "value": NERFS,
                "inline": True
            },
            {
                "name": "🎨 Nouveaux Skins",
                "value": SKINS,
                "inline": False
            },
            {
                "name": "📝 Note importante",
                "value": NOTE_CLE,
                "inline": False
            }
        ],
        "image": {"url": PATCH_IMAGE},
        "footer": {
            "text": "Bot League Update • Cliquez sur le titre pour les détails complets",
            "icon_url": "https://p3.stickers.cloud/packs/3673e48c-12f5-460d-9993-41c60f27c385/webp/7243b95a-9390-4841-8f5b-5544d6731998.webp"
        }
    }

    payload = {
        "content": "🔔 **Une nouvelle mise à jour est disponible !**",
        "embeds": [embed]
    }

    response = requests.post(WEBHOOK_URL, json=payload)
    
    if response.status_code in [200, 204]:
        print(f"Patch {VERSION} envoyé avec succès !")
    else:
        print(f"Erreur : {response.status_code} - {response.text}")

if __name__ == "__main__":
    send_detailed_patch()
