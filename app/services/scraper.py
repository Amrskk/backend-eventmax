import httpx
from bs4 import BeautifulSoup
from typing import List, Dict


def fetch_events_from_ticketon() -> List[Dict]:
    events = []
    url = "https://ticketon.kz/rrs"
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " 
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml",
    }   
    try:
        response = httpx.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        for card in soup.select(".poster__item"):
            print(card.prettify())
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
