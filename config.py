import os

DEFAULT_BOT_TOKEN = "9045755510:AAHKyTABmIkLF4OuWa3hdxdwyxNS5tI761Y"


def get_bot_token() -> str:
    token = os.getenv("BOT_TOKEN", "").strip() or DEFAULT_BOT_TOKEN.strip()
    if not token:
        raise RuntimeError("Не задан BOT_TOKEN!")
    return token


DB_PATH = os.getenv("DB_PATH", "bot_stats.db")
