"""Check a built deck on real phone, tablet and laptop screens, card by card.

    uv run --with playwright python check.py deck.html [--shots DIR]
    (or: pip install playwright && playwright install chromium && python check.py deck.html)

Runs nine screens: three phones, a phone held sideways, a tablet both ways, three laptop sizes.
Fails (exit 1) when a card does not fit the screen, the page scrolls sideways, a drawing is
letterboxed, text spills out of a drawing, bubbles or labels overlap, or speech-bubble text is wider
than its bubble. --shots saves one screenshot per card plus readable contact sheets (8 or 6 cards each) for the
phone, phone sideways, tablet and laptop screens, so you can look at every card.
"""
import argparse
import json
import pathlib
import sys

SCREENS = [
    dict(name="phone", width=390, height=844, mobile=True),
    dict(name="small-phone", width=360, height=740, mobile=True),
    dict(name="iphone-se", width=375, height=667, mobile=True),
    dict(name="phone-sideways", width=844, height=390, mobile=True),
    dict(name="tablet", width=820, height=1180, mobile=True),
    dict(name="tablet-sideways", width=1180, height=820, mobile=True),
    dict(name="laptop", width=1440, height=900, mobile=False),
    dict(name="small-laptop", width=1280, height=720, mobile=False),
    dict(name="desktop", width=1920, height=1080, mobile=False),
]
SHEETS = ("phone", "phone-sideways", "tablet", "laptop")

