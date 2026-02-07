import requests
import datetime

# ==============================================================================
# 🎛️ ZONE DE CONFIGURATION (MODIFIE ICI À CHAQUE PATCH)
# ==============================================================================

# 1. Numéro du Patch
VERSION = "26.3"

# 2. Lien officiel (Généré auto, mais tu peux le changer si besoin)
URL_PATCH = f"https://www.leagueoflegends.com/fr-fr/news/game-updates/patch-{VERSION.replace('.', '-')}-notes/"

# 3. Image de la bannière (Celle que tu vois en haut de la page du patch)
IMAGE_BANNIERE = "https://images.contentstack.io/v3/assets/blt731b4148e173d051/blt7e727e57c6179471/65b056801289133c99f9c733/013124_LoL_Patch_26_3_Notes_Banner.jpg"

# 4. Résumé des changements (Utilise les émojis pour le style)
# Astuce : Mets en GRAS (**nom**) les champions importants
BUFFS_LISTE = (
    "🚀 **Zeri** (Dégâts Q augmentés)\n"
    "🛡️ **Braum** (Coût en mana réduit)\n"
    "🌲 **Ivern** (Vitesse de clear)\n"
    "👻 **Viego** (Portée du R)"
)

NERFS_LISTE = (
    "🔥 **Brand** (Dégâts passif réduits)\n"
    "🗡️ **Aatrox** (Soin nerfé)\n"
    "🔫 **Caitlyn** (Ratio AD Headshot)"
)

AJUSTEMENTS_LISTE = (
    "⚖️ **Objets Supports** : Quêtes plus longues\n"
    "🐉 **Dragon Chemtech** : Soul buffée\n"
    "🐛 **Larves du Néant** : Spawn retardé de 30s"
)

SKINS_LISTE = "✨ **Porcelaine** : Kindred, Darius, Graves, Morgana\n🌙 **Lune de Sang** : Zyra, Yorick"

# 5. Phrase d'accroche
PHRASE_ACCROCHE = "Invocateurs, la méta change ! Voici tout ce qu'il faut savoir avant de lancer votre prochaine Ranked."

# ==============================================================================
# 🤖 CODE DU BOT (NE TOUCHE PAS EN DESSOUS)
# ==============================================================================

WEBHOOK_URL = "https://discord.com/api/webhooks/1469458508977279079/YL4KeSwJKfv9OtnkTk9traXj8itFPxpBNb8ZO-4TMkfneO1HjYBL3_rZ9tHZnOzk-XFO"

def send_ultimate_patch():
    # Création de l'embed
    embed = {
        "title": f"📜 NOTES DE PATCH {VERSION} | LEAGUE OF LEGENDS",
        "description": f"*{PHRASE_ACCROCHE}*\n\n[**👉 CLIQUER ICI POUR LIRE LE PATCH COMPLET**]({URL_PATCH})",
        "url": URL_PATCH,
        "color": 0xC8AA6E, # Couleur "Hextech Gold" officielle
        "fields": [
            {
                "name": "📈 UP (BUFFS)",
                "value": BUFFS_LISTE,
                "inline": True
            },
            {
                "name": "📉 DOWN (NERFS)",
                "value": NERFS_LISTE,
                "inline": True
            },
            {
                "name": "\u200b", # Séparateur invisible
                "value": "\u200b",
                "inline": False 
            },
            {
                "name": "🛠️ SYSTÈME & JUNGLE",
                "value": AJUSTEMENTS_LISTE,
                "inline": True
            },
            {
                "name": "🎨 NOUVEAUX SKINS",
                "value": SKINS_LISTE,
                "inline": True
            }
        ],
        "image": {
            "url": IMAGE_BANNIERE
        },
        "thumbnail": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/League_of_Legends_2019_vector.svg/1200px-League_of_Legends_2019_vector.svg.png"
        },
        "footer": {
            "text": f"Mise à jour officielle • Patch {VERSION} • Riot Games",
            "icon_url": "https://brand.riotgames.com/static/a91000434ed683358004b85c95d43ce0/8a26a/riot-logo.png"
        },
        "timestamp": datetime.datetime.now().isoformat()
    }

    # Structure du message
    payload = {
        "content": f"# 📣 MISE À JOUR {VERSION} DISPONIBLE !\n@everyone Préparez vos champions !",
        "embeds": [embed]
    }

    # Envoi
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        response.raise_for_status()
        print(f"✅ Patch {VERSION} envoyé avec succès (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi : {e}")

if __name__ == "__main__":
    send_ultimate_patch()
