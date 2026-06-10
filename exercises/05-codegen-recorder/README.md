# Exercise 5: Record Your Actions with Codegen

## Goal
Let Playwright **write the script for you**. With `playwright codegen` you
click around a real browser by hand, and Playwright records every action
and turns it into working Python code you can copy, run, and tweak. No
typing of selectors required.

This is the fastest way for a non-developer to get a working automation:
**do it once by hand, keep the generated code.**

## What you'll learn
- `playwright codegen` — open a browser that records your clicks/typing
- Reading the generated Python (it's the same `sync_playwright` style as
  the earlier exercises)
- Copying the recording into a script and cleaning it up
- Generating a screenshot or PDF straight from the recorder

## What is codegen?
`codegen` opens two windows:
1. **A browser** (Microsoft Edge here) — you browse normally.
2. **The Playwright Inspector** — a panel that shows the Python code
   building up live as you click, type, and navigate.

Every action you take (go to a page, click a link, fill a box, press a
button) appears as a line of code. When you're done, copy the code out.

## Instructions

### 1. Start the recorder
In your activated terminal, run:
```powershell
playwright codegen --channel=msedge --target python https://www.mas.gov.sg/publications
```
- `--channel=msedge` — record in Edge (same browser the workshop uses).
- `--target python` — generate Python (the default is JavaScript).
- The URL is just a starting page; you can navigate anywhere after.

> No URL? You can also run `playwright codegen --channel=msedge` and type
> the address in the browser yourself.

### 2. Do something worth recording
With both windows open, in the **browser** try:
1. Click into the search box and type `green finance`.
2. Press Enter (or click a search/filter button).
3. Click one of the publication results to open it.

Watch the **Inspector** — each action becomes a line of Python.

### 3. Grab a screenshot from the recorder (optional)
In the Inspector toolbar there's a camera / "screenshot" action. Use it
to add a `page.screenshot(...)` line to your recording without writing
any code.

### 4. Copy the code out
In the Inspector, click **Copy** (copies all generated code). Paste it
into `my_recording.py` in this folder. It will look something like
`example_generated.py` next to this README.

### 5. Run your recording
```powershell
python my_recording.py
```
It replays exactly what you did by hand.

## Cleaning up the recording (good habits)
**Codegen records *everything* you do — including mistakes.** Look at
`example_generated.py` in this folder: it's a raw, unedited recording,
and you can see the noise:
- a line that clicks the search box **twice** (an accidental double
  click) — one of them can be deleted;
- a stray `page2.goto("edge://downloads-hub/")` at the end, because the
  recorder happened to open Edge's downloads page — delete it, it's not
  part of the task;
- `with page.expect_popup() as page1_info:` — Playwright noticed a link
  opened a **new tab** and recorded the popup for you.

So the workflow is: **record loosely, then trim.** Typical clean-ups:
- Delete duplicate / accidental actions and any stray navigation.
- Make the replay watchable: keep `headless=False` in `launch()` (codegen
  already emits this) and optionally add `page.wait_for_timeout(2000)`
  before `context.close()` so the window doesn't vanish instantly.
- Rename or comment lines so the script reads like the task
  ("# open the consultation paper").

A recording is a **starting point**, not the finished script — the real
skill (which exercises 1-4 gave you) is reading and tidying what it
produced.

## Done when
You ran `playwright codegen`, performed a few actions in Edge, saw the
Python build up in the Inspector, copied it into `my_recording.py`, and
running that file replays your actions.

## Why this matters
Recording is the bridge from "I do this by hand every week" to "a script
does it for me." Record the manual steps once, then reuse and schedule
the generated script. Exercises 1-4 taught you to *read and edit* that
code — codegen is how you *get* it in the first place.