PROBE = r"""() => {
  const H = innerHeight, W = innerWidth, out = [];
  const doc = document.documentElement;
  if (doc.scrollWidth > W + 1) out.push({level: 'fail', card: '-', msg: `page scrolls sideways (${doc.scrollWidth}px wide on a ${W}px screen)`});
  const wide = matchMedia('(min-width:900px) and (min-height:560px)').matches;
  for (const p of document.querySelectorAll('.panel')) {
    const s = p.querySelector('svg'); if (!s) continue;
    const a = p.getBoundingClientRect(), b = s.getBoundingClientRect();
    if (a.width - b.width > 4 || a.height - b.height > 4) out.push({level: 'fail', card: p.closest('.card').id, msg: `drawing is letterboxed inside its frame (${Math.round(b.width)}x${Math.round(b.height)} in ${Math.round(a.width)}x${Math.round(a.height)})`});
  }
  for (const c of document.querySelectorAll('.card')) {
    const id = c.id, inn = c.querySelector('.in');
    if (!inn) continue;
    const z = parseFloat(inn.dataset.fit || '1');
    const room = H - parseFloat(getComputedStyle(c).paddingTop) - 22, ih = inn.getBoundingClientRect().height;
    if (ih > room + 1) out.push({level: 'fail', card: id, msg: `card is ${Math.round(ih)}px tall but only ${Math.round(room)}px fit on a ${H}px screen, even at ${Math.round(z * 100)}% size: cut the body text`});
    else if (z < 0.86) out.push({level: 'warn', card: id, msg: `text shrunk to ${Math.round(z * 100)}% to fit: shorten the body`});
    const ib = inn.getBoundingClientRect();
    for (const el of inn.querySelectorAll('table,pre,img,ul,ol,p,h1,h2,.levels')) {
      const r = el.getBoundingClientRect();
      if (r.width && (r.right > ib.right + 2 || el.scrollWidth > el.clientWidth + 2)) out.push({level: 'fail', card: id, msg: `<${el.tagName.toLowerCase()}> is wider than the card`});
    }
    for (const svg of inn.querySelectorAll('.panel svg')) {
      const boxes = [];
      for (const t of svg.querySelectorAll('text')) {
        let b; try { b = t.getBBox(); } catch (e) { continue; }
        if (!b.width) continue;
        const m = t.transform && t.transform.baseVal.length;
        if (!m && !t.closest('g[transform]') && (b.x < -1 || b.y < -1 || b.x + b.width > 321 || b.y + b.height > 171))
          out.push({level: 'fail', card: id, msg: `drawing text "${t.textContent.slice(0, 30)}" spills outside the panel`});
        const px = parseFloat(t.getAttribute('font-size') || '11') * (t.getScreenCTM() ? t.getScreenCTM().a : 1);
        if (px < 7 && innerWidth < 900) out.push({level: 'warn', card: id, msg: `drawing text "${t.textContent.slice(0, 24)}" is only ${px.toFixed(1)}px on this screen; use font size 8 or more`});
        const g = t.closest('g.bub');
        if (g) {
          const w = parseFloat(g.dataset.w);
          if (b.width > w - 4) out.push({level: 'fail', card: id, msg: `bubble text "${t.textContent.slice(0, 30)}" is wider than its bubble (${Math.round(b.width)} > ${w - 4}); shorten it or widen the bubble`});
        }
        if (!t.closest('g[transform]')) boxes.push({b, g, s: t.textContent});
      }
      const groups = [...svg.querySelectorAll('g.bub, g.lbl')].map(g => { try { return {g, b: g.getBBox()}; } catch (e) { return null; } }).filter(Boolean);
      for (let i = 0; i < groups.length; i++) for (let j = i + 1; j < groups.length; j++) {
        const a = groups[i].b, b = groups[j].b;
        if (groups[i].g.contains(groups[j].g) || groups[j].g.contains(groups[i].g)) continue;
        const ox = Math.min(a.x + a.width, b.x + b.width) - Math.max(a.x, b.x), oy = Math.min(a.y + a.height, b.y + b.height) - Math.max(a.y, b.y);
        if (ox > 2 && oy > 2) out.push({level: 'fail', card: id, msg: `two bubbles or labels overlap: "${groups[i].g.textContent.slice(0, 20)}" and "${groups[j].g.textContent.slice(0, 20)}"`});
      }
      const who = [...svg.querySelectorAll('g.who')].map(g => { try { return g.getBBox && g.getBoundingClientRect(); } catch (e) { return null; } }).filter(Boolean);
      const backs = [...svg.querySelectorAll('rect')].filter(x => !x.closest('g.who') && x.getAttribute('fill') && x.getAttribute('fill') !== 'none').map(x => x.getBoundingClientRect());
      for (const t of svg.querySelectorAll('text')) {
        if (t.closest('g.who')) continue;
        const r = t.getBoundingClientRect(); if (!r.width) continue;
        if (backs.some(b => b.width < 300 && b.left <= r.left + 1 && b.right >= r.right - 1 && b.top <= r.top + 1 && b.bottom >= r.bottom - 1)) continue;
        for (const w of who) {
          const ox = Math.min(r.right, w.right) - Math.max(r.left, w.left), oy = Math.min(r.bottom, w.bottom) - Math.max(r.top, w.top);
          if (ox > 4 && oy > 4) { out.push({level: 'warn', card: id, msg: `drawing text "${t.textContent.slice(0, 24)}" runs into a character`}); break; }
        }
      }
      for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
        const A = boxes[i], B = boxes[j];
        if (A.g && A.g === B.g) continue;
        const a = A.b, b = B.b, ox = Math.min(a.x + a.width, b.x + b.width) - Math.max(a.x, b.x), oy = Math.min(a.y + a.height, b.y + b.height) - Math.max(a.y, b.y);
        if (ox > 3 && oy > 3) out.push({level: 'warn', card: id, msg: `drawing texts overlap: "${A.s.slice(0, 20)}" and "${B.s.slice(0, 20)}"`});
      }
    }
  }
  return {wide, cards: document.querySelectorAll('.card').length, issues: out};
}"""


