import logging
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
import scrapy

LOGGER = logging.getLogger(__name__)


class StoragePipeline:
    """
    Pipeline that stores items into SQLite and writes CSV/JSON exports
    under the `data/` directory at the project root.
    """

    def __init__(self) -> None:
    self.items: List[Dict[str, Any]] = []
    self.conn: Optional[sqlite3.Connection] = None
    self.cursor: Optional[sqlite3.Cursor] = None
    self.db_path: Optional[Path] = None

    def _project_root(self) -> Path:
        # src/pipelines/storage.py -> src -> project root
    return Path(__file__).resolve().parents[2]

    def open_spider(self, spider: scrapy.Spider) -> None:
    root = self._project_root()
    data_dir = root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    self.db_path = data_dir / "leads.db"
    LOGGER.info("Opening SQLite DB at %s", self.db_path)
    self.conn = sqlite3.connect(self.db_path)
    self.cursor = self.conn.cursor()
    self.cursor.execute(
        """
 CREATE TABLE IF NOT EXISTS leads (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 company TEXT,
 decision_maker TEXT,
 position TEXT,
 email TEXT,
 linkedin TEXT,
 industry TEXT,
 country TEXT,
 unique_key TEXT UNIQUE
 )
 """
    )
    self.conn.commit()

    def process_item(self, item: Dict[str, Any], spider: scrapy.Spider) -> Dict[str, Any]:
    self.items.append(dict(item))

    if self.cursor is None:
    LOGGER.error("SQLite cursor not initialized.")
    return item

    LOGGER.debug("Storing item to SQLite: %s", item)
    self.cursor.execute(
        """
 INSERT OR IGNORE INTO leads
 (company, decision_maker, position, email, linkedin, industry, country, unique_key)
 VALUES (:company, :decision_maker, :position, :email, :linkedin, :industry, :country, :unique_key)
 """,
        item,
    )
    if self.conn:
    self.conn.commit()

    return item

    def close_spider(self, spider: scrapy.Spider) -> None:
    root = self._project_root()
    data_dir = root / "data"
    if self.items:
    df = pd.DataFrame(self.items)
    csv_path = data_dir / "output.csv"
    json_path = data_dir / "output.json"

    LOGGER.info("Writing %d items to %s and %s",
                len(self.items), csv_path, json_path)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_path, index=False)
    df.to_json(json_path, orient="records", indent=2, force_ascii=False)

    if self.conn:
    LOGGER.info("Closing SQLite connection.")
    self.conn.close()
