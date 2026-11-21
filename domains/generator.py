from domains.catalog import POPULAR_ZONES


def generate_domain_ideas(label: str, limit: int = 8) -> list[str]:
    """Подбирает варианты доменных имён в разных зонах."""
    clean = "".join(ch for ch in label.lower() if ch.isalnum() or ch == "-").strip("-")
    if not clean:
        clean = "project"

    zones = list(POPULAR_ZONES.keys())[:limit]
    return [f"{clean}.{z}" for z in zones]
