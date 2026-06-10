"""Exercise 3: MAS PDF Downloader - solution

Visits the MAS publications listing page and downloads any PDFs linked
from it. If none are found directly, follows the first few
publication-page links and looks for PDFs there instead.
"""
import os
from playwright.sync_api import sync_playwright

MAS_URL = "https://www.mas.gov.sg/publications"
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "downloads")
MAX_ENTRIES = 5


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
        # headless=False matters here, not just for visibility: MAS appears
        # to serve a different (maintenance-style) page to headless
        # browsers, which would make both the direct and fallback checks
        # below silently return 0.
        browser = p.chromium.launch(channel="msedge", headless=False)
        context = browser.new_context()

        # MAS serves PDFs without a "download this file" hint, so Edge's
        # built-in PDF viewer just opens them in a new tab instead of
        # triggering a download. Intercept .pdf responses and add a
        # Content-Disposition: attachment header so the browser downloads
        # them instead - this lets page.expect_download() work as expected.
        def force_pdf_download(route):
            response = route.fetch()
            headers = {**response.headers, "content-disposition": "attachment"}
            route.fulfill(response=response, headers=headers)

        context.route("**/*.pdf", force_pdf_download)

        page = context.new_page()
        page.goto(MAS_URL)

        # 1. Look for direct PDF links on the listing page itself.
        pdf_links = page.locator("a[href$='.pdf' i]")
        count = pdf_links.count()
        print(f"Found {count} direct PDF link(s) on the listing page.")

        downloaded = 0
        for i in range(count):
            download_pdf(page, pdf_links.nth(i), DOWNLOAD_DIR)
            downloaded += 1

        # 2. If none found directly, follow the first few publication
        #    entry links and look for PDFs on each detail page.
        if downloaded == 0:
            # The listing page links to both category pages
            # (/publications/<category>, no PDFs) and specific entry
            # pages (/publications/<category>/<year>/<slug>, which DO
            # have PDFs). Use the CSS selector to narrow to
            # "/publications/" links, then filter in Python for hrefs
            # with at least 3 path segments (i.e. 2+ slashes after
            # "/publications/") to skip the category index pages.
            entry_links = page.locator("a[href*='/publications/']")
            hrefs = []
            for i in range(entry_links.count()):
                href = entry_links.nth(i).get_attribute("href")
                if not href:
                    continue
                rest = href.split("?")[0].split("/publications/", 1)[-1]
                segments = [s for s in rest.split("/") if s]
                if len(segments) >= 3 and href not in hrefs:
                    hrefs.append(href)

            entry_count = min(len(hrefs), MAX_ENTRIES)
            hrefs = hrefs[:entry_count]

            if entry_count == 0:
                print(
                    "No publication links found either - the MAS site "
                    "structure may differ from what this script expects. "
                    "Inspect the live page and update the selectors above."
                )
            else:
                print(f"No direct PDFs - checking {entry_count} publication page(s) instead.")

                for href in hrefs:
                    detail_url = href if href.startswith("http") else f"https://www.mas.gov.sg{href}"
                    page.goto(detail_url)
                    detail_pdfs = page.locator("a[href$='.pdf' i]")
                    detail_count = detail_pdfs.count()
                    if detail_count == 0:
                        print(f"No PDF found on {detail_url}, skipping.")
                        continue
                    for i in range(detail_count):
                        download_pdf(page, detail_pdfs.nth(i), DOWNLOAD_DIR)
                        downloaded += 1

        print(f"Done. Downloaded {downloaded} PDF(s) to {DOWNLOAD_DIR}")
        browser.close()


if __name__ == "__main__":
    main()
