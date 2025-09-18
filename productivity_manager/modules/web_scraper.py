import json
from typing import List, Dict, Any, Tuple

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


def _geocode_city(city: str) -> Tuple[float, float, str]:
    """Return (lat, lon, display_name) using Open-Meteo geocoding."""
    try:
        r = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "ko", "format": "json"},
            timeout=10,
        )
        r.raise_for_status()
        data = r.json()
        res = (data.get("results") or [])[0]
        lat = float(res["latitude"])  # type: ignore[index]
        lon = float(res["longitude"])  # type: ignore[index]
        name = str(res.get("name") or city)
        country = str(res.get("country") or "")
        display = f"{name}{' ' + country if country else ''}"
        return lat, lon, display
    except Exception:
        return 0.0, 0.0, city


def get_weather_weekly(city: str = "Seoul") -> Dict[str, Any]:
    """Fetch last 7 days daily weather for the city and return structured data.

    Uses Open-Meteo API without API key.
    """
    lat, lon, display = _geocode_city(city)
    if lat == 0.0 and lon == 0.0:
        return {"city": display, "daily": []}
    try:
        r = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "past_days": 7,
                "forecast_days": 0,
                "daily": "temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum",
                "timezone": "auto",
            },
            timeout=10,
        )
        r.raise_for_status()
        dj = r.json().get("daily", {})
        times = dj.get("time", [])
        tmax = dj.get("temperature_2m_max", [])
        tmin = dj.get("temperature_2m_min", [])
        tavg = dj.get("temperature_2m_mean", [])
        prcp = dj.get("precipitation_sum", [])
        out: List[Dict[str, Any]] = []
        for i in range(min(len(times), len(tavg))):
            out.append({
                "date": times[i],
                "tmin": tmin[i] if i < len(tmin) else None,
                "tmax": tmax[i] if i < len(tmax) else None,
                "tavg": tavg[i],
                "precip": prcp[i] if i < len(prcp) else None,
            })
        return {"city": display, "daily": out}
    except Exception:
        return {"city": display, "daily": []}


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
