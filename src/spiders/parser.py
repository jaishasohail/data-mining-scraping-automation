import logging
import re
from typing import Any, Dict, Optional

from scrapy import Selector
from scrapy.http import Response

LOGGER = logging.getLogger(__name__)

EMAIL_SAFE_CHARS_RE = re.compile(r"[^a-z0-9]+")


def slugify_name(name: str) -> str:
    """
    Convert a human-readable name into a URL/email safe slug.
    """
    lowered = name.strip().lower()
    return EMAIL_SAFE_CHARS_RE.sub("-", lowered).strip("-")


def build_lead_from_quote(response: Response, quote_sel: Selector) -> Optional[Dict[str, Any]]:
    """
    Build a lead-like dictionary from a single quote block on quotes.toscrape.com.

    This is intentionally deterministic so our tests and pipelines stay stable.
    """
    author = quote_sel.css("small.author::text").get()
    if not author:
    LOGGER.debug("Skipping quote without author on %s", response.url)
    return None

    tags = quote_sel.css("div.tags a.tag::text").getall()
    company = f"{author.split()[0]} Ventures"
    position = "Thought Leader"
    industry = ", ".join(tags) if tags else "General"

    slug = slugify_name(author)
    email = f"{slug}@example.com"
    linkedin = f"https://linkedin.com/in/{slug}"

    item: Dict[str, Any] = {
        "company": company,
        "decision_maker": author,
        "position": position,
        "email": email,
        "linkedin": linkedin,
        "industry": industry,
        "country": "Unknown",
    }
    LOGGER.debug("Built lead item: %s", item)
    return item


def build_lead_from_html(html: str) -> Optional[Dict[str, Any]]:
    """
    Helper utility for tests: build a lead from a small HTML snippet.
    """
    selector = Selector(text=html)
    quote_sel = selector.css("div.quote")
    if not quote_sel:
    return None
    # Take the first match for determinism
    return build_lead_from_quote(Response(url="http://test.local", body=html.encode("utf-8")), quote_sel[0])
