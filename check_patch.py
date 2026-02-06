import requests
from bs4 import BeautifulSoup
import os

# CONFIGURATION
URL_NEWS = "https://www.leagueoflegends.com/fr-fr/news/tags/patch-notes/"
WEBHOOK_URL = "https://discord.com/api/webhooks/1469458508977279079/YL4KeSwJKfv9OtnkTk9traXj8itFPxpBNb8ZO-4TMkfneO1HjYBL3_rZ9tHZnOzk-XFO"

def get_latest_patch():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        response = requests.get(URL_NEWS, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # On cherche le premier article de la liste
        article = soup.find('a', href=True)
        if article:
            # Récupération du titre (souvent dans un h2 ou h3)
            title_el = article.find('h2') or article.find('h3')
            title = title_el.text.strip() if title_el else "Notes de patch LoL"
            
            # Récupération de l'URL
            href = article['href']
            url = href if href.startswith('http') else "https://www.leagueoflegends.com" + href
            
            # Récupération de l'image
            img_tag = article.find('img')
            image = img_tag['src'] if img_tag else ""
            
            return title, url, image
    except Exception as e:
        print(f"Erreur : {e}")
    return None, None, None

title, url, image = get_latest_patch()

if title and "patch" in title.lower():
    cache_file = "last_patch.txt"
    last_sent = ""
    
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            last_sent = f.read().strip()

    # FORCE L'ENVOI SI TU VIENS DE MODIFIER LE SCRIPT
    if url != last_sent:
        payload = {
            "content": "🚀 **Mise à jour League of Legends détectée !**",
            "embeds": [{
                "title": title,
                "url": url,
                "color": 16743424,
                "image": {"url": image} if image else None,
                "description": f"Le nouveau patch est là. Découvre tous les changements ici :\n{url}"
            }]
        }
        r = requests.post(WEBHOOK_URL, json=payload)
        
        if r.status_code in [200, 204]:
            with open(cache_file, "w") as f:
                f.write(url)
            print(f"Posté avec succès : {title}")
    else:
        print("Déjà à jour.")
