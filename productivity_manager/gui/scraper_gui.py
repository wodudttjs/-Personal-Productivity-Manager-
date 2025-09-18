import json
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from utils.config import load_config
from modules.web_scraper import (
    get_news_headlines,
    get_weather,
    get_exchange_rates,
    read_rss,
    get_weather_weekly,
)
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def build_scraper_tab(parent, base_dir: str):
    cfg = load_config(base_dir)
    frame = ttk.Frame(parent)

    controls = ttk.Frame(frame)
    controls.pack(fill=tk.X, padx=8, pady=8)

    # Weather
    city_var = tk.StringVar(value=cfg.get("web", {}).get("weather_city", "Seoul"))
    ttk.Label(controls, text="도시:").pack(side=tk.LEFT)
    ttk.Entry(controls, textvariable=city_var, width=20).pack(side=tk.LEFT, padx=4)
    ttk.Button(
        controls,
        text="날씨 (최근 1주 그래프)",
        command=lambda: _show_weather_weekly(output, plot_area, city_var.get()),
    ).pack(side=tk.LEFT)

    # News
    ttk.Button(controls, text="헤드라인", command=lambda: _show_headlines(output, cfg)).pack(side=tk.LEFT, padx=6)

    # Exchange
    ttk.Button(controls, text="환율", command=lambda: _show_rates(output, cfg)).pack(side=tk.LEFT)

    # RSS custom
    rss_var = tk.StringVar(value=(cfg.get("web", {}).get("rss_feeds") or [""])[0])
    ttk.Entry(controls, textvariable=rss_var, width=50).pack(side=tk.LEFT, padx=6)
    ttk.Button(controls, text="RSS 읽기", command=lambda: _read_rss(output, rss_var.get())).pack(side=tk.LEFT)

    # Plot area for weather graphs
    plot_area = ttk.Frame(frame)
    plot_area.pack(fill=tk.BOTH, expand=False, padx=8, pady=(0, 4))

    output = ScrolledText(frame, height=22)
    output.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    return frame


def _show_weather_weekly(output, plot_area, city: str):
    output.delete("1.0", tk.END)
    # Fetch weekly data (last 7 days)
    data = get_weather_weekly(city)
    output.insert(tk.END, json.dumps(data, ensure_ascii=False, indent=2) + "\n")

    # Clear previous plots
    for w in list(plot_area.winfo_children()):
        w.destroy()

    try:
        daily = data.get("daily", [])
        if not daily:
            lbl = ttk.Label(plot_area, text="날씨 데이터를 가져올 수 없습니다.")
            lbl.pack(anchor=tk.W)
            return
        dates = [d.get("date") for d in daily]
        tavg = [d.get("tavg") for d in daily]

        fig = Figure(figsize=(6.0, 2.6), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(dates, tavg, marker='o', color='#1f77b4', linewidth=2)
        ax.set_title(f"최근 7일 평균기온 (°C) - {data.get('city', city)}")
        ax.set_xlabel("날짜")
        ax.set_ylabel("°C")
        ax.grid(True, linestyle='--', alpha=0.3)
        for label in ax.get_xticklabels():
            label.set_rotation(45)
            label.set_ha('right')

        canvas = FigureCanvasTkAgg(fig, master=plot_area)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=False)
    except Exception as e:
        ttk.Label(plot_area, text=f"그래프 오류: {e}").pack(anchor=tk.W)


def _show_headlines(output, cfg):
    output.delete("1.0", tk.END)
    feeds = cfg.get("web", {}).get("rss_feeds", [])
    all_items = []
    for url in feeds:
        items = get_news_headlines(url)
        if items:
            all_items.extend(items)
    if not all_items:
        output.insert(tk.END, "헤드라인을 가져올 수 없습니다.\n")
    for i, t in enumerate(all_items[:20], start=1):
        output.insert(tk.END, f"{i}. {t}\n")


def _show_rates(output, cfg):
    output.delete("1.0", tk.END)
    base = cfg.get("web", {}).get("exchange_base", "USD")
    rates = get_exchange_rates(base)
    if not rates:
        output.insert(tk.END, "환율 정보를 가져올 수 없습니다.\n")
        return
    for k in sorted(["EUR", "KRW", "JPY", "CNY", "GBP", "USD"]):
        if k in rates:
            output.insert(tk.END, f"{base}->{k}: {rates[k]:.4f}\n")


def _read_rss(output, url):
    output.delete("1.0", tk.END)
    items = read_rss(url)
    if not items:
        output.insert(tk.END, "항목이 없습니다.\n")
        return
    for it in items:
        output.insert(tk.END, f"- {it['title']}\n  {it['link']}\n  {it['pubDate']}\n\n")
