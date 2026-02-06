import requests
from bs4 import BeautifulSoup
import os

# CONFIGURATION
URL_NEWS = "https://www.leagueoflegends.com/fr-fr/news/game-updates/"
# Utilise bien ton URL de webhook ici
WEBHOOK_URL = "https://discord.com/api/webhooks/1469458508977279079/YL4KeSwJKfv9OtnkTk9traXj8itFPxpBNb8ZO-4TMkfneO1HjYBL3_rZ9tHZnOzk-XFO"

def get_latest_patch():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(URL_NEWS, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            title_el = link.find('h2')
            if title_el and "Notes de patch" in title_el.text:
                title = title_el.text.strip()
                href = link.get('href', '')
                url = href if href.startswith('http') else "https://www.leagueoflegends.com" + href
                img = link.find('img')
                image = img['src'] if img and img.has_attr('src') else ""
                return title, url, image
    except Exception as e:
        print(f"Erreur de scan : {e}")
    return None, None, None

title, url, image = get_latest_patch()

if title:
    cache_file = "last_patch.txt"
    last_sent = ""
    
    # SECURITÉ : On vérifie si le fichier existe avant de le lire
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            last_sent = f.read().strip()
    else:
        # Si le fichier n'existe pas, on le crée vide
        open(cache_file, 'a').close()

    if url != last_sent:
        payload = {
            "content": "📢 **Nouveau patch LoL détecté !**",
            "embeds": [{
                "title": title,
                "url": url,
                "color": 16743424,
                "image": {"url": image} if image else None,
                "description": f"Les notes du patch sont disponibles ici.\n[Lien vers l'article]({url})"
            }]
        }
        r = requests.post(WEBHOOK_URL, json=payload)
        
        if r.status_code in [200, 204]:
            with open(cache_file, "w") as f:
                f.write(url)
            print(f"Succès : Patch {title} envoyé.")
        else:
            print(f"Erreur Discord : {r.status_code}")
    else:
        print("Déjà à jour.")
else:
    print("Patch introuvable sur la page.")
