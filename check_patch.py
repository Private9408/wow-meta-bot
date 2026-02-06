import requests
from bs4 import BeautifulSoup
import os

# Configuration
URL_NEWS = "https://www.leagueoflegends.com/fr-fr/news/game-updates/"
# Ton URL directe
WEBHOOK_URL = "https://discord.com/api/webhooks/1469458508977279079/YL4KeSwJKfv9OtnkTk9traXj8itFPxpBNb8ZO-4TMkfneO1HjYBL3_rZ9tHZnOzk-XFO"

def get_latest_patch():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(URL_NEWS, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            title_el = link.find('h2')
            if title_el and "Notes de patch" in title_el.text:
                title = title_el.text.strip()
                href = link.get('href', '')
                url = href if href.startswith('http') else "https://www.leagueoflegends.com" + href
                img = link.find('img')
                image = img['src'] if img and img.has_attr('src') else ""
                return title, url, image
    except:
        pass
    return None, None, None

title, url, image = get_latest_patch()

if title:
    cache_file = "last_patch.txt"
    last_sent = ""
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            last_sent = f.read().strip()

    if url != last_sent:
        payload = {
            "content": "📢 **Nouveau patch LoL !**",
            "embeds": [{
                "title": title, "url": url, "color": 16743424,
                "image": {"url": image} if image else None,
                "description": f"Les notes sont dispo ici : {url}"
            }]
        }
        requests.post(WEBHOOK_URL, json=payload)
        with open(cache_file, "w") as f:
            f.write(url)
        print("MATCH_FOUND") # Indicateur pour GitHub Actions
    else:
        print("NO_CHANGES")
