import json
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from utils.config import load_config
from modules.web_scraper import get_news_headlines, get_weather, get_exchange_rates, read_rss


def build_scraper_tab(parent, base_dir: str):
    cfg = load_config(base_dir)
    frame = ttk.Frame(parent)

    controls = ttk.Frame(frame)
    controls.pack(fill=tk.X, padx=8, pady=8)

    # Weather
    city_var = tk.StringVar(value=cfg.get("web", {}).get("weather_city", "Seoul"))
    ttk.Label(controls, text="City:").pack(side=tk.LEFT)
    ttk.Entry(controls, textvariable=city_var, width=20).pack(side=tk.LEFT, padx=4)
    ttk.Button(controls, text="Weather", command=lambda: _show_weather(output, cfg, city_var.get())).pack(side=tk.LEFT)

    # News
    ttk.Button(controls, text="Headlines", command=lambda: _show_headlines(output, cfg)).pack(side=tk.LEFT, padx=6)

    # Exchange
    ttk.Button(controls, text="Exchange", command=lambda: _show_rates(output, cfg)).pack(side=tk.LEFT)

    # RSS custom
    rss_var = tk.StringVar(value=(cfg.get("web", {}).get("rss_feeds") or [""])[0])
    ttk.Entry(controls, textvariable=rss_var, width=50).pack(side=tk.LEFT, padx=6)
    ttk.Button(controls, text="Read RSS", command=lambda: _read_rss(output, rss_var.get())).pack(side=tk.LEFT)

    output = ScrolledText(frame, height=22)
    output.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    return frame


def _show_weather(output, cfg, city):
    output.delete("1.0", tk.END)
    provider = cfg.get("web", {}).get("weather_provider", "wttr.in")
    api_key = cfg.get("web", {}).get("weather_api_key", "")
    data = get_weather(city, provider=provider, api_key=api_key)
    output.insert(tk.END, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def _show_headlines(output, cfg):
    output.delete("1.0", tk.END)
    feeds = cfg.get("web", {}).get("rss_feeds", [])
    all_items = []
    for url in feeds:
        items = get_news_headlines(url)
        if items:
            all_items.extend(items)
    if not all_items:
        output.insert(tk.END, "No headlines available.\n")
    for i, t in enumerate(all_items[:20], start=1):
        output.insert(tk.END, f"{i}. {t}\n")


def _show_rates(output, cfg):
    output.delete("1.0", tk.END)
    base = cfg.get("web", {}).get("exchange_base", "USD")
    rates = get_exchange_rates(base)
    if not rates:
        output.insert(tk.END, "No rates available.\n")
        return
    for k in sorted(["EUR", "KRW", "JPY", "CNY", "GBP", "USD"]):
        if k in rates:
            output.insert(tk.END, f"{base}->{k}: {rates[k]:.4f}\n")


def _read_rss(output, url):
    output.delete("1.0", tk.END)
    items = read_rss(url)
    if not items:
        output.insert(tk.END, "No items.\n")
        return
    for it in items:
        output.insert(tk.END, f"- {it['title']}\n  {it['link']}\n  {it['pubDate']}\n\n")

