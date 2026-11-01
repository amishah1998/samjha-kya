# Put a deck online (free, about two minutes)

The deck is one HTML file with everything inside it, so any static host works.

## GitHub Pages

1. Create a public repository on GitHub, for example `my-decks`.
2. Upload the deck file and rename it `index.html` (or keep its name and link to it).
3. Settings, Pages, "Deploy from a branch", branch `main`, folder `/ (root)`, Save.
4. After a minute it is live at `https://<username>.github.io/my-decks/`.

Several decks: keep each as its own file (`sleep.html`, `money.html`) and add a simple `index.html` that links them.

## Other ways to share

- Send the file itself on WhatsApp or email; it opens in any phone browser.
- Put it in iCloud Drive or Google Drive and share the link; the preview shows the cards.
- Netlify Drop (drag the file onto app.netlify.com/drop) gives a link without an account.

## Before you post a link

- Run `check.py` once more on the final file.
- Pass `site="https://.../"` to `Deck(...)` so link previews on WhatsApp and X show the title.
