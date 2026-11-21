def parse_domain_input(raw: str) -> tuple[str, str | None]:
    """Разбирает строку вида 'example.com' или 'example com' на (имя, зона)."""
    cleaned = raw.strip().lower()
    if not cleaned:
        return "", None

    cleaned = cleaned.replace("https://", "").replace("http://", "").split("/")[0]

    if "." in cleaned:
        parts = cleaned.rsplit(".", 1)
        label = parts[0].strip(".")
        zone = parts[1].strip(".")
        return label, zone or None

    parts = cleaned.split()
    if len(parts) >= 2:
        return parts[0].strip("."), parts[1].strip(".")

    return cleaned.strip("."), None
