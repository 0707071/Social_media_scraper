
import pandas as pd
import os
from app.scraper import scrape_social_links
from app.broken_link_checker import BrokenLinkChecker  # Import the class

PROCESSED_FOLDER = os.path.join(os.getcwd(), "processed")
os.makedirs(PROCESSED_FOLDER, exist_ok=True)  # Ensure the folder exists


def read_file(input_file):
    """
    Reads an input file (CSV or Excel) into a Pandas DataFrame.

    Args:
        input_file (str): Path to the input file.

    Returns:
        pd.DataFrame: Loaded data.
    """
    if input_file.endswith(".csv"):
        return pd.read_csv(input_file)
    elif input_file.endswith((".xls", ".xlsx")):
        return pd.read_excel(input_file)
    else:
        raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")


def export_file(df, format="csv"):
    """
    Saves the processed DataFrame as a CSV or Excel file.

    Args:
        df (pd.DataFrame): Processed data.
        format (str): File format to save ('csv' or 'excel').

    Returns:
        str: Path to the saved file.
    """
    valid_formats = {"csv": "processed_input.csv", "excel": "processed_input.xlsx"}
    
    if format not in valid_formats:
        raise ValueError(f"Invalid format: '{format}'. Supported formats: CSV, Excel")

    output_file = os.path.join(PROCESSED_FOLDER, valid_formats[format])

    if format == "csv":
        df.to_csv(output_file, index=False)
    elif format == "excel":
        try:
            with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
                df.to_excel(writer, index=False, sheet_name="Processed Data")
        except ModuleNotFoundError:
            raise ModuleNotFoundError("Missing dependency: 'xlsxwriter'. Install it using: pip install xlsxwriter")

    return output_file


def process_file(input_file, output_format="csv"):
    """
    Processes an input file (CSV or Excel) by extracting social media links.

    Steps:
    1. Reads the input file.
    2. Validates the presence of the "Company Website" column.
    3. Initializes empty columns for social media links.
    4. Checks for broken links before scraping.
    5. Scrapes social media links for valid websites.
    6. Saves the updated data in the chosen format.

    Args:
        input_file (str): Path to the input file.
        output_format (str): Desired output format ('csv' or 'excel').

    Returns:
        tuple: (output_file_path, list_of_broken_links)
    """
    df = read_file(input_file)

    if "Company Website" not in df.columns:
        raise ValueError("Input file must have a 'Company Website' column.")

    # Initialize social media columns if not present
    social_media_columns = ["LinkedIn", "Facebook", "Twitter", "Instagram", "TikTok"]
    for col in social_media_columns:
        if col not in df.columns:
            df[col] = ""

    # Step 1: Check for broken links before scraping
    websites = df["Company Website"].dropna().tolist()
    checker = BrokenLinkChecker(websites)
    broken_links = checker.check_links()

    if broken_links:
        print(f"Broken links found: {broken_links}")

    # Step 2: Process only valid links
    for index, row in df.iterrows():
        website = row["Company Website"]
        if pd.notna(website) and website not in broken_links:
            social_links = scrape_social_links(website)
            for key in social_media_columns:
                df.at[index, key] = social_links.get(key.lower(), "")  # Ensure no missing keys
        elif website in broken_links:
            print(f"Skipping broken link: {website}")

    # Save the processed file
    output_file = export_file(df, format=output_format)
    print(f"Processed file saved at: {output_file}")

    return output_file, broken_links
