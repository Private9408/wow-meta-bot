import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1469383829041975380/51UI7h8gILbV51o6AreYyRZTxeH3IjQ97KAGDlxKc7-qOLY3YHik0R-HCdskCoFCKIdm"

def send_meta():
    # Les données de ton image
    data = [
        {"r": "1", "s": "SURVIVAL HUNTER", "sc": "4127", "c": 0xABD473},
        {"r": "2", "s": "FURY WARRIOR", "sc": "4124", "c": 0xC79C6E},
        {"r": "3", "s": "UNHOLY DEATH KNIGHT", "sc": "4118", "c": 0xC41F3B},
        {"r": "4", "s": "FROST MAGE", "sc": "4111", "c": 0x3FC7EB},
        {"r": "5", "s": "DEVOURER DEMON HUNTER", "sc": "4092", "c": 0xA330C9}
    ]

    embed = {
        "title": "🏆 TOP DPS M+ - MURLOK.IO",
        "color": 0x2f3136,
        "fields": []
    }

    for item in data:
        embed["fields"].append({
            "name": f"{item['r']}. {item['s']}",
            "value": f"Score: `{item['sc']}`",
            "inline": True
        })

    requests.post(WEBHOOK_URL, json={"embeds": [embed]})

if __name__ == "__main__":
    send_meta()
