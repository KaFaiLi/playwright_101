# Exercise 2: Locate & Interact

## Goal
Find elements on a page, fill in a form, click a button, and read the
result.

## What you'll learn
- `page.locator(selector)` / `page.get_by_role(...)` — find elements
- `.fill(text)` — type into a field
- `.click()` — click a button
- `.text_content()` — read text from an element
- Playwright auto-waits for elements to be ready

## Instructions
This exercise uses https://the-internet.herokuapp.com/login, a public
demo site for practicing automation. The login page itself displays the
test credentials.

Open `starter.py` and fill in the TODOs:
1. Launch Edge and go to `https://the-internet.herokuapp.com/login`.
2. Locate the username field (`#username`) and fill in `tomsmith`.
3. Locate the password field (`#password`) and fill in
   `SuperSecretPassword!`.
4. Click the "Login" button.
5. Locate the result message (`#flash`) and print its text.
6. Close the browser.

Run with:
```
python starter.py
```

## Done when
Edge opens, fills in and submits the login form, and prints a message
containing "You logged into a secure area!". Compare against
`solution.py` if stuck.
