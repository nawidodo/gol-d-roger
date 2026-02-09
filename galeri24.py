import requests
from bs4 import BeautifulSoup
from decimal import Decimal
import json
from datetime import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
URL = "https://galeri24.co.id/harga-emas"

def clean_price(price_str: str) -> Decimal:
    """Clean price string like 'Rp1.041.000' to Decimal."""
    return Decimal(price_str.replace("Rp", "").replace(".", "").replace(",", "").strip())

def decimal_default(obj):
    """Handle Decimal serialization for JSON."""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def fetch_html(url: str) -> BeautifulSoup:
    """Fetch HTML content and return BeautifulSoup object."""
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def extract_gold_prices(soup: BeautifulSoup) -> dict:
    """Extract gold prices from the BeautifulSoup object."""
    galeri24_div = soup.find("div", {"id": "GALERI 24"})
    if not galeri24_div:
        raise ValueError("Could not find 'GALERI 24' section on the page.")

    main_container = galeri24_div.find("div", class_="grid divide-neutral-200 border-neutral-200")
    if not main_container:
        raise ValueError("Could not find the gold price container.")

    rows = main_container.find_all("div", class_="grid grid-cols-5 divide-x lg:hover:bg-neutral-50 transition-all")

    gold_prices = {}
    for row in rows:
        cols = row.find_all("div", class_="p-3 col-span-1 whitespace-nowrap w-fit") + \
               row.find_all("div", class_="p-3 col-span-2 whitespace-nowrap w-fit")
        cols_text = [col.get_text(strip=True) for col in cols]
        if len(cols_text) == 3:
            weight = Decimal(cols_text[0])
            sell_price = clean_price(cols_text[1])
            buy_price = clean_price(cols_text[2])
            gold_prices[weight] = {
                "sell": sell_price,
                "buy": buy_price
            }
    
    # Sort by weight before returning
    sorted_prices = dict(sorted(gold_prices.items(), key=lambda x: x[0]))
    
    # Convert keys back to string for JSON
    return {str(weight): prices for weight, prices in sorted_prices.items()}

def get_gold_price() -> dict:
    """Main function to get gold price and return dictionary."""
    try:
        soup = fetch_html(URL)
        gold_prices = extract_gold_prices(soup)

        result = {
            "last_update": datetime.now().isoformat(),
            "data": gold_prices
        }

        return result
    except (requests.RequestException, ValueError) as e:
        return {"error": str(e)}

def get_gold_price_json() -> str:
    """Get gold price and return JSON string (for CLI usage)."""
    result = get_gold_price()
    json_data = json.dumps(result, indent=2, default=decimal_default)
    print(json_data)
    return json_data

if __name__ == "__main__":
    get_gold_price_json()
