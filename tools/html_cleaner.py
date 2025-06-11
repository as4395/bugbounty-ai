# Purpose:
#   Clean and sanitize HTML strings into plain readable text.

from bs4 import BeautifulSoup

def clean_html(raw_html):
    if not raw_html:
        return ""

    soup = BeautifulSoup(raw_html, "html.parser")

    # Remove scripts, styles, and hidden elements
    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text(separator=' ', strip=True)
    return ' '.join(text.split())  
