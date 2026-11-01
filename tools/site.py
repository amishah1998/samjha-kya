"""Rebuild the example decks into docs/ (served by GitHub Pages) and write the gallery page.

    uv run --with playwright python tools/site.py

For every examples/<name>/deck.py: builds docs/<slug>.html, takes a phone and a laptop screenshot
of its cover and one story card into docs/media/, and lists it on docs/index.html.
"""
import pathlib
import sys
from html import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "skills" / "samjha-kya" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import build  # noqa: E402

DOCS = ROOT / "docs"
MEDIA = DOCS / "media"
SITE = "https://amishah1998.github.io/samjha-kya/"
REPO = "https://github.com/amishah1998/samjha-kya"
ORDER = ["procrastination", "money", "sleep-pdf"]


def shots(decks):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        for d in decks:
            for kind, vp, mobile in (("phone", (390, 844), True), ("laptop", (1440, 900), False)):
                ctx = b.new_context(viewport=dict(width=vp[0], height=vp[1]), device_scale_factor=2, is_mobile=mobile, has_touch=mobile)
                pg = ctx.new_page()
                pg.goto(d["html"].as_uri())
                pg.wait_for_timeout(400)
                pg.screenshot(path=str(MEDIA / f"{d['slug']}-{kind}.png"))
                pg.evaluate(f"window.scrollTo(0, document.getElementById('{d['card']}').offsetTop)")
                pg.wait_for_timeout(150)
                pg.screenshot(path=str(MEDIA / f"{d['slug']}-{kind}-card.png"))
                ctx.close()
        og = DOCS / "media" / "og.html"
        from art import chintu, pinky, sharma, svg
        cast = svg(chintu(80, 150, 1.0, mood="grin", arms="wave") + sharma(170, 150, 1.0, "flat", "skeptic") + pinky(250, 150, 1.0, "grin", arms="up"), "The cast")
        og.write_text(f'''<!doctype html><meta charset="utf-8"><style>body{{margin:0;width:1280px;height:640px;background:#f6f3ee;display:flex;align-items:center;
font-family:-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif;color:#1c1b19}}.a{{width:560px;margin:0 30px 0 50px}}h1{{font-size:84px;margin:0 0 14px;letter-spacing:-2px}}
p{{font-size:32px;line-height:1.25;color:#6d675f;margin:0 0 18px;font-weight:600}}code{{font:700 26px "SF Mono",Menlo,monospace;background:#1c1b19;color:#f6f3ee;padding:10px 16px;border-radius:12px}}</style>
<div class="a">{cast}</div><div><h1>Samjha kya?</h1><p>Any topic or PDF, as a desi comic flashcard deck.</p><code>/samjha-kya</code></div>''', encoding="utf-8")
        pg = b.new_page(viewport=dict(width=1280, height=640))
        pg.goto(og.as_uri())
        pg.screenshot(path=str(MEDIA / "og.png"))
        og.unlink()
        b.close()


def main():
    MEDIA.mkdir(parents=True, exist_ok=True)
    decks = []
    names = sorted(p.parent.name for p in (ROOT / "examples").glob("*/deck.py"))
    for name in sorted(names, key=lambda n: ORDER.index(n) if n in ORDER else 99):
        deck = build.load(ROOT / "examples" / name / "deck.py")
        deck.site = SITE + f"{deck.slug}.html"
        out, n = build.render(deck, DOCS / f"{deck.slug}.html")
        warn = build.lint(deck)
        first_story = next((f"c{ch.n}-{j + 2}" for kind in ("chat", "scene") for ch in deck.chapters
                            for j, c in enumerate(ch.cards) if c["kind"] == kind), "c1-2")
        decks.append(dict(slug=deck.slug, title=deck.title, tagline=deck.tagline, html=out, cards=n,
                          chapters=len(deck.chapters), pdf=bool(deck.source), card=first_story))
        print(f"{name}: {out.name} {n} cards, {len(warn)} warnings")
    shots(decks)
    items = "".join(
        f'<a class="deck" href="{d["slug"]}.html"><img src="media/{d["slug"]}-phone-card.png" alt="A card from {escape(d["title"])}" loading="lazy">'
        f'<div><span class="tag">{"From a PDF" if d["pdf"] else "Any topic"}</span><h2>{d["title"]}</h2><p>{d["tagline"]}</p>'
        f'<p class="n">{d["chapters"]} chapters, {d["cards"]} cards, 3 levels</p></div></a>' for d in decks)
    (DOCS / "index.html").write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>samjha-kya: any topic or PDF as comic flashcards</title>
<meta name="description" content="An Agent Skill that turns any topic or PDF into a swipeable comic flashcard deck with a desi cast, in beginner, intermediate and advanced levels.">
<meta property="og:title" content="samjha-kya"><meta property="og:description" content="Any topic or PDF, as a desi comic flashcard deck.">
<meta property="og:image" content="{SITE}media/og.png"><meta property="og:image:width" content="1280"><meta property="og:image:height" content="640"><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="{build.ICON}">
<style>
:root{{--bg:#f6f3ee;--ink:#1c1b19;--muted:#6d675f;--card:#fffdf9;--line:#e6e0d6;--accent:#0f5f6b}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:17px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}}
main{{max-width:1080px;margin:0 auto;padding:40px 16px 60px}}
h1{{font-size:clamp(34px,6vw,56px);line-height:1.05;margin:0 0 12px;letter-spacing:-1px}}
.lead{{font-size:clamp(18px,2.4vw,22px);color:var(--muted);margin:0 0 22px;max-width:46ch}}
pre{{background:var(--ink);color:#f6f3ee;border-radius:14px;padding:14px 18px;font:15px/1.5 "SF Mono",ui-monospace,Menlo,monospace;overflow-x:auto;margin:0 0 10px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:18px;margin:30px 0}}
.deck{{display:block;text-decoration:none;color:inherit;background:var(--card);border:1px solid var(--line);border-radius:20px;overflow:hidden;box-shadow:0 6px 24px rgba(0,0,0,.06)}}
.deck img{{width:100%;display:block;aspect-ratio:390/600;object-fit:cover;object-position:center 18%;border-bottom:1px solid var(--line)}}
.deck div{{padding:14px 18px 18px}}.deck h2{{font-size:21px;margin:6px 0}}.deck p{{margin:0 0 6px;color:var(--muted)}}
.deck .n{{font-size:14px;font-weight:600;color:var(--accent)}}
.tag{{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;background:var(--ink);color:#fff;border-radius:999px;padding:3px 9px}}
.wide{{width:100%;border-radius:16px;border:1px solid var(--line);display:block}}
a{{color:var(--accent)}}.small{{font-size:14px;color:var(--muted)}}
</style></head><body><main>
<h1>Samjha kya?</h1>
<p class="lead">An Agent Skill that turns any topic or PDF into a swipeable comic flashcard deck. Three levels, a desi cast, lots of examples. Works on phones and laptops.</p>
<pre>npx skills add amishah1998/samjha-kya</pre>
<p class="small">Then ask your coding agent: <b>/samjha-kya why we procrastinate</b>, or <b>turn guide.pdf into a samjha-kya deck</b>. <a href="{REPO}">Source and docs on GitHub</a>.</p>
<div class="grid">{items}</div>
<p class="small">Each example was written by an AI agent following the skill, fact-checked by separate reviewer agents, and checked on 18 screen sizes. By Ami Shah. Free and open source (MIT).</p>
</main></body></html>""", encoding="utf-8")
    print("wrote", DOCS / "index.html")


if __name__ == "__main__":
    main()
