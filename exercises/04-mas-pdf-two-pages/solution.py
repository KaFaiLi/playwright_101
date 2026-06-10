"""Exercise 4: MAS PDF Downloader - first two pages (solution)

Extends exercise 3 by walking the FIRST TWO pages of the MAS publications
listing. For each listing page it collects the publication-entry links,
visits each detail page, and downloads the PDFs found there.

Like exercise 3, this relies on headless=False (MAS serves a different
page to headless browsers) and on intercepting .pdf responses to force a
download instead of opening Edge's built-in PDF viewer.
"""
import os
from playwright.sync_api import sync_playwright

MAS_URL = "https://www.mas.gov.sg/publications"
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "downloads")
NUM_PAGES = 2           # how many listing pages to walk
MAX_ENTRIES_PER_PAGE = 10  # cap detail pages per listing page (keeps the demo quick)


def listing_url(page_number: int) -> str:
    """Build the URL for listing page N.

    MAS paginates with a ?page= query parameter (page 1 is the bare URL).
    If the site changes its pagination scheme, this is the one spot to
    update.
    """
    if page_number <= 1:
        return MAS_URL
    return f"{MAS_URL}?page={page_number}"


def entry_links_on_page(page):
    """Return publication-entry hrefs on the current listing page.

    The listing links to both category index pages
    (/publications/<category> - 1 segment, no PDFs) and specific entry
    pages (/publications/<category>/<year>/<slug> - 3+ segments, which DO
    have PDFs). Keep only the 3+ segment ones.
    """
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
    """Trigger a PDF link's download and save it.

    Uses a JavaScript click (el.click()) rather than Playwright's
    link.click(): some MAS detail pages list chapter PDFs that are hidden
    behind accordions/tabs, and Playwright's click waits for the element
    to be visible (and would time out). A JS click fires regardless.
    """
    with page.expect_download() as download_info:
        link.evaluate("el => el.click()")
    download = download_info.value
    path = os.path.join(download_dir, download.suggested_filename)
    download.save_as(path)
    print(f"Downloaded: {download.suggested_filename}")


def main() -> None:
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    with sync_playwright() as p:
        # headless=False matters: MAS serves a different page to headless
        # browsers, which would make every check below silently find 0.
        browser = p.chromium.launch(channel="msedge", headless=False)
        context = browser.new_context()

        # MAS serves PDFs inline (target="_blank" -> Edge's PDF viewer)
        # instead of as downloads. Add a Content-Disposition: attachment
        # header to .pdf responses so page.expect_download() fires.
        def force_pdf_download(route):
            response = route.fetch()
            headers = {**response.headers, "content-disposition": "attachment"}
            route.fulfill(response=response, headers=headers)

        context.route("**/*.pdf", force_pdf_download)

        page = context.new_page()

        # 1. Collect entry links from the first NUM_PAGES listing pages.
        #    Dedupe across pages in case the same entry appears twice.
        all_hrefs = []
        for page_number in range(1, NUM_PAGES + 1):
            url = listing_url(page_number)
            page.goto(url)
            # The listing renders its entries with JavaScript, so wait for
            # the network to settle before reading the links.
            page.wait_for_load_state("networkidle")
            hrefs = entry_links_on_page(page)[:MAX_ENTRIES_PER_PAGE]
            print(f"Listing page {page_number}: {len(hrefs)} publication link(s).")
            for href in hrefs:
                if href not in all_hrefs:
                    all_hrefs.append(href)

        if not all_hrefs:
            print(
                "No publication links found on the first two pages - the "
                "MAS site structure may have changed. Inspect the live page "
                "and update the selectors / pagination above."
            )
            browser.close()
            return

        # 2. Visit each entry page and download its PDFs.
        print(f"Visiting {len(all_hrefs)} publication page(s) total.")
        downloaded = 0
        for href in all_hrefs:
            detail_url = href if href.startswith("http") else f"https://www.mas.gov.sg{href}"
            page.goto(detail_url)
            detail_pdfs = page.locator("a[href$='.pdf' i]")
            detail_count = detail_pdfs.count()
            if detail_count == 0:
                print(f"No PDF found on {detail_url}, skipping.")
                continue
            for i in range(detail_count):
                try:
                    download_pdf(page, detail_pdfs.nth(i), DOWNLOAD_DIR)
                    downloaded += 1
                except Exception as exc:
                    print(f"  Skipped a PDF on {detail_url}: {exc}")

        print(f"Done. Downloaded {downloaded} PDF(s) to {DOWNLOAD_DIR}")
        browser.close()


if __name__ == "__main__":
    main()
