from playwright.async_api import async_playwright
from models import CardPrice, WatchlistEntry
import asyncio

async def get_card_price(entry: WatchlistEntry) -> CardPrice | None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        await page.goto(entry.url, wait_until="domcontentloaded")
        await asyncio.sleep(5)
        await page.wait_for_selector(".price-points__upper__price", timeout=60000)
        
        
        # Debug: save fully rendered HTML
        content = await page.content()
        with open("debug_rendered.html", "w") as f:
            f.write(content)
        print(f"[scraper] Rendered HTML saved, length: {len(content)}")
        
        # grab market price
        try:
            market_el = await page.wait_for_selector(".price-points__upper__price", timeout=10000)
            market_text = await market_el.inner_text()
            market_price = float(market_text.strip().replace("$", "").replace(",", ""))
        except Exception as e:
            print(f"[scraper] Could not find market price for {entry.card_name}: {e}")
            await browser.close()
            return None

        # grab lowest listing (top of the list is cheapest)
        try:
            listing_els = await page.query_selector_all(".listing-item__listing-data__info__price")
            if not listing_els:
                print(f"[scraper] No listings found for {entry.card_name}")
                await browser.close()
                return None
            lowest_text = await listing_els[0].inner_text()
            lowest_listing = float(lowest_text.strip().replace("$", "").replace(",", ""))
        except Exception as e:
            print(f"[scraper] Could not find lowest listing for {entry.card_name}: {e}")
            await browser.close()
            return None

        await browser.close()

        print(f"[scraper] market_price={market_price}, lowest_listing={lowest_listing}")

        return CardPrice(
            card_name=entry.card_name,
            set_name=entry.set_name,
            product_id=0,
            market_price=market_price,
            lowest_listing=lowest_listing,
        )