import httpx
from bs4 import BeautifulSoup
from typing import List, Dict
from datetime import datetime

BASE_URL = "https://sxodim.com/almaty/events/"

def parse_date(date_str: str) -> datetime:
    months = {
        'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4,
        'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8,
        'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12
    }
    parts = date_str.strip().split()
    if len(parts) != 3:
        return datetime.now()
    day, month, year = int(parts[0]), months[parts[1]], int(parts[2])
    return datetime(year, month, day)

def parse_price(price_str: str) -> float:
    if "бесплатно" in price_str.lower():
        return 0.0
    digits = ''.join(filter(str.isdigit, price_str))
    return float(digits) if digits else 0.0

def fetch_events_from_sxodim() -> List[Dict]:
    events = []

    response = httpx.get(BASE_URL)
    soup = BeautifulSoup(response.text, "lxml")

    for card in soup.select(".card-event"):
        try:
            title = card.select_one(".card-event__title").text.strip()
            link = card.select_one("a")["href"]
            full_url = "https://sxodim.com" + link

            detail = httpx.get(full_url)
            ds = BeautifulSoup(detail.text, "lxml")

            desc = ds.select_one(".event-description").text.strip()
            date = parse_date(ds.select_one(".event-date").text.strip())
            location = ds.select_one(".event-location").text.strip()
            price = parse_price(ds.select_one(".event-price").text.strip())

            events.append({
                "title": title,
                "description": desc,
                "location": location,
                "price": price,
                "date": date,
                "tags": ["sxodim"]
            })
        except Exception as e:
            print("Skip event due to error:", e)

    return events
