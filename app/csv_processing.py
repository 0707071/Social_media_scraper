
import pandas as pd
import os
from app.scraper import scrape_social_links
from app.broken_link_checker import BrokenLinkChecker  # Import the class

PROCESSED_FOLDER = os.path.join(os.getcwd(), "processed")


def process_csv(input_csv):
    """
    Processes a CSV file by extracting social media links from company websites.

    Steps:
    1. Reads the input CSV file.
    2. Validates the presence of the "Company Website" column.
    3. Initializes empty columns for social media links.
    4. Checks for broken links before scraping.
    5. Scrapes social media links for valid websites.
    6. Saves the updated data into a new CSV file in the "processed" folder.

    Args:
        input_csv (str): Path to the input CSV file.

    Returns:
        tuple: (output_csv_path, list_of_broken_links)
    """
    df = pd.read_csv(input_csv)

    if "Company Website" not in df.columns:
        raise ValueError("CSV must have a 'Company Website' column.")

    df["LinkedIn"] = ""
    df["Facebook"] = ""
    df["Twitter"] = ""
    df["Instagram"] = ""
    df["TikTok"] = ""

    # **Step 1: Check for broken links before scraping**
    websites = df["Company Website"].dropna().tolist()
    checker = BrokenLinkChecker(websites)
    broken_links = checker.check_links()

    if broken_links:
        print(f"Broken links found: {broken_links}")

    # **Step 2: Process only valid links**
    for index, row in df.iterrows():
        website = row["Company Website"]
        if pd.notna(website) and website not in broken_links:  # Skip broken links
            social_links = scrape_social_links(website)
            df.at[index, "LinkedIn"] = social_links["linkedin"]
            df.at[index, "Facebook"] = social_links["facebook"]
            df.at[index, "Twitter"] = social_links["twitter"]
            df.at[index, "Instagram"] = social_links["instagram"]
            df.at[index, "TikTok"] = social_links["tiktok"]
        elif website in broken_links:
            print(f"Skipping broken link: {website}")

    output_csv = os.path.join("processed", "processed_input.csv")
    df.to_csv(output_csv, index=False)
    print(f"Processed file path: {output_csv}")

    return output_csv, broken_links  # Return broken links
