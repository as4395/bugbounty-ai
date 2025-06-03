import requests
from bs4 import BeautifulSoup

def scrape_intigriti(session_cookie):
    print("Scraping Intigriti (with login)...")
    base_url = "https://app.intigriti.com"
    programs_url = f"{base_url}/programs"
    programs = []

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; BugBountyBot/1.0)",
        "Cookie": f"int_session={session_cookie}"
    }

    response = requests.get(programs_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch Intigriti programs: {response.status_code}")
        return programs

    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.find_all('a', class_='program-card')

    for card in cards:
        program_name = card.find('h3').text.strip() if card.find('h3') else 'Unknown'
        program_url = base_url + card.get('href')

        # Visit program page
        program_resp = requests.get(program_url, headers=headers)
        if program_resp.status_code != 200:
            print(f"Failed to fetch program page: {program_url}")
            continue

        program_soup = BeautifulSoup(program_resp.text, 'html.parser')

        # Extract reward
        reward_tag = program_soup.find('div', class_='reward-range')
        reward = reward_tag.text.strip() if reward_tag else 'Unknown'

        # Extract scope
        scope_assets = []
        scope_section = program_soup.find('div', class_='scope-assets')
        if scope_section:
            asset_tags = scope_section.find_all('span', class_='asset-identifier')
            for asset in asset_tags:
                scope_assets.append(asset.text.strip())

        programs.append({
            'program_name': program_name,
            'domain': program_url,
            'reward': reward,
            'scope': ', '.join(scope_assets) if scope_assets else 'Unknown'
        })

    print(f"Collected {len(programs)} Intigriti programs with detailed info.")
    return programs
