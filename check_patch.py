import requests
from bs4 import BeautifulSoup
import os

# Configuration
URL_NEWS = "https://www.leagueoflegends.com/fr-fr/news/game-updates/"
# Cette ligne récupère l'URL que tu as mise dans "Secrets" sur GitHub
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

def get_latest_patch():
    # Header pour simuler un navigateur et éviter d'être bloqué
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        response = requests.get(URL_NEWS, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # On cherche le premier lien qui parle de "Notes de patch"
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
    
    # Lecture du dernier patch envoyé
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            last_sent = f.read().strip()

    # Si c'est un nouveau patch, on l'envoie
    if url != last_sent:
        payload = {
            "content": "📢 **Nouveau patch disponible sur League of Legends !**",
            "embeds": [{
                "title": title,
                "url": url,
                "color": 16743424,
                "image": {"url": image} if image else None,
                "description": f"Les notes du dernier patch sont en ligne.\n[Consulter les modifications ici]({url})"
            }]
        }
        
        r = requests.post(WEBHOOK_URL, json=payload)
        
        if r.status_code == 204 or r.status_code == 200:
            # On enregistre l'URL pour ne pas renvoyer le même patch
            with open(cache_file, "w") as f:
                f.write(url)
            print(f"Patch envoyé : {title}")
        else:
            print(f"Erreur Discord : {r.status_code}")
    else:
        print("Pas de nouveau patch détecté.")
else:
    print("Impossible de trouver le patch sur la page.")
