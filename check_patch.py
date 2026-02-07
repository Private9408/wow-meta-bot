import requests
from bs4 import BeautifulSoup
import os

# CONFIGURATION
WEBHOOK_URL = "https://discord.com/api/webhooks/1469458508977279079/YL4KeSwJKfv9OtnkTk9traXj8itFPxpBNb8ZO-4TMkfneO1HjYBL3_rZ9tHZnOzk-XFO"
URL_NEWS = "https://www.leagueoflegends.com/fr-fr/news/tags/patch-notes/"

def get_latest_patch():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        print(f"Analyse de la page : {URL_NEWS}")
        response = requests.get(URL_NEWS, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # On cherche tous les liens
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            # On cherche un lien qui contient "notes-de-patch" ou "patch-notes"
            if "notes-de-patch" in href or "patch-notes" in href:
                url = href if href.startswith('http') else "https://www.leagueoflegends.com" + href
                
                # On essaie de trouver le titre
                title_el = link.find('h2') or link.find('h3') or link.find('span')
                title = title_el.text.strip() if title_el else "Nouveau Patch League of Legends"
                
                # On cherche l'image
                img = link.find('img')
                image = img['src'] if img else ""
                
                print(f"Trouvé : {title}")
                return title, url, image
    except Exception as e:
        print(f"Erreur lors de l'extraction : {e}")
    return None, None, None

title, url, image = get_latest_patch()

if title and url:
    cache_file = "last_patch.txt"
    last_sent = ""
    
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            last_sent = f.read().strip()

    # On vérifie si c'est un nouveau lien
    if url != last_sent:
        payload = {
            "content": "🚀 **Nouveau patch League of Legends détecté !**",
            "embeds": [{
                "title": title,
                "url": url,
                "color": 16743424,
                "image": {"url": image} if image else None,
                "description": f"Les notes du patch sont disponibles ici :\n{url}"
            }]
        }
        r = requests.post(WEBHOOK_URL, json=payload)
        if r.status_code in [200, 204]:
            with open(cache_file, "w") as f:
                f.write(url)
            print("Message du patch envoyé avec succès !")
    else:
        print("Le patch a déjà été envoyé (URL identique au cache).")
else:
    print("Impossible de trouver un patch sur la page.")
