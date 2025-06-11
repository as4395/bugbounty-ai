# Purpose:
#   Use Selenium to load Bugcrowd programs, then Requests + BeautifulSoup to scrape details.

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests
from bs4 import BeautifulSoup
import csv

def scrape_bugcrowd(session_cookie, output_file='data/raw/bugcrowd_targets.csv'):
    print("Launching Selenium browser for program listing...")

    # Set up Selenium
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://bugcrowd.com/")
        driver.add_cookie({
            'name': '_crowdcontrol_session',
            'value': session_cookie,
            'domain': 'bugcrowd.com',
            'path': '/',
            'secure': True,
            'httpOnly': True
        })

        driver.get("https://bugcrowd.com/programs")
        time.sleep(3)

        # Collect all program links
        program_links = []
        cards = driver.find_elements(By.CLASS_NAME, "bc-card__header")
        for card in cards:
            href = card.get_attribute("href")
            if href and href.startswith("https://bugcrowd.com/"):
                program_links.append(href)

    finally:
        driver.quit()

    print(f"Collected {len(program_links)} program URLs. Now scraping details with requests...")

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": f"_crowdcontrol_session={session_cookie}"
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

            reward_tag = soup.find('div', class_='stat__reward-range')
            reward = reward_tag.text.strip() if reward_tag else 'Unknown'

            scope_assets = []
            scope_section = soup.find('div', class_='program__targets')
            if scope_section:
                rows = scope_section.find_all('div', class_='bc-table__row')
                for row in rows:
                    name_tag = row.find('span', class_='bc-table__column-name')
                    if name_tag:
                        scope_assets.append(name_tag.text.strip())

            programs.append({
                'platform': 'Bugcrowd',
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
