import logging
import re
from typing import Any, Dict, Optional, Set

import scrapy
from scrapy.exceptions import DropItem

LOGGER = logging.getLogger(__name__)

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def clean_lead_item(raw_item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Normalize and validate a single lead item.

    - Strips whitespace
    - Validates email format
    - Computes a `unique_key` used for de-duplication
    """
    if not raw_item:
    return None

    item: Dict[str, Any] = {}
    for key, value in raw_item.items():
    if isinstance(value, str):
    item[key] = value.strip()
    else:
    item[key] = value

    email = item.get("email")
    if email and not EMAIL_RE.match(email):
    LOGGER.warning("Dropping item with invalid email: %s", email)
    return None

    company = item.get("company") or ""
    decision_maker = item.get("decision_maker") or ""
    unique_key = f"{company}|{decision_maker}|{email or ''}".lower()
    item["unique_key"] = unique_key
    return item


class CleaningPipeline:
    """
    Scrapy pipeline that validates and deduplicates lead items.
    """

    def __init__(self) -> None:
    self.seen_keys: Set[str] = set()

    def process_item(self, item: Dict[str, Any], spider: scrapy.Spider) -> Dict[str, Any]:
    cleaned = clean_lead_item(dict(item))
    if not cleaned:
    raise DropItem("Invalid or empty lead item")

    key = cleaned["unique_key"]
    if key in self.seen_keys:
    LOGGER.info("Dropping duplicate lead: %s", key)
    raise DropItem("Duplicate lead item")

    self.seen_keys.add(key)
    return cleaned
