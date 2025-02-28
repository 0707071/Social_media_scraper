

import re
import requests
from bs4 import BeautifulSoup
from apify_client import ApifyClient
import config

# Load API credentials from config
APIFY_API_TOKEN = config.APIFY_API_TOKEN
APIFY_ACTOR_ID = config.APIFY_ACTOR_ID

# Define social media URL patterns
SOCIAL_PATTERNS = {
    "linkedin": r"https?://(www\.)?linkedin\.com/.*",
    "facebook": r"https?://(www\.)?facebook\.com/.*",
    "twitter": r"https?://(www\.)?twitter\.com/.*",
    "instagram": r"https?://(www\.)?instagram\.com/.*",
    "tiktok": r"https?://(www\.)?tiktok\.com/.*"
}

def is_valid_url(url):
    """Check if the URL follows a valid format."""
    return bool(re.match(r"https?://[^\s/$.?#].[^\s]*", url))

def extract_social_links(html):
    """Extracts social media links from the HTML content."""
    soup = BeautifulSoup(html, "html.parser")
    links = {}

    for tag in soup.find_all("a", href=True):
        url = tag["href"].strip()
        for platform, pattern in SOCIAL_PATTERNS.items():
            if re.match(pattern, url):
                links[platform] = url  # Store only valid URLs

    return links if links else None

def scrape_social_links(website_url):
    """Attempts direct web scraping; falls back to Apify if unsuccessful."""
    if not website_url or not is_valid_url(website_url):
        raise ValueError(f"Invalid website URL: {website_url}")

    # Try direct scraping first
    try:
        response = requests.get(website_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # Raise an error for HTTP failures (4xx, 5xx)
        links = extract_social_links(response.text)
        if links:
            return links
    except requests.RequestException as e:
        print(f"[Error] Failed direct scraping for {website_url}: {e}")

    # Fallback to Apify API if direct scraping fails
    try:
        print(f"[Info] Falling back to Apify for {website_url}")
        client = ApifyClient(APIFY_API_TOKEN)
        run = client.actor(APIFY_ACTOR_ID).call(run_input={"startUrls": [{"url": website_url}]})

        # Process Apify results
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            if item.get("url") == website_url:
                return {platform: item.get(platform, "") for platform in SOCIAL_PATTERNS}
    except Exception as e:
        print(f"[Error] Apify API request failed: {e}")

    return {key: "" for key in SOCIAL_PATTERNS}  # Return empty links if all fail
