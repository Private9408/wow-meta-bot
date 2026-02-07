import requests
from bs4 import BeautifulSoup
import os

# CONFIGURATION
URL_NEWS = "https://www.leagueoflegends.com/fr-fr/news/tags/patch-notes/"
WEBHOOK_URL = "https://discord.com/api/webhooks/1469458508977279079/YL4KeSwJKfv9OtnkTk9traXj8itFPxpBNb8ZO-4TMkfneO1HjYBL3_rZ9tHZnOzk-XFO"

# TEST IMMEDIAT : Si tu ne reçois pas ce message, ton Webhook est mort
requests.post(WEBHOOK_URL, json={"content": "🚀 Test du bot : Connexion établie !"})

def get_latest_patch():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(URL_NEWS, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        article = soup.find('a', href=True) # On prend le tout premier article
        if article:
            title_el = article.find('h2') or article.find('h3')
            title = title_el.text.strip() if title_el else "Patch Note"
            href = article['href']
            url = href if href.startswith('http') else "https://www.leagueoflegends.com" + href
            img = article.find('img')
            image = img['src'] if img else ""
            return title, url, image
    except:
        return None, None, None
    return None, None, None

title, url, image = get_latest_patch()
if title:
    cache_file = "last_patch.txt"
    # Le script enverra le patch si last_patch.txt est absent ou different
    if not os.path.exists(cache_file) or open(cache_file).read().strip() != url:
        payload = {
            "embeds": [{
                "title": title,
                "url": url,
                "image": {"url": image},
                "description": f"Nouveau patch détecté !\n{url}"
            }]
        }
        requests.post(WEBHOOK_URL, json=payload)
        with open(cache_file, "w") as f:
            f.write(url)
