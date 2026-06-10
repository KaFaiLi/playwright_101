# Exercise 3: MAS PDF Downloader (Capstone)

## Goal
Combine everything from exercises 1 and 2 to do something genuinely
useful: visit the MAS publications page and download any PDFs you find
there, saving them into the `downloads/` folder at the repo root.

## What you'll learn
- Finding links by their `href` with a CSS attribute selector:
  `a[href$=".pdf" i]` (links ending in `.pdf`, case-insensitive)
- Handling file downloads with `page.expect_download()` and
  `download.save_as(path)`
- Looping over multiple matched elements with `.count()` / `.nth(i)`

## Instructions
Open `starter.py` and fill in the TODOs:
1. Go to `https://www.mas.gov.sg/publications`.
2. Find all links on the page whose `href` ends in `.pdf`
   (`page.locator("a[href$='.pdf' i]")`).
3. Print how many were found.
4. For each one, call the provided `download_pdf()` helper to download
   it into `downloads/`.

Run with:
```
python starter.py
```

## Done when
Edge opens the MAS publications page, prints how many PDF links it
found, and downloads each one into `downloads/` (printing a line per
file). If the page has **no** direct PDF links on this listing, that's
OK for the basic exercise — `0 found` is a valid, working result.

## What we actually found on the live site
As of testing, `https://www.mas.gov.sg/publications` has **0 direct
`.pdf` links** — `0 found` is the real, correct result for the basic
exercise above. Instead, the listing page links to:
- **Category pages** like `/publications/macroeconomic-review` or
  `/publications/consultations` (one path segment after
  `/publications/`) — these are themselves listings with no PDFs.
- **Specific publication pages** like
  `/publications/macroeconomic-review/2026/volume-xxv-issue-2-apr-2026`
  (category/year/slug — three path segments) — **these do have direct
  `.pdf` links**.

`solution.py`'s stretch-goal fallback (below) follows the second kind
of link and successfully downloads PDFs from them.

## Stretch goal
`solution.py` includes an extra fallback: if no direct PDF links are
found on the listing page, it follows publication-entry links
(`/publications/<category>/<year>/<slug>` — filtered to those with at
least 3 path segments, to skip the category index pages which only
have 1) and looks for PDFs on each detail page. On the live site this
fallback finds and downloads several PDFs (e.g. consultation papers and
information papers).

There's one more wrinkle: MAS serves PDFs as inline content (links open
with `target="_blank"` in Edge's built-in PDF viewer) rather than as
downloads, so a plain `link.click()` + `page.expect_download()` would
hang waiting for a download event that never fires. `solution.py` works
around this with `context.route("**/*.pdf", ...)`, which intercepts PDF
responses and adds a `Content-Disposition: attachment` header so Edge
downloads the file instead of opening its viewer. This is a realistic
example of a "the browser doesn't behave the way the docs imply"
problem you'll run into with real sites.

If you run this exercise during the workshop and find that **both**
paths print `0` (or the script prints "No publication links found
either..."), that's a sign the MAS site structure has changed since this
was written. That's OK — it's a realistic example of why automation
scripts need to handle "the page didn't look how I expected" gracefully
instead of crashing. In that case, open the live page, use
`page.locator(...)` experiments (or `page.content()`) to find the new
link pattern, and update the selectors in `solution.py` (and the hints
in `starter.py`) to match.

**Note:** if both paths unexpectedly print `0`, also double-check
`headless=False` hasn't been changed to `True` — MAS appears to serve a
different page to headless browsers, which causes both checks to
silently find nothing.
