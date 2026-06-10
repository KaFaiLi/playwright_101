# Playwright 101 Workshop

A short, hands-on introduction to browser automation with
[Playwright](https://playwright.dev/python/) (Python) using Microsoft
Edge — for business users with little or no coding background.

## What is Playwright?
[Playwright](https://playwright.dev/python/) is a free, open-source tool
(originally built by Microsoft) for **controlling a real web browser with
code**. Instead of clicking and typing by hand, you write a short script
that drives the browser for you — opening pages, filling forms, clicking
buttons, and reading what's on screen, exactly as a person would.

It runs real browsers (Chromium/Edge, Chrome, Firefox, and WebKit/Safari)
and works from Python, JavaScript, Java, or .NET. In this workshop we use
**Python** driving **Microsoft Edge**.

### What can it do?
- **Automate repetitive web tasks** — log in, navigate, and pull the same
  report off a website every day without doing it by hand.
- **Download files in bulk** — e.g. grab every PDF from a publications
  page (that's the capstone of this workshop).
- **Fill in and submit forms** — type into fields, tick boxes, pick from
  dropdowns, and click submit.
- **Scrape / extract information** — read text, tables, and links off a
  page and save them somewhere useful.
- **Take screenshots and PDFs** — capture what a page looks like for
  records or reporting.
- **Test websites** — its original purpose: check that a web app still
  works after changes (you won't need this, but it's why the tool is so
  reliable at the above).

### Why it's nice for non-developers
- **You watch it work.** We run with the browser visible
  (`headless=False`), so you see Edge open and click in real time.
- **It waits for you.** Playwright automatically waits for pages and
  elements to be ready before acting, so scripts are far less flaky than
  older automation tools.
- **Readable code.** A script reads top-to-bottom like a list of steps:
  go here, click this, type that, download.
- **You don't even have to write it.** `playwright codegen` records you
  clicking around and writes the script for you (exercise 5).

### How a Playwright script works
Every script in this workshop follows the same five-beat shape. Once you
recognise it, all the exercises read the same way:

1. **Start Playwright** — `with sync_playwright() as p:` opens the engine.
2. **Launch a browser** — `p.chromium.launch(channel="msedge",
   headless=False)` opens Edge.
3. **Open a page (tab)** — `browser.new_page()` / `context.new_page()`.
4. **Drive it** — `goto`, `click`, `fill`, `screenshot`, download… the
   actual work, one line per step.
5. **Close up** — `browser.close()` tidies everything away.

We use the **sync API** (`from playwright.sync_api import
sync_playwright`) throughout — it runs your steps one after another, in
order, which is the easiest mental model when you're starting out.

### Key words you'll see
| Term | Plain-English meaning |
|------|----------------------|
| **Browser** | The Edge program Playwright launches and controls. |
| **Page** | A single browser tab you navigate and act on. |
| **Context** | An isolated browser session (its own cookies/downloads); used in exercises 3-4 to tweak how downloads behave. |
| **Locator** | A "pointer" to an element on the page (a link, a box, a button), e.g. `page.locator("a[href$='.pdf']")`. |
| **Selector** | The text pattern inside a locator that describes *which* element you mean (CSS like `a[href$='.pdf']`, or a role like "the search box"). |
| **Headless** | Running the browser invisibly. We keep it **off** (`headless=False`) so you can see it. |
| **codegen** | Playwright's recorder: click by hand, get Python code out. |

## Prerequisites
- Python 3.9+
- Microsoft Edge installed
- A terminal (PowerShell) and a text editor (VS Code recommended)

## Setup
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install msedge
```

## 1. Check your setup
Before the workshop starts, run:
```powershell
python check_setup.py
```
A Microsoft Edge window should briefly open, visit a webpage, print its
title, and close. If this works, you're ready.

## 2. Workshop flow
Work through these folders in order. Each has its own `README.md` with
instructions:

1. **`exercises/01-launch-and-navigate/`** — the basics: launch Edge,
   go to a page, read its title/URL, take a screenshot, close. Start
   here even if it feels too simple — every later exercise reuses this
   shape.
2. **`exercises/02-locate-and-interact/`** — *locators*: find a specific
   element on a page, fill a form field, click a button, and read the
   result back. This is where you learn to point at things.
3. **`exercises/03-mas-pdf-downloader/`** — capstone: download PDFs from
   the live MAS publications page. Combines navigation + locators +
   file downloads, and shows how real sites misbehave (PDFs that open
   instead of download) and how to handle it gracefully.
4. **`exercises/04-mas-pdf-two-pages/`** — bonus: download PDFs across
   the **first two pages** of the listing (adds *pagination* — looping
   over more than one page of results).
5. **`exercises/05-codegen-recorder/`** — flip it around: instead of
   writing code, **record** yourself clicking with `playwright codegen`
   and let Playwright write the Python for you. The fastest way to get a
   working script.

Each exercise folder contains:
- **`README.md`** — the goal, the concepts, step-by-step instructions,
  and a "Done when" checklist so you know you've succeeded.
- **`starter.py`** — a skeleton with `TODO` comments for you to fill in.
- **`solution.py`** — the complete, working reference answer.

For each exercise: open `starter.py`, fill in the `TODO`s, and run it
with `python starter.py`. If you get stuck, `solution.py` has the
complete answer — it's fine to peek. (Exercise 5 has no `starter.py`:
you record your own script live, with `example_generated.py` as a sample
of what the recorder produces.)

## Troubleshooting
- **"Executable doesn't exist" / browser not found** — run
  `playwright install msedge` again.
- **No Edge window appears** — make sure the script uses
  `headless=False` in `launch()`.
- **Exercise 3 finds 0 PDFs on the listing page** — this is expected!
  The MAS publications page itself has no direct PDF links; the
  solution follows links to individual publication pages and downloads
  PDFs from there instead. If **both** the listing page *and* the
  publication pages return 0 PDFs, check that `headless=False` hasn't
  been changed to `True` (MAS appears to serve a different page to
  headless browsers) — otherwise the MAS site layout may have changed
  since this workshop was written. The script will print a message and
  exit cleanly rather than crash; see that exercise's `README.md` for
  notes on the page structure at the time of writing.
- **Exercise 4 page 2 finds the same links as page 1 (or nothing)** —
  MAS is assumed to paginate with `?page=N`. If that's no longer true,
  the live site may use a "Load more" button or infinite scroll instead;
  update `listing_url()` in that exercise's `solution.py`. See its
  `README.md`.
- **`playwright codegen` does nothing / wrong browser** — make sure you
  pass `--channel=msedge` (and `--target python` for Python output). If
  the command isn't found, your virtual environment isn't activated —
  run `.venv\Scripts\Activate.ps1` first.
- **Downloads blocked by a corporate proxy/firewall** — try running the
  workshop on a network that allows downloads from `mas.gov.sg`.
