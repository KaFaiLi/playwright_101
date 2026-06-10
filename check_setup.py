"""Pre-workshop environment check.

Run this before the workshop to confirm Python, Playwright, and
Microsoft Edge are all installed and working correctly.
"""
from playwright.sync_api import sync_playwright


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=False)
        page = browser.new_page()
        page.goto("https://playwright.dev")
        title = page.title()
        print(f"Page title: {title}")
        browser.close()

    print("Setup OK - Edge launched, navigated, and closed successfully.")


if __name__ == "__main__":
    main()
