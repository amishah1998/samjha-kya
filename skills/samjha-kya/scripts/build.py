"""Build a deck file into one self-contained HTML page that works on phones and laptops.

    python3 build.py path/to/deck.py            -> path/to/<slug>.html
    python3 build.py path/to/deck.py -o out.html

The deck file must define `deck = Deck(...)`. Standard library only.
"""
import argparse
import importlib.util
import json
import pathlib
import re
import sys
from html import escape, unescape

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from art import CORAL, CREAM, FACE, HALDI, INK, TEAL, TEAL2, chintu, lines, pinky, sharma, svg, text, wrap  # noqa: E402
from deck import _plain  # noqa: E402

REPO = "https://github.com/amishah1998/samjha-kya"


def engine_id():
    import hashlib
    h = hashlib.sha1()
    for f in ("art.py", "deck.py", "build.py"):
        h.update((HERE / f).read_bytes())
    return h.hexdigest()[:10]

CSS = """
:root{--bg:#f6f3ee;--ink:#1c1b19;--muted:#6d675f;--card:#fffdf9;--line:#e6e0d6;--accent:#0f5f6b;
 --scene:#c8902e;--mine:#e3f0f1;--myth-b:#b23a32;--quiz:#eef0fb;--quiz-b:#4b55b0;
 --red:#fff4f2;--red-b:#c0392b;--int:#ecf6ee;--int-b:#2a7a3e;--watch:#fff7e6;--watch-b:#b0641b}
*{box-sizing:border-box}
html{scroll-snap-type:y mandatory;-webkit-text-size-adjust:100%;text-size-adjust:100%}
html,body{margin:0;background:var(--bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Noto Sans","Noto Sans Devanagari",Helvetica,Arial,sans-serif}
body{overflow-x:hidden}
.card{min-height:100vh;min-height:100lvh;scroll-snap-align:start;display:flex;align-items:center;justify-content:center;padding:44px 10px 22px;padding-bottom:calc(22px + 100lvh - 100svh)}
.in{width:100%;max-width:520px;background:var(--card);border:1px solid var(--line);border-radius:20px;padding:12px 14px 14px;box-shadow:0 6px 24px rgba(0,0,0,.06)}
.meta{display:flex;justify-content:space-between;align-items:center;font-size:12px;color:var(--muted);margin-bottom:8px;gap:8px}
.chap{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
.lvl{flex:none;font-weight:700;font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:#fff;background:var(--lc);border-radius:999px;padding:2px 8px}
.num{flex:none}
.panel{border-radius:14px;overflow:hidden;margin:0 auto 10px;border:1px solid #ecdcc0;max-width:calc(26vh * 1.882);max-width:calc(26svh * 1.882);background:#fbf1df}
.panel svg{display:block;width:100%;height:auto;font-family:inherit}
.badge{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:3px 9px;border-radius:999px;background:#eee8dd;color:#5b5348;margin-bottom:6px}
h1,h2{font-size:clamp(19px,1.8vh + 9px,24px);line-height:1.2;margin:2px 0 8px;overflow-wrap:anywhere;text-wrap:balance}
.body p,.body li,.moral{text-wrap:pretty}
.body{font-size:clamp(14.5px,1.1vh + 7px,17.5px);line-height:1.42;overflow-wrap:break-word}
.body p{margin:0 0 9px}.body ul,.body ol{margin:0 0 9px;padding-left:20px}.body li{margin:0 0 5px}
.big{font-size:1.12em;font-weight:600}.small{font-size:.82em;color:var(--muted)}
pre{white-space:pre-wrap;word-break:break-word;font:13px/1.4 "SF Mono",ui-monospace,Menlo,monospace;background:#faf7f1;border:1px solid var(--line);border-radius:10px;padding:8px 10px;margin:0 0 9px}
table.t{width:100%;border-collapse:collapse;font-size:.9em;margin:0 0 9px;table-layout:fixed}
table.t th,table.t td{text-align:left;padding:5px 6px;border-bottom:1px solid var(--line);vertical-align:top;overflow-wrap:normal;word-break:normal;hyphens:auto}
table.t th{font-size:.78em;letter-spacing:.05em;text-transform:uppercase;color:var(--muted)}
a{color:var(--accent)}.src{font-size:.8em}
.caution{font-size:.85em;font-weight:600;background:#fff4e0;border-left:4px solid #b0641b;border-radius:8px;padding:6px 10px;margin:0 0 9px}
.pg{font-size:.75em;font-weight:700;color:var(--accent);background:#e3f0f1;border-radius:6px;padding:0 3px;white-space:nowrap}
.moral{margin-top:6px;padding:8px 11px;border-radius:12px;background:#f3efe6;font-size:clamp(14px,1vh + 7px,16.5px);line-height:1.4;font-weight:600}
.moral:before{content:"So: ";color:var(--accent);font-weight:800}
.t-scene .badge{background:var(--scene);color:#fff}
.t-chat .badge{background:var(--accent);color:#fff}
.talk{display:flex;flex-direction:column;gap:6px;margin:0 0 9px}
.line{display:flex;gap:8px;align-items:flex-start}
.line .av{flex:none;width:32px;height:32px;border-radius:50%;background:#fbf1df;border:1px solid #ecdcc0;overflow:hidden}
.line .av svg{display:block;width:100%;height:100%}
.line .say{background:#fff;border:1px solid var(--line);border-radius:4px 14px 14px 14px;padding:5px 11px 6px;line-height:1.38}
.line .say .who{display:block;font-size:.68em;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--accent);margin-bottom:1px}
.line.r{flex-direction:row-reverse}.line.r .say{border-radius:14px 4px 14px 14px;background:#e3f0f1}
.line.s .say .who{color:#4b55b0}.line.p .say .who{color:#c0392b}
.scene{font-style:italic;color:var(--muted);font-size:.9em;margin:0 0 7px}
.keys{background:#f3efe6;border-left:4px solid var(--accent);border-radius:10px;padding:6px 11px 7px;margin:0 0 6px}
.keys .kh{font-size:.68em;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);margin:0 0 2px}
.keys ul{margin:0;padding-left:17px}.keys li{margin:2px 0}
.myth{display:block;font-size:.88em;color:var(--muted)}.t-myth .myth s{color:var(--myth-b)}
.review li{margin:0 0 8px}.review details summary{font-size:.85em;padding:4px 12px}
.t-true .in{background:var(--mine)}.t-true .badge{background:var(--accent);color:#fff}
.t-watch .in{background:var(--watch)}.t-watch .badge{background:var(--watch-b);color:#fff}
.t-try .badge{background:var(--quiz-b);color:#fff}
.t-myth .badge{background:var(--myth-b);color:#fff}.t-myth s{color:var(--myth-b)}
.t-quiz .in{background:var(--quiz)}.t-quiz .badge{background:var(--quiz-b);color:#fff}
.t-quiz summary,.t-try summary,.review summary{cursor:pointer;display:inline-block;background:var(--quiz-b);color:#fff;border-radius:999px;padding:7px 16px;font-weight:600;list-style:none;margin:2px 0 8px}
.t-quiz summary::-webkit-details-marker,.t-try summary::-webkit-details-marker{display:none}
.t-redpen .in{background:var(--red)}.t-redpen .badge{background:var(--red-b);color:#fff}
.t-interview .in{background:var(--int)}.t-interview .badge{background:var(--int-b);color:#fff}
.t-intro .badge,.t-done .badge,.t-cover .badge,.t-finale .badge{background:var(--ink);color:#fff}
.t-level .badge{background:var(--lc);color:#fff}.t-level .in{border-top:6px solid var(--lc)}
.btn{display:inline-block;background:var(--accent);color:#fff;text-decoration:none;padding:9px 16px;border-radius:999px;font-weight:600;border:0;font:inherit;font-weight:600;cursor:pointer}
.levels{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:4px 0 12px}
.levels a{display:block;text-decoration:none;color:#fff;background:var(--lc);border-radius:14px;padding:9px 10px;line-height:1.2}
.levels b{display:block;font-size:15px}.levels span{font-size:12px;opacity:.92}
.toc{padding-left:20px;margin:0 0 9px}.toc li{margin:4px 0}
.cover-cast{font-size:.92em}
#bar{position:fixed;top:0;left:0;height:3px;background:var(--accent);width:0;z-index:5;transition:width .2s}
#menu,#back{position:fixed;top:8px;z-index:6;border-radius:999px;padding:6px 13px;font:600 13px/1.2 inherit;cursor:pointer}
#menu{right:10px;background:rgba(255,253,249,.95);border:1px solid var(--line);color:var(--ink)}
#back{left:10px;background:var(--accent);border:0;color:#fff;max-width:calc(100vw - 110px);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#nav{position:fixed;inset:0;z-index:9;background:rgba(28,27,25,.45);display:flex;justify-content:center;align-items:flex-start;padding:10px}
#nav[hidden],#back[hidden]{display:none}
.navin{background:var(--card);width:100%;max-width:560px;max-height:calc(100vh - 20px);max-height:calc(100dvh - 20px);overflow-y:auto;border-radius:18px;padding:12px 14px 16px;box-shadow:0 10px 40px rgba(0,0,0,.25)}
.navtop{display:flex;gap:8px;position:sticky;top:-12px;background:var(--card);padding:4px 0 10px}
#q{flex:1;min-width:0;font-size:16px;padding:9px 12px;border:1.5px solid var(--line);border-radius:12px;background:#fff}
#close{border:0;background:#eee8dd;border-radius:12px;padding:0 14px;font-weight:700;cursor:pointer}
.navin h3{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--lc);margin:12px 0 2px}
.navin summary{cursor:pointer;font-weight:700;padding:8px 2px;border-top:1px solid var(--line)}
.navin ol{margin:0 0 8px;padding-left:24px}.navin li{margin:6px 0;font-size:15px}
.navin a{text-decoration:none}.navin a:hover{text-decoration:underline}
#results .r{display:block;padding:8px 2px;border-top:1px solid var(--line);text-decoration:none;color:var(--ink)}
#results .r small{display:block;color:var(--muted);font-size:12px}
#results .none{color:var(--muted);padding:8px 2px}
.hint{position:fixed;bottom:4px;left:0;right:0;text-align:center;font-size:11px;color:var(--muted);pointer-events:none}
.hint .wide{display:none}
@media (min-width:900px) and (min-height:560px){
 .card{padding:54px 40px 30px}
 .in{max-width:1160px;display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);grid-template-rows:auto 1fr;column-gap:36px;align-items:center;padding:22px 34px 26px;border-radius:26px;min-height:min(560px,calc(100svh - 120px))}
 .meta{grid-column:1/-1;align-self:start;font-size:14px;margin-bottom:14px}
 .lvl{font-size:11.5px;padding:3px 10px}
 .panel{grid-column:1;grid-row:2;margin:0;max-width:none}
 .txt{grid-column:2;grid-row:2}
 .badge{font-size:12px}
 .txt>h2{font-size:30px;margin:4px 0 12px}
 .body{font-size:18.5px;line-height:1.5}
 .moral{font-size:17.5px;padding:12px 16px}
 pre{font-size:14px}
 .t-cover .in,.t-finale .in{display:block;max-width:860px}
 .t-finale .panel{max-width:calc(34vh * 1.882);margin:0 auto 12px}
 .t-cover h1{font-size:44px}
 .levels a{padding:12px 14px}.levels b{font-size:18px}.levels span{font-size:13.5px}
}
@media (hover:hover) and (pointer:fine){.hint .tap{display:none}.hint .wide{display:inline}}
@media (min-width:900px) and (min-height:560px) and (max-height:800px){
 .card{padding:46px 32px 18px}
 .in{padding:14px 28px 16px}
 .meta{margin-bottom:8px}
 .txt>h2{font-size:25px;margin:2px 0 8px}
 .body{font-size:16px;line-height:1.45}
 .moral{font-size:15.5px;padding:9px 13px}
 .t-cover h1{font-size:34px}
 .t-cover .body{font-size:15.5px}
}
@media (min-width:640px) and (max-width:899.98px) and (min-height:900px){
 .in{max-width:660px;padding:18px 22px 20px;border-radius:24px}
 .panel{max-width:calc(30svh * 1.882)}
 .txt>h2,.t-cover h1{font-size:28px}
 .body{font-size:19px;line-height:1.48}
 .moral{font-size:18px;padding:11px 14px}
 .meta{font-size:14px}
}
@media (orientation:landscape) and (max-height:559.98px){
 .card{padding:40px 14px 10px;padding-bottom:calc(10px + 100lvh - 100svh)}
 .in{max-width:100%;display:grid;grid-template-columns:minmax(0,.85fr) minmax(0,1fr);column-gap:18px;align-items:center;padding:10px 14px 12px}
 .meta{grid-column:1/-1;margin-bottom:6px}
 .panel{grid-column:1;grid-row:2;margin:0;max-width:none}
 .txt{grid-column:2;grid-row:2}
 .txt>h2{font-size:18px;margin:0 0 6px}
 .body{font-size:14px;line-height:1.38}
 .moral{font-size:13.5px;padding:6px 10px}
 .t-cover .in,.t-finale .in{display:block;max-width:820px}
 .t-cover h1{font-size:22px;margin:2px 0 6px}
 .t-cover .body{display:grid;grid-template-columns:1fr 1fr;column-gap:18px;font-size:13.5px}
 .t-cover .toc-wrap{display:none}
 .t-finale .in{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1fr);column-gap:18px;align-items:center}
 .t-finale .in>.badge{grid-row:1;grid-column:1/-1}
 .t-finale .in>h2{grid-row:2;grid-column:1/-1;margin:0 0 6px}
 .t-finale .in>.panel{grid-row:3;grid-column:1;max-width:none;margin:0}
 .t-finale .in>.body{grid-row:3;grid-column:2}
 .levels a{padding:6px 10px}
}
@media (max-width:899.98px) and (max-height:720px){.t-cover .toc-wrap{display:none}}
@media print{html{scroll-snap-type:none}.card{min-height:0;break-inside:avoid}#menu,#back,#bar,.hint{display:none}}
@media (prefers-reduced-motion:reduce){#bar{transition:none}}
"""

