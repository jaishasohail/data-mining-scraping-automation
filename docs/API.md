wn# Data Mining & Scraping Automation – API Guide

This document describes how to use the scraping automation tool from the command line and how the core modules fit together.

---

## 1. Running the Scraper

From the project root:

```bash
# Use the default example configuration and run both spiders
python src/main.py

# Run only the generic spider
python src/main.py --spider generic

# Run only the LinkedIn-style spider
python src/main.py --spider linkedin

# Use a custom configuration JSON
python src/main.py --config path/to/settings.json

The tool will:

Load configuration from config/settings.example.json or the path you provide.

Start one or both spiders (GenericLeadSpider, LinkedInLeadSpider).

Pass all scraped items through validation and cleaning.

Persist results to SQLite and export CSV/JSON under data/.

2. Configuration Schema
Example file: src/config/settings.example.json
Key sections:

log_level – One of DEBUG, INFO, WARNING, ERROR.

download_delay – Delay (in seconds) between requests from a single spider.

concurrent_requests – Maximum number of concurrent requests the crawler can perform.

robots_txt_obey – Whether to honor robots.txt.

Spider-specific options:

generic_start_urls – List of URLs for GenericLeadSpider.

linkedin_start_urls – List of URLs for LinkedInLeadSpider.

Networking:

proxies – List of proxy URLs. If provided, spiders will randomly pick one for each request.

Output layout:
json"output": {
 "csv": "data/output.csv",
 "json": "data/output.json",
 "sqlite": "data/leads.db"
}

These paths are relative to the project root.

3. Data Model
Each scraped lead item follows the same schema:
json{
 "company": "Example Ventures",
 "decision_maker": "Jane Doe",
 "position": "Thought Leader",
 "email": "jane-doe@example.com",
 "linkedin": "https://linkedin.com/in/jane-doe",
 "industry": "Testing, Scraping",
 "country": "Unknown",
 "unique_key": "example ventures|jane doe|jane-doe@example.com"
}

Fields

company – Synthetic or scraped company name.

decision_maker – Name of the person associated with the record.

position – Role or title.

email – Derived or scraped email address (validated for basic syntax).

linkedin – Profile URL or constructed identifier.

industry – Category or tags from the source.

country – Country of operation when known.

unique_key – Internal composite identifier used to deduplicate data.

4. Pipelines
Two pipelines are registered:

CleaningPipeline (pipelines.cleaner.CleaningPipeline)

Strips whitespace.

Validates email format.

Computes unique_key.

Drops duplicates and invalid entries.

StoragePipeline (pipelines.storage.StoragePipeline)

Stores each item in a SQLite database under data/leads.db.

On spider shutdown, exports all items to:

data/output.csv