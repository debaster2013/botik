import re

LABEL_RE = re.compile(r"^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$")
ZONE_RE = re.compile(r"^[a-z0-9-]{2,24}$")


def is_valid_label(label: str) -> bool:
    return bool(label and LABEL_RE.match(label))


def is_valid_zone(zone: str | None) -> bool:
    return bool(zone and ZONE_RE.match(zone))