JS = r"""<script>
(function(){
  var cards=[].slice.call(document.querySelectorAll('.card')),bar=document.getElementById('bar');
  var KEY='%s',nav=document.getElementById('nav'),q=document.getElementById('q'),res=document.getElementById('results'),back=document.getElementById('back'),prev=null,idx=null;
  var WIDE='(min-width:900px) and (min-height:560px)',probe=document.createElement('div');
  probe.style.cssText='position:fixed;top:0;left:0;width:0;height:100vh;height:100svh;visibility:hidden;pointer-events:none';document.body.appendChild(probe);
  function room(c){var s=getComputedStyle(c);return Math.min(window.innerHeight,probe.offsetHeight||window.innerHeight)-parseFloat(s.paddingTop)-22}
  function fit(){var wide=window.matchMedia(WIDE).matches,min=wide?0.8:0.72;
    cards.forEach(function(c){var i=c.querySelector('.in');if(!i)return;i.style.zoom='';var z=1,R=room(c);
      while(i.getBoundingClientRect().height>R+1&&z>min){z=Math.round((z-0.03)*100)/100;i.style.zoom=z}i.dataset.fit=z})}
  fit();window.addEventListener('resize',function(){clearTimeout(window.__f);window.__f=setTimeout(fit,150)});
  if(document.fonts&&document.fonts.ready)document.fonts.ready.then(fit);
  function cur(){var t=window.scrollY+window.innerHeight*0.35,b=0;for(var i=0;i<cards.length;i++){if(cards[i].offsetTop<=t)b=i;else break}return b}
  function upd(){var i=cur();bar.style.width=((i+1)/cards.length*100)+'%%';try{localStorage.setItem(KEY,cards[i].id)}catch(e){}}
  window.addEventListener('scroll',function(){window.requestAnimationFrame(upd)});
  function show(el){if(el)window.scrollTo({top:el.offsetTop})}
  function jump(id){var el=document.getElementById(id);if(!el)return;var here=cards[cur()];
    if(here&&here.id!==id&&here.id!=='toc'){prev=here.id;back.textContent='Back to where I was';back.hidden=false}
    nav.hidden=true;show(el);history.replaceState(null,'','#'+id)}
  back.onclick=function(){if(prev){var p=prev;prev=null;back.hidden=true;show(document.getElementById(p));history.replaceState(null,'','#'+p)}};
  document.addEventListener('click',function(e){var a=e.target.closest('a[href^="#"]');if(!a||a.getAttribute('href').length<2)return;e.preventDefault();jump(a.getAttribute('href').slice(1))});
  document.getElementById('menu').onclick=function(){nav.hidden=false;q.value='';res.innerHTML='';var c=cards[cur()].id.split('-')[0];
    [].forEach.call(nav.querySelectorAll('details'),function(d){d.open=d.dataset.ch===c});setTimeout(function(){q.focus()},50)};
  document.getElementById('close').onclick=function(){nav.hidden=true};
  nav.addEventListener('click',function(e){if(e.target===nav)nav.hidden=true});
  function build(){idx=cards.filter(function(c){return /^c\d+-/.test(c.id)}).map(function(c){var h=c.querySelector('h2');
    return {id:c.id,t:h?h.textContent:'',ch:(c.querySelector('.chap')||{}).textContent||'',x:c.textContent.toLowerCase()}})}
  q.addEventListener('input',function(){var v=q.value.trim().toLowerCase();if(!v){res.innerHTML='';return}if(!idx)build();
    var words=v.split(/\s+/),hits=idx.filter(function(c){return words.every(function(w){return c.x.indexOf(w)>=0})});
    hits.sort(function(a,b){return (b.t.toLowerCase().indexOf(words[0])>=0)-(a.t.toLowerCase().indexOf(words[0])>=0)});
    res.innerHTML=hits.length?hits.slice(0,40).map(function(c){return '<a class="r" href="#'+c.id+'">'+c.t.replace(/</g,'&lt;')+'<small>'+c.ch+'</small></a>'}).join(''):'<div class="none">No cards match.</div>'});
  document.addEventListener('keydown',function(e){if(!nav.hidden){if(e.key==='Escape')nav.hidden=true;return}if(e.target&&/INPUT|TEXTAREA/.test(e.target.tagName))return;var i=cur();
    if(['ArrowDown','PageDown','j',' '].indexOf(e.key)>=0){e.preventDefault();window.scrollTo({top:cards[Math.min(cards.length-1,i+1)].offsetTop,behavior:'smooth'})}
    if(['ArrowUp','PageUp','k'].indexOf(e.key)>=0){e.preventDefault();window.scrollTo({top:cards[Math.max(0,i-1)].offsetTop,behavior:'smooth'})}});
  var sh=document.getElementById('share');if(sh)sh.onclick=function(){var u=location.href.split('#')[0];
    if(navigator.share){navigator.share({title:document.title,url:u}).catch(function(){})}
    else if(navigator.clipboard){navigator.clipboard.writeText(u).then(function(){sh.textContent='Link copied'})}};
  if(location.hash.length>1){show(document.getElementById(location.hash.slice(1)))}
  else{var saved=null;try{saved=localStorage.getItem(KEY)}catch(e){}
    if(saved&&saved!=='toc'&&document.getElementById(saved)){prev=saved;back.textContent='Resume where I left off';back.hidden=false;
      setTimeout(function(){if(prev===saved){back.hidden=true;prev=null}},9000)}}
  upd();
})();
</script>"""

