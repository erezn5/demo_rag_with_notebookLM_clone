import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
import re


def clean_text(text):
    """Removes extra whitespace and weird characters."""
    # Collapse multiple spaces into one
    return re.sub(r'\s+', ' ', text).strip()


def scrape_url_to_pdf(url, output_path):
    """
    Scrapes the text from a URL and saves it as a simple PDF.
    Returns True if successful, False otherwise.
    """
    try:
        # 1. Fetch the HTML
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/',
            'DNT': '1',  # Do Not Track Request Header
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # 2. Parse Text
        soup = BeautifulSoup(response.content, 'html.parser')

        # Kill all script and style elements (we just want text)
        for script in soup(["script", "style", "nav", "footer"]):
            script.extract()

        # Get text
        text = soup.get_text()
        clean_content = clean_text(text)

        # 3. Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)

        # Add Title
        pdf.set_font("Arial", style='B', size=16)
        pdf.cell(200, 10, txt=f"Scraped Content: {url}", ln=True, align='C')
        pdf.ln(10)

        # Add Content (fpdf doesn't handle utf-8 well by default,
        # so we encode/decode to latin-1 to avoid crashes, or use a font that supports it.
        # For simplicity, we stick to basic encoding here).
        pdf.set_font("Arial", size=12)

        # FPDF generic multi_cell
        # We replace smart quotes/dashes to prevent encoding errors in standard font
        safe_text = clean_content.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, safe_text)

        pdf.output(output_path)
        return True

    except Exception as e:
        print(f"Scraping Error: {e}")
        return False