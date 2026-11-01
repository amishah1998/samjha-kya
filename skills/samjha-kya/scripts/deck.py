"""Deck structure: levels, chapters and the card types every chapter repeats.

A deck file builds one `deck = Deck(...)`, adds chapters with `deck.chapter(...)`, and fills each
chapter with cards. build.py turns it into one self-contained HTML file.
"""
import re
from html import escape

from art import *

LEVELS = [
    dict(id="beginner", name="Beginner", desi="Naya khiladi", color="#2a7a3e"),
    dict(id="intermediate", name="Intermediate", desi="Pakka khiladi", color="#b0641b"),
    dict(id="advanced", name="Advanced", desi="Ustaad", color="#a5302a"),
]

CAST = dict(
    chintu=dict(name="Chintu", role="the robot who read the entire internet",
                line="Chintu knows a lot and explains it well, but sometimes sounds sure when it should not."),
    sharma=dict(name="Sharma ji", role="the sceptic",
                line="Sharma ji believes nothing without proof. \"Data dikhao.\""),
    pinky=dict(name="Pinky", role="the eager learner",
               line="Pinky asks what everyone is thinking and tries every shortcut first."),
)


def src(url, label):
    """A small source link, placed at the end of the sentence it supports."""
    return f'<a class="src" href="{escape(url, quote=True)}">{escape(label)}</a>'


def pg(n):
    """A page citation for PDF decks: pg(12) -> 'p. 12'."""
    return f'<span class="pg">p.&nbsp;{n}</span>'


def _plain(s):
    """Card HTML to drawing text: drop page and source tags, tags and entities."""
    import html as _h
    s = re.sub(r'<span class="pg">.*?</span>|<a class="src".*?</a>', "", s)
    return re.sub(r"\s+", " ", _h.unescape(re.sub(r"<[^>]+>", "", s))).strip().rstrip(" .") + ("" if s.strip().endswith(("?", "!")) else "")


def _short(s, n):
    if len(s) <= n:
        return s
    cut = s[:n - 3].rsplit(" ", 1)[0]
    return cut + "..."


_NAMES = {k: v["name"] for k, v in CAST.items()}


def _face(who):
    if who == "chintu":
        return f'<svg viewBox="-27 -101 54 54" aria-hidden="true">{chintu(0, 0, 1.0, mood="smile")}</svg>'
    draw = {"sharma": lambda: sharma(0, 0, 1.0, "flat", "skeptic"), "pinky": lambda: pinky(0, 0, 1.0, "smile")}
    head = draw[who]() if who in draw else person(0, 0, 1.0, "smile", shirt=BLUE)
    return f'<svg viewBox="-21 -88 42 42" aria-hidden="true">{head}</svg>'


def talk(*lines):
    """A conversation for a card body: talk(("pinky", "Why...?"), ("chintu", "Because...")).
    Speakers: "chintu", "sharma", "pinky", or any other name for an extra (drawn as a person)."""
    out = ""
    for who, said in lines:
        side = " r" if who == "chintu" else ""
        tag = {"sharma": " s", "pinky": " p"}.get(who, "")
        name = _NAMES.get(who, who)
        out += (f'<div class="line{side}{tag}"><span class="av">{_face(who)}</span>'
                f'<span class="say"><span class="who">{escape(name)}</span>{said}</span></div>')
    return f'<div class="talk">{out}</div>'


def keys(*points, head="Yaad rakho"):
    """The 2 or 3 things to remember from this card, each starting with its bold key term."""
    return f'<div class="keys"><div class="kh">{head}</div><ul>' + "".join(f"<li>{p}</li>" for p in points) + "</ul></div>"


def scene(s):
    """A one-line stage direction (where and when), shown in italics."""
    return f'<p class="scene">{s}</p>'


