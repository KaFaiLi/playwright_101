"""Exercise 4: MAS PDF Downloader - first two pages

Extends exercise 3 to walk the FIRST TWO pages of the MAS publications
listing and download the PDFs from each entry.

Fill in the TODOs below. Run with: python starter.py
Downloaded files go into ../../downloads/
"""
import os
from playwright.sync_api import sync_playwright

MAS_URL = "https://www.mas.gov.sg/publications"
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "downloads")
NUM_PAGES = 2
MAX_ENTRIES_PER_PAGE = 5


def listing_url(page_number: int) -> str:
    """URL for listing page N. Page 1 is the bare URL; later pages use
    a ?page= query parameter."""
    if page_number <= 1:
        return MAS_URL
    return f"{MAS_URL}?page={page_number}"


def entry_links_on_page(page):
    """Return publication-entry hrefs (3+ path segments) on the current
    listing page - these are the ones that actually have PDFs."""
    links = page.locator("a[href*='/publications/']")
    hrefs = []
    for i in range(links.count()):
        href = links.nth(i).get_attribute("href")
        if not href:
            continue
        rest = href.split("?")[0].split("/publications/", 1)[-1]
        segments = [s for s in rest.split("/") if s]
        if len(segments) >= 3 and href not in hrefs:
            hrefs.append(href)
    return hrefs


def download_pdf(page, link, download_dir):
    """Click a PDF link, wait for the download, and save it."""
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
        context = browser.new_context()

        # Force MAS's inline PDFs to download (see exercise 3's README).
        def force_pdf_download(route):
            response = route.fetch()
            headers = {**response.headers, "content-disposition": "attachment"}
            route.fulfill(response=response, headers=headers)

        context.route("**/*.pdf", force_pdf_download)

        page = context.new_page()

        # TODO 1: loop page_number from 1 to NUM_PAGES. For each:
        #   - page.goto(listing_url(page_number))
        #   - call entry_links_on_page(page) and keep the first
        #     MAX_ENTRIES_PER_PAGE links
        #   - collect them into one list, skipping duplicates
        all_hrefs = []

        # TODO 2: loop over all_hrefs. For each href:
        #   - build detail_url (prepend "https://www.mas.gov.sg" if the
        #     href doesn't start with "http")
        #   - page.goto(detail_url)
        #   - find PDF links: page.locator("a[href$='.pdf' i]")
        #   - for each, call download_pdf(page, ..., DOWNLOAD_DIR)

        browser.close()


if __name__ == "__main__":
    main()
