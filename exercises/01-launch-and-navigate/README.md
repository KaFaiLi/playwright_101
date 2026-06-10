# Exercise 1: Launch & Navigate

## Goal
Get comfortable launching a browser, navigating between pages, and
reading basic page info.

## What you'll learn
- `p.chromium.launch(channel="msedge", headless=False)` — start Edge
- `browser.new_page()` — open a tab
- `page.goto(url)` — navigate
- `page.title()` / `page.url` — read page info
- `page.screenshot(path=...)` — capture a screenshot
- `browser.close()` — clean up

## Instructions
Open `starter.py` and fill in the TODOs:
1. Launch Edge (visible, not headless).
2. Open a new page and go to `https://www.mas.gov.sg`. Print its title.
3. Navigate to `https://www.mas.gov.sg/publications`. Print its new
   title and current URL.
4. Save a screenshot of the publications page to `publications.png`
   (in this folder).
5. Close the browser.

Run with:
```
python starter.py
```

## Done when
Edge opens, visits the MAS homepage then the publications page,
prints two titles plus a URL, saves `publications.png` next to this
file, and the browser closes. Compare against `solution.py` if stuck.
