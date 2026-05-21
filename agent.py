from pydantic_ai import Agent
from pydantic_ai.tools import RunContext
from models import ArbitrageAlert, CardPrice, WatchlistEntry
from tools.scraper import get_card_price
from tools.sms import send_sms_alert
import json

agent = Agent(
    model="anthropic:claude-sonnet-4-20250514",
    result_type=ArbitrageAlert | None,
    system_prompt=(
        "You are an MTG card arbitrage sniper. "
        "Given a watchlist entry, you must:\n"
        "1. Call get_price to fetch current market price and lowest listing.\n"
        "2. Check if lowest_listing <= market_price * snipe_threshold.\n"
        "3. If the condition is met, call send_alert with a concise SMS message "
        "   including card name, market price, lowest listing, and the TCGplayer URL.\n"
        "4. Return an ArbitrageAlert if you fired an alert, or null if no opportunity.\n"
        "Only alert if the condition is strictly met. Be precise."
    ),
)

@agent.tool
async def get_price(ctx: RunContext[None], entry_json: str) -> dict:
    """Fetch current market price and lowest listing for a card. Pass WatchlistEntry as JSON string."""
    entry = WatchlistEntry(**json.loads(entry_json))
    price = await get_card_price(entry)
    if price is None:
        return {"error": "Could not scrape price data"}
    return price.model_dump()

@agent.tool
def send_alert(ctx: RunContext[None], message: str) -> str:
    """Send an SMS alert. Call this when an arbitrage opportunity is detected."""
    send_sms_alert(message)
    return "Alert sent."