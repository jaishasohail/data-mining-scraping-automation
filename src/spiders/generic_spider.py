import logging
from typing import Any, Dict, Iterable, Optional

import scrapy

from .parser import build_lead_from_quote
from utils.proxy_manager import ProxyManager

LOGGER = logging.getLogger(__name__)


class GenericLeadSpider(scrapy.Spider):
    """
    Generic spider that scrapes public pages and converts them
    into lead-like records.

    By default it hits https://quotes.toscrape.com/ which is a
    public demo website specifically built for scraping practice.
    """

    name = "generic_leads"

    def __init__(self, config: Optional[Dict[str, Any]] = None, *args: Any, **kwargs: Any) -> None:
    super().__init__(*args, **kwargs)
    self.config: Dict[str, Any] = config or {}
    self.start_urls = self._resolve_start_urls()
    self.proxy_manager = ProxyManager(self.config.get("proxies") or [])
    LOGGER.info("GenericLeadSpider initialized with start URLs: %s",
                self.start_urls)

    def _resolve_start_urls(self) -> Iterable[str]:
    urls = self.config.get("generic_start_urls")
    if urls and isinstance(urls, list):
    return urls
    return ["https://quotes.toscrape.com/"]

    def start_requests(self) -> Iterable[scrapy.Request]:
    for url in self.start_urls:
    meta: Dict[str, Any] = {}
    proxy = self.proxy_manager.get_random_proxy()
    if proxy:
    meta["proxy"] = proxy
    LOGGER.debug("Using proxy %s for URL %s", proxy, url)
    yield scrapy.Request(url=url, callback=self.parse, meta=meta)

    def parse(self, response: scrapy.http.Response, **kwargs: Any) -> Iterable[Dict[str, Any]]:
    LOGGER.info("Parsing page: %s", response.url)
    for quote_sel in response.css("div.quote"):
    item = build_lead_from_quote(response, quote_sel)
    if item:
    LOGGER.debug("Yielding item: %s", item)
    yield item

    next_page = response.css("li.next a::attr(href)").get()
    if next_page:
    LOGGER.info("Following next page: %s", next_page)
    yield response.follow(next_page, callback=self.parse)
