"""main.py — entry point for the Telegram Group Management Bot"""
from __future__ import annotations

import asyncio
import logging
import sys

from telegram.ext import Application

from bot.config import (
    BOT_TOKEN,
    WEBHOOK_LISTEN,
    WEBHOOK_PORT,
    WEBHOOK_URL,
)
from bot.handlers import register_all
from bot.models import init_db

# ── Logging setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)-8s | %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("bot.log", encoding="utf-8"),
    ],
)
# Silence noisy libraries
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

log = logging.getLogger(__name__)


async def main() -> None:
    log.info("Initialising database …")
    await init_db()

    log.info("Building application …")
    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    register_all(app)
    log.info("All handlers registered.")

    if WEBHOOK_URL:
        log.info("Starting in webhook mode: %s", WEBHOOK_URL)
        await app.run_webhook(
            listen=WEBHOOK_LISTEN,
            port=WEBHOOK_PORT,
            webhook_url=WEBHOOK_URL,
            allowed_updates=["message", "callback_query", "chat_member"],
            drop_pending_updates=True,
        )
    else:
        log.info("Starting in long-polling mode …")
        await app.run_polling(
            allowed_updates=["message", "callback_query", "chat_member"],
            drop_pending_updates=True,
        )


if __name__ == "__main__":
    asyncio.run(main())
