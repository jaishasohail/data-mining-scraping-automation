import logging
import random
from typing import Iterable, List, Optional

LOGGER = logging.getLogger(__name__)


class ProxyManager:
    """
    Simple in-memory proxy manager.

    It rotates over a list of HTTP proxies. Proxies are expected to be full
    URLs, for example:

    http://user:pass@host:port
    https://host:port
    """

    def __init__(self, proxies: Optional[Iterable[str]] = None) -> None:
    self._proxies: List[str] = [p for p in (
        proxies or []) if isinstance(p, str) and p.strip()]
    if self._proxies:
    LOGGER.info("ProxyManager initialized with %d proxies.",
                len(self._proxies))
    else:
    LOGGER.info(
        "ProxyManager initialized with no proxies; requests will not use a proxy.")

    def get_random_proxy(self) -> Optional[str]:
    """
 Return a random proxy from the list, or None if no proxies are configured.
 """
    if not self._proxies:
    return None
    return random.choice(self._proxies)
