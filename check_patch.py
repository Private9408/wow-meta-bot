import requests
from bs4 import BeautifulSoup
import os

# Configuration
URL_NEWS = "https://www.leagueoflegends.com/fr-fr/news/game-updates/"
# Ton URL de Webhook directe
WEBHOOK_URL = "https://discord.com/api/webhooks/1469458508977279079/YL4KeSwJKfv9OtnkTk9traXj8itFPxpBNb8ZO-4TMkfneO1HjYBL3_rZ9tHZnOzk-XFO"

def get_latest_patch():
    # Header pour simuler un navigateur et éviter d'être bloqué par Riot
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        response = requests.get(URL_NEWS, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # On cherche le premier lien qui contient "Notes de patch"
        for link in soup.find_all('a'):
            title_element = link.find('h2')
            if title_element and "Notes de patch" in title_element.text:
                title = title_element.text.strip()
                href = link.get('href', '')
                # Reconstruit l'URL si elle est relative
                url = href if href.startswith('http') else "https://www.leagueoflegends.com" + href
                
                # Cherche l'image du patch
                img_tag = link.find('img')
                image = img_tag['src'] if img_tag and img_tag.has_attr('src') else ""
                
                return title, url, image
    except Exception as e:
        print(f"Erreur lors du scan : {e}")
    return None, None, None

title, url, image = get_latest_patch()

if title and url:
    cache_file = "last_patch.txt"
    last_sent = ""
    
    # Lecture du dernier patch envoyé pour éviter les doublons
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            last_sent = f.read().strip()

    # Si l'URL est différente de la dernière fois, on envoie le message
    if url != last_sent:
        payload = {
            "content": "📢 **Nouveau patch disponible sur League of Legends !**",
            "embeds": [{
                "title": title,
                "url": url,
                "color": 16743424, # Couleur Orange LoL
                "image": {"url": image} if image else None,
                "description": f"Les notes du dernier patch sont en ligne.\n[Consulter les modifications ici]({url})"
            }]
        }
        
        r = requests.post(WEBHOOK_URL, json=payload)
        
        if r.status_code == 204 or r.status_code == 200:
            # On enregistre l'URL dans le fichier de cache
            with open(cache_file, "w") as f:
                f.write(url)
            print(f"Succès : Patch {title} envoyé sur Discord.")
        else:
            print(f"Erreur Discord : {r.status_code}")
    else:
        print("Le dernier patch a déjà été posté.")
else:
    print("Aucun patch détecté sur la page.")
