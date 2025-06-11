# Purpose:
#   Use Selenium to authenticate and load Intigriti programs, then Requests + BeautifulSoup to extract program details.

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests
from bs4 import BeautifulSoup
import csv

def scrape_intigriti(session_cookie, output_file='data/raw/intigriti_targets.csv'):
    print("Launching Selenium browser for Intigriti...")

    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://app.intigriti.com")
        driver.add_cookie({
            'name': 'int_session',
            'value': session_cookie,
            'domain': 'app.intigriti.com',
            'path': '/',
            'secure': True,
            'httpOnly': True
        })

        driver.get("https://app.intigriti.com/researcher/programs")
        time.sleep(4)

        program_links = []
        cards = driver.find_elements(By.CLASS_NAME, "program-card")
        for card in cards:
            href = card.get_attribute("href")
            if href and href.startswith("https://app.intigriti.com"):
                program_links.append(href)

    finally:
        driver.quit()

    print(f"Collected {len(program_links)} Intigriti programs. Now scraping details...")

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": f"int_session={session_cookie}"
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

            reward_tag = soup.find('div', class_='reward-range')
            reward = reward_tag.text.strip() if reward_tag else 'Unknown'

            scope_assets = []
            scope_section = soup.find('div', class_='scope-assets')
            if scope_section:
                asset_tags = scope_section.find_all('span', class_='asset-identifier')
                for asset in asset_tags:
                    scope_assets.append(asset.text.strip())

            programs.append({
                'platform': 'Intigriti',
                'program_name': program_name,
                'domain': url,
                'reward': reward,
                'scope': ', '.join(scope_assets) if scope_assets else 'Unknown'
            })

        except Exception as e:
            print(f"Error scraping {url}: {e}")

    # Save results to CSV
    if programs:
        keys = programs[0].keys()
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(programs)

    print(f"Scraped {len(programs)} programs and saved to {output_file}.")
