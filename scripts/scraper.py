# Purpose:
# Scrape bug bounty listings using BeautifulSoup and Requests.
# Collect basic info and save it to a CSV file.

import requests
from bs4 import BeautifulSoup

def scrape_hackerone():
    print("Scraping HackerOne...")
    base_url = "https://hackerone.com"
    directory_url = f"{base_url}/directory"
    programs = []

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; BugBountyBot/1.0)"
    }
