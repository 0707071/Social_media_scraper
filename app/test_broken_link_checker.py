import pytest
from .broken_link_checker import BrokenLinkChecker

def test_broken_links():
    """
    Tests the BrokenLinkChecker class to ensure it correctly identifies broken and working links.

    Steps:
    1. Define a list of test URLs:
       - A valid, working URL (Google).
       - A non-existent URL (expected to be broken).
    2. Initialize the BrokenLinkChecker with the test URLs.
    3. Call the check_links() method to retrieve a list of broken links.
    4. Assert that the non-existent URL is classified as broken.
    5. Assert that the working URL is NOT classified as broken.

    Run the test using:
        pytest .
    """
    test_urls = [
        "https://www.google.com",  # Working
        "https://thiswebsitedoesnotexist12345.com"  # Broken
    ]
    checker = BrokenLinkChecker(test_urls)
    broken_links = checker.check_links()
    
    assert "https://thiswebsitedoesnotexist12345.com" in broken_links
    assert "https://www.google.com" not in broken_links

 # Run the test using: pytest .