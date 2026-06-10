"""Exercise 2: Locate & Interact - solution"""
from playwright.sync_api import sync_playwright


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=False)
        page = browser.new_page()

        page.goto("https://the-internet.herokuapp.com/login")

        page.locator("#username").fill("tomsmith")
        page.locator("#password").fill("SuperSecretPassword!")
        page.get_by_role("button", name="Login").click()

        flash = page.locator("#flash")
        flash.wait_for()
        print(f"Result: {flash.text_content().strip()}")

        browser.close()


if __name__ == "__main__":
    main()
