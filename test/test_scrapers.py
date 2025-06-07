# Purpose:
# Unit tests for scraping functions from HackerOne, Bugcrowd, and Intigriti.

# Requirements:
# Install pytest in your environment:
# ```bash
# pip install pytest

import pytest
from unittest.mock import patch
from scripts.hackerone_scraper import scrape_hackerone
from scripts.bugcrowd_scraper import scrape_bugcrowd
from scripts.intigriti_scraper import scrape_intigriti

# Simulated HTML content with the minimal structure needed for testing

hackerone_html = '''
<a class="directory-profile-link" aria-label="Test Program" href="/program/test"></a>
<div class="structured-field__value">Up to $500</div>
<div id="structured-scope">
  <span class="structured-scope__asset-identifier">test.com</span>
</div>
'''

bugcrowd_html = '''
<a class="bc-card__header" href="/program/test">Test Program</a>
<div class="stat__reward-range">$100-$1000</div>
<div class="bc-table__row">
  <span class="bc-table__column-name">test.bugcrowd.com</span>
</div>
'''

intigriti_html = '''
<a class="program-card" href="/programs/test">
  <h3>Test Program</h3>
</a>
<div class="reward-range">€50–€1500</div>
<div class="scope-assets">
  <span class="asset-identifier">test.intigriti.com</span>
</div>
'''

@patch("scripts.hackerone_scraper.requests.get")
def test_scrape_hackerone(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = hackerone_html

    results = scrape_hackerone("fake_session_cookie")
    assert isinstance(results, list)
    assert results[0]["program_name"] == "Test Program"
    assert "test.com" in results[0]["scope"]

@patch("scripts.bugcrowd_scraper.requests.get")
def test_scrape_bugcrowd(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = bugcrowd_html

    results = scrape_bugcrowd("fake_session_cookie")
    assert isinstance(results, list)
    assert results[0]["reward"] == "$100-$1000"
    assert "test.bugcrowd.com" in results[0]["scope"]

@patch("scripts.intigriti_scraper.requests.get")
def test_scrape_intigriti(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = intigriti_html

    results = scrape_intigriti("fake_session_cookie")
    assert isinstance(results, list)
    assert results[0]["program_name"] == "Test Program"
    assert "test.intigriti.com" in results[0]["scope"]