ICON = ("data:image/svg+xml," + re.sub(r"\s+", " ", f"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'>
<rect width='64' height='64' rx='14' fill='{CREAM}'/><rect x='10' y='14' width='44' height='38' rx='10' fill='{TEAL}'/>
<rect x='16' y='20' width='32' height='26' rx='7' fill='{FACE}'/><circle cx='25' cy='31' r='3.5' fill='{INK}'/>
<circle cx='39' cy='31' r='3.5' fill='{INK}'/><path d='M24 38 Q32 44 40 38' stroke='{INK}' stroke-width='3' fill='none' stroke-linecap='round'/>
<line x1='32' y1='14' x2='32' y2='7' stroke='{INK}' stroke-width='3'/><circle cx='32' cy='6' r='4' fill='{HALDI}'/></svg>""")
        .replace("#", "%23").replace("<", "%3C").replace(">", "%3E"))


def load(path):
    path = pathlib.Path(path).resolve()
    spec = importlib.util.spec_from_file_location(f"deck_{path.stem}", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"{path}: cannot load")
    mod = importlib.util.module_from_spec(spec)
    # Load the engine first and put the deck's folder LAST on the path: a user file named
    # deck.py or art.py must never shadow the engine modules of the same name.
    import samjha  # noqa: F401
    if str(path.parent) not in sys.path:
        sys.path.append(str(path.parent))
    spec.loader.exec_module(mod)
    if not hasattr(mod, "deck"):
        raise SystemExit(f"{path}: no `deck = Deck(...)` found")
    return mod.deck


def _noref(body):
    return re.sub(r'<p class="small ref">.*?</p>', " ", body)


def _labels(body):
    """A body without source and page tags, the points-box header and the quiz hint."""
    return re.sub(r'<a class="src".*?</a>|<span class="pg">.*?</span>|<div class="kh">.*?</div>', " ", _noref(body))


def lint(deck):
    """Warnings an author should fix before shipping. Returns a list of strings."""
    out = []
    for ch in deck.chapters:
        kinds = [c["kind"] for c in ch.cards]
        where = f"ch{ch.n} '{ch.title}'"
        if not kinds or kinds[0] != "intro":
            out.append(f"{where}: should start with ch.opener(...)")
        if "quiz" not in kinds:
            out.append(f"{where}: no quick checks (ch.quizzes)")
        if kinds and kinds[-1] != "done":
            out.append(f"{where}: should end with ch.done(...)")
        if not 12 <= len(kinds) <= 24:
            out.append(f"{where}: {len(kinds)} cards; aim for 14 to 20")
        for j, c in enumerate(ch.cards):
            if deck.source and c["kind"] in ("redpen", "interview", "myth") and 'class="pg"' not in c["body"]:
                out.append(f"{where} card c{ch.n}-{j + 2}: PDF deck recap card with no pg(n) citation (references/pdf-mode.md: cite myths, red-pen notes and one-breath lines too)")
            if c["kind"] in ("redpen", "myth") and c.get("auto"):
                limit, items = (44, re.findall(r"<li>(.*?)</li>", c["body"])) if c["kind"] == "redpen" else (60, re.findall(r"<b>Fact:</b> (.*?) <span class=\"myth\">", c["body"]))
                items = [_plain(x) for x in items]
                long_ = [x for x in items if len(x) > limit]
                long_ += [x for x in c.get("cut") or [] if x not in long_]
                if long_ or (c["kind"] == "redpen" and len(items) > 5):
                    out.append(f"{where} card c{ch.n}-{j + 2}: {'notes' if c['kind'] == 'redpen' else 'facts'} too long for the drawing (limit {limit} characters"
                               + (", 5 notes" if c["kind"] == "redpen" else "") + f"): {'; '.join(x[:40] for x in long_[:3])}")
            plain = re.sub(r"<[^>]+>", " ", _labels(c["body"]))
            n = sum(1 for w in plain.split() if re.search(r"\w", w))
            cap = 70 if c["kind"] == "chat" or 'class="talk"' in c["body"] else 95
            if n > cap:
                out.append(f"{where} card c{ch.n}-{j + 2} '{c['title']}': {n} words in the body; keep it under {cap} so it fits a phone"
                           + (" (each chat line and the points box cost extra height)" if cap == 70 else ""))
            if len(re.sub(r"<[^>]+>", "", c["title"])) > 64:
                out.append(f"{where} card c{ch.n}-{j + 2}: title over 64 characters")
            for field in ("title", "body", "moral"):
                if c.get(field) and re.search("[\u2013\u2014]", c[field]):
                    out.append(f"{where} card c{ch.n}-{j + 2}: em or en dash in {field}; use a comma, colon or full stop")
    pages = (deck.source or {}).get("pages") or 0
    need = 3 if pages <= 20 else 6 if pages <= 80 else 9
    if pages and len(deck.chapters) < need:
        out.append(f"PDF has {pages} pages but the deck has {len(deck.chapters)} chapters; aim for at least {need} so facts are not lost (references/pdf-mode.md)")
    if deck.source and deck.left_out is None:
        out.append("PDF deck without left_out=[(what, why), ...]: list every part of the source that is not on a card (an empty list if nothing was left out)")
    for name, val, cap in (("tagline", deck.tagline, 90), ("about", deck.about, 200), ("caution", deck.caution or "", 140)):
        n = len(re.sub(r"<[^>]+>", "", val))
        if n > cap:
            out.append(f"Deck {name} is {n} characters; keep it under {cap} so the cover fits a phone")
    blob = (deck.title + " " + deck.tagline).lower()
    if re.search(r"\b(101|basics|intro|introduction|fundamentals|beginner'?s guide|crash course)\b", blob) and len(deck.chapters) < 6:
        out.append(f"'{deck.title}' reads as a whole subject but has {len(deck.chapters)} chapters; list the subject's standard syllabus and give it 6 to 9 chapters, or narrow the title (SKILL.md, topic breadth)")
    teach = {"scene", "true", "idea", "diagram", "table", "watch", "try", "chat"}
    no_key, key_not_drawn, bold_off, bubble_off = [], [], [], []
    for ch in deck.chapters:
        for j, c in enumerate(ch.cards):
            cid = f"c{ch.n}-{j + 2}"
            if c["kind"] not in teach:
                continue
            nb = len(re.findall(r"<b>", c["body"]))
            if nb == 0 or nb > 3:
                bold_off.append(f"{cid} ({nb})")
            drawn = " ".join(re.findall(r"<text[^>]*>(.*?)</text>", c["panel"])).lower()
            if not c.get("key"):
                no_key.append(cid)
            elif c["key"].lower() not in drawn:
                key_not_drawn.append(f"{cid} '{c['key']}'")
            if c["kind"] == "chat":
                said = re.sub(r"[^a-z0-9 ]", "", unescape(re.sub(r"<[^>]+>", " ", c["body"])).lower())
                said = re.sub(r"\s+", " ", said)
                for g in re.findall(r'<g class="bub"[^>]*>(.*?)</g>', c["panel"]):
                    bub = re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", "", unescape(" ".join(re.findall(r"<text[^>]*>(.*?)</text>", g))).lower())).strip()
                    if bub and bub not in said:
                        bubble_off.append(cid)
                        break
    if no_key:
        out.append(f"{len(no_key)} teaching cards have no key= term ({', '.join(no_key[:8])}{'...' if len(no_key) > 8 else ''}): name the one term each card teaches")
    if key_not_drawn:
        out.append(f"{len(key_not_drawn)} cards do not show their key term in the picture ({', '.join(key_not_drawn[:6])}{'...' if len(key_not_drawn) > 6 else ''}): label it in the panel")
    if bold_off:
        out.append(f"{len(bold_off)} teaching cards bold 0 or more than 3 terms ({', '.join(bold_off[:8])}{'...' if len(bold_off) > 8 else ''}): bold 1 to 3 key terms, never whole sentences")
    if bubble_off:
        out.append(f"{len(bubble_off)} chat cards have a speech bubble that is not a line of their conversation ({', '.join(bubble_off[:8])}): the picture and the chat must be one story")
    leaks = []
    stop = {"the", "a", "an", "and", "or", "of", "to", "in", "on", "it", "is", "for", "with", "its", "that", "this", "your", "you", "not", "no", "yes", "be"}
    for ch in deck.chapters:
        for j, c in enumerate(ch.cards):
            if c["kind"] != "quiz" or c.get("ref"):
                continue
            drawn = set(re.findall(r"[a-z0-9%]+", unescape(" ".join(re.findall(r"<text[^>]*>(.*?)</text>", c["panel"]))).lower())) - stop
            ans = re.search(r"<details><summary>Answer</summary><p>(.*?)</p>", c["body"], re.S)
            words = set(re.findall(r"[a-z0-9%]+", unescape(re.sub(r"<[^>]+>", " ", ans.group(1))).lower())) - stop if ans else set()
            hit = {w for w in drawn & words if len(w) > 3}
            if len(hit) >= 2:
                leaks.append(f"c{ch.n}-{j + 2} ({', '.join(sorted(hit)[:3])})")
    if leaks:
        out.append(f"{len(leaks)} quiz cards show words of their answer in the picture ({', '.join(leaks[:6])}): draw the question's situation, not its answer")
    for ch in deck.chapters[1:]:
        if not ch.has_recall:
            out.append(f"ch{ch.n} '{ch.title}': no ch.recall(...) 'Yaad hai?' question about an earlier chapter (spacing)")
    for ch in deck.chapters:
        n = sum(1 for c in ch.cards if c["kind"] in teach)
        if n < 9:
            out.append(f"ch{ch.n} '{ch.title}': only {n} teaching cards (story, idea, picture, example, watch out, try it); aim for 9 or more so the recap cards do not outweigh the teaching")
    # standalone: a term another chapter had to define must be defined again where it is used
    terms = {}
    for ch in deck.chapters:
        for term, _ in ch.glossary:
            for part in re.split(r"\s*[,/]\s*", re.sub(r"<[^>]+>", "", term).strip().lower()):
                terms.setdefault(part, ch.n)
    for ch in deck.chapters:
        own = {part for t_, _ in ch.glossary for part in re.split(r"\s*[,/]\s*", re.sub(r"<[^>]+>", "", t_).strip().lower())}
        text_ = " ".join(re.sub(r"<[^>]+>", " ", (c["title"] or "") + " " + _noref(c["body"]) + " " + (c.get("moral") or "")) for c in ch.cards).lower()
        bold = {re.sub(r"<[^>]+>", "", b).strip().lower() for c in ch.cards for b in re.findall(r"<b>(.*?)</b>", c["body"])}
        missing = sorted(k for k, n in terms.items() if n != ch.n and k not in own and k not in bold and len(k) > 2
                         and re.search(r"\b" + re.escape(k) + r"(s|es)?\b", text_))
        if missing:
            out.append(f"ch{ch.n} '{ch.title}' uses {', '.join(missing)} (defined only in another chapter's glossary); add them to this chapter's glossary so it stands alone")
    if deck.stock:
        out.append(f"{len(deck.stock)} cards need attention in their drawing ({', '.join(deck.stock[:8])}{'...' if len(deck.stock) > 8 else ''}): "
                   "quizzes name the card they test (ch.quizzes([(q, a, 'card title')])), done, red-pen and one-breath cards get their own scene (panel=)")
    always = ("crore", "lakh", "tapri", "kirana", "chaiwala", "sabziwala", "jugaad", "emi", "upi", "fd", "sip", "pg", "gst")
    for ch in deck.chapters:
        own = {part for t_, _ in ch.glossary for part in re.split(r"\s*[,/]\s*", re.sub(r"<[^>]+>", "", t_).strip().lower())}
        bodies = " ".join((c["title"] or "") + " " + _noref(c["body"]) + " " + (c.get("moral") or "") for c in ch.cards)
        bold = {re.sub(r"<[^>]+>", "", b).strip().lower() for b in re.findall(r"<b>(.*?)</b>", bodies)}
        plain = re.sub(r"<[^>]+>", " ", re.sub(r'<a class="src".*?</a>|<span class="pg">.*?</span>', " ", bodies))
        words = [w for w in always if re.search(r"\b" + w + r"\b", plain.lower()) and w not in own and w not in bold]
        caps_phrases = " ".join(re.findall(r"\b[A-Z]{2,}(?:\s+[A-Z]{2,})+\b", plain))
        acr = sorted({a for a in re.findall(r"\b[A-Z]{2,5}\b", plain) if a.lower() not in own and a.lower() not in bold
                      and a not in caps_phrases and not re.search(re.escape(a) + r"\s*\(", plain)
                      and a not in ("OK", "TV", "AM", "PM", "ID", "VS", "US", "UK", "IT", "AI", "PDF", "HTML", "SO", "NO", "GO")})
        acr = [a for a in acr if a.lower() not in words]
        if words or acr:
            out.append(f"ch{ch.n} '{ch.title}': explain for readers outside India or new to the topic: {', '.join(words + acr[:8])} "
                       "(add to the glossary, bold the term where a card explains it, or expand it in brackets)")
    levels_used = {ch.level for ch in deck.chapters}
    for l in deck.levels:
        if l["id"] not in levels_used:
            out.append(f"level '{l['id']}' has no chapters")
    return out


def level_panel(color, stars, titles):
    s = "".join(text(30 + i * 30, 34, "*", 30, fill=HALDI if i < stars else "#d8cfbf", weight=800) for i in range(3))
    rows = []
    for k, ttl in enumerate(titles[:4]):
        rows += wrap(f"{k + 1}. {re.sub(r'<[^>]+>', '', ttl)}", 176, 9)[:2]
    body = lines(126, 34, rows[:7], 9, anchor="start", fill="#fff", weight=700)
    return svg(chintu(62, 150, 0.95, mood="grin", arms="wave") + s
               + f'<rect x="116" y="14" width="196" height="{min(132, 24 + len(rows[:7]) * 11)}" rx="8" fill="{color}"/>' + body,
               "Chintu waves beside the list of this level's chapters")


def review_panel():
    return svg(pinky(70, 150, 1.0, mood="o", arms="up") + chintu(165, 150, 0.95, mood="smile", eyes="up")
               + sharma(255, 150, 1.0, "flat", "skeptic", arms="point")
               + text(112, 46, "?", 34, weight=800, fill=HALDI) + text(205, 34, "?", 28, weight=800, fill=CORAL)
               + text(298, 50, "?", 30, weight=800, fill=TEAL2), "The cast puzzles over questions from different chapters")


GLUE = re.compile(r'\s+(<span class="pg">|<a class="src")')


def glue(html):
    """Keep a page or source tag on the same line as the word before it."""
    html = GLUE.sub(lambda m: "&nbsp;" + m.group(1), html)
    # no single word alone on the last line: tie the last two words of every paragraph and list item
    html = re.sub(r"(\S)[ \t]+([^\s<>]+(?:</?(?:b|i|em|strong|s|a|span)\b[^>]*>)*)(?=</p>|</li>|\Z)", r"\1&nbsp;\2", html)
    return re.sub(r"(\d)\s+(am|pm|km|kg|min|%)\b", r"\1&nbsp;\2", html)


def _stop(s):
    return s if re.sub(r"<[^>]+>", "", s).rstrip().endswith((".", "?", "!")) else s + "."


def _first_check(x):
    return next((c_ for c_ in x.cards if c_["kind"] == "quiz" and c_["badge"].startswith("Quick check")), None)


def _review_picks(chs, level):
    """One quick check per chapter of the level; a level with one chapter adds the chapters before it."""
    picks = [(x, q) for x in chs if x.level == level for q in [_first_check(x)] if q]
    if len(picks) < 2:
        first = next(i for i, x in enumerate(chs) if x.level == level)
        picks += [(x, q) for x in reversed(chs[:first]) for q in [_first_check(x)] if q]
    return picks


def render(deck, out):
    chs = deck.chapters
    first_of_level = {}
    for ch in chs:
        first_of_level.setdefault(ch.level, ch)
    levels = [l for l in deck.levels if l["id"] in first_of_level]
    ncards = sum(len(ch.cards) + 1 for ch in chs) + 2 * len(levels) + 2
    ncards += sum(1 for l in levels if len(_review_picks(chs, l["id"])) >= 2)
    sections = []

    lvl_btns = "".join(f'<a href="#L-{l["id"]}" style="--lc:{l["color"]}"><b>{l["name"]}</b><span>{l["desi"]}</span></a>' for l in levels)
    toc = ""
    for l in levels:
        items = "".join(f'<li><a href="#c{ch.n}-1">{ch.title}</a></li>' for ch in chs if ch.level == l["id"])
        toc += f'<p style="margin:8px 0 2px"><b style="color:{l["color"]}">{l["name"]}</b></p><ol class="toc" start="{min(ch.n for ch in chs if ch.level == l["id"])}">{items}</ol>'
    c = deck.cast
    cast_line = (f'<b>Cast:</b> {c["chintu"]["name"]}, {c["chintu"]["role"]}. {c["sharma"]["name"]}, {c["sharma"]["role"]}. '
                 f'{c["pinky"]["name"]}, {c["pinky"]["role"]}.')
    source = ""
    if deck.source:
        s = deck.source
        link = f'<a href="{escape(s["url"], quote=True)}">{escape(s["title"])}</a>' if s.get("url") else escape(s["title"])
        source = f'<p class="small"><b>Made from:</b> {link}{(". " + s["note"]) if s.get("note") else ""}</p>'
    if deck.left_out:
        source += ('<details class="small"><summary><b>Left out of this deck</b> (' + str(len(deck.left_out)) + ')</summary><ul>'
                   + "".join(f"<li>{w}: {y}</li>" for w, y in deck.left_out) + "</ul></details>")
    if deck.caution:
        source = f'<p class="caution">{deck.caution}</p>' + source
    sections.append(
        f'<section class="card t-cover" id="toc"><div class="in"><span class="badge">Start here</span><h1>{deck.title}</h1>'
        f'<div class="body"><div class="cover-a"><p class="big">{deck.tagline}</p>' + (f"<p>{deck.about}</p>" if deck.about else "")
        + f'<p><b>Pick your level:</b></p><div class="levels">{lvl_btns}</div></div>'
        f'<div class="cover-b"><p class="cover-cast">{cast_line}</p>'
        f'<p class="small">Swipe up, or press the down arrow. <b>Menu</b> searches every card and lists every chapter. Every chapter stands alone.</p>'
        + (f'<div class="toc-wrap">{toc}</div>' if len(chs) <= 4 else
           f'<details class="toc-wrap"><summary><b>All {len(chs)} chapters</b></summary>{toc}</details>')
        + (f'<p class="small">{deck.disclaimer}</p>' if deck.disclaimer else "") + source
        + "</div></div></div></section>")

    for ch in chs:
        lv = deck.level(ch.level)
        style = f' style="--lc:{lv["color"]}"'
        if first_of_level[ch.level] is ch:
            k = [l["id"] for l in levels].index(ch.level)
            names = "".join(f"<li>{x.title}</li>" for x in chs if x.level == ch.level)
            sections.append(
                f'<section class="card t-level" id="L-{lv["id"]}"{style}><div class="in">'
                f'<div class="meta"><span class="lvl">{lv["name"]}</span><span class="chap">Level {k + 1} of {len(levels)}</span></div>'
                f'<div class="panel">{level_panel(lv["color"], k + 1, [x.title for x in chs if x.level == ch.level])}</div><div class="txt"><span class="badge">Level {k + 1}</span>'
                f'<h2>{lv["name"]}: {lv["desi"]}</h2><div class="body"><p>In this level:</p><ol>{names}</ol></div>'
                f'<div class="moral">Each chapter stands alone. Start anywhere.</div></div></div></section>')
        cs = [deck.before_card(ch)] + ch.cards
        last_of_level = [x for x in chs if x.level == ch.level][-1] is ch
        for j, cd in enumerate(cs):
            moral = f'<div class="moral">{glue(cd["moral"])}</div>' if cd.get("moral") else ""
            sections.append(
                f'<section class="card t-{cd["kind"]}" id="c{ch.n}-{j + 1}"{style}><div class="in">'
                f'<div class="meta"><span class="lvl">{lv["name"]}</span><span class="chap">Ch {ch.n}: {ch.title}</span><span class="num">{j + 1}/{len(cs)}</span></div>'
                f'<div class="panel">{cd["panel"]}</div><div class="txt"><span class="badge">{cd["badge"]}</span><h2>{cd["title"]}</h2>'
                f'<div class="body">{glue(cd["body"])}</div>{moral}</div></div></section>')
        if last_of_level:
            k = [l["id"] for l in levels].index(ch.level)
            picks = _review_picks(chs, ch.level)[:4]
            if len(picks) >= 2:
                scope = "this level" if all(x.level == ch.level for x, _ in picks) else "this level and earlier ones"
                items = "".join(f'<li><b>{re.sub(r"<[^>]+>", "", q_["title"])}</b> <span class="small">(Ch {x.n})</span>{q_["body"]}</li>' for x, q_ in picks)
                sections.append(
                    f'<section class="card t-quiz" id="R-{lv["id"]}"{style}><div class="in">'
                    f'<div class="meta"><span class="lvl">{lv["name"]}</span><span class="chap">Mixed review</span></div>'
                    f'<div class="panel">{review_panel()}</div><div class="txt"><span class="badge">Mixed review</span>'
                    f'<h2>{len(picks)} questions from {scope}</h2><div class="body"><ol class="review">{items}</ol></div>'
                    f'<div class="moral">Mixed questions from different chapters: the harder recall is what makes it stick.</div></div></div></section>')
            done_lines = "".join(f"<li><b>{x.title}</b>" + (f" {x.summary}" if x.summary else "") + "</li>" for x in chs if x.level == ch.level)
            nxt = levels[k + 1] if k + 1 < len(levels) else None
            nxt_line = (f'<p>Next: <a href="#L-{nxt["id"]}">{nxt["name"]}, {nxt["desi"]}</a>: '
                        + _stop(", ".join(x.title for x in chs if x.level == nxt["id"])) + "</p>") if nxt else "<p>That was the last level.</p>"
            sections.append(
                f'<section class="card t-level" id="D-{lv["id"]}"{style}><div class="in">'
                f'<div class="meta"><span class="lvl">{lv["name"]}</span><span class="chap">Level {k + 1} complete</span></div>'
                f'<div class="panel">{level_panel(lv["color"], k + 1, [x.title for x in chs if x.level == ch.level])}</div><div class="txt">'
                f'<span class="badge">Level {k + 1} done</span><h2>You finished {lv["name"]}</h2>'
                f'<div class="body"><p>What you now know:</p><ul>{done_lines}</ul>{nxt_line}</div>'
                f'<div class="moral">{"Stop here and you have the basics. Or keep going." if nxt else "Samjha kya? Samajh gaye!"}</div></div></div></section>')

    sections_final = sections
    recap = "".join(f'<li><a href="#L-{l["id"]}">{l["name"]}</a>: {" / ".join(ch.title for ch in chs if ch.level == l["id"])}</li>' for l in levels)
    sections.append(
        f'<section class="card t-finale" id="end"><div class="in"><span class="badge">The end</span><h2>Samjha kya? Samajh gaye!</h2>'
        f'<div class="panel">{svg(chintu(80, 150, 1.0, mood="grin", arms="up") + sharma(170, 150, 1.0, "smile", "flat") + pinky(250, 150, 1.0, "grin", arms="up"), "The whole cast cheers")}</div>'
        f'<div class="body"><p>You finished <b>{deck.title}</b>{"" if re.sub(r"<[^>]+>", "", deck.title).rstrip()[-1:] in "?!." else "."}</p><ol>{recap}</ol>'
        f'<p><button class="btn" id="share" type="button">Share this deck</button> <a class="btn" href="#toc" style="background:#eee8dd;color:var(--ink)">Start page</a></p>'
        f'<p class="small">Made with <a href="{REPO}">samjha-kya</a>: turn any topic or PDF into a comic flashcard deck.</p></div></div></section>')

    navlist = ""
    for l in levels:
        navlist += f'<h3 style="--lc:{l["color"]}">{l["name"]}: {l["desi"]}</h3>'
        for ch in chs:
            if ch.level != l["id"]:
                continue
            cs = [deck.before_card(ch)] + ch.cards
            navlist += (f'<details data-ch="c{ch.n}"><summary>Ch {ch.n}: {ch.title}</summary><ol>'
                        + "".join(f'<li><a href="#c{ch.n}-{j + 1}">{cd["title"]}</a></li>' for j, cd in enumerate(cs)) + "</ol></details>")
    nav = (f'<div id="nav" hidden><div class="navin"><div class="navtop"><input id="q" type="search" placeholder="Search every card" aria-label="Search cards">'
           f'<button id="close" type="button">Close</button></div><div id="results"></div>'
           f'<a href="#toc" class="r" style="display:block;padding:8px 2px;font-weight:700">Start page</a>{navlist}</div></div>'
           f'<button id="back" type="button" hidden>Back</button>')
    desc = escape(re.sub(r"<[^>]+>", "", deck.tagline), quote=True)
    meta = f'<meta name="description" content="{desc}"><meta property="og:title" content="{escape(deck.title, quote=True)}"><meta property="og:description" content="{desc}">'
    if deck.site:
        meta += f'<link rel="canonical" href="{deck.site}"><meta property="og:url" content="{deck.site}">'
    html = (f'<!doctype html><html lang="{deck.lang}"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
            f'<title>{escape(re.sub(r"<[^>]+>", "", deck.title))}</title>{meta}<meta name="theme-color" content="#f6f3ee">'
            f'<link rel="icon" href="{ICON}"><meta name="generator" content="samjha-kya {engine_id()}">'
            f'<style>{CSS}</style></head><body><div id="bar"></div><button id="menu" type="button">Menu</button>{nav}'
            f'<main class="feed">{"".join(sections)}</main>'
            f'<div class="hint"><span class="tap">swipe up</span><span class="wide">scroll, or press the down arrow</span></div>'
            f'{JS % ("samjha-kya-" + deck.slug + "-pos")}</body></html>')
    out = pathlib.Path(out)
    out.write_text(html, encoding="utf-8")
    return out, ncards


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("deck", help="path to a deck .py file")
    ap.add_argument("-o", "--out", help="output HTML path (default: <slug>.html next to the deck file)")
    a = ap.parse_args()
    deck = load(a.deck)
    out = a.out or pathlib.Path(a.deck).resolve().parent / f"{deck.slug}.html"
    warnings = lint(deck)
    path, n = render(deck, out)
    print(f"built {path} ({n} cards, {len(deck.chapters)} chapters)")
    for w in warnings:
        print("warn:", w)
    print(json.dumps({"out": str(path), "cards": n, "warnings": len(warnings)}))


if __name__ == "__main__":
    main()
