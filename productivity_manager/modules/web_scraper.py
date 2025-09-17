import json
from typing import List, Dict, Any

import requests
from bs4 import BeautifulSoup


def get_news_headlines(feed_url: str = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en", limit: int = 10) -> List[str]:
    try:
        resp = requests.get(feed_url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "xml")
        items = soup.find_all("item")[:limit]
        return [item.title.text.strip() for item in items if item.title]
    except Exception:
        return []


def get_weather(city: str = "Seoul", provider: str = "wttr.in", api_key: str = "") -> Dict[str, Any]:
    try:
        if provider == "openweathermap" and api_key:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            data = r.json()
            return {
                "city": data.get("name", city),
                "temp_c": data["main"].get("temp"),
                "description": data["weather"][0].get("description", ""),
            }
        else:
            r = requests.get(f"https://wttr.in/{city}?format=j1", timeout=10)
            r.raise_for_status()
            data = r.json()
            current = data.get("current_condition", [{}])[0]
            return {
                "city": city,
                "temp_c": float(current.get("temp_C", 0)),
                "description": current.get("weatherDesc", [{}])[0].get("value", ""),
            }
    except Exception:
        return {"city": city, "temp_c": None, "description": "N/A"}


def get_exchange_rates(base: str = "USD") -> Dict[str, float]:
    try:
        r = requests.get(f"https://api.exchangerate.host/latest?base={base}", timeout=10)
        r.raise_for_status()
        data = r.json()
        return data.get("rates", {})
    except Exception:
        return {}


def read_rss(url: str, limit: int = 10) -> List[Dict[str, str]]:
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "xml")
        items = soup.find_all("item")[:limit]
        out: List[Dict[str, str]] = []
        for it in items:
            out.append({
                "title": it.title.text.strip() if it.title else "",
                "link": it.link.text.strip() if it.link else "",
                "pubDate": it.pubDate.text.strip() if it.pubDate else "",
            })
        return out
    except Exception:
        return []

