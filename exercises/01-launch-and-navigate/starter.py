"""Exercise 1: Launch & Navigate

Fill in the TODOs below. Run with: python starter.py
"""
import os
from playwright.sync_api import sync_playwright

SCREENSHOT_PATH = os.path.join(os.path.dirname(__file__), "publications.png")


def main() -> None:
    with sync_playwright() as p:
        # TODO 1: launch Edge (channel="msedge", headless=False)
        browser = None

        # TODO 2: open a new page
        page = None

        # TODO 3: go to https://www.mas.gov.sg and print page.title()

        # TODO 4: go to https://www.mas.gov.sg/publications

        # TODO 5: print the new page title and page.url

        # TODO 6: save a screenshot to SCREENSHOT_PATH
        #   hint: page.screenshot(path=SCREENSHOT_PATH)

        # TODO 7: close the browser


if __name__ == "__main__":
    main()
