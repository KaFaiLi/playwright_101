"""Exercise 3: MAS PDF Downloader

Fill in the TODOs below. Run with: python starter.py
Downloaded files go into ../../downloads/
"""
import os
from playwright.sync_api import sync_playwright

MAS_URL = "https://www.mas.gov.sg/publications"
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "downloads")


def download_pdf(page, link, download_dir):
    """Click a PDF link, wait for the download, and save it.

    Note: on the live MAS site, the listing page itself has 0 direct PDF
    links (see README), so this helper won't actually run for the basic
    exercise - `pdf_links.count()` will be 0 and the loop body never
    executes. It's here so the pattern is ready if you extend the
    exercise (see solution.py's stretch-goal fallback, which DOES find
    and download PDFs from publication detail pages).
    """
    with page.expect_download() as download_info:
        link.click()
    download = download_info.value
    path = os.path.join(download_dir, download.suggested_filename)
    download.save_as(path)
    print(f"Downloaded: {download.suggested_filename}")


def main() -> None:
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=False)
        page = browser.new_page()
        page.goto(MAS_URL)

        # TODO 1: find all links whose href ends in ".pdf"
        #   hint: page.locator("a[href$='.pdf' i]")
        pdf_links = None

        # TODO 2: print how many were found
        #   hint: pdf_links.count()

        # TODO 3: loop over pdf_links (use .count() and .nth(i)) and call
        #   download_pdf(page, pdf_links.nth(i), DOWNLOAD_DIR) for each

        browser.close()


if __name__ == "__main__":
    main()
