# Playwright 101 Workshop

A short, hands-on introduction to browser automation with
[Playwright](https://playwright.dev/python/) (Python) using Microsoft
Edge — for business users with little or no coding background.

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

1. `exercises/01-launch-and-navigate/` — launch a browser, navigate,
   read page info, take a screenshot.
2. `exercises/02-locate-and-interact/` — find elements, fill a form,
   click, and read the result.
3. `exercises/03-mas-pdf-downloader/` — capstone: download PDFs from
   the MAS publications page.

For each exercise: open `starter.py`, fill in the `TODO`s, and run it
with `python starter.py`. If you get stuck, `solution.py` has the
complete answer.

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
- **Downloads blocked by a corporate proxy/firewall** — try running the
  workshop on a network that allows downloads from `mas.gov.sg`.
