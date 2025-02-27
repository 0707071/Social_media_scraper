import requests  

class BrokenLinkChecker:

    """
    A class to check the validity of a list of URLs.
    
    Attributes:
        urls (list): A list of URLs to be checked.
    """
    def __init__(self, urls):
        """
        Initializes the BrokenLinkChecker with a list of URLs.

        Args:
            urls (list): A list of URLs to check.
        """
        self.urls = urls  

    def check_links(self):
        """Check all URLs and return a list of broken links."""
        broken_links = []
        for url in self.urls:
            if not self.is_link_working(url):
                broken_links.append(url)
        return broken_links  

    def is_link_working(self, url):
        """Check if a given URL is working (returns status code < 400)."""
        try:
            response = requests.head(url, allow_redirects=True, timeout=5)  
            return response.status_code < 400  
        except requests.RequestException:
            return False  
