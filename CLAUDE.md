# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

This repo is a **Playwright workshop for business users** (non-developers): Python + Playwright, driving **Microsoft Edge** (`channel="msedge"`). It is a short (~1.5-2h), hands-on, 3-exercise workshop ending in a capstone that downloads PDFs from https://www.mas.gov.sg/publications.

## Setup & running

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install msedge
python check_setup.py
```

Run any exercise's solution directly, e.g.:
```powershell
python exercises\01-launch-and-navigate\solution.py
```

## Structure

- `check_setup.py` — pre-workshop smoke test (launch Edge, navigate, print title).
- `exercises/NN-name/` — one folder per exercise:
  - `README.md` — goal, concepts, step-by-step instructions, "done when" criteria.
  - `starter.py` — skeleton with `TODO`s for attendees to fill in.
  - `solution.py` — complete reference implementation.
- `downloads/` — output folder for exercise 3's PDFs (gitignored, created at runtime).

Exercises are self-contained on purpose (no shared helper module) — each script should be readable top-to-bottom on its own.

## Conventions

- Sync API only (`from playwright.sync_api import sync_playwright`), `headless=False` everywhere so the browser is visible during the workshop.
- No automated test suite — verification is "run `solution.py`, observe the described output/behavior" (see each exercise's README "Done when" section).
- Exercise 3 (MAS capstone) is intentionally scoped to the single publications listing page (no pagination) and must degrade gracefully (print + skip) if expected links aren't found, since it depends on a live external site.
- Exercise 3's solution intercepts `.pdf` responses with `context.route()` to force `Content-Disposition: attachment` (MAS serves PDFs inline via `target="_blank"`, which Edge would otherwise open in its built-in viewer instead of downloading). It also relies on `headless=False` — MAS appears to serve a different page to headless browsers. Preserve both when touching exercise 3.
