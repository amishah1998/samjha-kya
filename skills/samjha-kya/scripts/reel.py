"""Turn a built deck into a vertical video reel (Instagram, WhatsApp Status, Shorts): real frames of
the real deck, scrolled card by card, with an optional title card at the start and end.

    uv run --with playwright python reel.py deck.html                       # cover + first cards
    uv run --with playwright python reel.py deck.html --cards toc c1-2 c1-4 c1-11 --out reel.mp4
    uv run --with playwright python reel.py --plan plan.json                # several decks, captions, laptop shots

Needs ffmpeg. Every deck frame is a screenshot of the deck running in Chromium; title cards are
plain text on the deck's paper colour, so nothing in the video pretends to be something else.

plan.json:
{"out": "launch.mp4", "gif": "launch.gif",
 "segments": [
   {"type": "title", "lines": ["Any topic.", "Any PDF."], "sub": "Comic flashcards", "seconds": 2.2},
   {"type": "deck", "html": "money.html", "caption": "Topic: money", "layout": "phone",
    "cards": [{"id": "toc", "hold": 1.6}, {"id": "c1-3", "hold": 2.4, "tap": true}]},
   {"type": "deck", "html": "sleep.html", "caption": "Works on a laptop too", "layout": "laptop", "cards": [...]}
 ]}
"tap": true opens the card's Answer button before holding. Consecutive cards scroll; others cut.
"""
import argparse
import functools
import http.server
import json
import math
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import threading
from html import escape

FPS = 30
PHONE = (432, 768)
LAPTOP = (1440, 900)

STAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;width:%(W)dpx;height:%(H)dpx;overflow:hidden;background:#f6f3ee;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:#1c1b19}
.view{position:absolute;left:0;top:0;transform-origin:0 0}
.view iframe{border:0;display:block;background:#f6f3ee}
.view.framed iframe{border-radius:28px;box-shadow:0 0 0 3px #1c1b19,0 18px 50px rgba(0,0,0,.18)}
.tag{position:absolute;font-weight:700;font-size:26px;color:#6d675f;transform:translateX(-50%%)}
#cap{position:absolute;left:50%%;transform:translateX(-50%%);top:34px;background:#1c1b19;color:#fff;font-weight:800;font-size:40px;padding:16px 34px;border-radius:999px;white-space:nowrap;z-index:3}
#cap:empty{display:none}
#title{position:absolute;inset:0;display:none;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:60px;background:#f6f3ee;z-index:5}
#title h1{font-size:10.4vmin;line-height:1.05;margin:0 0 3vmin;letter-spacing:-2px}
#title p{font-size:4.2vmin;line-height:1.3;margin:0 0 1.8vmin;color:#6d675f;font-weight:600}
#title code{font:700 min(4vmin,calc(88vw / var(--n,30) / .6))/1.3 "SF Mono",ui-monospace,Menlo,monospace;white-space:nowrap;background:#1c1b19;color:#f6f3ee;padding:1.3vmin 2.4vmin;border-radius:18px;display:inline-block;margin-top:1.8vmin}
#title .art{width:66vmin;margin-bottom:3vmin}
</style></head><body><div id="views"></div><div id="cap"></div><div id="title"></div></body></html>"""


def layout(kind, W, H):
    """Views for a deck segment: (css width, css height, x, y, scale, framed, label)."""
    if kind == "duo":
        ps = (H - 230) / 844
        pw = 390 * ps
        ls = (W - pw - 160) / 1440
        lx = 60 + pw + 60
        ly = (H - 900 * ls) / 2 + 30
        return [(390, 844, 50, 150, ps, True, "Phone"), (1440, 900, lx, ly, ls, True, "Laptop")]
    if kind == "laptop":
        s = min(W / 1440, (H - 140) / 900)
        return [(1440, 900, (W - 1440 * s) / 2, (H - 900 * s) / 2 + 40, s, False, "")]
    s = W / PHONE[0]
    return [(PHONE[0], PHONE[0] * H / W, 0, 0, s, False, "")]


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve(root):
    handler = functools.partial(Quiet, directory=str(root))
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def title_html(seg):
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from art import chintu, pinky, sharma, svg
    art = ""
    if seg.get("cast", True):
        art = ('<div class="art">' + svg(chintu(80, 150, 1.0, mood="grin", arms="wave") + sharma(170, 150, 1.0, "flat", "skeptic")
                                         + pinky(250, 150, 1.0, "grin", arms="up"), "The cast") + "</div>")
    h = "".join(f"{escape(l)}<br>" for l in seg.get("lines", []))
    sub = "".join(f"<p>{escape(s)}</p>" for s in ([seg["sub"]] if isinstance(seg.get("sub"), str) else seg.get("sub", [])))
    code = f'<code style="--n:{len(seg["code"])}">{escape(seg["code"])}</code>' if seg.get("code") else ""
    return f"{art}<h1>{h}</h1>{sub}{code}"


class Recorder:
    def __init__(self, page, frames):
        self.page, self.frames, self.n, self.last = page, frames, 0, None

    def shot(self):
        p = self.frames / f"{self.n:05d}.png"
        self.page.screenshot(path=str(p))
        self.last, self.n = p, self.n + 1

    def hold(self, seconds):
        if self.last is None:
            self.shot()
        assert self.last is not None
        for _ in range(max(1, round(seconds * FPS)) - 1):
            p = self.frames / f"{self.n:05d}.png"
            os.link(self.last, p)
            self.n += 1


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * t)


def run_plan(plan, base):
    from playwright.sync_api import sync_playwright
    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg is required (brew install ffmpeg / apt install ffmpeg)")
    out = (base / plan.get("out", "reel.mp4")).resolve()
    W, H = plan.get("size", (1080, 1920))
    work = pathlib.Path(tempfile.mkdtemp(prefix="reel-"))
    frames = work / "frames"
    frames.mkdir()
    (work / "stage.html").write_text(STAGE % dict(W=W, H=H), encoding="utf-8")
    decks = {}
    for seg in plan["segments"]:
        if seg["type"] == "deck" and seg["html"] not in decks:
            name = f"d{len(decks)}.html"
            shutil.copy((base / seg["html"]).resolve(), work / name)
            decks[seg["html"]] = name
    httpd = serve(work)
    url = f"http://127.0.0.1:{httpd.server_address[1]}"
    js_views = """([src, views, cap]) => Promise.all((() => {
        document.getElementById('title').style.display='none';
        document.getElementById('cap').textContent=cap||'';
        const box=document.getElementById('views'); box.innerHTML='';
        return views.map(([vw, vh, x, y, s, framed, label], i) => new Promise(res => {
          const v=document.createElement('div'); v.className='view'+(framed?' framed':'');
          v.style.transform=`translate(${x}px, ${y}px) scale(${s})`;
          const f=document.createElement('iframe'); f.id='f'+i; f.style.width=vw+'px'; f.style.height=vh+'px';
          v.appendChild(f); box.appendChild(v);
          if(label){const t=document.createElement('div');t.className='tag';t.textContent=label;t.style.left=(x+vw*s/2)+'px';t.style.top=(y+vh*s+14)+'px';box.appendChild(t)}
          f.onload=()=>{const d=f.contentDocument; try{f.contentWindow.localStorage.clear()}catch(e){}
            const st=d.createElement('style');st.textContent='html{scroll-snap-type:none!important;scroll-behavior:auto!important}#back,.hint{display:none!important}';
            d.head.appendChild(st); setTimeout(res,600)};
          f.src=src;}));
      })())"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport=dict(width=W, height=H))
        page.goto(f"{url}/stage.html")
        rec = Recorder(page, frames)
        for seg in plan["segments"]:
            if seg["type"] == "title":
                page.evaluate("h => {const t=document.getElementById('title');t.innerHTML=h;t.style.display='flex'}", title_html(seg))
                page.wait_for_timeout(150)
                rec.last = None
                rec.shot()
                rec.hold(seg.get("seconds", 2.0))
                continue
            views = layout(seg.get("layout", "phone"), W, H)
            page.evaluate(js_views, [f"{url}/{decks[seg['html']]}", views, seg.get("caption", "")])
            nv = len(views)
            ids = page.evaluate("[...document.getElementById('f0').contentDocument.querySelectorAll('.card')].map(c=>c.id)")
            pos = [page.evaluate(f"[...document.getElementById('f{i}').contentDocument.querySelectorAll('.card')].map(c=>c.offsetTop)") for i in range(nv)]
            scroll = "([i, y]) => document.getElementById('f'+i).contentWindow.scrollTo(0, y)"
            cur = None
            for c in seg["cards"]:
                if c["id"] not in ids:
                    raise SystemExit(f"{seg['html']}: no card with id {c['id']!r}")
                k = ids.index(c["id"])
                if cur is not None and k == cur + 1:
                    steps = round(seg.get("scroll", 0.5) * FPS)
                    for s in range(1, steps + 1):
                        for i in range(nv):
                            page.evaluate(scroll, [i, pos[i][cur] + (pos[i][k] - pos[i][cur]) * ease(s / steps)])
                        rec.shot()
                else:
                    for i in range(nv):
                        page.evaluate(scroll, [i, pos[i][k]])
                    page.wait_for_timeout(80)
                    rec.shot()
                cur = k
                if c.get("tap"):
                    rec.hold(c.get("before_tap", 1.2))
                    for i in range(nv):
                        page.evaluate("([i, id]) => {const s=document.getElementById('f'+i).contentDocument.querySelector('#'+id+' details');if(s)s.open=true}", [i, c["id"]])
                    page.wait_for_timeout(80)
                    rec.shot()
                rec.hold(c.get("hold", 2.2))
        browser.close()
    httpd.shutdown()
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(frames / "%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "slow", "-movflags", "+faststart", str(out)], check=True)
    print(f"video: {out} ({rec.n / FPS:.1f} s, {rec.n} frames)")
    if plan.get("gif"):
        gif = (base / plan["gif"]).resolve()
        gw = plan.get("gif_width", 360)
        vf = f"fps=12,scale={gw}:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse=dither=bayer:bayer_scale=4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(out), "-vf", vf, str(gif)], check=True)
        print(f"gif: {gif} ({gif.stat().st_size / 1e6:.1f} MB)")
    shutil.rmtree(work, ignore_errors=True)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html", nargs="?", help="a built deck (single-deck mode)")
    ap.add_argument("--cards", nargs="*", help="card ids in order (default: cover and the first chapter's first six cards)")
    ap.add_argument("--hold", type=float, default=2.4, help="seconds on each card")
    ap.add_argument("--out", default=None)
    ap.add_argument("--plan", help="JSON plan for several decks, captions and title cards")
    a = ap.parse_args()
    if a.plan:
        plan = json.loads(pathlib.Path(a.plan).read_text())
        run_plan(plan, pathlib.Path(a.plan).resolve().parent)
        return
    if not a.html:
        ap.error("give a deck HTML file or --plan")
    html = pathlib.Path(a.html).resolve()
    cards = a.cards or ["toc"] + [f"c1-{i}" for i in range(2, 8)]
    plan = {"out": a.out or str(html.with_suffix(".mp4")),
            "segments": [{"type": "deck", "html": str(html), "cards": [{"id": c, "hold": a.hold} for c in cards]}]}
    run_plan(plan, html.parent)


if __name__ == "__main__":
    sys.exit(main())
