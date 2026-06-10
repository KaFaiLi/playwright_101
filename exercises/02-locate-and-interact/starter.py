"""Exercise 2: Locate & Interact

Fill in the TODOs below. Run with: python starter.py
"""
from playwright.sync_api import sync_playwright


def main() -> None:
    with sync_playwright() as p:
        # TODO 1: launch Edge (channel="msedge", headless=False) and open a page
        browser = None
        page = None

        # TODO 2: go to https://the-internet.herokuapp.com/login

        # TODO 3: fill "#username" with "tomsmith"

        # TODO 4: fill "#password" with "SuperSecretPassword!"

        # TODO 5: click the "Login" button
        #   hint: page.get_by_role("button", name="Login").click()

        # TODO 6: read and print the text of "#flash"
        #   hint: page.locator("#flash").text_content()

        # TODO 7: close the browser


if __name__ == "__main__":
    main()