def _cue(panel):
    """A teaching panel reused on a quiz: keep the drawing, remove every word, so it is a memory cue
    and not the answer key."""
    p = re.sub(r'<g class="bub".*?</g>', "", panel, flags=re.S)
    p = re.sub(r"<text\b[^>]*>.*?</text>", "", p, flags=re.S)
    p = re.sub(r'aria-label="[^"]*"', 'aria-label="The picture from the card this question tests, without its words"', p, count=1)
    return p.replace("</svg>", f'<g><circle cx="292" cy="28" r="17" fill="{HALDI}" stroke="{INK}" stroke-width="1.4"/>'
                     f'<text x="292" y="36" font-size="24" text-anchor="middle" font-weight="800" fill="{INK}">?</text></g></svg>', 1)


def table(head, rows):
    """A small HTML table for a card body. Keep it to 2 or 3 columns and 3 to 6 rows."""
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="t"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


class Chapter:
    def __init__(self, deck, level, title, glossary, number, caution=True):
        self.deck, self.level, self.title, self.glossary, self.n = deck, level, title, glossary or [], number
        self.caution, self.summary, self.has_recall = caution, None, False
        self.cards = []

    def card(self, kind, badge, title, panel, body, moral=None, key=None):
        """key: the card's one key term; it should appear bold in the body and as a label in the panel."""
        self.cards.append(dict(kind=kind, badge=badge, title=title, panel=panel, body=body, moral=moral, key=key, chapter=self.n))
        return self

    # ---- the core flow, in the order a chapter uses them ----
    def opener(self, panel, body, moral=None):
        """First card after 'Before you start': the hook scene that sets up the chapter's question."""
        return self.card("intro", f"Chapter {self.n}", self.title, panel, body, moral)

    def story(self, title, panel, body, moral=None, badge="Story", key=None):
        return self.card("scene", badge, title, panel, body, moral, key)

    def true_story(self, title, panel, body, moral=None, key=None):
        """A real, sourced event. The body must carry a src() link."""
        return self.card("true", "True story", title, panel, body, moral, key)

    def chat(self, title, panel, lines, points=None, moral=None, badge="Talk", key=None, intro=None, after=""):
        """The default teaching card: a short conversation, then 2 or 3 things to remember.
        lines: [(speaker, text)], 2 to 4 turns; Pinky asks a real why or how, or Sharma ji voices the wrong belief,
        and Chintu explains or corrects. The panel's speech bubble must be one of these lines, word for word.
        points: 2 or 3 strings for the "Yaad rakho" box, each starting with its <b>key term</b>.
        intro: an optional one-line stage direction; after: optional HTML (a table, a list) between chat and box."""
        body = (scene(intro) if intro else "") + talk(*lines) + (after or "") + (keys(*points) if points else "")
        return self.card("chat", badge, title, panel, body, moral, key)

    def idea(self, title, panel, body, moral=None, badge="Idea", key=None):
        return self.card("idea", badge, title, panel, body, moral, key)

    def picture(self, title, panel, body, moral=None, badge="Picture it", key=None):
        return self.card("diagram", badge, title, panel, body, moral, key)

    def glance(self, title, panel, body, moral=None, badge="At a glance", key=None):
        return self.card("table", badge, title, panel, body, moral, key)

    def example(self, title, panel, body, moral=None, badge="Worked example", key=None):
        return self.card("table", badge, title, panel, body, moral, key)

    def watch_out(self, title, panel, body, moral=None, badge="Watch out", key=None):
        return self.card("watch", badge, title, panel, body, moral, key)

    def try_it(self, title, panel, body, moral=None, badge="Try it yourself", key=None):
        return self.card("try", badge, title, panel, body, moral, key)

    # ---- the fixed closing run: myths, red pen, one breath, quick checks, done ----
    def myths(self, pairs, moral=None, panel=None):
        """pairs: [(myth, reality)]. 2 to 4 pairs. Fact first, myth once: repeating a myth makes it feel true.
        The default panel pins up each FACT with a tick; the myth appears once, struck out, in the body."""
        auto = panel is None
        cut = []
        if panel is None:
            n = len(pairs)
            cols = 2 if n > 2 else n
            w = 136 if cols == 2 else 260
            notes = ""
            for i, (_, r) in enumerate(pairs[:4]):
                cx, cy = 14 + (i % cols) * (w + 16), 12 + (i // cols) * 68
                rows = wrap(_short(_plain(r), 60), w - 30, 9)
                if len(rows) > 3:
                    cut.append(_plain(r))
                rows = rows[:3]
                notes += (paper(cx, cy, w, 58, rows, 9, rot=[-2, 2, 1.5, -1.5][i], fill="#fff")
                          + tick(cx + w - 14, cy + 44, 1.1))
            panel = svg(notes, "The facts pinned up, each with a tick", floor=False)
        self.card("myth", "Myth busters", f"{len(pairs)} myths, busted", panel,
                  "<ul>" + "".join(f'<li><b>Fact:</b> {r} <span class="myth">Myth: <s>{m}</s></span></li>' for m, r in pairs) + "</ul>", moral)
        self.cards[-1]["auto"] = auto
        self.cards[-1]["cut"] = cut
        return self

    def redpen(self, points, where=None, panel=None):
        """3 to 5 short lines worth remembering, as the sceptic's margin notes."""
        who = self.deck.cast["sharma"]["name"]
        where = where or self.title
        auto = panel is None
        notes = ""
        # shrink, then single-line, until every note fits the page; never drop a note silently
        for fs, max_rows in ((9, 2), (8.5, 2), (8, 2), (8, 1)):
            notes, y, fitted = "", 36, 0
            for i, p_ in enumerate(points[:5]):
                rows = wrap(f"{i + 1}. " + _short(_plain(p_), 44), 166, fs)[:max_rows]
                if y + fs * 1.22 * len(rows) > 146:
                    break
                notes += lines(80, y, rows, fs, anchor="start", fill=CORAL, weight=700)
                y += fs * 1.22 * len(rows) + 5
                fitted += 1
            if fitted == min(len(points), 5):
                break
        if auto:
            self.deck.stock.append(f"c{self.n}-{len(self.cards) + 2} (red pen)")
        if fitted < min(len(points), 5) or len(points) > 5:
            self.deck.stock.append(f"c{self.n}-{len(self.cards) + 2} (red pen: only {fitted} of {len(points)} notes fit the drawing)")
        self.card("redpen", f"{who}'s red pen", f"{len(points)} things to remember",
                         panel or svg(paper(66, 10, 192, 140, [_short(where.upper(), 30)], 8.5, fill="#fff")
                             + notes + sharma(288, 150, 0.62, "flat", "skeptic", arms="point"),
                             f"{who}'s page of red-pen notes: " + "; ".join(_plain(p_) for p_ in points)),
                         "<ol>" + "".join(f"<li>{p}</li>" for p in points) + "</ol>",
                         f"Scribbled by {who} in the margin of \"{where}\".")
        self.cards[-1]["auto"] = auto
        return self

    def oneliner(self, question, line, bubble_text=None, panel=None):
        """The chapter in one sentence, as an answer to a friend's question.
        panel=: draw the moment someone asks and gets this answer; the default is a stock microphone."""
        self.summary = line
        if panel is None:
            self.deck.stock.append(f"c{self.n}-{len(self.cards) + 2} (one breath)")
        return self.card("interview", "Say it in one breath", f"If someone asks \"{question}\"",
                         panel or svg(f'<rect x="146" y="70" width="28" height="44" rx="14" fill="{INK}"/>'
                             f'<path d="M136 96 Q136 128 160 128 Q184 128 184 96" fill="none" stroke="{INK}" stroke-width="4"/>'
                             f'<path d="M160 128 L160 146 M144 148 L176 148" stroke="{INK}" stroke-width="4"/>'
                             + [lambda: chintu(250, 150, 0.7, mood="smile", arms="wave"), lambda: pinky(252, 150, 0.75, mood="grin", arms="up"),
                                lambda: sharma(70, 150, 0.75, "flat", "flat")][(self.n - 1) % 3]()
                             + bubble(30, 12, 260, bubble_text or line, 160, 66, fs=11),
                             "A microphone with the one-line answer above it"),
                         f"<p class=\"big\">\"{line}\"</p>",
                         "Say it out loud once. Now you can explain it to anyone.")

    def quizzes(self, qa, panels=None):
        """qa: [(question, answer, tested_card_title)], 2 or 3. Each becomes a card with a tap-to-reveal answer.
        The third item names the teaching card the question tests: its picture is shown again, because seeing
        the same picture at test helps recall. panels=: optional drawings instead, one per question."""
        self._quiz_cards(qa, panels, "Quick check")
        return self

    def recall(self, qa):
        """'Yaad hai?': 1 or 2 questions about an EARLIER chapter (spacing). qa: [(question, answer, earlier_card_title)]."""
        self._quiz_cards(qa, None, "Yaad hai?")
        self.has_recall = True
        return self

    def _quiz_cards(self, qa, panels, label):
        marks = [(108, 60, HALDI, 214, 70, CORAL), (100, 70, CORAL, 222, 58, HALDI), (112, 52, TEAL2, 210, 76, HALDI)]
        poses = [lambda: chintu(160, 150, 1.0, mood="o", eyes="up"),
                 lambda: pinky(110, 150, 1.0, mood="o", arms="up") + chintu(220, 150, 0.85, mood="smile", arms="wave"),
                 lambda: sharma(120, 150, 1.0, "flat", "skeptic", arms="point") + chintu(225, 150, 0.85, mood="flat", eyes="up")]
        for i, item in enumerate(qa):
            q, a = item[0], item[1]
            ref = item[2] if len(item) > 2 else None
            panel = panels[i] if panels and i < len(panels) and panels[i] else None
            hint = ""
            if panel is None and ref:
                found = self.deck.find(ref)
                if found is None:
                    raise ValueError(f"quiz {q!r}: no card titled {ref!r} written before it")
                panel = _cue(found["panel"])
                hint = f'<p class="small ref">The picture is from the card <i>{escape(_plain(found["title"]))}</i>.</p>'
            if panel is None:
                self.deck.stock.append(f"c{self.n}-{len(self.cards) + 2}")
                x1, y1, c1, x2, y2, c2 = marks[i % 3]
                panel = svg(poses[i % 3]() + text(x1 - 40 if i % 3 else x1, y1, "?", 40, weight=800, fill=c1)
                            + text(x2 + 50 if i % 3 else x2, y2, "?", 30, weight=800, fill=c2), "The cast puzzles over a question")
            badge = f"{label} {i + 1} of {len(qa)}" if label == "Quick check" else label
            self.card("quiz", badge, q, panel, f"<details><summary>Answer</summary><p>{a}</p>{hint}</details>",
                      "Answer in your head first, then tap." if label == "Quick check" else "From an earlier chapter: recalling it again is what makes it stick.")
            self.cards[-1]["ref"] = ref

    def done(self, title, body, moral="Samjha kya? Keep swiping.", panel=None):
        """The payoff. Pass panel= to close the opener's story in a drawing; the default is the cast cheering."""
        if panel is None:
            self.deck.stock.append(f"c{self.n}-{len(self.cards) + 2}")
        panel = panel or svg(chintu(70, 150, 0.95, mood="grin", arms="up") + sharma(160, 150, 0.95, "flat", "skeptic")
                             + pinky(250, 150, 0.95, mood="grin", arms="up") + text(115, 62, "*", 28, fill=HALDI, weight=800)
                             + text(210, 56, "*", 24, fill=CORAL, weight=800), "The cast celebrates the end of the chapter")
        return self.card("done", f"Chapter {self.n} done", title, panel, f"<p>{body}</p>", moral)


class Deck:
    def __init__(self, title, tagline, slug, about="", cast=None, levels=None, source=None, site=None,
                 disclaimer="All people and numbers in the stories are made up, except where a source is linked.",
                 lang="en", left_out=None, caution=None):
        self.title, self.tagline, self.slug, self.about = title, tagline, slug, about
        self.cast = {k: dict(CAST[k], **(cast or {}).get(k, {})) for k in CAST}
        _NAMES.update({k: v["name"] for k, v in self.cast.items()})
        self.levels = levels or LEVELS
        self.source, self.site, self.disclaimer, self.lang = source, site, disclaimer, lang
        self.left_out = left_out  # [(what, why)] for every part of the source or syllabus not on a card
        self.caution = caution  # money, health, legal: shown on the cover AND every chapter's first card
        self.chapters = []
        self.stock = []  # card ids that fell back to a stock drawing

    def chapter(self, level, title, glossary=None, caution=True):
        """level: one of the level ids ('beginner', 'intermediate', 'advanced').
        glossary: [(term, plain one-line meaning)] for words this chapter uses without explaining."""
        if level not in [l["id"] for l in self.levels]:
            raise ValueError(f"unknown level {level!r}; use one of {[l['id'] for l in self.levels]}")
        ch = Chapter(self, level, title, glossary, len(self.chapters) + 1, caution)
        self.chapters.append(ch)
        return ch

    def find(self, title):
        """The card with this exact title, from any chapter written so far."""
        for ch in self.chapters:
            for c in ch.cards:
                if re.sub(r"<[^>]+>", "", c["title"]) == title:
                    return c
        return None

    def level(self, lid):
        return next(l for l in self.levels if l["id"] == lid)

    def before_card(self, ch):
        c = self.cast
        cast = (chintu(56, 150, 0.8, mood="grin") + text(56, 164, f"{c['chintu']['name']}", 9, weight=800)
                + sharma(160, 150, 0.9, "flat", "skeptic") + text(160, 164, f"{c['sharma']['name']}", 9, weight=800)
                + pinky(264, 150, 0.9, mood="smile", arms="up") + text(264, 164, f"{c['pinky']['name']}", 9, weight=800))
        words = "".join(f"<li><b>{t}:</b> {d}</li>" for t, d in ch.glossary)
        who = " ".join(c[k]["line"] for k in ("chintu", "sharma", "pinky"))
        show_caution = self.caution and ch.caution
        if len(ch.glossary) >= 3 or show_caution:
            who = f"{c['chintu']['name']} explains, {c['sharma']['name']} asks for proof, {c['pinky']['name']} asks what you are thinking."
        k = (ch.n - 1) % 3
        cast = (chintu(56, 150, 0.8, mood=["grin", "smile", "o"][k], arms=["down", "wave", "up"][k]) + text(56, 164, f"{c['chintu']['name']}", 9, weight=800)
                + sharma(160, 150, 0.9, "flat", "skeptic", arms=["down", "point", "hold"][k]) + text(160, 164, f"{c['sharma']['name']}", 9, weight=800)
                + pinky(264, 150, 0.9, mood=["smile", "grin", "o"][k], arms=["up", "down", "up"][k]) + text(264, 164, f"{c['pinky']['name']}", 9, weight=800))
        return dict(kind="intro", badge="Before you start", title="The cast, and words this chapter uses" if words else "Meet the cast",
                    panel=svg(cast, f"{c['chintu']['name']}, {c['sharma']['name']} and {c['pinky']['name']}"),
                    body=(f'<p class="caution">{self.caution}</p>' if show_caution else "") + f"<p>{who}</p>" + (f"<ul>{words}</ul>" if words else ""),
                    moral="You can start this chapter cold. Everything it needs is on this card.")
