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
        # On cible le premier article de la liste de Riot
        article = soup.find('a', href=True)
        if article:
            title_el = article.find('h2') or article.find('h3')
            title = title_el.text.strip() if title_el else "Notes de patch"
            href = article['href']
            url = href if href.startswith('http') else "https://www.leagueoflegends.com" + href
            
            # On cherche l'image avec plus de précision
            img_tag = article.find('img')
            image = img_tag['src'] if img_tag else ""
            if image and not image.startswith('http'):
                image = image # Parfois l'URL est complète, parfois non
                
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

    if url != last_sent:
        payload = {
            "content": "🚀 **Nouveau patch League of Legends !**",
            "embeds": [{
                "title": title,
                "url": url,
                "color": 16743424,
                "image": {"url": image} if image else None,
                "description": f"Les modifications sont disponibles. Cliquez sur le lien pour voir les détails.\n\n[Lien direct vers l'article]({url})"
            }],
            "footer": {"text": "Bot LoL Update"}
        }
        r = requests.post(WEBHOOK_URL, json=payload)
        
        if r.status_code in [200, 204]:
            with open(cache_file, "w") as f:
                f.write(url)
            print(f"Succès : {title} envoyé.")
