# Purpose:
#   Use Selenium to load HackerOne programs, then Requests + BeautifulSoup to scrape details.

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests
from bs4 import BeautifulSoup
import csv

def scrape_hackerone(session_cookie, output_file='data/raw/hackerone_targets.csv'):
    print("Launching Selenium browser for HackerOne directory...")

    # Set up Selenium
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://hackerone.com/")
        driver.add_cookie({
            'name': 'hackerone_session',
            'value': session_cookie,
            'domain': 'hackerone.com',
            'path': '/',
            'secure': True,
            'httpOnly': True
        })

        driver.get("https://hackerone.com/directory")
        time.sleep(3)

        program_links = []
        cards = driver.find_elements(By.CLASS_NAME, "directory-profile-link")
        for card in cards:
            href = card.get_attribute("href")
            if href and href.startswith("https://hackerone.com/"):
                program_links.append(href)

    finally:
        driver.quit()

    print(f"Collected {len(program_links)} HackerOne programs. Now scraping details...")

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": f"hackerone_session={session_cookie}"
    }

    programs = []

    for url in program_links:
        try:
            resp = requests.get(url, headers=headers)
            if resp.status_code != 200:
                print(f"Failed to load: {url}")
                continue

            soup = BeautifulSoup(resp.text, 'html.parser')
            program_name = soup.find('h1').text.strip() if soup.find('h1') else 'Unknown'

            reward_tag = soup.find('div', class_='structured-field__value')
            reward = reward_tag.text.strip() if reward_tag else 'Unknown'

            scope_assets = []
            scope_section = soup.find('div', id='structured-scope')
            if scope_section:
                asset_tags = scope_section.find_all('span', class_='structured-scope__asset-identifier')
                for asset in asset_tags:
                    scope_assets.append(asset.text.strip())

            programs.append({
                'platform': 'HackerOne',
                'program_name': program_name,
                'domain': url,
                'reward': reward,
                'scope': ', '.join(scope_assets) if scope_assets else 'Unknown'
            })

        except Exception as e:
            print(f"Error scraping {url}: {e}")

    # Save to CSV
    if programs:
        keys = programs[0].keys()
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(programs)

    print(f"Scraped {len(programs)} programs and saved to {output_file}.")
