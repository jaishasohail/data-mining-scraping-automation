import sys
from pathlib import Path

import pytest

# Ensure `src` is on sys.path so we can import project modules when running `pytest` from repo root.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from spiders.parser import build_lead_from_html  # noqa: E402
from pipelines.cleaner import clean_lead_item  # noqa: E402

SAMPLE_HTML = """

 “A clever quote for testing.”

 Jane Doe

 Testing
 Scraping

"""


def test_build_lead_from_html_creates_expected_fields():
    lead = build_lead_from_html(SAMPLE_HTML)
    assert lead is not None, "Lead should not be None"
    for field in ["company", "decision_maker", "position", "email", "linkedin", "industry", "country"]:
    assert field in lead, f"Missing field {field}"
    assert lead[field], f"Field {field} should not be empty"


def test_clean_lead_item_adds_unique_key_and_validates_email():
    lead = build_lead_from_html(SAMPLE_HTML)
    cleaned = clean_lead_item(lead)
    assert cleaned is not None, "Cleaned item should not be None"
    assert "unique_key" in cleaned
    assert cleaned["unique_key"]
    assert "jane-doe" in cleaned["email"]


def test_clean_lead_item_rejects_invalid_email():
    lead = build_lead_from_html(SAMPLE_HTML)
    lead["email"] = "not-an-email"
    cleaned = clean_lead_item(lead)
    assert cleaned is None, "Invalid email should cause item to be rejected"
