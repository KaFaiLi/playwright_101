"""Exercise 5: example of codegen output (lightly cleaned up)

This is roughly what `playwright codegen --channel=msedge --target python
https://www.mas.gov.sg/publications` produces after you search for
"green finance" and open a result. Yours will differ depending on what
you click - that's the point.

Two hand-edits were made to the raw recording (see README "Cleaning up"):
  1. headless=False so you can watch the replay.
  2. a wait_for_timeout before closing so the window doesn't vanish.

Run with: python example_generated.py
"""
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(channel="msedge", headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.mas.gov.sg/publications")
    page.get_by_role("textbox", name="Search input").click()
    page.get_by_role("textbox", name="Search input").click()
    page.get_by_role("textbox", name="Search input").fill("green finance")
    page.get_by_role("textbox", name="Search input").press("Enter")
    page.locator("#masx-search-header").get_by_role("button", name="Search").click()
    page.get_by_role("link", name="Consultation Paper on Guidelines on Transition Planning for Insurers").click()
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="MAS Response to Feedback").click()
    page1 = page1_info.value
    page2 = context.new_page()
    page2.goto("edge://downloads-hub/")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
