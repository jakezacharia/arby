import httpx
from bs4 import BeautifulSoup
from models import CardPrice, WatchlistEntry

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

async def get_card_price(entry: WatchlistEntry) -> CardPrice | None:
    async with httpx.AsyncClient() as client:
        resp = await client.get(entry.url, headers=HEADERS, follow_redirects=True)
        resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # Market price
    market_el = soup.find(class_="price-points__upper__price")
    if not market_el:
        print(f"[scraper] Could not find market price for {entry.card_name}")
        return None

    # Lowest listing -- first result is cheapest (TCGplayer sorts ascending)
    listing_els = soup.find_all(class_="listing-item__listing-data__info__price")
    if not listing_els:
        print(f"[scraper] No listings found for {entry.card_name}")
        return None

    try:
        market_price = float(market_el.text.strip().replace("$", "").replace(",", ""))
        lowest_listing = float(listing_els[0].text.strip().replace("$", "").replace(",", ""))
    except ValueError as e:
        print(f"[scraper] Price parsing error: {e}")
        return None

    return CardPrice(
        card_name=entry.card_name,
        set_name=entry.set_name,
        product_id=0,  # not needed for scraping
        market_price=market_price,
        lowest_listing=lowest_listing,
    )