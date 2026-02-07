import requests
from bs4 import BeautifulSoup
import os

# CONFIGURATION
WEBHOOK_URL = "https://discord.com/api/webhooks/1469458508977279079/YL4KeSwJKfv9OtnkTk9traXj8itFPxpBNb8ZO-4TMkfneO1HjYBL3_rZ9tHZnOzk-XFO"
# On utilise la page globale des news, plus souvent mise à jour
URL_NEWS = "https://www.leagueoflegends.com/fr-fr/news/game-updates/"

def get_latest_patch():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        response = requests.get(URL_NEWS, headers=headers)
        if response.status_code != 200:
            print(f"Erreur de connexion au site : {response.status_code}")
            return None, None, None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # On cherche tous les articles (généralement dans des balises 'a')
        articles = soup.find_all('a')
        
        for art in articles:
            # On cherche "Notes de patch" dans le texte du lien ou des titres à l'intérieur
            text_content = art.get_text().lower()
            if "notes de patch" in text_content:
                title = art.find('h2').text.strip() if art.find('h2') else "Nouvelles Notes de Patch"
                href = art['href']
                url = href if href.startswith('http') else "https://www.leagueoflegends.com" + href
                
                # Récupération de l'image
                img = art.find('img')
                image = img['src'] if img and img.has_attr('src') else ""
                
                # Si on trouve un match, on s'arrête au premier (le plus récent)
                return title, url, image
                
    except Exception as e:
        print(f"Erreur lors du scan : {e}")
    return None, None, None

title, url, image = get_latest_patch()

if title and url:
    cache_file = "last_patch.txt"
    last_sent = ""
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            last_sent = f.read().strip()

    if url != last_sent:
        payload = {
            "content": "📢 **Mise à jour LoL détectée !**",
            "embeds": [{
                "title": title,
                "url": url,
                "color": 16743424,
                "image": {"url": image} if image else None,
                "description": f"Les dernières notes de patch sont disponibles ici : \n{url}"
            }]
        }
        r = requests.post(WEBHOOK_URL, json=payload)
        if r.status_code in [200, 204]:
            with open(cache_file, "w") as f:
                f.write(url)
            print("Envoyé avec succès !")
    else:
        print("Déjà posté.")
else:
    print("Aucun article 'Notes de patch' trouvé sur la page.")
