import logging
from typing import Any, Dict, Iterable, Optional

import scrapy

from .generic_spider import GenericLeadSpider

LOGGER = logging.getLogger(__name__)


class LinkedInLeadSpider(GenericLeadSpider):
    """
    A specialized spider that reuses GenericLeadSpider logic but is configured
    for LinkedIn-like scraping workflows.

    In this demo implementation, it still uses the quotes.toscrape.com website
    but reads dedicated `linkedin_start_urls` from the config, so the rest of
    the system can be wired and tested end-to-end without external credentials.
    """

    name = "linkedin_leads"

    def __init__(self, config: Optional[Dict[str, Any]] = None, *args: Any, **kwargs: Any) -> None:
    super().__init__(config=config, *args, **kwargs)
    self.start_urls = self._resolve_start_urls()
    LOGGER.info(
        "LinkedInLeadSpider initialized with start URLs: %s", self.start_urls)

    def _resolve_start_urls(self) -> Iterable[str]:
    urls = self.config.get("linkedin_start_urls")
    if urls and isinstance(urls, list):
    return urls
    # Use a tag-filtered page from the same demo site to simulate a
    # segmented/sales-navigator-like view.
    return ["https://quotes.toscrape.com/tag/inspirational/"]

    def parse(self, response: scrapy.http.Response, **kwargs: Any):
    LOGGER.info("LinkedInLeadSpider parsing page: %s", response.url)
    # We simply reuse the parsing logic from GenericLeadSpider
    yield from super().parse(response, **kwargs)
