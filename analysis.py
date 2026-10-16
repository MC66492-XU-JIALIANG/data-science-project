"""Download World Bank indicators and recreate both portfolio figures."""
from pathlib import Path
import csv
import json
import urllib.request
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont

COUNTRIES = {"USA": "United States", "CHN": "China", "GBR": "United Kingdom", "JPN": "Japan"}
INDICATORS = {"NY.GDP.PCAP.CD": "GDP per capita current US dollars", "SP.POP.TOTL": "Population total"}
COLORS = {"USA": "#2563EB", "CHN": "#DC2626", "GBR": "#16A34A", "JPN": "#9333EA"}


def fetch_indicator(indicator):
    url = ("https://api.worldbank.org/v2/country/USA;CHN;GBR;JPN/indicator/" + indicator
           + "?date=2000:2024&format=json&per_page=500")
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))[1]


def get_font(size, bold=False):
    name = r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"
    return ImageFont.truetype(name, size) if Path(name).exists() else ImageFont.load_default()


def create_chart(series, indicator, filename, title, ylabel, divisor=1, suffix=""):
    width, height, left, right, top, bottom = 1500, 850, 145, 85, 105, 125
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    values = [value / divisor for code in COUNTRIES for year, value in series[(indicator, code)]]
    low, high = min(values), max(values)
    pad = (high - low) * .10 or 1
    low, high = max(0, low - pad), high + pad
    x = lambda year: left + (year - 2000) * (width - left - right) / 24
    y = lambda value: height - bottom - (value / divisor - low) * (height - top - bottom) / (high - low)
    draw.text((left, top - 60), title, fill="#111827", font=get_font(34, True))
    for index in range(6):
        value = low + index * (high - low) / 5
        ypos = y(value * divisor)
        draw.line((left, ypos, width - right, ypos), fill="#E5E7EB", width=2)
        draw.text((20, ypos - 11), f"{value:,.0f}{suffix}", fill="#4B5563", font=get_font(18))
    draw.line((left, top, left, height - bottom), fill="#374151", width=2)
    draw.line((left, height - bottom, width - right, height - bottom), fill="#374151", width=2)
    for year in range(2000, 2025, 4):
        xpos = x(year)
        draw.text((xpos - 23, height - bottom + 20), str(year), fill="#4B5563", font=get_font(18))
    draw.text((width // 2 - 120, height - 55), "Year", fill="#374151", font=get_font(22))
    draw.text((left, top + 5), ylabel, fill="#374151", font=get_font(22))
    for code, name in COUNTRIES.items():
        points = [(x(year), y(value)) for year, value in series[(indicator, code)]]
        draw.line(points, fill=COLORS[code], width=5)
        for point in points:
            draw.ellipse((point[0]-3, point[1]-3, point[0]+3, point[1]+3), fill=COLORS[code])
    for index, (code, name) in enumerate(COUNTRIES.items()):
        ypos = top + 25 + index * 38
        draw.line((width-420, ypos, width-385, ypos), fill=COLORS[code], width=5)
        draw.text((width-370, ypos-10), name, fill="#111827", font=get_font(18))
    draw.text((left, height-35), "Source: World Bank World Development Indicators accessed 2026-10-16", fill="#6B7280", font=get_font(15))
    image.save(filename)


def main():
    rows = []
    for indicator, label in INDICATORS.items():
        for item in fetch_indicator(indicator):
            if item["value"] is not None:
                rows.append({"country_code": item["countryiso3code"], "country": item["country"]["value"],
                             "year": int(item["date"]), "indicator_code": indicator,
                             "indicator": label, "value": float(item["value"])})
    rows.sort(key=lambda row: (row["indicator_code"], row["country_code"], row["year"]))
    data = Path("data"); figures = Path("figures")
    data.mkdir(exist_ok=True); figures.mkdir(exist_ok=True)
    with (data / "world_bank_indicators_2000_2024.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys()); writer.writeheader(); writer.writerows(rows)
    series = defaultdict(list)
    for row in rows:
        series[(row["indicator_code"], row["country_code"])].append((row["year"], row["value"]))
    create_chart(series, "NY.GDP.PCAP.CD", figures / "gdp_per_capita_trend.png", "GDP per capita trend 2000 to 2024", "Current US dollars")
    create_chart(series, "SP.POP.TOTL", figures / "population_trend.png", "Population trend 2000 to 2024", "Population in millions", 1_000_000, "M")
    print(f"Saved {len(rows)} observations and recreated two figures.")


if __name__ == "__main__":
    main()
