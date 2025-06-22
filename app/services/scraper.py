import httpx
from bs4 import BeautifulSoup
from typing import List, Dict
from playwright.sync_api import sync_playwright

def fetch_events_from_ticketon() -> List[Dict]:
    events = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://ticketon.kz/rrs", timeout=60000)
        page.wait_for_selector(".poster__item", timeout=20000)

        cards = page.query_selector_all(".poster__item")
        print(f"Found {len(cards)} cards")

        for card in cards:
            try:
                title = card.query_selector(".poster__name").inner_text().strip()
                location = card.query_selector(".poster__city").inner_text().strip()
                date = card.query_selector(".poster__date").inner_text().strip()
                link = "https://ticketon.kz" + card.query_selector("a").get_attribute("href")

                events.append({
                    "title": title,
                    "description": "",
                    "location": location,
                    "price": 0.0,
                    "date": date,
                    "tags": ["ticketon"]
                })
            except Exception as e:
                print("skip card:", e)

        browser.close()

    return events