def run(html, shots=None, only=None):
    from playwright.sync_api import sync_playwright
    html = pathlib.Path(html).resolve()
    total_fail, report = 0, {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for s in SCREENS:
            if only and s["name"] not in only:
                continue
            ctx = browser.new_context(viewport=dict(width=s["width"], height=s["height"]), device_scale_factor=2,
                                      is_mobile=s["mobile"], has_touch=s["mobile"])
            page = ctx.new_page()
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.goto(html.as_uri())
            page.evaluate("document.fonts && document.fonts.ready")
            page.wait_for_timeout(400)
            r = page.evaluate(PROBE)
            gen = page.evaluate("(document.querySelector('meta[name=generator]')||{}).content||''")
            sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
            import build as _b
            if gen.split(" ")[-1] != _b.engine_id():
                r["issues"].append(dict(level="fail", card="-", msg="this HTML was built with an older engine; rebuild it with build.py, then check again"))
            r["issues"] += [dict(level="fail", card="-", msg=f"script error: {e}") for e in errors]
            expect_wide = s["width"] >= 900 and s["height"] >= 560
            if expect_wide != r["wide"]:
                r["issues"].append(dict(level="fail", card="-", msg=f"wrong layout: wide={r['wide']} on {s['name']}"))
            fails = [i for i in r["issues"] if i["level"] == "fail"]
            warns = [i for i in r["issues"] if i["level"] == "warn"]
            total_fail += len(fails)
            report[s["name"]] = r
            print(f"{s['name']:13} {s['width']}x{s['height']}  {r['cards']} cards  {len(fails)} fail  {len(warns)} warn")
            seen = set()
            for i in fails + warns:
                key = (i["card"], i["msg"])
                if key in seen:
                    continue
                seen.add(key)
                print(f"   {i['level']:4} {i['card']:8} {i['msg']}")
            if shots and s["name"] in SHEETS:
                d = pathlib.Path(shots).resolve() / s["name"]
                d.mkdir(parents=True, exist_ok=True)
                ids = page.evaluate("[...document.querySelectorAll('.card')].map(c => c.id)")
                for k, cid in enumerate(ids):
                    page.evaluate(f"window.scrollTo(0, document.getElementById('{cid}').offsetTop)")
                    page.wait_for_timeout(60)
                    page.screenshot(path=str(d / f"{k:03d}-{cid}.png"))
                tall = s["height"] > s["width"]
                cols, per = (4, 8) if tall else (2, 6)
                files = sorted(d.glob("[0-9]*.png"))
                for old in d.glob("sheet*.png"):
                    old.unlink()
                for k in range(0, len(files), per):
                    imgs = "".join(f'<figure><img src="{f.name}"><figcaption>{f.stem}</figcaption></figure>' for f in files[k:k + per])
                    sheet = d / "sheet.html"
                    sheet.write_text(f'<!doctype html><style>body{{margin:0;background:#ddd;font:16px sans-serif}}'
                                     f'main{{display:grid;grid-template-columns:repeat({cols},1fr);gap:8px;padding:8px}}'
                                     f'img{{width:100%;display:block;border:1px solid #999}}figure{{margin:0}}</style><main>{imgs}</main>')
                    sp = browser.new_page(viewport=dict(width=1800 if tall else 1600, height=1000))
                    sp.goto(sheet.as_uri())
                    sp.wait_for_timeout(300)
                    sp.screenshot(path=str(d / f"sheet-{k // per + 1}.png"), full_page=True)
                    sp.close()
                sheet.unlink()
                print(f"   screenshots: {d}  (contact sheets: {d}/sheet-1.png to sheet-{-(-len(files) // per)}.png, {per} cards each)")
            ctx.close()
        browser.close()
    return total_fail, report


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html")
    ap.add_argument("--shots", help="folder for per-card screenshots and contact sheets")
    ap.add_argument("--only", nargs="*", help="screen names to run, e.g. phone laptop")
    ap.add_argument("--json", help="write the full report here")
    a = ap.parse_args()
    fails, report = run(a.html, a.shots, a.only)
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(report, indent=1))
    print("PASS" if not fails else f"FAIL: {fails} problems")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
