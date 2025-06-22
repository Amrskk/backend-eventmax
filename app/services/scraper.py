import httpx
from bs4 import BeautifulSoup
from typing import List, Dict
from datetime import datetime

BASE_URL = "https://sxodim.com/almaty/afisha"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}


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

    response = httpx.get(BASE_URL, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    for card in soup.select(".impression-card"):
        try:
            title = card.get("title")
            link_suffix = card.select_one(".impression-card-image a")["href"]
            full_url = "https://sxodim.com" + link_suffix
            price = parse_price(card.get("data-minprice", "0"))
            tags = [tag.text.strip() for tag in card.select(".badge")]

            detail = httpx.get(full_url, headers=headers)
            ds = BeautifulSoup(detail.text, "lxml")
            desc = ds.select_one(".event-description")
            description = desc.text.strip() if desc else ""

            events.append({
                "title": title,
                "description": description,
                "location": "Алматы",  # Fallback if no exact location
                "price": price,
                "date": datetime.now(),  # recheck laterr
                "tags": tags
            })
        except Exception as e:
            print("Skip event due to error:", e)

    return events