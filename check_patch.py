import requests
from bs4 import BeautifulSoup
import os

# URL SPECIFIQUE LOL
WEBHOOK_URL = "https://discord.com/api/webhooks/1469458508977279079/YL4KeSwJKfv9OtnkTk9traXj8itFPxpBNb8ZO-4TMkfneO1HjYBL3_rZ9tHZnOzk-XFO"
URL_NEWS = "https://www.leagueoflegends.com/fr-fr/news/tags/patch-notes/"

def get_latest_patch():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(URL_NEWS, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        article = soup.find('a', href=True)
        if article:
            title_el = article.find('h2') or article.find('h3')
            title = title_el.text.strip() if title_el else "Notes de patch"
            href = article['href']
            url = href if href.startswith('http') else "https://www.leagueoflegends.com" + href
            img = article.find('img')
            image = img['src'] if img else ""
            return title, url, image
    except:
        return None, None, None
    return None, None, None

# TEST DE CONNEXION IMMEDIAT
requests.post(WEBHOOK_URL, json={"content": "🛠️ Test du Bot LoL : Tentative d'envoi..."})

title, url, image = get_latest_patch()

if title:
    cache_file = "last_patch.txt"
    # On force l'envoi si le fichier n'existe pas ou si l'URL a changé
    last_sent = ""
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            last_sent = f.read().strip()

    if url != last_sent:
        payload = {
            "embeds": [{
                "title": title,
                "url": url,
                "color": 16743424,
                "image": {"url": image},
                "description": f"Nouveau patch LoL détecté !\n[Lire les notes ici]({url})"
            }]
        }
        r = requests.post(WEBHOOK_URL, json=payload)
        if r.status_code in [200, 204]:
            with open(cache_file, "w") as f:
                f.write(url)
            print("Succès LoL")
