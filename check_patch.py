import requests
from bs4 import BeautifulSoup
import os

# Configuration
URL_NEWS = "https://www.leagueoflegends.com/fr-fr/news/game-updates/"
WEBHOOK_URL = os.getenv("https://discord.com/api/webhooks/1469458508977279079/YL4KeSwJKfv9OtnkTk9traXj8itFPxpBNb8ZO-4TMkfneO1HjYBL3_rZ9tHZnOzk-XFO")

def get_latest_patch():
    response = requests.get(URL_NEWS)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # On cherche le premier lien qui contient "Notes de patch"
    for link in soup.find_all('a'):
        title_element = link.find('h2')
        if title_element and "Notes de patch" in title_element.text:
            title = title_element.text
            url = "https://www.leagueoflegends.com" + link['href']
            image = link.find('img')['src'] if link.find('img') else ""
            return title, url, image
    return None, None, None

title, url, image = get_latest_patch()

if title:
    # On vérifie si ce patch a déjà été posté (via un fichier local de cache)
    cache_file = "last_patch.txt"
    last_sent = ""
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            last_sent = f.read().strip()

    if url != last_sent:
        # Envoi à Discord
        payload = {
            "embeds": [{
                "title": title,
                "url": url,
                "color": 16743424, # Orange League
                "image": {"url": image},
                "description": f"Le nouveau patch est disponible !\n[Lire les notes ici]({url})"
            }]
        }
        requests.post(WEBHOOK_URL, json=payload)
        
        # Mise à jour du cache
        with open(cache_file, "w") as f:
            f.write(url)
