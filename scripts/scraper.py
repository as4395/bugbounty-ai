# Purpose:
# Scrape bug bounty listings using BeautifulSoup, Selenium, and Requests.
# Collect basic info and save it to a CSV file.

import requests
from bs4 import BeautifulSoup
import csv

def fetch_page(url):
    print(f"Fetching {url}...")
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"Failed to fetch {url}")
        return None

def extract_bounties(soup):
    print("Extracting bounties...")
    bounties = []
    for i in range(5):  # Sample data
        bounty = {'title': f"Bug {i + 1}", 'reward': 500 + i * 50}
        bounties.append(bounty)
    return bounties

def save_bounties(bounties, filename):
    print(f"Saving to {filename}...")
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'reward'])
        writer.writeheader()
        for bounty in bounties:
            writer.writerow(bounty)

def main():
    url = "https://example.com/bugbounty"
    soup = fetch_page(url)
    if soup:
        bounties = extract_bounties(soup)
        save_bounties(bounties, 'data/raw/bounties.csv')
    print("Scraping completed.")

if __name__ == "__main__":
    main()
