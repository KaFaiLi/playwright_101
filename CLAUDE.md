# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

This repo is a **Playwright workshop/training project for business users** (non-developers). It has two parts:

1. **Intro/demo material** — short scripts and a workshop walkthrough showing what Playwright is and what it can do (launching a browser, navigating, clicking, extracting data, etc.), aimed at an audience with little to no coding background.
2. **A practical automation**: crawl https://www.mas.gov.sg/publications, follow the publication links, and download every PDF found into a local folder.

The repo also needs **end-user documentation** (a step-by-step guide) explaining how to set up the environment and run the scripts, written for business users rather than engineers.

The repo is currently empty/bootstrap — this file describes the intended stack and conventions to follow as the project is built out.

## Tech stack

- **Python** with the **Playwright** library (`pip install playwright`).
- **Browser: Microsoft Edge**, via Playwright's `msedge` channel (not the bundled Chromium) — workshop attendees already have Edge installed, and using their familiar browser makes the demo more relatable.
  - Launch example: `browser = playwright.chromium.launch(channel="msedge", headless=False)`
  - Use `headless=False` for workshop/demo scripts so the audience can see the browser driving itself. The PDF-download automation can run headless once it's past the demo stage.

## Environment setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install playwright
playwright install msedge
```

## MAS publications PDF downloader — key requirements

- Entry point: https://www.mas.gov.sg/publications
- Walk the publication listing (including pagination if present), open each publication page, and locate PDF links.
- Download PDFs to a local output folder (e.g. `downloads/`), preserving useful naming (publication title/date) so business users can find files easily.
- Be a polite scraper: add delays between requests/page loads, avoid excessive parallelism, and don't hammer the MAS site.
- Since this targets a real external government site, verify selectors against the live page structure as it may change — don't assume a fixed DOM layout without checking.

## Documentation

Any user-facing guide should be written for non-technical business users: step-by-step, including environment setup, how to run each script, and what output to expect (e.g. where downloaded PDFs land).
