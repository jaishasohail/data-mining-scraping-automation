import argparse
import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

from scrapy.crawler import CrawlerProcess

from spiders.generic_spider import GenericLeadSpider
from spiders.linkedin_spider import LinkedInLeadSpider

LOGGER = logging.getLogger("data-mining-scraping-automation")


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )


def project_root() -> Path:
    """
    Returns the repository root based on this file's location.
    """
    return Path(__file__).resolve().parents[1]


def load_config(config_path: Optional[str]) -> Dict[str, Any]:
    """
    Load configuration JSON. If not provided, falls back to the example config.
    """
    root = project_root()
    if config_path:
    path = Path(config_path)
    else:
    path = root / "config" / "settings.example.json"

    if not path.exists():
    LOGGER.warning("Config file %s not found, using defaults.", path)
    return {}

    try:
    with path.open("r", encoding="utf-8") as f:
    cfg = json.load(f)
    LOGGER.info("Loaded configuration from %s", path)
    return cfg
    except Exception as exc:  # noqa: BLE001
    LOGGER.error("Failed to load config %s: %s", path, exc)
    return {}


def build_scrapy_settings(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build Scrapy settings dictionary from config and sensible defaults.
    """
    return {
        "LOG_LEVEL": config.get("log_level", "INFO"),
        "DOWNLOAD_DELAY": config.get("download_delay", 0.5),
        "CONCURRENT_REQUESTS": config.get("concurrent_requests", 8),
        "ROBOTSTXT_OBEY": config.get("robots_txt_obey", True),
        "ITEM_PIPELINES": {
            "pipelines.cleaner.CleaningPipeline": 300,
            "pipelines.storage.StoragePipeline": 400,
        },
        "FEED_EXPORT_ENCODING": "utf-8",
    }


def run(spider: str, config_path: Optional[str]) -> None:
    """
    Run one or both spiders based on CLI arguments.
    """
    cfg = load_config(config_path)
    configure_logging(cfg.get("log_level", "INFO"))

    settings = build_scrapy_settings(cfg)
    process = CrawlerProcess(settings=settings)

    spider = spider.lower()
    if spider == "generic":
    LOGGER.info("Starting GenericLeadSpider...")
    process.crawl(GenericLeadSpider, config=cfg)
    elif spider == "linkedin":
    LOGGER.info("Starting LinkedInLeadSpider...")
    process.crawl(LinkedInLeadSpider, config=cfg)
    else:
    LOGGER.info("Starting both GenericLeadSpider and LinkedInLeadSpider...")
    process.crawl(GenericLeadSpider, config=cfg)
    process.crawl(LinkedInLeadSpider, config=cfg)

    process.start()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Data Mining & Scraping Automation Tool"
    )
    parser.add_argument(
        "--spider",
        choices=["generic", "linkedin", "all"],
        default="all",
        help="Which spider to run (default: all).",
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to JSON config file (default: config/settings.example.json).",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(spider=args.spider, config_path=args.config)
