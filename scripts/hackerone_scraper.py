import requests
from bs4 import BeautifulSoup

def scrape_hackerone(session_cookie):
    print("Scraping HackerOne (with login)...")
    base_url = "https://hackerone.com"
    directory_url = f"{base_url}/directory"
    programs = []

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; BugBountyBot/1.0)",
        "Cookie": f"hackerone_session={session_cookie}"
    }

    response = requests.get(directory_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch HackerOne directory: {response.status_code}")
        return programs

    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.find_all('a', class_='directory-profile-link')

    for card in cards:
        program_name = card.get('aria-label')
        program_url = base_url + card.get('href')

        # Visit program page (with same session)
        program_resp = requests.get(program_url, headers=headers)
        if program_resp.status_code != 200:
            print(f"Failed to fetch program page: {program_url}")
            continue

        program_soup = BeautifulSoup(program_resp.text, 'html.parser')

        # Extract reward info
        reward_tag = program_soup.find('div', class_='structured-field__value')
        reward = reward_tag.text.strip() if reward_tag else 'Unknown'

        # Extract scope assets
        scope_assets = []
        scope_section = program_soup.find('div', id='structured-scope')
        if scope_section:
            asset_tags = scope_section.find_all('span', class_='structured-scope__asset-identifier')
            for asset in asset_tags:
                scope_assets.append(asset.text.strip())

        programs.append({
            'program_name': program_name,
            'domain': program_url,
            'reward': reward,
            'scope': ', '.join(scope_assets) if scope_assets else 'Unknown'
        })

    print(f"Collected {len(programs)} HackerOne programs with detailed info.")
    return programs
