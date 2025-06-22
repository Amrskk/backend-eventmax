import httpx
from bs4 import BeautifulSoup
from typing import List, Dict


def fetch_events_from_ticketon() -> List[Dict]:
    events = []
    url = "https://ticketon.kz/rrs"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    try:
        response = httpx.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        for card in soup.select(".poster__item"):
            try:
                title = card.select_one(".poster__name").text.strip()
                link = "https://ticketon.kz" + card.select_one("a")["href"]
                location = card.select_one(".poster__city").text.strip()
                date = card.select_one(".poster__date").text.strip()
                price = 0.0  # unavailable in the card (

                events.append({
                    "title": title,
                    "description": "",
                    "location": location,
                    "price": price,
                    "date": date,
                    "tags": ["ticketon"]
                })

            except Exception as e:
                print("Skip ticketon event:", e)
    except Exception as e:
        print("Ticketon page load failed:", e)

    return events

def fetch_events_from_yandex_afisha() -> List[Dict]:
    events = []
    base_url = "https://afisha.yandex.ru/api/events"
    params = {
        "location": "almaty",
        "limit": 50,
        "page": 1
    }
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    try:
        response = httpx.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        for item in data.get("data", []):
            title = item.get("title", "").strip()
            description = item.get("description", "").strip()
            location = item.get("location", {}).get("title", "Алматы")
            tags = [genre.get("name") for genre in item.get("genres", [])]
            date = item.get("schedule", {}).get("start", None)
            price = 0.0  # No price info in API

            events.append({
                "title": title,
                "description": description,
                "location": location,
                "price": price,
                "date": date,
                "tags": tags + ["yandex_afisha"]
            })

    except Exception as e:
        print("Yandex Afisha error:", e)

    return events
