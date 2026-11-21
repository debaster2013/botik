from handlers.common import router as common_router
from handlers.domains import router as domains_router
from handlers.fun_text import router as fun_text_router
from handlers.media import router as media_router
from handlers.stats import router as stats_router

__all__ = [
    "common_router",
    "domains_router",
    "fun_text_router",
    "media_router",
    "stats_router",
]
