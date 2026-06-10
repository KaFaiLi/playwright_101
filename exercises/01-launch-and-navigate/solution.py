"""Exercise 1: Launch & Navigate - solution"""
import os
from playwright.sync_api import sync_playwright

SCREENSHOT_PATH = os.path.join(os.path.dirname(__file__), "publications.png")


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=False)
        page = browser.new_page()

        page.goto("https://www.mas.gov.sg")
        print(f"Home page title: {page.title()}")

        page.goto("https://www.mas.gov.sg/publications")
        print(f"Publications page title: {page.title()}")
        print(f"Current URL: {page.url}")

        page.screenshot(path=SCREENSHOT_PATH)
        print(f"Saved screenshot to {SCREENSHOT_PATH}")

        browser.close()


if __name__ == "__main__":
    main()
