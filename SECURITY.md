# Security

samjha-kya runs only on your machine: Python scripts that write an HTML file, plus an optional headless browser for the layout check. Decks are static pages with no network calls.

One script talks to GitHub. After a finished deck, `star_ask.py` runs once per machine: if the GitHub CLI (`gh`) is signed in, it asks GitHub whether your account already starred this repo. It never stars anything by itself; your agent stars the repo only after you say yes. It keeps one small file in `~/.local/state/samjha-kya/` so it never asks twice.

If you find a security problem, please open an issue titled "Security" with no exploit details, and the maintainer will reply there to arrange a private channel.
