import requests
from bs4 import BeautifulSoup
import os

# CONFIGURATION
# Ton URL Webhook LoL
WEBHOOK_URL = "https://discord.com/api/webhooks/1469458508977279079/YL4KeSwJKfv9OtnkTk9traXj8itFPxpBNb8ZO-4TMkfneO1HjYBL3_rZ9tHZnOzk-XFO"
# Lien vers la catégorie League of Legends (plus stable)
URL_NEWS = "https://www.leagueoflegends.com/fr-fr/news/game-updates/"

def get_latest_patch():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        response = requests.get(URL_NEWS, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # On cherche le premier lien qui contient "Notes de patch" dans le texte
        for link in soup.find_all('a'):
            title_el = link.find('h2') or link.find('h3')
            if title_el and "Notes de patch" in title_el.text:
                title = title_el.text.strip()
                href = link.get('href', '')
                url = href if href.startswith('http') else "https://www.leagueoflegends.com" + href
                
                # Cherche l'image
                img_tag = link.find('img')
                image = img_tag['src'] if img_tag else ""
                
                return title, url, image
    except Exception as e:
        print(f"Erreur : {e}")
    return None, None, None

title, url, image = get_latest_patch()

if title and url:
    cache_file = "last_patch.txt"
    last_sent = ""
    
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            last_sent = f.read().strip()

    # Si c'est un nouveau patch, on envoie
    if url != last_sent:
        payload = {
            "content": "🚀 **Nouveau patch League of Legends !**",
            "embeds": [{
                "title": title,
                "url": url,
                "color": 16743424,
                "image": {"url": image} if image else None,
                "description": f"Découvre les changements ici : {url}"
            }]
        }
        r = requests.post(WEBHOOK_URL, json=payload)
        
        if r.status_code in [200, 204]:
            with open(cache_file, "w") as f:
                f.write(url)
            print("Envoyé !")
    else:
        print("Déjà à jour.")
else:
    print("Patch introuvable sur cette page.")
