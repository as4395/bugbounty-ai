import requests
from bs4 import BeautifulSoup

def scrape_bugcrowd(session_cookie):
    print("Scraping Bugcrowd (with login)...")
    base_url = "https://bugcrowd.com"
    programs_url = f"{base_url}/programs"
    programs = []

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; BugBountyBot/1.0)",
        "Cookie": f"_crowdcontrol_session={session_cookie}"
    }

    response = requests.get(programs_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch Bugcrowd programs: {response.status_code}")
        return programs

    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.find_all('a', class_='bc-card__header')

    for card in cards:
        program_name = card.text.strip()
        program_url = base_url + card.get('href')

        # Visit individual program page
        program_resp = requests.get(program_url, headers=headers)
        if program_resp.status_code != 200:
            print(f"Failed to fetch program page: {program_url}")
            continue

        program_soup = BeautifulSoup(program_resp.text, 'html.parser')

        # Extract reward
        reward_tag = program_soup.find('div', class_='stat__reward-range')
        reward = reward_tag.text.strip() if reward_tag else 'Unknown'

        # Extract scope
        scope_assets = []
        scope_section = program_soup.find('div', class_='program__targets')
        if scope_section:
            asset_tags = scope_section.find_all('div', class_='bc-table__row')
            for asset in asset_tags:
                asset_name = asset.find('span', class_='bc-table__column-name')
                if asset_name:
                    scope_assets.append(asset_name.text.strip())

        programs.append({
            'program_name': program_name,
            'domain': program_url,
            'reward': reward,
            'scope': ', '.join(scope_assets) if scope_assets else 'Unknown'
        })

    print(f"Collected {len(programs)} Bugcrowd programs with detailed info.")
    return programs
