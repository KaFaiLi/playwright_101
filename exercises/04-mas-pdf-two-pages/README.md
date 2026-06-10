# Exercise 4: MAS PDF Downloader - First Two Pages (Bonus)

## Goal
Extend exercise 3: instead of just the first listing page, download the
PDFs from publications across the **first two pages** of the MAS
publications listing. This adds **pagination** - walking more than one
page of results.

## What you'll learn
- Building paginated URLs with a `?page=` query parameter
- Looping over several listing pages and collecting links from each
- Deduplicating links so the same publication isn't downloaded twice
- Reusing helpers (`download_pdf`, `entry_links_on_page`) across exercises

## Background (read exercise 3 first)
This builds directly on exercise 3, so its quirks still apply:
- The MAS listing page has **no direct `.pdf` links**. PDFs live on the
  individual publication pages (`/publications/<category>/<year>/<slug>`
  - 3+ path segments), so we follow those links.
- MAS serves PDFs **inline** (Edge opens them in its viewer) rather than
  as downloads, so we intercept `.pdf` responses with `context.route()`
  and add a `Content-Disposition: attachment` header.
- `headless=False` is required - MAS serves a different page to headless
  browsers.

## Instructions
Open `starter.py` and fill in the TODOs:
1. Loop `page_number` from 1 to `NUM_PAGES` (2). For each page:
   - `page.goto(listing_url(page_number))`
   - get entry links with `entry_links_on_page(page)`, keep the first
     `MAX_ENTRIES_PER_PAGE`
   - add them to one combined list, skipping duplicates.
2. Loop over the combined list. For each entry:
   - build the full `detail_url`
   - `page.goto(detail_url)`
   - find `.pdf` links and download each with `download_pdf()`.

Run with:
```
python starter.py
```

## Done when
Edge opens, walks the first two listing pages, prints how many
publication links it found on each, visits each publication page, and
downloads the PDFs into `downloads/` (one line per file), ending with a
`Done. Downloaded N PDF(s)...` summary.

## Notes & gotchas
- **Pagination scheme.** MAS paginates with `?page=N`. If both pages
  return the same links (or page 2 finds nothing), the site may use a
  different scheme (e.g. a "Load more" button or infinite scroll instead
  of page URLs). Inspect the live pagination control and update
  `listing_url()` to match - that's the only spot to change.
- **Keep it polite / quick.** `MAX_ENTRIES_PER_PAGE` caps how many detail
  pages we visit per listing page so the demo stays fast. Raise it to
  fetch more.
- **Graceful failure.** If no publication links are found on either page,
  the script prints a message and exits cleanly rather than crashing -
  the same "handle the page not looking how you expected" lesson as
  exercise 3.
