
import re
import requests
from bs4 import BeautifulSoup
from apify_client import ApifyClient
import config

APIFY_API_TOKEN = config.APIFY_API_TOKEN
APIFY_ACTOR_ID = config.APIFY_ACTOR_ID

# Social media regex patterns
SOCIAL_PATTERNS = {
    "linkedin": r"https?://(www\.)?linkedin\.com/.*",
    "facebook": r"https?://(www\.)?facebook\.com/.*",
    "twitter": r"https?://(www\.)?twitter\.com/.*",
    "instagram": r"https?://(www\.)?instagram\.com/.*",
    "tiktok": r"https?://(www\.)?tiktok\.com/.*"
}

def is_valid_url(url):
    """Check if the URL is valid before proceeding"""
    return re.match(r"https?://[^\s/$.?#].[^\s]*", url) is not None

def extract_social_links(html):
    """Extracts social media links using regex and ensures they belong to the same section."""
    soup = BeautifulSoup(html, "html.parser")
    links = {key: "" for key in SOCIAL_PATTERNS}

    for tag in soup.find_all("a", href=True):
        url = tag["href"]
        for platform, pattern in SOCIAL_PATTERNS.items():
            if re.match(pattern, url):
                links[platform] = url

    return links if any(links.values()) else None

def scrape_social_links(website_url):
    """First tries direct scraping; falls back to Apify if needed."""
    if not website_url or not is_valid_url(website_url):
        raise ValueError(f"Invalid website URL: {website_url}")

    try:
        response = requests.get(website_url, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors (4xx, 5xx)
        links = extract_social_links(response.text)
        if links:
            return links
    except requests.RequestException as e:
        print(f"Request failed: {e}")

    # If direct scraping fails, fallback to Apify
    try:
        client = ApifyClient(APIFY_API_TOKEN)
        run = client.actor(APIFY_ACTOR_ID).call(run_input={"startUrls": [{"url": website_url}]})

        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            if item.get("url") == website_url:
                return {
                    "linkedin": item.get("linkedin", ""),
                    "facebook": item.get("facebook", ""),
                    "twitter": item.get("twitter", ""),
                    "instagram": item.get("instagram", ""),
                    "tiktok": item.get("tiktok", "")
                }
    except Exception as e:
        print(f"Apify API Error: {e}")

    return {key: "" for key in SOCIAL_PATTERNS}
