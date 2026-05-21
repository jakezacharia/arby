import os
from config import settings
os.environ["ANTHROPIC_API_KEY"] = settings.anthropic_api_key

import asyncio
from datetime import datetime
from agent import agent
from watchlist import WATCHLIST
from config import settings

async def check_card(entry) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking {entry.card_name} ({entry.printing})")

    result = await agent.run(
        f"Check this card for a snipe opportunity: {entry.model_dump_json()}"
    )

    if result.output is not None:
        print(f"  OPPORTUNITY FOUND: {result.output.message}")
    else:
        print(f"  No opportunity yet.")

async def poll_loop() -> None:
    print(f"Bot started. Watching {len(WATCHLIST)} card(s) every {settings.poll_interval_seconds // 60} minutes.\n")

    while True:
        for entry in WATCHLIST:
            await check_card(entry)
        print(f"\nSleeping until next check...\n")
        await asyncio.sleep(settings.poll_interval_seconds)

if __name__ == "__main__":
    asyncio.run(poll_loop())