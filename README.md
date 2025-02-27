📌 Social Media Scraper

📢 Overview
This module is designed for lead generation by extracting social media links of companies from their websites. By leveraging web scraping and Apify, it automates the process of fetching social media profiles from a list of company websites provided in a CSV file.

Additionally, it features a broken link detection functionality to improve data accuracy, helping analysts identify and fix invalid links efficiently.

✨ Features
✅ Automated Lead Generation – Fetches social media links of companies from their websites
✅ Broken Link Detection – Identifies and highlights invalid or missing links
✅ User-Friendly GUI – Improved interface for easy file upload and results visualization
✅ CSV Processing – Upload, process, and download the enriched data effortlessly
✅ Fast & Efficient – Uses Apify & Web Scraping for rapid data extraction

📂 How It Works
Upload CSV – The CSV file should contain a list of company websites.
Scraping & Processing – The system extracts social media links and checks for broken links.
Results Displayed in GUI – Identified links and broken links are shown directly.
Download Processed File – The final dataset can be downloaded for further use.

⚙️ Configuration
Before running the scraper, ensure you have your Apify API token set up in the config file:

  "APIFY_API_TOKEN": "your_apify_token_here"

📂 Installation
To install and set up the scraper on your local machine, follow these steps:

# Clone the repository
git clone https://github.com/your-username/social-media-scraper.git

# Navigate to the project directory
cd social-media-scraper

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # For macOS/Linux
venv\Scripts\activate      # For Windows

⚙️ Usage
Run the scraper with the following command:
python run.py

🖥️ Example Output
A sample processed CSV file will contain:

Company Website	Facebook	Twitter	LinkedIn	Broken Links
example.com	✅ Found	✅ Found	❌ Broken	LinkedIn
company.com	✅ Found	❌ Broken	✅ Found	Twitter


🛠️ Technologies Used
Python (Core Programming)
Flask (Web Interface)
BeautifulSoup & Scrapy (Web Scraping)
Apify (Data Extraction)
Pandas (CSV Processing)
Bootstrap (GUI Enhancement)
