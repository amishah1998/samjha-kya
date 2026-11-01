"""Neend: the NIH "Your Guide to Healthy Sleep" (2011) as a comic flashcard deck.

Every fact on a card comes from the PDF and ends with pg(n), the PDF page number.
Build: python3 <skill>/scripts/build.py deck.py
"""
from samjha import *

PDF = "https://www.nhlbi.nih.gov/files/docs/public/sleep/healthy_sleep.pdf"
P = pg

LEFT_OUT = [
    ("US numbers and costs (p. 8, 39, 46, 53, 56), including apnea in about 3% of US children and 10% of over-65s (p. 46)", "counts of Americans affected and dollar costs are US-only figures that do not change what a reader should do"),
    ("Sleep in 1910, the 24/7 world, the share of sleepy adults, and screens shortening children's sleep (p. 8)", "background trends; the deck keeps the advice: 7 to 8 hours, screens out of the bedroom"),
    ("Delta waves, deep sleep coming mostly early in the night, REM rebound, why we dream and when we remember dreams (p. 10 to 12)", "brain-wave and dream research; the stages, their order and shares, and what each stage does are on cards"),
    ("Bedwetting and sleepwalking happen in deep sleep (p. 11)", "a side note on timing; sleepwalking itself, and when to see a doctor about it, are on two cards"),
    ("Night-shift mistakes behind nuclear plant accidents and an oil spill (p. 14)", "historic examples; night workers' crash risk, health problems and shift tips are on cards"),
    ("Cytokines making you sleep more when ill (p. 14)", "the deck keeps the stronger point that sleep helps fight infection (p. 20, 21)"),
    ("Jet-lag preparation steps, short trips, and alcohol and caffeine while travelling (p. 16)", "travel detail; daylight, catnaps and the 1 to 2 hours a day limit are on cards"),
    ("Melatonin stopping in the middle of the night (p. 17)", "fine detail; the melatonin supplement facts are on a card"),
    ("Creative problem solving and Mary Shelley (p. 18), and sleep and infant brain development (p. 19)", "study examples; the learning and memory findings they support are on cards"),
    ("C-reactive protein and hardening of the arteries (p. 20), and a study of women's sleep hours and diabetes (p. 21)", "a lab marker and a second study; short sleep's heart risk, the blood-sugar study and women snorers' diabetes risk are on cards"),
    ("New York drivers who fell asleep at the wheel (p. 22)", "a US survey; nodding off without knowing it, and the warning signs and tips, are on cards"),
    ("Rat studies, 8 to 8.5 hours when unrestricted, needs from 7 to 9 or more hours (p. 25)", "research detail; the guide's 7 to 8 hours for adults is on cards"),
    ("More waking at night from midlife on (p. 26)", "a change in sleep pattern, not advice; the older-adults card keeps the causes worth checking, the risks of poor sleep and that the need does not shrink"),
    ("How many children snore, and snoring's link to lower test scores and IQ (p. 37, 38)", "study detail; the guide's advice to take a snoring child to a doctor is on a card"),
    ("Insomnia after 11 September 2001 (p. 41), and sedating antidepressants for insomnia (p. 43)", "a US example and a prescription detail; the cards say to see a doctor before any sleep medicine"),
    ("What doctors measure in primary insomnia: hormone levels, body temperature, heart rate and brain waves (p. 42)", "lab findings a reader cannot check at home; the \"revved up\" idea and the treatments are on cards"),
    ("Adult apnea surgeries (UPPP, tracheostomy) (p. 49), and anticonvulsants or pain relievers for severe restless legs (p. 54)", "specialist treatment detail decided with a doctor"),
    ("Periodic limb movements in sleep (PLMS), restless legs behind a third of insomnia after 60, and its link to ADHD symptoms (p. 53)", "specialist detail; the sign itself (limbs jerking in sleep), who gets restless legs, and the growing-pains mix-up are on cards"),
    ("How to find a qualified US sleep centre, research, clinical trials and contacts (p. 62 to 66)", "US directories and research plans, not advice for readers elsewhere"),
    ("That the stages other than REM also help learning (p. 12), and sleep hormones' role in puberty and fertility (p. 20)", "fine detail; the cards keep that REM builds learning pathways, that broken sleep misses every stage, and the night-shift miscarriage risk"),
]

deck = Deck(
    title="Neend: a sleep guide, card by card",
    tagline="The NIH's 72-page sleep guide, with the doctor signs first.",
    slug="sleep",
    caution="Education, not medical advice. Signs of a sleep problem? See a doctor.",
    source={"title": "Your Guide to Healthy Sleep (NIH Publication 11-5271, 2011)",
            "url": PDF, "pages": 72,
            "note": "Public domain (US federal work). Stories are made up; p. N is the PDF page"},
    disclaimer="",
    left_out=LEFT_OUT,
    cast={"chintu": {"role": "the know-it-all robot", "line": "Chintu the robot explains, sometimes too sure."},
          "sharma": {"line": "Sharma ji wants proof: \"Data dikhao.\""},
          "pinky": {"line": "Pinky asks your questions."}},
)


# ---------------------------------------------------------------- drawing helpers
def tank(x, level, label, color=TEAL2):
    """A tall sleep-pressure tank, `level` from 0 to 1, label under it."""
    h = 92
    fill = h * level
    return (f'<rect x="{x}" y="{40 + h - fill:.0f}" width="44" height="{fill:.0f}" rx="4" fill="{color}"/>'
            f'<rect x="{x}" y="40" width="44" height="{h}" rx="6" fill="none" stroke="{INK}" stroke-width="2"/>'
            + text(x + 22, 146, label, 9, weight=700))


def car(x, y, color=BLUE):
    """A side-on car whose wheels sit on y."""
    return (f'<path d="M{x + 22} {y - 34} L{x + 40} {y - 52} L{x + 86} {y - 52} L{x + 104} {y - 34} Z" fill="{color}"/>'
            f'<rect x="{x}" y="{y - 36}" width="128" height="26" rx="8" fill="{color}"/>'
            f'<path d="M{x + 44} {y - 47} L{x + 60} {y - 47} L{x + 60} {y - 36} L{x + 32} {y - 36} Z" fill="{FACE}"/>'
            f'<path d="M{x + 66} {y - 47} L{x + 84} {y - 47} L{x + 96} {y - 36} L{x + 66} {y - 36} Z" fill="{FACE}"/>'
            f'<circle cx="{x + 28}" cy="{y - 8}" r="9" fill="{INK}"/><circle cx="{x + 100}" cy="{y - 8}" r="9" fill="{INK}"/>'
            f'<circle cx="{x + 28}" cy="{y - 8}" r="3.5" fill="{GREY}"/><circle cx="{x + 100}" cy="{y - 8}" r="3.5" fill="{GREY}"/>'
            f'<rect x="{x + 120}" y="{y - 30}" width="8" height="6" rx="2" fill="{HALDI}"/>')


def driver(x, y):
    """A sleepy head in the car window: car(x, y) puts the window here."""
    return (f'<circle cx="{x + 54}" cy="{y - 46}" r="7" fill="{SKIN}"/>'
            f'<path d="M{x + 51} {y - 46} l3 1 M{x + 57} {y - 46} l-3 1" stroke="{INK}" stroke-width="1.2"/>')


def loop_back(x1, x2, y, depth=36):
    """A dashed return path from under box x1 back up to box x2."""
    return (f'<path d="M{x1} {y} L{x1} {y + depth} L{x2} {y + depth} L{x2} {y + 6}" fill="none" stroke="{INK}" stroke-width="1.6" stroke-dasharray="4 3"/>'
            f'<path d="M{x2 - 5} {y + 12} L{x2} {y + 5} L{x2 + 5} {y + 12}" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')


def aunty(x, y, s=1.0, mood="o", arms="down"):
    """Sharma aunty."""
    return person(x, y, s, mood=mood, shirt=GREEN, arms=arms, hair_col="#2b2320", hair="bun", bindi=True)


def mummy(x, y, s=1.0, mood="flat", arms="down"):
    """Pinky's mummy."""
    return person(x, y, s, mood=mood, shirt="#8a5a9e", arms=arms, hair_col="#3b302b", hair="long", bindi=True)


def mausi(x, y=150, s=1.0, mood="o", arms="down"):
    """Golu's mausi (Lata mausi in the last chapter)."""
    return person(x, y, s, mood=mood, shirt=CORAL, arms=arms, hair_col="#6d6d6d", hair="bun", bindi=True)


def golu(x, y=150, s=0.6, mood="grin", arms="down"):
    """Golu, Pinky's six-year-old cousin."""
    return person(x, y, s, mood=mood, shirt=HALDI, arms=arms, hair_col="#2b2320")


def rohit(x, y=150, s=1.0, mood="flat", arms="down"):
    """Rohit from accounts."""
    return person(x, y, s, mood=mood, shirt=GREEN, arms=arms, hair_col="#3b302b")


def doctor(x, y=150, s=1.0, mood="smile", arms="down"):
    """A doctor in a white coat with a stethoscope."""
    return (person(x, y, s, mood=mood, shirt="#ffffff", arms=arms, hair_col="#2b2320", hair="bun")
            + f'<path d="M{x - 8 * s:.1f} {y - 40 * s:.1f} Q{x - 9 * s:.1f} {y - 20 * s:.1f} {x:.1f} {y - 18 * s:.1f} Q{x + 9 * s:.1f} {y - 20 * s:.1f} {x + 8 * s:.1f} {y - 40 * s:.1f}" '
              f'fill="none" stroke="{INK}" stroke-width="{1.6 * s:.1f}"/><circle cx="{x:.1f}" cy="{y - 17 * s:.1f}" r="{2.6 * s:.1f}" fill="{GREY}"/>')


def sharma_in_bed(x, y=150, w=150):
    """bed() with the sleeper given Sharma ji's grey hair and moustache."""
    hx, hy = x + 26, y - 34
    return (bed(x, y, w, sleeper=True)
            + f'<path d="M{hx - 11} {hy - 2} Q{hx - 11} {hy - 13} {hx} {hy - 12} Q{hx + 11} {hy - 13} {hx + 11} {hy - 2} Q{hx} {hy - 8} {hx - 11} {hy - 2} Z" fill="{GREY}"/>'
            + f'<path d="M{hx - 6} {hy + 4} Q{hx} {hy + 1} {hx + 6} {hy + 4} Q{hx} {hy + 6} {hx - 6} {hy + 4} Z" fill="{INK}"/>')


def awake_in_bed(x, y=150, w=130):
    """bed() with a sleeper whose eyes are wide open."""
    hx, hy = x + 26, y - 34
    return (bed(x, y, w, sleeper=False)
            + f'<circle cx="{hx}" cy="{hy}" r="11" fill="{SKIN}"/>'
            + f'<circle cx="{hx - 4}" cy="{hy - 2}" r="2.2" fill="#fff" stroke="{INK}" stroke-width="1"/><circle cx="{hx + 4}" cy="{hy - 2}" r="2.2" fill="#fff" stroke="{INK}" stroke-width="1"/>'
            + f'<circle cx="{hx - 4}" cy="{hy - 2}" r="0.9" fill="{INK}"/><circle cx="{hx + 4}" cy="{hy - 2}" r="0.9" fill="{INK}"/>')


def legs(x, y=150):
    """Two lower legs with shoes and tingle marks: restless legs."""
    return (f'<rect x="{x}" y="{y - 86}" width="12" height="76" rx="5" fill="{SKIN2}"/><rect x="{x + 26}" y="{y - 86}" width="12" height="76" rx="5" fill="{SKIN2}"/>'
            f'<ellipse cx="{x + 8}" cy="{y - 6}" rx="11" ry="5" fill="{INK}"/><ellipse cx="{x + 34}" cy="{y - 6}" rx="11" ry="5" fill="{INK}"/>'
            f'<path d="M{x - 10} {y - 76} q-6 6 0 12 q6 6 0 12 q-6 6 0 12 M{x + 48} {y - 76} q6 6 0 12 q-6 6 0 12 q6 6 0 12" fill="none" stroke="{CORAL}" stroke-width="2.2"/>')


def week(x, y, marks, w=26, gap=4, color=CORAL):
    """Seven day boxes M to S; `marks` are the indexes that get a coral dot."""
    out = ""
    for i, d in enumerate("MTWTFSS"):
        bx = x + i * (w + gap)
        out += (f'<rect x="{bx}" y="{y}" width="{w}" height="{w}" rx="4" fill="#fff" stroke="{INK}" stroke-width="1.2"/>'
                + text(bx + w / 2, y + w * 0.4, d, min(9.5, w * 0.38), weight=800))
        if i in marks:
            out += f'<circle cx="{bx + w / 2}" cy="{y + w * 0.7:.1f}" r="{w * 0.16:.1f}" fill="{color}"/>'
    return out


def pills(x, y, n=4):
    """A blister strip of pills."""
    out = f'<rect x="{x}" y="{y}" width="{14 * n + 6}" height="22" rx="4" fill="#dfe6ea" stroke="{INK}" stroke-width="1.2"/>'
    for i in range(n):
        out += f'<ellipse cx="{x + 10 + i * 14}" cy="{y + 11}" rx="5" ry="7" fill="#fff" stroke="{INK}" stroke-width="1"/>'
    return out


def cpap(x, y=150):
    """A small CPAP box on the floor."""
    return (f'<rect x="{x}" y="{y - 38}" width="52" height="38" rx="6" fill="{TEAL2}"/>'
            + text(x + 26, y - 14, "CPAP", 10, weight=800, fill="#fff"))


def armchair(x, y=150):
    """A coral armchair standing on y; x is its left edge."""
    return (f'<rect x="{x}" y="{y - 48}" width="70" height="20" rx="6" fill="{CORAL}"/><rect x="{x}" y="{y - 70}" width="14" height="42" rx="5" fill="{CORAL}"/>'
            f'<rect x="{x + 6}" y="{y - 28}" width="6" height="28" fill="{WOOD}"/><rect x="{x + 60}" y="{y - 28}" width="6" height="28" fill="{WOOD}"/>')


def table2(head, rows, first=30):
    """A two-column table with a narrow label column, so the facts in the second column get the room."""
    return table(head, rows).replace('<table class="t">', f'<table class="t"><colgroup><col style="width:{first}%"><col></colgroup>', 1)


def factboard(facts, label):
    """Myth-buster panel: each fact pinned up in a short form that keeps its qualifier, with a tick.
    Three facts leave room for Sharma ji checking them; four fill a 2 by 2 grid."""
    out = ""
    four = len(facts) > 3
    spots = [(14, 10), (166, 10), (14, 86), (166, 86)] if four else [(14, 12), (166, 12), (14, 86)]
    for i, f in enumerate(facts[:4]):
        cx, cy = spots[i]
        out += paper(cx, cy, 136, 62, wrap(f, 122, 9.5)[:3], 9.5, rot=[-2, 2, 1.5, -1.5][i], fill="#fff") + tick(cx + 122, cy + 50, 1.1)
    if not four:
        out += sharma(240, 150, 0.72, "flat", "skeptic", arms="point")
    return svg(out, label, floor=not four)


def notes(x, y, w, h, rows, fs=12.5):
    """Sharma ji's red-pen page: a white sheet with short notes written in red, well spaced.
    The font shrinks so the longest note fits the sheet (bold text runs about 0.6 em a letter)."""
    fs = round(min(fs, (w - 20) / (0.6 * max(len(r) for r in rows))), 1)
    return (f'<g class="lbl"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="#fff" stroke="{INK}" stroke-width="1.2"/>'
            + lines(x + 10, y + 8 + fs, rows, fs, anchor="start", fill=CORAL, weight=800, lh=1.75) + "</g>")


# ======================= BEGINNER 1 =======================
ch = deck.chapter("beginner", "What is sleep, and what makes you sleepy?", glossary=[
    ("REM", "rapid eye movement: the dreaming stage."),
    ("PG", "a paying-guest room."),
    ("Non-REM sleep", "the three other stages."),
    ("Deep sleep", "stage 3, the hardest to wake from."),
    ("Body clock", "the brain's timer for sleep and waking."),
    ("Melatonin", "a hormone that makes you sleepy at night."),
])

ch.opener(
    svg(moon(150, 30, 13)
        + pinky(70, 150, mood="grin", arms="hold") + phone(82, 94, ["47"], fs=10, h=44, w=28)
        + chintu(165, 150, 0.9, mood="o")
        + sharma(262, 150, 0.95, "flat", "skeptic")
        + bubble(8, 8, 124, "Sleep is just switch-off.", 70, 64)
        + bubble(200, 18, 112, "Data dikhao.", 262, 62),
        "Pinky in her PG room at night on reel 47, while Sharma ji asks for proof"),
    scene("1:30 am, a PG room. Pinky is on reel number 47.")
    + talk(("pinky", "Sleep is just switch-off. I can do it later."),
           ("sharma", "Data dikhao."),
           ("chintu", f"The guide says spend about one-third of your time sleeping {P(7)}. Asleep, your brain is hard at work building pathways for learning and memory {P(7)}.")),
    "Sleep is not switch-off time. Your brain uses it to learn and remember.")

ch.chat("Lights off, brain on",
        svg(bed(14, 150, 150, sleeper=True)
            + sign(20, 14, 128, ["LIGHTS OFF,", "BRAIN ON"], fs=10, fill=HALDI)
            + text(84, 66, "learning, memory: busier", 9, weight=700, fill=TEAL)
            + chintu(266, 150, 0.9, mood="grin", arms="wave")
            + bubble(170, 8, 144, "No major organ, the brain included, shuts down", 266, 60, fs=9.5),
            "A sleeper in bed under a sign saying lights off, brain on, while Chintu says no major organ shuts down"),
        [("pinky", "Does the brain switch off when we sleep?"),
         ("chintu", f"No major organ, the brain included, shuts down {P(28)}. Some work speeds up: certain hormones, and the <b>learning and memory</b> pathways {P(28)}.")],
        points=[f"<b>Brain on</b>: no major organ shuts down in sleep {P(28)}",
                f"In light sleep, heart rate and breathing slow {P(10)}"],
        moral="Lights off, brain on: no major organ shuts down in sleep.", key="brain on")

ch.picture("One night, four stages, on repeat",
           svg(text(160, 26, "ONE NIGHT OF SLEEP", 11, weight=800, fill=TEAL)
               + flow(["Stage 1", "Stage 2", "Stage 3", "REM"], y=44, x0=12, w=58, gap=18, h=34, fs=10)
               + text(41, 94, "light", 9) + text(117, 94, "slower", 9) + text(193, 94, "deep", 9) + text(269, 94, "dreams", 9)
               + loop_back(269, 41, 100, 30)
               + text(155, 146, "then the cycle repeats all night", 9, weight=700),
               "Four boxes, stage 1, 2, 3 and REM, with a dashed arrow looping back to the start", floor=False),
           f"<p>Sleep starts with <b>non-REM</b> sleep {P(10)}:</p>"
           f"<ol><li>Stage 1, light: noises wake you easily {P(10)}.</li>"
           f"<li>Stage 2: slower brain waves {P(10)}.</li>"
           f"<li>Stage 3, deep sleep: very hard to wake from {P(11)}.</li>"
           f"<li><b>REM</b>, about an hour to an hour and a half after you fall asleep {P(12)}.</li></ol>"
           f"<p>The stages repeat all night; REM grows longer while deep sleep gets shorter {P(12)}. "
           f"How rested you feel depends on this timing, not only on total hours {P(10)}.</p>",
           "Sleep is not one long blank. It is a loop that repeats all night.", key="REM")

ch.chat("Sleeping through the baraat",
        svg(sign(14, 14, 92, "DHOL BAND", fs=9, fill=HALDI)
            + text(40, 56, "dhum", 12, weight=800, fill=CORAL) + text(84, 70, "dhum!", 13, weight=800, fill=CORAL)
            + sign(26, 76, 86, "DEEP SLEEP", fs=9, fill=BLUE, color="#fff")
            + bed(20, 150, 120, sleeper=True)
            + pinky(200, 150, 0.9, mood="o", arms="up")
            + chintu(276, 150, 0.85, mood="smile")
            + bubble(150, 10, 164, "How is Golu still asleep?", 200, 62),
            "A dhol band plays loudly while a small child sleeps on in deep sleep, and Pinky is amazed"),
        [("pinky", "The dhol is shaking the windows. How is Golu still asleep?"),
         ("chintu", f"<b>Deep sleep</b>, stage 3: very hard to wake from, and the restorative stage you need to feel rested {P(11)}. It changes with age, so children can sleep through loud noises and may not wake when moved {P(25)}"),
         ("sharma", "Mausi carried him to the car!")],
        moral="Deep sleep is the stage that is hardest to wake from, and children can sleep through a lot.",
        badge="Story", key="deep sleep")

ch.glance("Your night, by the numbers",
          svg(layers([("Stage 2", TEAL2, "almost half the night"),
                      ("Deep (stage 3)", BLUE, "about one-fifth"),
                      ("REM", CORAL, "about one-fifth"),
                      ("Stage 1", HALDI, "the rest, light")], x=16, y=26, w=150, h=24, gap=6)
              + text(160, 16, "WHERE ADULT SLEEP TIME GOES", 9, weight=800, fill=TEAL)
              + text(160, 150, "Babies: half or more is REM", 9, weight=700),
              "Four bands: stage 2 is almost half the night, deep sleep and REM about a fifth each", floor=False),
          table2(["Stage", "What happens"], [
              ["1", "Light; easy to wake"],
              ["2", "Eyes still; slower waves"],
              ["3", "Deep; hard to wake"],
              ["REM", "Eyes dart; dreams; arm and leg muscles paralysed for a while"],
          ], first=18)
          + f"<p>Stages from the guide's table {P(11)}. In REM, breathing gets fast and irregular, and heart rate and blood pressure rise {P(11)}. "
            f"Almost half the night is <b>stage 2</b>; about one-fifth each is deep sleep and REM; babies spend half or more in REM {P(12)}.</p>",
          "Almost half your night is stage 2, not dreams.", key="stage 2")

ch.chat("The clock in your head",
        svg(sun(40, 40, 14) + text(40, 78, "Light: be alert", 9, weight=700)
            + clock(160, 62, 34, 11, 50) + text(160, 112, "BODY CLOCK", 10, weight=800, fill=TEAL)
            + moon(282, 40, 14) + text(276, 78, "Dark: melatonin", 9, weight=700)
            + arrow(64, 50, 120, 58) + arrow(256, 50, 200, 58),
            "A sun and a moon on either side of a body clock: light means alert, dark means melatonin"),
        [("pinky", "Why do I get sleepy at night and not at noon?"),
         ("chintu", f"Your <b>body clock</b>, a small bundle of brain cells, reads light through your eyes {P(13)}. As evening comes, it makes your body release <b>melatonin</b>, a hormone that makes you sleepy {P(13)}.")],
        points=[f"Sleepiest: <b>midnight to 7 am</b>; most alert in daylight {P(13)}",
                f"Melatonin builds up through the early evening {P(17)}"],
        moral="Light tells your brain the time. Melatonin tells your body it is bedtime.", key="body clock")

ch.chat("The 2:30 pm office slump",
        svg(desk(10, 112, 110) + monitor(22, 50, 86, 54, ["Q3 REVIEW", "slide 41"], fs=9)
            + clock(150, 30, 17, 2, 30)
            + sign(112, 52, 78, ["1 PM TO 4 PM:", "MILD DIP"], fs=9, fill=HALDI)
            + rohit(160, 150, 0.85, mood="o")
            + text(184, 98, "z", 12, fill=BLUE, weight=800) + text(194, 86, "z", 15, fill=BLUE, weight=800)
            + sharma(262, 150, 0.95, "flat", "skeptic")
            + bubble(206, 10, 108, "Biryani effect. Simple.", 262, 62, fs=10),
            "A colleague yawns at his desk at 2:30 pm under a sign saying 1 pm to 4 pm is a mild dip, while Sharma ji blames the biryani"),
        [("sharma", "Biryani effect. Simple."),
         ("chintu", f"Partly your <b>body clock</b>. You may feel mildly sleepy between 1 pm and 4 pm, when your body makes another rise in melatonin {P(13)}.")],
        intro="2:30 pm, after a heavy biryani lunch. Rohit from accounts is fighting to keep his eyes open.",
        points=[f"<b>1 pm to 4 pm</b>: a mild dip, from more melatonin {P(13)}"],
        moral="A mild dip between 1 and 4 pm is your body clock at work, not only the biryani.",
        badge="Story", key="1 pm to 4 pm")

ch.chat("The sleep-pressure tank",
        svg(tank(30, 0.18, "8 AM") + tank(110, 0.55, "3 PM", HALDI) + tank(190, 0.92, "11 PM", CORAL)
            + arrow(80, 92, 104, 92) + arrow(160, 92, 184, 92)
            + text(130, 28, "ADENOSINE BUILDS UP", 9, weight=800, fill=TEAL)
            + chintu(278, 150, 0.7, mood="o", eyes="up"),
            "Three tanks filling up through the day, from 8 am to 11 pm, labelled adenosine builds up"),
        [("pinky", "Why do I get sleepier the longer I stay up?"),
         ("chintu", f"<b>Adenosine</b> builds up in your blood while you are awake, and sleep breaks it down. Its level may help trigger sleep {P(13)}"),
         ("sharma", "And after a few short nights?"),
         ("chintu", f"A <b>sleep debt</b>: you may sleep longer than normal, or doze at odd times {P(13)}")],
        moral="Every waking hour tops up the tank. Sleep drains it.", key="adenosine")

ch.glance("Mausi lands in Tokyo",
          svg(sign(18, 14, 96, "TOKYO: 8 AM", fs=9, fill="#fff") + clock(66, 64, 20, 8, 0)
              + sign(206, 14, 96, "BODY: 4:30 AM", fs=9, fill=BLUE, color="#fff") + moon(254, 62, 15)
              + f'<g transform="translate(160 36) rotate(-12)"><ellipse rx="26" ry="5" fill="{GREY}"/><path d="M-4 0 L-14 -16 L-6 -16 L8 0 Z M-4 0 L-14 16 L-6 16 L8 0 Z M-22 0 L-28 -9 L-24 -9 L-16 0 Z" fill="{GREY}"/></g>'
              + text(160, 70, "JET LAG", 11, weight=800, fill=CORAL)
              + mausi(160, 150, 0.85, mood="sad")
              + f'<rect x="186" y="118" width="30" height="32" rx="4" fill="{WOOD}"/><rect x="196" y="112" width="10" height="7" rx="2" fill="none" stroke="{INK}" stroke-width="2"/>',
              "Mausi with her suitcase and jet lag, between a Tokyo clock showing 8 am and a moon showing her body thinks it is 4:30 am"),
          scene("Mausi flies east, Delhi to Tokyo. Clocks say 8 am; her body says 4:30 am.")
          + table2(["<b>Jet lag</b>", "What happens"], [
              ["Signs", f"sleepy by day, poor sleep at night, poor focus, confusion, nausea, irritability {P(15)}"],
              ["East or west", f"east is usually worse: your clock copes better with a longer day {P(16)}"],
              ["Reset", f"1 to 2 hours a day at best, so it can take over a week {P(28)}"],
              ["Help", f"time outdoors in daylight; 10 to 15 minute catnaps, no long naps {P(16)}"],
          ], first=28),
          "Your body clock does not change time zones when the plane does.", badge="Story", key="jet lag")

ch.watch_out("\"I will train myself to need 5 hours\"",
             svg(calendar(22, 30, "DAY 1", "5h") + calendar(76, 30, "DAY 7", "5h") + calendar(130, 30, "DAY 30", "5h", color=GREY)
                 + text(100, 100, "still tired", 12, weight=800, fill=CORAL)
                 + text(100, 124, "Adults: 7 to 8 hours", 9, weight=700, fill=TEAL)
                 + pinky(252, 150, mood="sad")
                 + bubble(194, 8, 120, "Kal se pakka: 5 hours a night", 252, 60, fs=10),
                 "Three calendar pages, each showing 5 hours, and Pinky still tired"),
             talk(("pinky", "Kal se pakka: 5 hours a night until my body gets used to it."),
                  ("chintu", f"Myth: people can learn to get by on under 6 hours {P(8)}. You cannot adapt to less sleep than you need {P(13)}."),
                  ("sharma", "How much, then?"),
                  ("chintu", f"Adults: at least <b>7 to 8 hours</b> {P(8)}. Preschoolers 11 to 12, school-age children at least 10, teens 9 to 10 {P(25)}")),
             "You cannot train your body to need less sleep than it needs.", key="7 to 8 hours")

ch.glance("Tonight's 5 habits",
          svg(paper(14, 22, 190, 106, ["TONIGHT'S 5", "1. Same times, daily", "2. No late chai", "3. No nightcap",
                                       "4. Cool, dark, no phone", "5. Awake 20 min? Get up"], fs=13, anchor="start", fill="#fff")
              + moon(234, 26, 11)
              + pinky(262, 150, 0.9, mood="grin", arms="up"),
              "Pinky cheers next to her list of five habits for tonight, under the moon"),
          "<p>From the guide's 13 tips:</p>"
          + table(["Habit", "Why"], [
              ["<b>Same times</b> daily", f"lie-ins do not fully repay the week {P(33)}"],
              ["No late chai or coffee", f"caffeine can last up to 8 hours {P(33)}"],
              ["No drink at bedtime", f"alcohol blocks deep and REM sleep {P(31)}"],
              ["Cool, dark, no screens", f"a TV or phone steals sleep {P(35)}"],
              ["Awake 20+ min? Get up", f"relax till sleepy {P(35)}"],
          ])
          + f"<p>Still sleeping badly? <b>See a doctor</b> {P(35)}.</p>",
          "Fixed times, no late caffeine or alcohol, a cool dark room, and get up if sleep will not come.",
          badge="Start tonight", key="same times")

ch.myths([
    ("Sleep is when the brain shuts down to rest.", f"No major organ shuts down in sleep, the brain included {P(28)}."),
    ("You can learn to get by on under 6 hours.", f"Adults need at least 7 to 8 hours to be well rested {P(8)}."),
    ("Your body adjusts to new sleep hours fast.", f"Most people reset their clock by only 1 to 2 hours a day {P(28)}."),
])

ch.redpen([f"Sleep is busy work, not off time {P(28)}.", f"Stages loop; REM grows near morning {P(12)}.",
           f"Adenosine builds while you are awake {P(13)}.", f"Light sets the body clock {P(13)}.", f"Sleepiest: midnight to 7 am {P(13)}."],
          where="the sleep basics",
          panel=svg(notes(12, 12, 180, 104, ["Busy work, not off time", "Stages loop all night", "Light sets the clock",
                                              "Sleepiest: 12 to 7 am"])
                    + moon(212, 26, 12)
                    + sharma(262, 150, 1.0, "flat", "skeptic", arms="point"),
                    "Sharma ji points at his red-pen page: sleep is busy work, stages loop, light sets the clock, sleepiest midnight to 7 am"))

ch.oneliner("why do I even get sleepy?",
            f"Adenosine piles up while you are awake, and at night your body clock releases melatonin {P(13)}.",
            panel=svg(moon(40, 22, 11) + bed(106, 150, 104)
                      + golu(66, 150, 0.7, mood="o")
                      + bubble(8, 40, 112, "Why do I even get sleepy?", 66, 92, fs=10)
                      + pinky(256, 150, 0.95, mood="smile", arms="hold")
                      + bubble(130, 8, 184, "Adenosine piles up while you are awake", 256, 62, fs=10),
                      "At bedtime Golu asks why he gets sleepy, and Pinky answers in one breath"))

ch.quizzes([
    ("Golu sleeps through a dhol band. What stage is he probably in?",
     f"Stage 3, deep sleep. It is very hard to wake from, and children can sleep through loud noises {P(11)} {P(25)}.",
     "Sleeping through the baraat"),
    ("Why can you not act out the fight scene you are dreaming?",
     f"In REM sleep your arm and leg muscles are temporarily paralysed, so the dream stays in your head {P(11)}.",
     "Your night, by the numbers"),
    ("You slept well, yet at 2:30 pm your eyes droop. Why?",
     f"Your body clock adds another small rise in melatonin between 1 pm and 4 pm {P(13)}.",
     "The 2:30 pm office slump"),
])

ch.done("Pinky puts the phone down at 11",
        "Reel 47 can wait. Pinky now knows her brain has a night shift of its own: four stages on loop, a tank to empty, and a clock that runs on light. "
        "Chintu grins: \"Picture abhi baaki hai, mere dost\" (Om Shanti Om, 2007). Sharma ji, next door, finally hears silence.",
        panel=svg(moon(36, 32, 14) + clock(100, 40, 20, 11, 0) + bed(14, 150, 120)
                  + desk(190, 116, 56) + phone(198, 84, ["OFF"], fs=8, h=32, w=40)
                  + pinky(282, 150, 0.9, mood="grin", arms="up")
                  + chintu(160, 150, 0.6, mood="grin"),
                  "Pinky cheers at 11 pm with her phone off on the table and the bed ready"))


# ======================= BEGINNER 2: SAFETY FIRST =======================
ch = deck.chapter("beginner", "When does bad sleep need a doctor?", glossary=[
    ("Sleep disorder", "a medical problem that spoils your sleep."),
    ("Sleep apnea", "breathing that keeps stopping during sleep."),
    ("Sleep diary", "a daily note of your sleep."),
    ("ADHD", "trouble sitting still and paying attention."),
    ("Sleep specialist", "a doctor trained in sleep problems."),
])

ch.opener(
    svg(phone(14, 20, ["FAMILY", "GROUP", "Always", "tired.", "Normal!"], fs=10, h=108, w=66)
        + mummy(118, 150, 0.85, mood="flat")
        + pinky(196, 150, 0.85, mood="o")
        + chintu(272, 150, 0.85, mood="smile", arms="wave")
        + bubble(214, 10, 100, "Kitni raatein?", 272, 60),
        "Mummy's message on the family group says always tired is normal, and Chintu asks how many nights"),
    scene("Family WhatsApp group, 10 pm.")
    + talk(("Mummy", "I wake up tired every day. Everyone does. Normal."),
           ("chintu", f"Sholay (1975) asked \"Kitne aadmi the?\" I ask: kitni raatein? A sign on 3 or more nights a week is worth telling your doctor {P(40)}. Tired after a full night in bed? You may have a sleep disorder {P(59)}"),
           ("sharma", f"Many go unrecognised: tell the doctor what you notice {P(9)}")),
    "Signs on 3 or more nights a week are worth telling a doctor about.")

ch.glance("Night signs: count them",
          svg(text(116, 16, "3 OR MORE NIGHTS A WEEK?", 9, weight=800, fill=TEAL)
              + week(14, 24, {0, 2, 3, 5})
              + awake_in_bed(14, 150, 140)
              + clock(196, 98, 20, 12, 40) + text(196, 132, "40 min awake", 9, weight=700)
              + mummy(274, 150, 0.85, mood="sad"),
              "A week with four nights marked, and Mummy lying awake for 40 minutes"),
          table2(["Sign", "What it looks like"], [
              ["Falling asleep", "takes <b>more than 30 minutes</b>"],
              ["In the night", "you wake often and cannot drift off again"],
              ["Early morning", "you wake too early"],
              ["After 7 to 8 hours or more", "you often still do not feel rested"],
          ], first=36)
          + f"<p>All four are on the guide's list: talk to your doctor if any shows up on <b>3 or more nights</b> a week {P(40)}. "
            "Mummy lies awake 40 minutes on 4 nights a week (our example): that counts.</p>",
          "Over 30 minutes to fall asleep, on 3 or more nights a week, is a sign to report.", key="3 or more nights")

ch.chat("Signs your family notices",
        svg(paper(14, 14, 140, 84, ["BED PARTNER SAW:", "1. Loud snores", "2. Gasps, chokes", "3. Breathing stops", "4. Legs jerk"], fs=10, anchor="start", fill="#fff")
            + aunty(202, 150, 0.9, mood="o", arms="hold")
            + sharma(282, 150, 0.85, "flat", "flat")
            + bubble(162, 8, 152, "He snores, gasps, and then his breathing just stops.", 202, 64, fs=9.5),
            "Sharma aunty, holding up her list of what she saw at night, says he snores, gasps and stops breathing, while Sharma ji looks blank"),
        [("Sharma aunty", "He snores, gasps, and then his breathing just stops."),
         ("chintu", f"Signs your <b>bed partner</b> sees: loud snoring, snorting, gasping or choking, or breathing that stops for short periods {P(40)}"),
         ("pinky", "And legs or arms that jerk in sleep?"),
         ("chintu", f"Also a sign, like creeping, tingling legs that ease when you move or rub them, especially in the evening {P(40)}")],
        moral="You cannot see yourself asleep, so ask the person next to you.", key="bed partner")

ch.glance("Signs in the daytime",
          svg(desk(12, 114, 120) + chai(40, 114, 0.9, steam=False) + chai(60, 114, 0.9, steam=False) + chai(80, 114, 0.9, steam=False)
              + text(60, 132, "cup number 6", 8, weight=700)
              + rohit(170, 150, 0.85, mood="flat")
              + text(196, 78, "z", 12, fill=BLUE, weight=800) + text(206, 66, "z", 15, fill=BLUE, weight=800)
              + sign(212, 10, 102, ["ASLEEP IN", "5 MINUTES"], fs=9, fill=CORAL, color="#fff")
              + clock(268, 76, 18, 3, 5),
              "Rohit nods off at his desk beside six cups of tea, with a sign saying asleep in 5 minutes"),
          table2(["Sign", "Looks like"], [
              ["Sleepy in the day", "asleep <b>within 5 minutes</b> given a chance, or at odd times"],
              ["Stimulants", "you need them to stay awake"],
              ["Strong feelings", "sudden weakness when angry, afraid or laughing"],
              ["Dozing, waking", "dreamlike visions, or you cannot move"],
          ], first=34)
          + f"<p>All four are on the guide's list of signs {P(40)}.</p>",
          "Falling asleep within 5 minutes of a chance to nap is a sign, not a talent.", key="5 minutes")

ch.watch_out("Loud snoring with pauses is not a joke",
             svg(text(160, 18, "ONE NIGHT, RECORDED", 9, weight=800, fill=TEAL)
                 + f'<path d="M14 44 q6 -22 12 0 t12 0 t12 0 t12 0 t12 0" fill="none" stroke="{CORAL}" stroke-width="2.6"/>'
                 + f'<path d="M74 44 L170 44" stroke="{GREY}" stroke-width="2.6" stroke-dasharray="5 4"/>'
                 + f'<path d="M170 44 q8 -34 16 0 q8 34 16 0" fill="none" stroke="{CORAL}" stroke-width="3"/>'
                 + f'<path d="M202 44 q6 -22 12 0 t12 0 t12 0 t12 0" fill="none" stroke="{CORAL}" stroke-width="2.6"/>'
                 + text(44, 74, "snore", 10, weight=700) + text(122, 74, "pause", 10, weight=800, fill=CORAL)
                 + text(186, 74, "SNORT", 10, weight=800, fill=CORAL) + text(240, 74, "snore", 10, weight=700)
                 + aunty(40, 150, 0.8, mood="o")
                 + sharma_in_bed(90, 150, 130),
                 "A sound line: snoring, a flat pause with no breath, then a loud snort, above Sharma ji asleep"),
             talk(("pinky", "His snoring is a family joke. Harmless?"),
                  ("chintu", f"Loud, frequent snoring with <b>pauses in breathing</b> is the hallmark of sleep apnea {P(37)}. Not everyone who snores has it {P(36)}, but it is serious, so get it checked {P(30)}."),
                  ("sharma", f"Untreated, apnea raises blood pressure and heart attack and stroke risk {P(44)}")),
             "Snoring with pauses in breathing needs a doctor, not a joke on the family group.", key="pause")

ch.chat("Golu is not sleepy. He is wild.",
        svg(clock(40, 34, 18, 10, 30) + text(40, 66, "10:30 pm", 9, weight=700)
            + sign(6, 74, 100, ["HYPERACTIVE,", "NOT SLEEPY"], fs=9, fill=HALDI)
            + f'<rect x="80" y="104" width="120" height="30" rx="8" fill="{BLUE}"/><rect x="80" y="134" width="10" height="16" fill="{INK}"/><rect x="190" y="134" width="10" height="16" fill="{INK}"/>'
            + golu(140, 104, 0.6, mood="grin", arms="up")
            + text(104, 30, "boing!", 11, weight=800, fill=CORAL) + text(160, 40, "boing!", 11, weight=800, fill=CORAL)
            + mausi(268, 150, 0.9, mood="sad")
            + bubble(200, 8, 114, "He is not even yawning!", 268, 64, fs=10),
            "Golu bounces on the sofa at 10:30 pm, hyperactive, not sleepy, while his tired Mausi watches"),
        [("Mausi", "He is not even yawning! Too much sugar?"),
         ("chintu", f"Or too little sleep. Unlike adults, children short of sleep typically turn <b>hyperactive</b>, irritable and inattentive, not sleepy {P(30)}. It may be mistaken for ADHD {P(30)}"),
         ("sharma", f"And a child with a sleep disorder often seems overactive, cannot focus, and may not do their best at school {P(40)}")],
        intro="10:30 pm, a week of late nights.",
        moral="A tired child can look wild, not sleepy. Check the child's sleep.", badge="Story", key="hyperactive")

ch.watch_out("A child who snores 3 to 4 nights a week",
             svg(sticky(14, 18, "MON", rot=-6) + sticky(50, 22, "TUE", rot=4) + sticky(86, 18, "THU", rot=-3) + sticky(122, 22, "FRI", rot=5)
                 + text(84, 60, "loud snoring, 3 to 4 nights", 9, weight=800, fill=CORAL)
                 + bed(14, 150, 120, sleeper=True)
                 + mausi(220, 150, 0.9, mood="o", arms="hold")
                 + phone(228, 94, ["Dr."], fs=10, h=36, w=28)
                 + chintu(286, 150, 0.6, mood="smile"),
                 "Four sticky notes mark the nights a child snored loudly; Mausi picks up the phone to call the doctor"),
             talk(("Mausi", "Golu snores. Cute, na?"),
                  ("chintu", f"See a doctor if a child snores loudly <b>3 to 4 times a week</b>, especially with pauses in breathing, hyperactivity or daytime sleepiness {P(38)}. Children with apnea snore, snort or gasp, often seem <b>agitated</b>, not sleepy, and can do worse at school {P(47)}"),
                  ("sharma", f"Removing adenoids and tonsils often cures children's snoring and apnea {P(38)}")),
             "Loud snoring on 3 to 4 nights a week is a reason to take a child to the doctor.", key="3 to 4")

ch.chat("Meenu didi starts snoring",
        svg(sign(10, 8, 150, "SNORING IN PREGNANCY", fs=8.5, fill=HALDI)
            + f'<rect x="20" y="96" width="120" height="30" rx="8" fill="{TEAL2}"/><rect x="20" y="126" width="10" height="24" fill="{INK}"/><rect x="130" y="126" width="10" height="24" fill="{INK}"/>'
            + person(80, 120, 0.85, mood="flat", shirt=HALDI, hair_col="#2b2320", hair="long", bindi=True)
            + f'<ellipse cx="80" cy="102" rx="15" ry="13" fill="{HALDI}"/>'
            + text(118, 46, "zzz... GHRR", 11, weight=800, fill=CORAL)
            + doctor(254, 150, 0.95, arms="hold")
            + bubble(180, 8, 134, "Good that you told me.", 254, 56),
            "Meenu didi, six months pregnant, snores on the sofa while her doctor says it was good to tell her"),
        [("Meenu", "Six months pregnant, and I snore louder than my husband!"),
         ("Doctor", f"Good that you told me. About one-third of pregnant women start snoring in months 4 to 6 {P(37)}. It can go with <b>high blood pressure</b> and affect the baby's growth {P(37)}")],
        points=[f"<b>Snoring in pregnancy</b>: tell your doctor {P(37)}", f"In most cases it goes away soon after delivery {P(37)}"],
        moral="Snoring in pregnancy is a reason to tell your doctor.", badge="Story", key="snoring in pregnancy")

ch.watch_out("Too sleepy to drive",
             svg(sign(10, 8, 146, "EYES HEAVY? YAWNING?", fs=9, fill=HALDI)
                 + sign(10, 32, 146, "LAST 5 KM, GONE?", fs=9, fill=CORAL, color="#fff")
                 + car(14, 150) + driver(14, 150)
                 + text(84, 92, "z", 11, fill=BLUE, weight=800)
                 + sign(170, 12, 140, ["PULL OVER:", "NAP 15 TO 20 MIN"], fs=9, fill="#fff")
                 + chintu(258, 150, 0.85, mood="o", arms="wave"),
                 "Warning signs above a car, and Chintu waving the driver over for a short nap"),
             f"<p>Warning signs: trouble keeping your eyes open, constant yawning, not remembering the last few kilometres {P(22)}.</p>"
             f"<p>Driving sleepy is <b>as dangerous as driving drunk</b>, and you do not have to fall asleep to crash {P(22)}. "
             f"Just one beer when short of sleep hits like two or three when rested {P(23)}.</p>"
             f"<p>Sleepy? <b>Pull over</b> and nap 15 to 20 minutes. On long trips, take frequent breaks. Avoid driving between midnight and 7 am {P(23)}. "
             f"Night shift workers crash more on the early-morning drive home {P(14)}.</p>",
             "Any of these signs means stop driving now.", key="pull over")

ch.chat("Golu walks in his sleep",
        svg(moon(30, 28, 12) + text(130, 30, "PARASOMNIAS", 9, weight=800, fill=TEAL)
            + f'<rect x="196" y="70" width="6" height="80" fill="{WOOD}"/><rect x="290" y="70" width="6" height="80" fill="{WOOD}"/>'
            + "".join(f'<rect x="{204 + i * 14}" y="78" width="4" height="72" fill="{WOOD}"/>' for i in range(6))
            + f'<rect x="196" y="70" width="100" height="6" fill="{WOOD}"/>'
            + text(246, 62, "SAFETY GATE", 9, weight=800, fill=TEAL)
            + golu(130, 150, 0.65, mood="flat", arms="hold")
            + text(158, 92, "z", 11, fill=BLUE, weight=800)
            + mausi(50, 150, 0.85, mood="o"),
            "Golu sleepwalks with his arms out towards a safety gate at the top of the stairs while Mausi watches"),
        [("Mausi", "Is it serious?"),
         ("chintu", f"Sleepwalking, sleep talking, night terrors and acting out dreams are <b>parasomnias</b>: body actions normally switched off in sleep. Most are more common in children, who tend to outgrow them {P(57)}"),
         ("sharma", f"If it keeps happening: talk with your doctor, and keep the child and family <b>safe</b> {P(57)}")],
        intro="2 am at Nani's house. Golu walks the corridor, eyes half open.",
        moral="Keep a sleepwalker safe, and tell a doctor if it keeps happening.", badge="Story", key="parasomnias")

ch.try_it("Keep a sleep diary for one week",
          svg(paper(14, 14, 156, 94, ["MUMMY'S SLEEP DIARY", "Bed: 11 pm", "Asleep: 11:45 pm", "Woke: 4 times", "Naps: 2", "Sleepy today: very"], fs=11, anchor="start", fill="#fff")
              + mummy(232, 150, 0.95, mood="smile", arms="hold")
              + chai(282, 150, 1.0),
              "Mummy fills in a sleep diary page with her bedtime, wake-ups and naps"),
          f"<p>The guide's best home test: a <b>sleep diary</b> for a week or so. Note your sleep, medicines, alcohol, caffeine, exercise, and how sleepy you feel in the day {P(59)}.</p>"
          "<p><b>Try it:</b> which diary results mean see a doctor?</p>"
          f"<details><summary>Answer</summary><p>Over 30 minutes to fall asleep most nights; waking more than a few times or for long spells; "
          f"frequent naps; often sleepy in the day, or falling asleep at the wrong times {P(59)}.</p></details>",
          "A week of notes shows when it is time to see a doctor.", key="sleep diary")

ch.chat("Do not fix it alone",
        svg(mummy(60, 150, 0.95, mood="flat", arms="hold")
            + bubble(8, 8, 126, "I will just take a sleeping pill", 60, 70, fs=10)
            + pills(98, 96, 3) + cross(122, 107, 1.4)
            + sign(186, 8, 128, "SLEEP SPECIALIST", fs=9, fill=HALDI)
            + paper(146, 42, 72, 44, ["WHAT I", "NOTICE"], fs=9, fill="#fff", rot=-4)
            + doctor(254, 150, 1.0, arms="hold"),
            "Mummy reaches for a sleeping pill, crossed out, while a sleep specialist waits with a note of what Mummy noticed"),
        [("Mummy", "I will just take a sleeping pill and sort it out."),
         ("chintu", f"Talk to a doctor first: alcohol, pills and over-the-counter sedatives have limited benefits and risks {P(43)}. Your family doctor or a <b>sleep specialist</b> can help, and rule out other health problems {P(35)}")],
        points=[f"Still tired after enough time in bed? <b>See a doctor</b> {P(35)}", f"Tell the doctor what you notice {P(9)}"],
        moral="Take the signs to a doctor before you take a pill.", key="sleep specialist")

ch.myths([
    ("Snoring is a normal part of sleep.", f"Regular snoring is linked to daytime sleepiness, diabetes and heart disease; loud snoring can be sleep apnea {P(30)}."),
    ("A child who lacks sleep will look sleepy.", f"Tired children typically turn hyperactive, irritable and inattentive, not sleepy {P(30)}."),
    ("One long night of sleep fixes daytime tiredness.", f"Poor sleep quality from a disorder is not cured by more sleep, but many disorders can be treated {P(29)}."),
], panel=factboard(["Regular snoring: linked to diabetes, heart disease", "Tired children often turn hyperactive",
                    "More sleep will not cure a disorder; many can be treated"],
                   "Three facts pinned up with ticks: regular snoring is linked to diabetes and heart disease, tired children turn hyperactive, a disorder needs treatment; Sharma ji checks them"))

ch.redpen([f"Signs on 3+ nights a week: see a doctor {P(40)}.", f"Loud snoring plus pauses: get checked {P(37)}.", f"Wild, tired child? Check their sleep {P(30)}.",
           f"Snoring in pregnancy: tell your doctor {P(37)}.", f"Sleepy at the wheel: pull over {P(23)}."],
          where="the warning signs",
          panel=svg(week(14, 14, {0, 2, 4}, w=24, gap=4)
                    + notes(14, 50, 196, 92, ["3+ nights a week: doctor", "Snoring + pauses: check", "Sleepy driving? Pull over"])
                    + phone(226, 18, ["Dr."], fs=9, h=40, w=28)
                    + sharma(274, 150, 1.0, "flat", "skeptic", arms="point"),
                    "Sharma ji points at his red-pen page under a week with three nights marked: see a doctor, get snoring checked, pull over"))

ch.oneliner("when should I see a doctor about sleep?",
            f"When the signs show up on 3 or more nights a week {P(40)}, or you are still tired after enough time in bed {P(59)}.",
            panel=svg(mummy(64, 150, 0.95, mood="o")
                      + bubble(8, 8, 120, "When should I see a doctor about sleep?", 64, 70, fs=10)
                      + calendar(134, 92, "NIGHTS", "3+", w=52, h=48)
                      + chintu(262, 150, 0.95, mood="smile", arms="wave")
                      + bubble(140, 8, 174, "When the signs show up on 3 or more nights a week", 262, 52, fs=10),
                      "Mummy asks when to see a doctor and Chintu answers: signs on 3 or more nights a week"))

ch.quizzes([
    ("Mummy needs 40 minutes to fall asleep, 4 nights a week. Doctor?",
     f"Yes, mention it. More than 30 minutes to fall asleep, on 3 or more nights a week, is one of the guide's signs {P(40)}.",
     "Night signs: count them"),
    ("You snore and your wife says you stop breathing. What now?",
     f"See a doctor. Loud snoring with pauses in breathing is the hallmark of sleep apnea, which should be checked and treated {P(37)} {P(30)}.",
     "Loud snoring with pauses is not a joke"),
])

ch.recall([
    ("What builds up in your blood all day and helps trigger sleep?",
     f"Adenosine. It builds up while you are awake, your body breaks it down while you sleep, and its level may help trigger sleep {P(13)}.",
     "The sleep-pressure tank"),
])

ch.done("Mummy books a check-up",
        "Mummy counts her nights: 4 out of 7 with a long wait to fall asleep. She writes them in a diary and books a doctor's visit for Saturday. "
        "Pinky posts a thumbs up on the family group. Nobody calls it normal any more.",
        panel=svg(calendar(20, 20, "SAT", "10 AM", w=60, h=52)
                  + paper(96, 24, 92, 60, ["DOCTOR", "visit booked"], fs=10, fill="#fff", rot=3)
                  + mummy(110, 150, 0.85, mood="smile", arms="hold")
                  + pinky(200, 150, 0.85, mood="grin", arms="up")
                  + chintu(278, 150, 0.8, mood="grin"),
                  "Mummy holds her doctor's appointment note while Pinky and Chintu cheer"))


# ======================= INTERMEDIATE 1 =======================
ch = deck.chapter("intermediate", "What does sleep do, and how much do you need?", glossary=[
    ("REM", "rapid eye movement: the dreaming stage."),
    ("Deep sleep", "stage 3, the hardest stage to wake from."),
    ("Body clock", "the brain's timer for sleep and waking."),
    ("Insomnia", "trouble falling or staying asleep."),
    ("Sleep apnea", "breathing that keeps stopping during sleep."),
])

ch.opener(
    svg(desk(16, 110, 120) + books(50, 110, 4) + chai(104, 110, 1.0) + clock(40, 34, 16, 3, 0)
        + person(76, 150, 0.8, mood="grin", shirt=GREEN)
        + chintu(176, 150, 0.85, mood="o")
        + sharma(266, 150, 0.9, "flat", "skeptic")
        + bubble(64, 6, 118, "All-nighter. Topper move!", 76, 72)
        + bubble(210, 12, 104, "Data dikhao.", 266, 66),
        "Bunty at his desk at 3 am with books and chai, planning an all-nighter, while Sharma ji asks for data"),
    scene("3 am, the night before a 9 am board exam. Pinky's cousin Bunty has chai, books and zero sleep planned.")
    + talk(("Bunty", "All-nighter. Topper move!"),
           ("chintu", f"Studies say otherwise: people learn a task better when well rested, and remember it better after a good night's sleep {P(18)}."),
           ("sharma", "So how many hours, exactly? Data dikhao.")),
    "You learn better rested, and you remember better after sleep.")

ch.chat("Sleep on it: what the volunteers showed",
           svg(text(160, 22, "LEARNING GAIN AFTER A NIGHT OF SLEEP", 9, weight=800, fill=TEAL)
               + bars([("Under 6 h", 3, GREY, "no gain"), ("6 to 7 h", 60, HALDI, "some"), ("8 h", 100, TEAL2, "best")],
                      x=84, y=36, step=30, scale=1.6)
               + text(160, 140, "bar lengths show the order, not exact scores", 8.5, weight=500, fill="#6d675f"),
               "Three bars: under 6 hours no learning gain, 6 to 7 hours some, 8 hours the most", floor=False),
           [("pinky", "Bunty says toppers skip sleep. What did the studies find?"),
                ("chintu", f"Volunteers had to sleep at least 6 hours to show any <b>learning gain</b> {P(18)}. Those who slept 8 hours beat those on 6 or 7 {P(18)}"),
                ("sharma", "And the night before?"),
                ("chintu", f"Get enough rest the night <b>before</b> a hard mental task, not only after it {P(18)}")],
           moral="Rest the night before a hard task, not only after it.", badge="Worked example", key="learning gain")

ch.chat("Your brain on no sleep",
        svg(monitor(14, 16, 168, 96, ["Thinking: slow", "Focus: low", "Faulty decisions", "Reaction: late"], fs=12)
            + pinky(262, 150, mood="sad")
            + bubble(194, 8, 120, "How bad, compared to drinking?", 262, 60, fs=10),
            "A status screen showing slow thinking, low focus, faulty decisions and late reactions, with Pinky asking how bad it is"),
        [("sharma", "One short night. A bit slow, that is all."),
         ("chintu", f"Worse: slower thinking, poor focus, confusion {P(19)}, plus <b>faulty decisions</b>, more risk taking and slower reactions {P(19)}."),
         ("pinky", "How bad, compared to drinking?"),
         ("chintu", f"On a driving simulator, sleep-deprived people do as poorly as drunk people {P(19)}")],
        moral="A tired brain does not just feel slow. It decides worse.", key="faulty decisions")

ch.chat("Short sleep, short temper",
        svg(text(110, 18, "PINKY'S MOOD METER", 9, weight=800, fill=TEAL)
            + f'<path d="M40 110 A80 80 0 0 1 200 110" fill="none" stroke="{GREEN}" stroke-width="12"/>'
            + f'<path d="M120 30 A80 80 0 0 1 200 110" fill="none" stroke="{CORAL}" stroke-width="12"/>'
            + f'<path d="M120 110 L178 54" stroke="{INK}" stroke-width="3" stroke-linecap="round"/><circle cx="120" cy="110" r="6" fill="{INK}"/>'
            + text(52, 132, "calm", 9, weight=700) + text(196, 132, "irritable", 9, weight=800, fill=CORAL)
            + pinky(272, 150, 0.9, mood="sad")
            + bubble(214, 8, 100, "Why am I so snappy?", 272, 66, fs=10),
            "A mood meter pointing at irritable, beside a grumpy Pinky asking why she is so snappy"),
        [("pinky", "Sorry! Why am I so snappy?"),
         ("chintu", f"Most people report being <b>irritable</b> when short of sleep {P(19)}. Long term, from too little time in bed or an untreated sleep problem, it raises the risk of <b>depression</b> {P(19)}"),
         ("sharma", f"It works both ways: depression often leads to insomnia, and insomnia can cause depression {P(32)}")],
        intro="Four short nights. Pinky snaps at Chintu over the last paratha.",
        moral="Long-term short sleep raises the risk of depression, and depression often spoils sleep.", key="irritable")

ch.chat("The nightly dip your heart needs",
           svg(line_chart(40, 36, 190, 84, [72, 62, 50, 44, 46, 56, 70], labels=("bedtime", "morning"))
               + text(136, 22, "BLOOD PRESSURE THROUGH THE NIGHT", 9, weight=800, fill=TEAL)
               + text(135, 133, "the dip", 10, weight=800, fill=CORAL)
               + heart(276, 70, 2.2)
               + text(276, 116, "rest time", 9, weight=700)
               + text(150, 152, "shape only, not real readings", 8.5, weight=500, fill="#6d675f"),
               "A line that dips in the middle of the night and rises by morning, next to a heart", floor=False),
           [("pinky", "Why does sleep matter for the heart?"),
            ("chintu", f"In deeper sleep, heart rate and blood pressure slow step by step {P(19)}. That nightly <b>dip</b> appears to matter for heart health {P(20)}"),
            ("sharma", f"And too little sleep or untreated apnea can take it away. Short sleep may also release more <b>stress hormones</b>, which block the dip and raise heart disease risk {P(20)}")],
           moral="Too little sleep can take away the heart's nightly dip in blood pressure.", badge="Picture it", key="dip")

ch.glance("What sleep runs for you overnight",
          svg(sign(8, 14, 98, "GROWTH HORMONE", fs=8.5, fill=HALDI) + sign(114, 14, 92, "CYTOKINES", fs=8.5, fill=TEAL2, color="#fff")
              + sign(214, 14, 98, "LEPTIN UP", fs=8.5, fill=CORAL, color="#fff")
              + text(57, 50, "grow, repair", 9, weight=700) + text(160, 50, "fight germs", 9, weight=700) + text(263, 50, "less hunger", 9, weight=700)
              + arrow(56, 56, 90, 98) + arrow(160, 56, 140, 98) + arrow(264, 56, 210, 102)
              + bed(80, 150, 160, sleeper=True),
              "Three labels, growth hormone, cytokines and leptin, all pointing at a sleeper in bed"),
          table(["During sleep", "What it does"], [
              [f"Deep sleep releases more <b>growth hormone</b> {P(20)}", "growth in children; muscle and repair in everyone"],
              [f"More <b>cytokines</b> (immune hormones) are made {P(20)}", "help fight infections"],
              [f"<b>Leptin</b> goes up, ghrelin goes down {P(21)}", "keeps appetite in check; short sleepers crave high-calorie food"],
          ])
          + f"<p>Over time, too little sleep raises the risk of obesity, diabetes, heart disease and infections {P(7)}.</p>",
          "Mummy was right: sleep helps you grow, fight germs and keep your appetite in check.", key="growth hormone")

ch.chat("The flu shot test",
           svg(text(160, 24, "FLU ANTIBODIES, SAME VACCINE", 9, weight=800, fill=TEAL)
               + bars([("Well rested", 100, TEAL2, "full"), ("Sleep-deprived", 45, CORAL, "under half")],
                      x=96, y=46, step=36, scale=1.7)
               + f'<rect x="120" y="126" width="64" height="10" rx="3" fill="#fff" stroke="{INK}" stroke-width="1.4"/>'
               + f'<path d="M184 131 L204 131 M112 131 L120 131 M114 125 L114 137" stroke="{INK}" stroke-width="1.6"/>'
               + f'<rect x="124" y="128" width="30" height="6" rx="2" fill="{TEAL2}"/>',
               "Two bars: sleep-deprived volunteers made under half the flu antibodies of rested ones, with a syringe", floor=False),
           [("sharma", "Sleep and catching flu? Data dikhao."),
            ("chintu", f"Sleep-deprived volunteers given the flu vaccine made <b>less than half</b> as many flu <b>antibodies</b> as rested volunteers given the same vaccine {P(21)}")],
           points=[f"Healthy young men on 4 hours a night for 6 nights: insulin and blood sugar like people developing diabetes {P(21)}",
                   f"5 hours a night: much more likely to become obese than 7 to 8 {P(21)}"],
           moral="Same vaccine, under half the antibodies when sleep-deprived.", badge="Worked example", key="antibodies")

ch.glance("How much is enough, by age",
          svg(person(40, 150, 0.45, mood="smile", shirt=HALDI) + sign(8, 84, 64, "16 to 18 h", fs=9, fill="#fff")
              + person(120, 150, 0.68, mood="grin", shirt=GREEN) + sign(92, 64, 56, "10+ h", fs=9, fill="#fff")
              + pinky(200, 150, 0.85, mood="smile") + sign(166, 46, 68, "9 to 10 h", fs=9, fill="#fff")
              + sharma(278, 150, 0.95, "flat", "flat") + sign(246, 36, 66, "7 to 8 h", fs=9, fill="#fff")
              + text(150, 20, "SLEEP NEEDED, BABY TO ADULT", 9, weight=800, fill=TEAL),
              "Four people from baby to adult, each with their nightly sleep need above them"),
          table2(["Who", "Sleep needed"], [
              ["Newborns", f"16 to 18 hours a day {P(25)}"],
              ["Preschoolers", f"11 to 12 hours a day {P(25)}"],
              ["School kids and teens", f"<b>at least 10 hours</b> {P(27)}; teens 9 to 10 {P(25)}"],
              ["Adults", f"about <b>7 to 8 hours</b> {P(27)}"],
          ], first=36)
          + f"<p>Similar amounts seem needed to avoid a higher risk of obesity, diabetes and heart disease {P(27)}.</p>",
          "Adults need about 7 to 8 hours; children and teens need more.", key="7 to 8")

ch.chat("Bunty's clock runs late",
        svg(sign(8, 12, 124, ["BODY CLOCK:", "SLEEP AT 1 AM"], fs=9, fill=BLUE, color="#fff") + clock(70, 74, 20, 1, 0)
            + sign(188, 12, 124, ["SCHOOL BUS:", "6:30 AM"], fs=9, fill=HALDI) + clock(250, 74, 20, 6, 30)
            + text(160, 30, "PUBERTY", 9, weight=800, fill=CORAL)
            + person(160, 150, 0.8, mood="sad", shirt=GREEN)
            + text(196, 104, "yawn", 10, weight=700, fill="#6d675f"),
            "Bunty between a body clock saying sleep at 1 am and a school bus at 6:30 am, with puberty between them"),
        [("Mummy", "Bunty sleeps at 1 am and misses the 6:30 bus. Lazy boy!"),
         ("chintu", f"Partly biology. <b>Puberty</b> hormones shift a teen's body clock later, so teens want to sleep later and wake later {P(25)}"),
         ("sharma", f"And teens need 9 to 10 hours, but early school starts help explain why most get only 7 to 7.5 {P(25)}")],
        moral="A teen's late bedtime is partly biology: puberty shifts the body clock.", badge="Story", key="puberty")

ch.chat("Dadi wakes at 4:30 am",
        svg(moon(28, 24, 11) + clock(70, 34, 17, 4, 30)
            + person(76, 150, 0.95, mood="smile", shirt=TEAL2, hair="grey", bindi=True) + chai(116, 150, 1.0)
            + sharma(186, 150, 0.9, "flat", "skeptic")
            + bubble(130, 8, 98, "Old age: less sleep needed.", 186, 64, fs=9.5)
            + sign(234, 12, 80, ["NOT JUST", "OLD AGE"], fs=9, fill=HALDI)
            + sign(234, 46, 80, ["pills? apnea?", "legs? loo?"], fs=8.5, fill="#fff")
            + chintu(278, 150, 0.7, mood="smile", arms="wave"),
            "Dadi up at 4:30 am with chai, Sharma ji saying old age means less sleep, and Chintu's signs listing other causes"),
        [("sharma", "<b>Old age</b>: less sleep needed."),
         ("chintu", f"No evidence shows older people can get by with less sleep {P(26)}. They tend to sleep earlier and lighter {P(25)} {P(26)}. Many sleep problems in older people are not a natural part of ageing: illness, medicines, sleep apnea, restless legs, night trips to urinate {P(26)}")],
        points=[f"Poor sleep may bring sleepiness, memory and mood problems, pill overuse {P(26)}"],
        moral="Poor sleep in old age has causes worth checking, and the need for sleep stays.", key="old age")

ch.chat("Eight broken hours are not eight hours",
        svg(text(160, 18, "TWO NIGHTS, BOTH 8 HOURS IN BED", 9, weight=800, fill=TEAL)
            + text(14, 48, "Night A", 10, anchor="start", weight=700)
            + f'<rect x="70" y="36" width="230" height="16" rx="4" fill="{TEAL2}"/>'
            + text(14, 88, "Night B", 10, anchor="start", weight=700)
            + "".join(f'<rect x="{70 + i * 47}" y="76" width="38" height="16" rx="4" fill="{CORAL}"/>' for i in range(5))
            + text(175, 114, "woken 4 times: worse quality", 9, weight=700, fill=CORAL)
            + pinky(40, 150, 0.4, mood="sad") + chintu(290, 150, 0.4, mood="smile"),
            "A solid bar for one unbroken night and a bar cut into five pieces for a broken night of worse quality", floor=False),
        [("pinky", "8 hours in bed, woke 4 times. Still counts?"),
         ("chintu", f"<b>Quality</b> and timing matter as much as amount {P(27)}. Broken sleep can miss enough of both dreaming (REM) and non-dreaming sleep {P(27)}"),
         ("sharma", f"Some sleep 8 or 9 hours and still wake unrested. More sleep will not fix poor quality, but many causes can be treated {P(29)}")],
        moral="Count unbroken sleep, not just hours in bed.", key="quality")

ch.chat("The Sunday 11 am catch-up",
        svg(calendar(20, 24, "SUN", "11") + text(42, 84, "am", 9, weight=700)
            + sign(66, 8, 140, ["SLEEP DEBT:", "NOT FULLY ERASED"], fs=9, fill=CORAL, color="#fff")
            + bed(70, 150, 110, sleeper=True)
            + calendar(214, 24, "MON", "7", color=BLUE) + text(236, 84, "am", 9, weight=700)
            + pinky(272, 150, 0.85, mood="sad"),
            "Pinky asleep till 11 am on Sunday, then miserable at 7 am on Monday: the sleep debt is not fully erased"),
        [("pinky", "Five short nights, then Sunday till 11 am to recharge. Smart, na?"),
         ("chintu", f"Sleep-ins help you feel more rested but do not fully erase your <b>sleep debt</b>, the sleep you owe {P(29)}. They shift your body clock, so Sunday night and Monday morning get harder {P(29)}"),
         ("sharma", f"And even one short night can affect your mood and work the next day {P(27)}")],
        moral="Sunday cannot pay off the whole week's sleep debt.", badge="Story", key="sleep debt")

ch.try_it("The office power nap, done right",
          svg(desk(14, 112, 130) + phone(54, 52, ["NAP", "20:00"], fs=9, h=56, w=40)
              + clock(120, 54, 18, 1, 30)
              + sign(176, 12, 136, ["20 MINUTES MAX,", "BEFORE 3 PM"], fs=9, fill=HALDI)
              + chintu(250, 150, 0.9, mood="grin", arms="wave"),
              "A phone timer set for a 20-minute nap and a clock at 1:30 pm on a desk, under a sign saying 20 minutes max, before 3 pm"),
          f"<p>Short <b>naps</b> can partly make up for lost sleep and lift alertness and mood, but do not replace a good night {P(27)}. "
          f"Keep them to <b>20 minutes</b> or less, since longer naps make it hard to wake up, and take none after 3 pm {P(29)}. "
          f"More than one or two naps a day may mean a sleep problem that should be treated {P(30)}.</p>"
          "<p><b>Try it:</b> is 4:30 pm a good time for a nap?</p>"
          f"<details><summary>Answer</summary><p>No. Late afternoon naps can make it harder to fall asleep at night {P(27)}.</p></details>",
          "Twenty minutes at most, and before 3 pm.", key="20 minutes")

ch.watch_out("Driving home from the wedding at 3 am",
             svg(sign(14, 12, 104, "NH 48, 3 AM", fs=9, fill=GREEN, color="#fff")
                 + moon(150, 30, 12)
                 + text(80, 78, "nod off without knowing", 9, weight=700, fill=CORAL)
                 + car(20, 150) + driver(20, 150)
                 + chintu(264, 150, 0.85, mood="o", arms="wave")
                 + bubble(186, 10, 128, "Window down will not help.", 264, 60),
                 "A car on the highway at 3 am, the driver nodding off, while Chintu says opening the window will not help"),
             talk(("pinky", "Window down, music up. I will be fine till home."),
                  ("chintu", f"Window down will not help, nor loud music: there is no substitute for sleep {P(22)}. People often <b>nod off</b> for a moment without knowing it {P(22)}"),
                  ("sharma", f"And crashes from sleepy drivers are as deadly as those from drunk drivers {P(22)}. Pull over and nap 15 to 20 minutes {P(23)}")),
             "Sleepy at the wheel is as dangerous as drunk at the wheel. Stop the car.", key="nod off")

ch.glance("Before the long drive home",
          svg(board(14, 14, 168, 104, ["Rested for days?", "Company in the car?", "No alcohol?", "Not counting on coffee?"], fs=10, title="BEFORE YOU DRIVE")
              + car(186, 150, CORAL)
              + text(250, 62, "?", 22, weight=800, fill=TEAL),
              "A pre-drive checklist on a board next to a car"),
          table2(["Tip", "Why"], [
              ["Be rested", "reaction time can take several good nights to recover"],
              ["Do not drive alone", "a companion who talks may help"],
              ["<b>No alcohol</b>", "one beer when short of sleep hits like two or three when rested"],
              ["No coffee tricks", "it will not beat extreme sleepiness or repay sleep debt"],
          ], first=34)
          + f"<p>All from the guide {P(23)}. Sleep loss plus inexperience, common in teens, is a lethal mix {P(22)}.</p>",
          "When you are short of sleep, one drink counts as two or three.", key="no alcohol")

ch.myths([
    ("One hour less a night makes no difference.", f"Even slightly less sleep can hurt thinking, reaction, heart health and fighting infection {P(28)}."),
    ("Older people need less sleep.", f"Older people do not need less sleep; they may just get less, or find it less refreshing {P(28)}."),
    ("Naps are a waste of time.", f"Short naps can restore you and even help you learn some tasks faster {P(29)}."),
    ("Coffee cures a sleepy drive.", f"Coffee helps briefly but will not beat extreme sleepiness {P(23)}."),
], panel=factboard(["A little less sleep can hurt thinking and heart", "Older people do not need less sleep",
                    "Short naps can restore you", "Coffee will not beat extreme sleepiness"],
                   "Four facts pinned up with ticks: a little less sleep can hurt, older people do not need less, short naps can restore you, coffee will not beat extreme sleepiness"))

ch.redpen([f"Adults: 7 to 8 hours, every night {P(27)}.", f"Sleep well the night before the exam {P(18)}.",
           f"Sleepy? Do not drive. Nap {P(22)} {P(23)}.", f"Naps: 20 minutes, before 3 pm {P(29)}.", f"Short of sleep? 1 beer hits like 2 or 3 {P(23)}."],
          where="the how-much chapter",
          panel=svg(notes(12, 12, 176, 100, ["Adults: 7 to 8 hours", "Rest before the exam", "Sleepy? Do not drive", "Naps: 20 min, before 3"])
                    + books(212, 150, 4)
                    + sharma(270, 150, 1.0, "flat", "skeptic", arms="point"),
                    "Sharma ji points at his red-pen page: adults 7 to 8 hours, rest before the exam, do not drive sleepy, short naps before 3"))

ch.oneliner("how much sleep do I actually need?",
            f"About 7 to 8 hours a night for adults, more for kids and teens {P(27)}, and Sunday cannot fully pay back the week {P(27)}.",
            panel=svg(person(64, 150, 0.9, mood="o", shirt=GREEN)
                      + bubble(8, 8, 116, "How much sleep do I actually need?", 64, 76, fs=10)
                      + books(150, 150, 3) + chai(150, 126, 0.9)
                      + sharma(256, 150, 0.95, "flat", "flat")
                      + bubble(136, 8, 178, "About 7 to 8 hours a night for adults", 256, 64, fs=10),
                      "Bunty asks how much sleep he needs and Sharma ji answers: about 7 to 8 hours for adults"))

ch.quizzes([
    ("Exam at 9 am. Revise until 4 am, or sleep 8 hours?",
     f"Sleep. Volunteers who slept 8 hours learned better than those on 6 or 7, and rest before a hard mental task matters {P(18)}.",
     "Sleep on it: what the volunteers showed"),
    ("Why will a cup of coffee not save a sleepy drive home?",
     f"Caffeine keeps you awake only briefly and cannot overcome extreme sleepiness or repay sleep debt. Pull over and nap 15 to 20 minutes {P(23)}.",
     "Before the long drive home"),
])

ch.recall([
    ("A sleep sign on how many nights a week means tell a doctor?",
     f"3 or more nights a week, for signs like taking more than 30 minutes to fall asleep {P(40)}.",
     "Night signs: count them"),
])

ch.done("Bunty sleeps at 11, wakes at 7",
        "Bunty closes the books at 11 pm and sleeps 8 hours. He walks in calm, remembers what he revised, and says \"Kaabil bano,\" as 3 Idiots (2009) taught him. "
        "Sharma ji nods, which for Sharma ji is applause.",
        panel=svg(sun(36, 34, 13) + sign(60, 14, 130, "EXAM HALL", fs=10, fill=HALDI)
                  + person(90, 150, 0.85, mood="grin", shirt=GREEN, arms="up")
                  + chintu(180, 150, 0.8, mood="grin", arms="wave")
                  + sharma(268, 150, 0.95, "flat", "flat"),
                  "Bunty cheers outside the exam hall in the morning sun while Sharma ji nods"))


# ======================= INTERMEDIATE 2 =======================
ch = deck.chapter("intermediate", "Which habits help sleep, and which hurt?", glossary=[
    ("REM", "rapid eye movement: the dreaming stage."),
    ("Tapri", "a roadside tea stall"),
    ("Body clock", "the brain's timer for sleep and waking."),
    ("Insomnia", "trouble falling or staying asleep."),
    ("Deep sleep", "stage 3, the most restorative stage."),
])

ch.opener(
    svg(sticky(30, 22, "KAL", rot=-8) + sticky(58, 26, "SE", rot=6) + sticky(90, 20, "PAKKA", rot=-4)
        + pinky(80, 150, 0.95, mood="grin", arms="up")
        + paper(150, 14, 96, 50, ["THE GUIDE'S", "SLEEP TIPS", "p. 33 to 35"], fs=9, fill="#fff")
        + chintu(276, 150, 0.85, mood="smile", arms="wave"),
        "Pinky's sticky notes say kal se pakka while Chintu holds up the guide's list of sleep tips"),
    scene("Pinky sticks three notes on her mirror: KAL SE PAKKA.")
    + talk(("pinky", "From tomorrow, for sure, I fix my sleep!"),
           ("chintu", f"Better than willpower: the guide's own tips for a good night's sleep {P(33)}. Many things spoil a night, from coffee to some pain relievers and decongestants {P(31)}."),
           ("sharma", "Fine. One habit at a time. Data dikhao.")),
    "The guide lists the habits that help you sleep.")

ch.chat("The 7 pm cutting chai",
        svg(sign(8, 10, 112, "CHAI TAPRI, 7 PM", fs=9, fill=HALDI)
            + sign(8, 36, 112, ["CAFFEINE: UP", "TO 8 HOURS"], fs=9, fill=CORAL, color="#fff")
            + chai(62, 134, 1.2)
            + arrow(96, 110, 150, 110)
            + clock(186, 84, 24, 1, 0) + text(186, 126, "1 am, still awake", 9, weight=700)
            + pinky(276, 150, 0.85, mood="sad")
            + bubble(196, 8, 118, "Still staring at the ceiling.", 276, 70, fs=9.5),
            "A glass of chai at 7 pm, an arrow to a clock at 1 am, and Pinky wide awake: caffeine lasts up to 8 hours"),
        [("pinky", "One cutting chai at 7 pm. Now 1 am, still staring at the ceiling. Why?"),
         ("chintu", f"<b>Caffeine</b> in tea, coffee and cola is thought to block the sleep signal from adenosine, so your body thinks it is not tired {P(31)}. Its effects can take up to <b>8 hours</b> to wear off fully {P(33)}"),
         ("sharma", f"Chocolate and some teas have it too {P(33)}")],
        moral="Caffeine can take up to 8 hours to wear off, so a 7 pm chai can still work at 1 am.", badge="Story", key="caffeine")

ch.glance("The usual sleep thieves",
          svg(sign(112, 14, 94, "LATE CHAI", fs=9, fill=HALDI) + sign(216, 14, 94, "NIGHTCAP", fs=9, fill=CORAL, color="#fff")
              + sign(112, 52, 94, "BIG DINNER", fs=9, fill="#fff") + sign(216, 52, 94, "PHONE IN BED", fs=9, fill=BLUE, color="#fff")
              + sign(112, 90, 94, "SMOKING", fs=9, fill=GREY) + sign(216, 90, 94, "STRESS", fs=9, fill=TEAL2, color="#fff")
              + sharma(52, 150, mood="flat", brow="skeptic", arms="point"),
              "Six labels of sleep thieves, from late chai and a nightcap to stress, with Sharma ji pointing at them"),
          table2(["Thief", "What it does"], [
              ["Alcohol, a <b>nightcap</b>", f"easier to fall asleep, but it blocks deep and REM sleep; you wake when it wears off {P(31)}"],
              ["Heavy drinking", f"may also impair breathing at night {P(34)}"],
              ["<b>Nicotine</b>", f"lighter sleep; heavy smokers wake early from withdrawal {P(31)}"],
              ["Screens in bed", f"distract you and steal sleep {P(35)}"],
          ], first=32),
          "A nightcap helps you drop off, then robs your deep and REM sleep.", key="nightcap")

ch.chat("Same time, every day",
        svg(clock(60, 50, 26, 11, 0) + text(60, 92, "Bed: 11 pm", 10, weight=800)
            + clock(160, 50, 26, 7, 0) + text(160, 92, "Up: 7 am", 10, weight=800)
            + text(250, 30, "SLEEP", 11, weight=800, fill=TEAL) + text(250, 46, "SCHEDULE", 11, weight=800, fill=TEAL)
            + week(20, 108, set(range(7)), w=24, gap=4, color=TEAL2)
            + text(226, 126, "even Sunday", 9, weight=700, anchor="start", fill=TEAL)
            + chintu(298, 150, 0.45, mood="grin", arms="wave"),
            "Two clocks, bed at 11 pm and up at 7 am, ticked on all seven days of the week: a sleep schedule"),
        [("pinky", "Lights off at 11 pm, up at 7 am. Even on Sunday?"),
         ("chintu", f"Even Sunday. The guide's first tip: a <b>sleep schedule</b>, the same bed and wake-up time each day {P(33)}"),
         ("sharma", f"Fair. People are creatures of habit, and sleeping late at the weekend makes Monday morning harder {P(33)}")],
        moral="Same bedtime, same wake-up time, every day of the week.", key="sleep schedule")

ch.chat("The 10 pm gym session",
        svg(bubble(52, 8, 128, "My heart is racing!", 120, 50, fs=10)
            + clock(32, 100, 16, 10, 0) + text(32, 130, "10 pm", 9, weight=700)
            + pinky(120, 150, 0.95, mood="grin", arms="up")
            + f'<rect x="84" y="62" width="72" height="5" rx="2" fill="{INK}"/><rect x="80" y="54" width="8" height="20" rx="2" fill="{GREY}"/><rect x="152" y="54" width="8" height="20" rx="2" fill="{GREY}"/>'
            + sign(192, 8, 120, ["STOP 2 TO 3 HOURS", "BEFORE BED"], fs=9, fill=HALDI)
            + bed(196, 150, 116)
            + text(256, 72, "wide awake", 9, weight=700, fill=CORAL),
            "Pinky lifts weights at 10 pm, next to a bed she will not sleep in for hours, under a sign saying stop 2 to 3 hours before bed"),
        [("pinky", "A hard workout at 10 pm, so I am tired for bed. But at 12:30, my heart is racing!"),
         ("chintu", f"<b>Vigorous exercise</b> just before bed can make it harder to fall asleep, while daytime exercise goes with better sleep {P(32)}"),
         ("sharma", f"So: at least 30 minutes on most days, but not later than <b>2 to 3 hours</b> before bed {P(33)}")],
        moral="Exercise most days, and finish 2 to 3 hours before bed.", badge="Story", key="2 to 3 hours")

ch.chat("A bedroom built for sleep",
           svg(f'<rect x="14" y="14" width="72" height="62" rx="3" fill="{BLUE}"/><rect x="18" y="14" width="30" height="62" fill="{TEAL}"/><rect x="52" y="14" width="30" height="62" fill="{TEAL}"/>'
               + text(50, 92, "dark", 9, weight=700)
               + f'<rect x="112" y="18" width="10" height="52" rx="5" fill="#fff" stroke="{INK}" stroke-width="1.4"/><rect x="114" y="46" width="6" height="22" rx="3" fill="{TEAL2}"/>'
               + text(117, 92, "cool", 9, weight=700)
               + phone(142, 14, ["TV", "PHONE"], fs=8.5, h=60, w=44) + cross(164, 58, 1.0)
               + text(164, 92, "no screens", 9, weight=700)
               + f'<circle cx="236" cy="44" r="20" fill="{GREY}" stroke="{INK}" stroke-width="1.6"/>'
               + text(242, 92, "clock face away", 9, weight=700)
               + bed(60, 150, 150) + f'<circle cx="86" cy="116" r="11" fill="{SKIN}"/><path d="M78 114 q8 4 16 0" stroke="{INK}" stroke-width="1.5" fill="none"/>'
               + text(276, 140, "quiet", 9, weight=700),
               "A bedroom checklist: dark curtains, a cool thermometer, a crossed-out phone, a clock turned away, and a sleeper in bed"),
           [("pinky", "What should my bedroom be like?"),
            ("chintu", f"Clear it of noise, bright lights, a TV, a phone or a computer, and keep it on the <b>cool</b> side {P(33)}. A comfortable mattress and pillow help {P(35)}"),
            ("sharma", f"And turn the <b>clock</b> face away, so you do not worry about the time {P(35)}")],
           moral="Cool, dark, quiet, no screens, and the clock turned away.", badge="Picture it", key="cool")

ch.chat("Morning sun, dim evenings",
        svg(sun(56, 36, 16) + f'<rect x="14" y="98" width="110" height="6" fill="{WOOD}"/>'
            + pinky(70, 150, 0.85, mood="smile", arms="hold") + chai(94, 118, 0.9)
            + text(70, 74, "7 am: morning sun", 9, weight=700)
            + bulb(232, 60, on=False) + moon(282, 30, 11)
            + text(240, 96, "lights down at night", 9, weight=700)
            + chintu(240, 150, 0.5, mood="smile"),
            "Pinky with chai in the morning sun on the balcony, and a dimmed lamp at night"),
        [("pinky", "I cannot fall asleep at night. What helps?"),
         ("chintu", f"An hour of <b>morning sunlight</b>, and lights turned down before bedtime {P(35)}. Any day, get at least 30 minutes of natural sunlight: <b>daylight</b> sets your daily sleep pattern {P(35)}")],
        points=[f"If you can, wake with the sun or use very bright morning lights {P(35)}"],
        moral="Bright mornings and dim evenings set your body clock.", key="morning sun")

ch.chat("The wind-down hour",
        svg(f'<path d="M22 100 L30 146 L84 146 L92 100 Z" fill="{BLUE}"/><ellipse cx="57" cy="100" rx="35" ry="7" fill="{TEAL2}"/>'
            + f'<path d="M44 90 q-6 -10 0 -20 M58 88 q-6 -10 0 -20 M72 90 q-6 -10 0 -20" fill="none" stroke="{GREY}" stroke-width="2"/>'
            + text(57, 60, "hot water", 9, weight=700)
            + sign(14, 10, 96, "WIND DOWN", fs=10, fill=HALDI)
            + books(150, 150, 3) + text(150, 112, "a book", 9, weight=700)
            + pinky(236, 150, 0.9, mood="smile", arms="hold")
            + bubble(180, 8, 134, "Jaadu ki jhappi", 236, 66),
            "A steaming bucket of hot water, a book, and a relaxed Pinky winding down"),
        [("pinky", "Jaadu ki jhappi, Munna Bhai M.B.B.S. (2003) style. Does it help?"),
         ("chintu", f"Most people fall asleep more easily after time to <b>wind down</b> {P(33)}. Make reading or music your bedtime ritual {P(34)}"),
         ("sharma", f"And after a hot bath your body temperature drops, a bit like what happens as you fall asleep {P(33)}")],
        intro="10 pm: phone away, a hot bucket bath, then a novel.",
        moral="Give yourself time to wind down before bed.", badge="Story", key="wind down")

ch.glance("Late dinner, late water, late pills",
          svg(f'<ellipse cx="60" cy="116" rx="46" ry="10" fill="#fff" stroke="{INK}" stroke-width="1.4"/>'
              + f'<path d="M26 112 Q60 70 94 112 Z" fill="{HALDI}"/>' + text(60, 64, "huge dinner", 9, weight=700)
              + f'<path d="M126 82 L132 132 L152 132 L158 82 Z" fill="#cfe8ee" stroke="{INK}" stroke-width="1.3"/>' + text(142, 64, "3 glasses", 9, weight=700)
              + pills(176, 104, 4) + text(206, 92, "cough syrup?", 9, weight=700)
              + sign(166, 12, 100, ["ASK A", "PHARMACIST"], fs=9, fill=HALDI)
              + sharma(286, 150, 0.85, "flat", "skeptic", arms="point"),
              "A big late dinner, a tall glass of water and a strip of pills, with Sharma ji pointing at a sign saying ask a pharmacist"),
          table2(["Habit", "What the guide says"], [
              ["Big late dinner", "a light snack is fine; a large meal can bring indigestion"],
              ["Lots of water at night", "you wake up to pass urine"],
              ["Some medicines", "some heart, blood pressure and asthma drugs, and cough, cold or allergy remedies"],
          ], first=34)
          + f"<p>All three from the guide {P(34)}. Ask a doctor or <b>pharmacist</b> if a medicine affects sleep {P(34)}. Decongestants, steroids, "
            f"headache pills with caffeine and beta blockers (heart pills) can keep you awake {P(31)}.</p>",
          "Ask your doctor or pharmacist if a medicine could be stealing your sleep.", key="pharmacist")

ch.chat("Stress keeps the brain switched on",
        svg(awake_in_bed(14, 150, 150)
            + bubble(8, 8, 132, "Why am I still awake?", 40, 102, fs=10)
            + clock(222, 32, 20, 2, 10)
            + sign(150, 62, 96, ["STRESS: LESS", "DEEP SLEEP"], fs=9, fill=CORAL, color="#fff")
            + chintu(276, 150, 0.8, mood="sad"),
            "Rohit lies awake at 2:10 am in appraisal week; stress means less deep sleep"),
        [("Rohit", "Appraisal week. Bed by 11. Why am I still awake at 2?"),
         ("chintu", f"<b>Stress</b> makes it harder to fall or stay asleep, and stressed people tend to get less deep and REM sleep {P(32)}. Anxiety disorders disrupt sleep too, and depression and insomnia can each cause the other {P(32)}"),
         ("sharma", f"Loss, divorce, work stress: many people sleep badly after them {P(32)}")],
        moral="Stress can cut your deep and REM sleep, not just your hours.", key="stress")

ch.glance("Women's sleep and hormones",
          svg(calendar(14, 22, "DAY 27", "2 am", w=60, h=52, fs=10)
              + text(44, 94, "before a period", 10, weight=700)
              + person(136, 150, 1.0, mood="smile", shirt=HALDI, hair_col="#2b2320", hair="long", bindi=True)
              + f'<ellipse cx="143" cy="127" rx="13" ry="12" fill="{HALDI}" stroke="{INK}" stroke-width="1"/>'
              + text(136, 30, "pregnant", 10, weight=700)
              + mummy(254, 150, 1.0, mood="sad")
              + "".join(f'<path d="M{x} 66 q-5 -6 0 -12 q5 -6 0 -12" fill="none" stroke="{CORAL}" stroke-width="2.4" stroke-linecap="round"/>' for x in (240, 254, 268))
              + text(254, 30, "menopause: hot flash", 10, weight=800, fill=CORAL),
              "A calendar before a period, a pregnant woman, and Pinky's mummy fanning herself through a menopause hot flash"),
          table2(["When", "The guide says"], [
              ["Before a period", f"worse sleep as <b>progesterone</b> (a sleep hormone) drops {P(32)}"],
              ["<b>Menopause</b>", f"more insomnia; hot flashes {P(32)}"],
              ["Pregnancy", f"new snoring? Tell your doctor {P(37)}"],
              ["Night work", f"may raise miscarriage risk {P(20)}"],
              ["New mothers", f"short sleep may partly cause postpartum blues {P(19)}"],
          ], first=30),
          "A woman's sleep can change through the month, in pregnancy and at menopause.", key="menopause")

ch.watch_out("Neha's drive home at 7 am",
             svg(sign(14, 10, 126, "NIGHT SHIFT OVER", fs=9, fill=BLUE, color="#fff")
                 + sun(180, 30, 12)
                 + car(20, 150, TEAL2) + driver(20, 150)
                 + text(92, 92, "z", 11, fill=BLUE, weight=800)
                 + sign(206, 52, 108, ["BODY CLOCK: NO", "ALERTING SIGNAL"], fs=8.5, fill="#fff")
                 + chintu(262, 150, 0.7, mood="o"),
                 "Neha drives home after a night shift as the sun rises; her body clock sends no alerting signal"),
             "<p>Neha drives home at 7 am after her call-centre night shift in Gurgaon.</p>"
             f"<p>Night shift workers have a higher risk of a crash on the early-morning drive home, because the body clock sends no <b>alerting signal</b>. "
             f"In one study, one-fifth had a crash or near miss in a year {P(14)}.</p>"
             f"<p>Nearly a quarter of workers work outside daytime hours, and over two-thirds of them have sleep problems {P(13)}. Night workers are also more likely to have heart disease, "
             f"digestive trouble, infertility and emotional problems, perhaps partly from chronic sleepiness {P(14)}.</p>",
             "After a night shift, the drive home carries a higher crash risk.", key="alerting signal")

ch.try_it("Neha's night-shift plan",
          svg(paper(14, 12, 168, 132, ["NEHA'S SHIFT PLAN", "Fewer night shifts", "Nap and sleep longer", "Bright office lights",
                                       "Fewer shift changes", "Dark, quiet day sleep", "Chai: early in shift"], fs=12, anchor="start", fill="#fff")
              + person(250, 150, 0.95, mood="smile", shirt=BLUE, hair_col="#2b2320", hair="long", arms="hold"),
              "Neha holds her night-shift plan with six points"),
          f"<p><b>Limit night shifts</b> if you can {P(15)}. If you must work them:</p>"
          f"<ol><li>Add naps and allow more time for sleep {P(15)}.</li><li>Use bright lights at work {P(15)}.</li>"
          f"<li>Keep shift changes few, so your clock can adjust {P(15)}.</li><li>For day sleep, cut sound and light in the bedroom {P(15)}.</li>"
          f"<li>Caffeine only early in the shift {P(15)}.</li></ol>"
          "<p><b>Try it:</b> what if Neha still cannot sleep in the day?</p>"
          f"<details><summary>Answer</summary><p>If all else fails, she can ask her doctor whether short-acting sleeping pills are wise {P(15)}.</p></details>",
          "Night shifts need a plan: naps, bright work lights, a dark bedroom, early caffeine.", key="night shifts")

ch.watch_out("Wide awake? Do not stay in bed",
             svg(awake_in_bed(14, 150, 130) + clock(90, 40, 20, 1, 20) + text(90, 76, "20 minutes, still awake", 9, weight=700)
                 + arrow(150, 110, 200, 110)
                 + armchair(206, 150)
                 + books(250, 102, 2) + text(240, 72, "read till sleepy", 9, weight=700),
                 "Someone awake in bed for 20 minutes, with an arrow to an armchair and a book"),
             talk(("pinky", "Awake 20 minutes already. If I lie still, sleep will come, na?"),
                  ("chintu", f"Still awake after more than <b>20 minutes</b>, or getting anxious? Get up and do something relaxing until you feel sleepy. The anxiety of not sleeping can itself make sleep harder {P(35)}"),
                  ("sharma", "Our tip: an armchair, a dull book, a dim lamp. Not the phone.")),
             "Awake for 20 minutes? Get up, do something calm, come back when sleepy.", key="20 minutes")

ch.myths([
    ("A nightcap helps you sleep well.", f"Alcohol robs deep and REM sleep; you wake as it wears off {P(31)}."),
    ("A late workout tires you out for bed.", f"Vigorous exercise just before bed can delay sleep {P(32)}."),
    ("A 4 pm coffee is gone by bedtime.", f"Caffeine can take up to 8 hours to wear off fully {P(33)}."),
])

ch.redpen([f"Same bed and wake time, daily {P(33)}.", f"No caffeine late in the day {P(33)}.", f"Exercise, but not 2 to 3 h before bed {P(33)}.",
           f"Cool, dark, quiet, screen-free room {P(35)}.", f"Awake 20 minutes? Get up {P(35)}."],
          where="the sleep habits",
          panel=svg(notes(12, 12, 178, 104, ["Same bed and wake time", "No caffeine late", "Cool, dark, no screens", "Awake 20 min? Get up"])
                    + clock(222, 40, 18, 11, 0)
                    + sharma(270, 150, 1.0, "flat", "skeptic", arms="point"),
                    "Sharma ji points at his red-pen page: same bed and wake time, no late caffeine, a cool dark room, get up after 20 minutes awake"))

ch.oneliner("which habits help me sleep?",
            f"Go to bed and wake up at the same time every day {P(33)}, and keep caffeine {P(33)}, alcohol {P(34)} and screens {P(35)} away from bedtime.",
            panel=svg(person(62, 150, 0.95, mood="o", shirt=BLUE, hair_col="#2b2320", hair="long")
                      + bubble(8, 8, 112, "Which habits help me sleep?", 62, 70, fs=10)
                      + chai(150, 150, 1.2)
                      + pinky(256, 150, 0.95, mood="grin", arms="wave")
                      + bubble(130, 8, 184, "Go to bed and wake up at the same time every day", 256, 60, fs=10),
                      "Neha asks which habits help, and Pinky answers: same bedtime and wake-up time every day"))

ch.quizzes([
    ("Pinky has a coffee at 4 pm and bed at 11 pm. Problem?",
     f"Possibly. Caffeine can take up to 8 hours to wear off fully, so a late afternoon coffee can make it hard to fall asleep {P(33)}.",
     "The 7 pm cutting chai"),
    ("Neha ends a night shift at 7 am. What should she watch out for?",
     f"The drive home: in the early morning her body clock sends no alerting signal, and night shift workers crash more on that drive {P(14)}.",
     "Neha's drive home at 7 am"),
])

ch.recall([
    ("What sets your body clock each day?",
     f"Light. Your body clock reads light signals coming in through your eyes {P(13)}, and daylight is key to your daily sleep pattern {P(35)}.",
     "The clock in your head"),
])

ch.done("Pinky's kal finally comes",
        "Two weeks on, the sticky notes are gone. Pinky sleeps at 11, wakes at 7, takes her chai on the balcony, and her last cup is before 3 pm. "
        "Sharma ji checks her diary twice and finds nothing to circle.",
        panel=svg(sun(40, 34, 14)
                  + paper(80, 16, 100, 70, ["2 WEEKS", "11 pm to 7 am", "every day"], fs=9, fill="#fff", rot=-3)
                  + pinky(120, 150, 0.9, mood="grin", arms="up")
                  + sharma(210, 150, 0.9, "flat", "flat", arms="hold")
                  + chintu(280, 150, 0.75, mood="grin", arms="wave"),
                  "Pinky cheers next to her two-week sleep log while Sharma ji holds it and finds nothing to circle"))


# ======================= ADVANCED 1 =======================
ch = deck.chapter("advanced", "Is your snoring sleep apnea, and what fixes it?", glossary=[
    ("PSG", "the overnight sleep-lab test."),
    ("Sleep apnea", "breathing that keeps stopping during sleep."),
    ("Airway", "the path air takes to the lungs."),
    ("CPAP", "a mask that blows gentle air."),
    ("Deep sleep", "stage 3, the most restorative stage."),
    ("Sleep specialist", "a doctor trained in sleep problems."),
])

ch.opener(
    svg(sharma_in_bed(16, 150, 150)
        + text(90, 70, "GHRRR", 16, weight=800, fill=CORAL) + text(130, 92, "zzz", 12, weight=800, fill=BLUE)
        + aunty(250, 150, mood="o", arms="hold")
        + phone(266, 98, ["REC"], fs=9, h=36, w=28)
        + bubble(176, 6, 138, "Every night, like a pressure cooker!", 250, 60),
        "Sharma ji snores loudly in bed while Sharma aunty records it on her phone"),
    scene("Sharma aunty posts a 40-second clip on the family WhatsApp group: Sharma ji, snoring.")
    + talk(("Sharma aunty", "Every night, like a pressure cooker!"),
           ("sharma", "\"Bade bade deshon mein aisi chhoti chhoti baatein hoti rehti hain.\" Everyone snores."),
           ("chintu", f"Dilwale Dulhania Le Jayenge (1995) aside, snoring is no laughing matter: frequent loud snoring is often a sign of sleep apnea {P(36)}.")),
    "Frequent loud snoring can be a sign of sleep apnea.")

ch.idea("Why snoring happens",
        svg(text(80, 22, "OPEN AIRWAY", 9, weight=800, fill=TEAL) + text(240, 22, "NARROW AIRWAY", 9, weight=800, fill=CORAL)
            + f'<rect x="20" y="40" width="120" height="44" rx="10" fill="#fff" stroke="{INK}" stroke-width="2"/>'
            + arrow(32, 62, 128, 62, TEAL2, 2.4)
            + f'<path d="M180 40 L300 40 L300 84 L180 84 Z" fill="#fff" stroke="{INK}" stroke-width="2"/>'
            + f'<path d="M216 40 Q240 58 264 40 Z M216 84 Q240 66 264 84 Z" fill="{CORAL}"/>'
            + f'<path d="M188 62 q8 -8 16 0 t16 0 t16 0 t16 0 t16 0 t16 0" fill="none" stroke="{CORAL}" stroke-width="2.4"/>'
            + text(80, 104, "quiet", 11, weight=700) + text(240, 104, "flutter = snore", 11, weight=700)
            + text(160, 134, "soft tissue relaxes, the pipe narrows", 9, weight=600, fill="#6d675f"),
            "An open tube with smooth air, and a narrowed tube where the air flutters into a snore"),
        f"<p>Snoring comes from a narrowed or partly blocked <b>airway</b> at the back of the mouth, throat or nose: the air turns turbulent and soft tissues vibrate {P(36)}.</p>"
        f"<p>A relaxed palate, tongue and throat, allergies, sinus trouble and extra weight narrow it; alcohol or sedatives near bedtime make snoring worse {P(36)}.</p>"
        f"<p><b>About half</b> of adults snore, half of them loudly and often. It rises with age, and US surveys find loud, frequent snoring more common in African Americans, Asians and Hispanics {P(36)}.</p>",
        "A snore is air squeezing through a pipe that got narrower.", key="airway")

ch.example("Snoring without pauses still costs",
           svg(text(160, 18, "VERY SLEEPY IN THE DAY (OLDER ADULTS)", 9, weight=800, fill=TEAL)
               + bars([("Never snore", 40, GREY, "1x"), ("6-7 nights", 90, CORAL, "over 2x")], x=96, y=36, step=34, scale=1.8)
               + text(160, 118, "more than twice as likely, not exact data", 8.5, weight=500, fill="#6d675f"),
               "Two bars: older adults who snore 6 to 7 nights a week are more than twice as likely to be very sleepy", floor=False),
           f"<p>Even without breathing pauses, snoring adds effort to your breathing and can lower your sleep quality {P(37)}.</p>"
           f"<p>Older adults who snored 6 to 7 nights a week, without apnea, were more than <b>twice as likely</b> to be extremely sleepy in the day, "
           f"and snorers are more likely to be in car crashes {P(37)}.</p>"
           f"<p>Women who snored regularly were twice as likely to develop <b>diabetes</b>; regular snoring may also raise the risk of high blood pressure, heart failure and stroke {P(37)}.</p>",
           "Regular snoring may be a health risk even without pauses in breathing.", key="twice as likely")

ch.picture("Sleep apnea: the pause and the snort",
           svg(text(160, 22, "ALL NIGHT, AGAIN AND AGAIN", 9, weight=800, fill=TEAL)
               + flow([["Airway", "closes"], ["Oxygen", "drops"], ["Brain", "wakes"], ["Snort,", "breathe"]],
                      y=36, x0=12, w=58, gap=18, h=40, fs=9, cols=[BLUE, CORAL, HALDI, TEAL2])
               + loop_back(269, 41, 78, 26)
               + text(155, 136, "each pause: 10 to 120 seconds", 9, weight=700)
               + text(155, 154, "20 to 30 or more times an hour", 9, weight=700),
               "Four boxes in a loop: the airway closes, oxygen drops, the brain wakes, a snort, then again", floor=False),
           f"<p>In sleep apnea, breathing stops again and again {P(44)}:</p>"
           f"<ol><li>Soft tissue at the back of the throat collapses and partly or fully closes the airway {P(44)}.</li>"
           f"<li>Oxygen in the blood falls {P(44)}.</li><li>The brain wakes you just enough to reopen the airway {P(44)}.</li>"
           f"<li>Breathing restarts, often with a loud snort or choking sound {P(44)}.</li></ol>"
           f"<p>Each pause lasts <b>10 to 120 seconds</b> and can come 20 to 30 times or more an hour, so people rarely get enough <b>deep, restorative sleep</b> {P(44)}.</p>",
           "With apnea, you can spend all night in bed and still get little deep sleep.", key="10 to 120 seconds")

ch.watch_out("What untreated apnea does",
             svg(heart(80, 76, 4.2)
                 + sign(150, 12, 160, "BLOOD PRESSURE UP", fs=9, fill=CORAL, color="#fff")
                 + sign(150, 38, 160, "HEART ATTACK, STROKE", fs=9, fill=CORAL, color="#fff")
                 + sign(150, 64, 160, "IRREGULAR HEARTBEAT", fs=9, fill=HALDI)
                 + sign(150, 90, 160, "HEART FAILURE", fs=9, fill=HALDI)
                 + sign(150, 116, 160, "MORNING HEADACHES", fs=9, fill="#fff")
                 + text(80, 140, "stress hormones", 9, weight=700),
                 "A big heart next to five warning labels: blood pressure up, heart attack and stroke, irregular heartbeat, heart failure, morning headaches"),
             table2(["Where", "What it can do"], [
                 ["Brain", f"morning headaches; poor focus, learning and memory {P(44)}"],
                 ["Heart", f"<b>stress hormones</b> raise blood pressure, heart rate, and the risk of heart attack, stroke, irregular heartbeat, heart failure {P(44)}"],
                 ["Body", f"higher risk of obesity and diabetes {P(46)}"],
                 ["Daytime", f"sleepiness <b>more than triples</b> traffic and work accident risk; linked to depression {P(44)}"],
             ], first=24),
             "Untreated sleep apnea is a risk to your heart, not just your mood.", key="stress hormones")

ch.chat("You cannot hear your own snoring",
        duo(sharma(70, 150, mood="flat", brow="flat"), ("I slept perfectly.", 10),
            aunty(240, 150, mood="o"), ("You stopped breathing. Twice.", 10),
            "Sharma ji says he slept perfectly while his wife says he stopped breathing twice; over half are not diagnosed",
            extra=sign(104, 96, 110, ["OVER HALF ARE", "NOT DIAGNOSED"], fs=9, fill=HALDI)),
        [("sharma", "I slept perfectly."),
         ("Sharma aunty", "You stopped breathing. Twice."),
         ("chintu", f"More than half of people with sleep apnea are <b>not diagnosed</b> {P(46)}. They usually do not know their breathing stops, so bed partners are the ones who notice {P(46)}")],
        points=[f"A doctor must confirm it with <b>overnight</b> sleep monitoring {P(46)}"],
        moral="If your family complains about your snoring, they are giving you data.", badge="Watch out", key="not diagnosed")

ch.glance("Who is more likely to get sleep apnea",
          svg(sign(12, 12, 96, "RELAXED THROAT", fs=9, fill="#fff") + sign(12, 44, 96, "BIG TONSILS", fs=9, fill="#fff")
              + sign(12, 76, 96, "OVERWEIGHT", fs=9, fill=HALDI)
              + sign(212, 12, 96, "SMALL AIRWAY", fs=9, fill="#fff") + sign(212, 44, 96, "ALLERGY BLOCK", fs=9, fill="#fff")
              + sign(212, 76, 96, "RUNS IN FAMILY", fs=9, fill=HALDI)
              + sharma(160, 150, 1.0, "flat", "skeptic"),
              "Six risk-factor labels around Sharma ji: relaxed throat, big tonsils, overweight, small airway, allergy block, family history"),
          table2(["Risk factor", "Why"], [
              ["<b>Overweight</b>", "neck fat makes it harder to keep the throat open"],
              ["Throat and tongue", "relax more than normal in sleep"],
              ["Tonsils, airway", "big tonsils and adenoids, a smaller airway, allergy congestion"],
              ["Family history", "it runs in families"],
          ], first=32)
          + f"<p>Risk factors from the guide {P(47)}. More common in men; over half of people with it are overweight; "
            f"in US data, more common in African American, Asian, Native American and Hispanic people {P(46)}.</p>",
          "Weight, throat shape and family history all raise the risk.", key="overweight")

ch.chat("Sharma ji at the sleep lab",
        svg(bed(14, 150, 150, sleeper=True)
            + f'<path d="M46 108 Q90 60 186 50 M52 110 Q110 76 186 64" fill="none" stroke="{GREY}" stroke-width="2"/>'
            + monitor(186, 20, 96, 62, ["PSG:", "oxygen,", "breathing"], fs=9)
            + f'<path d="M192 76 l8 0 l4 -8 l4 14 l4 -6 l52 0" fill="none" stroke="{CORAL}" stroke-width="1.6"/>'
            + chintu(296, 150, 0.55, mood="smile"),
            "Sharma ji asleep in bed, wired to a PSG monitor that tracks oxygen and breathing overnight"),
        [("sharma", "Fine. What will they do to me?"),
         ("chintu", f"First, questions for you and your family about your sleep, and a check of your mouth, nose and throat {P(47)}. Then a night of <b>polysomnogram, or PSG</b>: it records brain activity, breathing, heart rate and blood oxygen {P(50)}")],
        points=[f"A PSG is painless, and in some cases done at home {P(50)}"],
        moral="Apnea is confirmed by recording a night of your sleep, and it does not hurt.", badge="Story", key="PSG")

ch.chat("Simple fixes for snoring",
        svg(bed(14, 150, 150, sleeper=True)
            + f'<rect x="20" y="96" width="34" height="18" rx="6" fill="{CREAM}" stroke="{INK}" stroke-width="1.2"/>'
            + text(40, 78, "head raised", 9, weight=700)
            + f'<rect x="210" y="40" width="8" height="40" rx="2" fill="{GREY}"/>' + cross(214, 60, 1.6)
            + text(214, 96, "no smoking", 9, weight=700)
            + f'<path d="M262 40 L266 80 L282 80 L286 40 Z" fill="#fff" stroke="{INK}" stroke-width="1.3"/>' + cross(274, 60, 1.6)
            + text(274, 96, "no late drink", 9, weight=700)
            + text(110, 30, "sleep on your side", 10, weight=800, fill=TEAL),
            "A sleeper on raised pillows, sleeping on the side, with a crossed-out cigarette and a crossed-out drink"),
        [("pinky", "Any simple fixes before machines?"),
         ("chintu", f"For adults, these may help: lose weight, stop tobacco, sleep on <b>your side</b>, raise your head, treat a blocked nose, skip alcohol or sedatives before sleep. Some are helped by dental appliances {P(38)}"),
         ("sharma", f"And the nasal strips on TV? No scientific evidence supports their claims {P(38)}")],
        moral="Side sleeping, weight loss and no alcohol before bed can quiet a snore.", key="your side")

ch.chat("Mild, moderate or severe: what each needs",
        svg(pills(12, 14, 3) + cross(36, 25, 1.4)
            + sign(8, 44, 112, ["SEDATIVES:", "LONGER PAUSES"], fs=9, fill=CORAL, color="#fff")
            + layers([("Mild", GREEN, "habits may be enough"),
                      ("Moderate or severe", CORAL, "more direct treatment")], x=10, y=80, w=128, h=26, gap=8)
            + sharma(288, 150, 0.85, "flat", "skeptic")
            + bubble(130, 8, 140, "Can I just take a sleeping pill?", 288, 70, fs=9.5),
            "Sharma ji asks about a sleeping pill, crossed out because sedatives make pauses longer; mild apnea may need only habits, moderate or severe needs more"),
        [("sharma", "Can I just take a sleeping pill?"),
         ("chintu", f"No. With apnea, <b>sedatives</b> can make the pauses longer and worse {P(48)}. Start with habits: sleep on your side, lose weight if overweight, avoid alcohol, smoking, sleeping pills and herbal supplements {P(48)}"),
         ("pinky", f"So habits may be enough for <b>mild</b> apnea, but moderate or severe apnea needs more direct treatment {P(48)}")],
        moral="With apnea, avoid sleeping pills: they can make the pauses longer.", key="mild")

ch.true_story("Jim's machine, from the guide",
              svg(bed(14, 150, 150, sleeper=True)
                  + cpap(194, 150)
                  + f'<path d="M194 128 Q140 96 50 112" fill="none" stroke="{GREY}" stroke-width="4" stroke-linecap="round"/>'
                  + sign(160, 10, 152, ["MILD AIR PRESSURE KEEPS", "THE AIRWAY OPEN"], fs=9, fill="#fff")
                  + chintu(282, 150, 0.7, mood="smile", arms="wave"),
                  "A sleeper wearing a CPAP mask connected by a tube to a small machine, under a note that mild air pressure keeps the airway open"),
              f"<p>The guide quotes Jim. His wife noticed he snored loudly and sometimes stopped breathing, and pushed him to see a doctor {P(36)}. "
              f"He was prescribed <b>CPAP</b> but found it uncomfortable and rarely used it. One day at work he felt so bad he went to hospital, with symptoms like a stroke. He went back to his doctor and got a more comfortable machine {P(49)}.</p>"
              f"<p>CPAP is the most effective treatment for adults: mild air pressure through a mask keeps the airway open. "
              f"Apnea returns if CPAP is stopped or used wrongly {P(48)}. {src(PDF, 'Read the guide')}</p>",
              "Apnea returns when CPAP stops, so tell your doctor if the mask is uncomfortable.", key="CPAP")

ch.glance("CPAP, mouthpiece, surgery, pills",
          svg(cpap(24, 150) + text(50, 102, "mask + air", 10, weight=800)
              + f'<path d="M104 112 Q134 90 164 112 L160 130 Q134 118 108 130 Z" fill="#fff" stroke="{INK}" stroke-width="1.4"/>' + text(134, 80, "mouthpiece", 10, weight=800)
              + pills(186, 108, 4) + cross(219, 119, 1.8) + text(219, 90, "no cure pill", 10, weight=800)
              + sign(60, 14, 200, "TREATMENTS FOR SLEEP APNEA", fs=9, fill=HALDI)
              + chintu(288, 150, 0.6, mood="smile"),
              "A CPAP box, a dental mouthpiece and a crossed-out pill strip"),
          table2(["Option", "What the guide says"], [
              ["CPAP", f"does not breathe for you; a specialist can ease a dry or stuffy nose, sore skin or eyes, bloating, headaches {P(48)}"],
              ["<b>Mouthpiece</b>", f"mild apnea or loud snoring; made by a dentist; recheck with a sleep study {P(49)}"],
              ["Surgery", f"tonsils and adenoids out, often in children {P(49)}"],
              ["Medicines", f"<b>none cure</b> sleep apnea; some ease sleepiness {P(48)}"],
          ], first=28),
          "No pill cures sleep apnea; CPAP is the strongest treatment for adults.", key="mouthpiece")

ch.myths([
    ("Everyone who snores has sleep apnea.", f"Not everyone who snores has sleep apnea {P(36)}."),
    ("Nasal strips cure snoring.", f"No scientific evidence shows nasal strips stop snoring {P(38)}."),
    ("A pill can cure sleep apnea.", f"No medicine cures apnea; some only ease the sleepiness {P(48)}."),
    ("Once CPAP works, you can stop.", f"Sleep apnea returns if CPAP is stopped or used wrongly {P(48)}."),
])

ch.redpen([f"Loud snoring plus pauses: see a doctor {P(37)}.", f"Apnea raises heart attack and stroke risk {P(44)}.", f"Sleep on your side; skip the nightcap {P(48)}.",
           f"Avoid sleeping pills and herbal supplements {P(48)}.", f"Stop CPAP and apnea returns {P(48)}."],
          where="the snoring chapter",
          panel=svg(notes(12, 12, 182, 104, ["Snoring + pauses: doctor", "Sleep on your side", "Avoid sleeping pills", "Stop CPAP, apnea returns"])
                    + cpap(200, 150)
                    + sharma(282, 150, 1.0, "flat", "skeptic", arms="point"),
                    "Sharma ji points at his red-pen page next to his CPAP machine: snoring with pauses means a doctor, side sleeping, no pills without asking, keep using CPAP"))

ch.oneliner("is my snoring actually a problem?",
            f"Loud, frequent snoring with pauses in breathing can be sleep apnea {P(37)}: get it checked {P(30)}.",
            panel=svg(sharma(64, 150, 0.95, "flat", "skeptic")
                      + bubble(8, 8, 116, "Is my snoring actually a problem?", 64, 70, fs=10)
                      + phone(140, 98, ["REC"], fs=9, h=36, w=28)
                      + chintu(256, 150, 0.95, mood="smile", arms="wave")
                      + bubble(134, 8, 180, "Loud, frequent snoring with pauses in breathing can be sleep apnea", 256, 56, fs=9.5),
                      "Sharma ji asks if his snoring is a problem, and Chintu answers in one breath"))

ch.quizzes([
    ("A sleeping pill on apnea nights. Wise?",
     f"No. With apnea, sleeping pills and sedatives can make the breathing pauses longer and more severe {P(48)}.",
     "Mild, moderate or severe: what each needs"),
    ("Jim rarely used his CPAP mask. What happened?",
     f"Not enough oxygen reached his brain, and he went to hospital with stroke-like symptoms {P(49)}. Apnea returns if CPAP is stopped or used incorrectly {P(48)}.",
     "Jim's machine, from the guide"),
])

ch.recall([
    ("A child snores loudly 3 to 4 times a week. What should you do?",
     f"Have a doctor check the child, especially with pauses in breathing, hyperactivity or daytime sleepiness {P(38)}.",
     "A child who snores 3 to 4 nights a week"),
])

ch.done("Sharma ji wears the mask",
        "The sleep study confirms it: moderate sleep apnea. Sharma ji sleeps on his side, skips the nightcap and wears his CPAP mask every night. "
        "Sharma aunty deletes the WhatsApp clip. The house is quiet at last.",
        panel=svg(paper(16, 16, 128, 40, ["SLEEP STUDY", "result: treat it"], fs=10, fill="#fff")
                  + bed(14, 150, 150, sleeper=True) + cpap(176, 150)
                  + f'<path d="M176 128 Q120 96 46 112" fill="none" stroke="{GREY}" stroke-width="4" stroke-linecap="round"/>'
                  + aunty(276, 150, mood="grin", arms="up"),
                  "Sharma ji asleep with his CPAP mask while Sharma aunty cheers the quiet night"))


# ======================= ADVANCED 2 =======================
ch = deck.chapter("advanced", "Why can't I sleep? Insomnia explained", glossary=[
    ("Sleep disorder", "a medical problem that spoils your sleep."),
    ("Insomnia", "trouble falling or staying asleep."),
    ("CBT", "therapy for sleep habits and thoughts."),
    ("Melatonin", "a sleep hormone, also a pill."),
    ("Sleep apnea", "breathing that keeps stopping during sleep."),
    ("Sleep diary", "a daily note of your sleep."),
])

ch.opener(
    svg(awake_in_bed(14, 150, 150) + clock(120, 40, 22, 2, 0) + text(120, 76, "2 am again", 9, weight=700)
        + think(14, 6, 86, "Week 3.", 40, 100)
        + chintu(262, 150, 0.9, mood="sad")
        + bubble(190, 10, 124, "How many nights a week?", 262, 62),
        "Rohit lies awake at 2 am for the third week while Chintu asks how many nights a week"),
    scene("Rohit has slept badly for three weeks.")
    + talk(("Rohit", "Week 3. Still awake at 2 am."),
           ("chintu", f"How many nights a week? Insomnia means trouble falling or staying asleep, or sleep that does not refresh you despite the chance to sleep {P(41)}. "
                      f"Short spells are common, often from work stress, family pressure or a shock {P(41)}."),
           ("sharma", "Three weeks of what, exactly? Data dikhao.")),
    "Insomnia is trouble falling or staying asleep, or sleep that does not refresh you.")

ch.glance("A few bad nights, or chronic?",
          svg(text(160, 16, "ROHIT'S MONTH", 9, weight=800, fill=TEAL)
              + "".join(week(14, 24 + r * 30, {0, 2, 4, 5} if r % 2 else {1, 3, 4}, w=24, gap=4) for r in range(4))
              + text(226, 52, "CHRONIC:", 11, weight=800, anchor="start", fill=TEAL)
              + text(226, 72, "3+ nights", 10, weight=800, anchor="start", fill=CORAL)
              + text(226, 88, "a week", 10, weight=800, anchor="start", fill=CORAL)
              + text(226, 112, "over 1 month", 10, weight=800, anchor="start", fill=CORAL),
              "Four weeks of a calendar, each with three or four bad nights marked: chronic insomnia", floor=False),
          table2(["Type", "What it means"], [
              ["Short-term", "a few bad nights after stress or a shock; common"],
              ["<b>Chronic</b>", "symptoms at least <b>3 nights a week</b>, for over a month"],
          ], first=28)
          + f"<p>From the guide {P(41)}. About 30 to 40% of adults have some insomnia in a year, and 10 to 15% have it long term. "
            f"It is more common with age and in women, and untreated it can hurt quality of life as much as other long-term illnesses {P(41)}.</p>",
          "Three nights a week for over a month is chronic insomnia.", key="chronic")

ch.glance("Causes of chronic insomnia",
          svg(sign(12, 12, 140, "DEPRESSION, ANXIETY", fs=9, fill=CORAL, color="#fff")
              + sign(12, 40, 140, "ARTHRITIS, ASTHMA", fs=9, fill="#fff")
              + sign(12, 68, 140, "SOME MEDICINES", fs=9, fill="#fff")
              + sign(12, 96, 140, "LATE CHAI, TV IN BED", fs=9, fill=HALDI)
              + sign(12, 124, 140, "APNEA, RESTLESS LEGS", fs=9, fill=BLUE, color="#fff")
              + rohit(236, 150, 1.0, mood="o")
              + text(236, 30, "secondary:", 10, weight=800, fill=TEAL) + text(236, 46, "which one?", 10, weight=700),
              "Five labelled causes of insomnia, from depression to restless legs, next to Rohit wondering which one"),
          table2(["Cause", "Examples"], [
              ["Mood", f"depression, anxiety (most common) {P(41)}"],
              ["Illness, drugs", f"thyroid, asthma, bronchitis, arthritis, heart failure, sickle cell, Alzheimer's, Parkinson's {P(31)} {P(32)} {P(41)}; decongestants, steroids"],
              ["Habits", f"late alcohol, caffeine, exercise; TV in bed {P(42)}"],
              ["Other disorders", f"sleep apnea, restless legs {P(42)}"],
          ], first=30)
          + f"<p>Most chronic insomnia is <b>secondary</b>: caused by another problem or a medicine {P(41)}. In primary insomnia, people are more \"revved up\" {P(42)}.</p>",
          "Most long-term insomnia has another cause: treat that.", key="secondary")

ch.chat("The insomnia loop",
           svg(sign(16, 16, 110, "A bad night", fs=10, fill="#fff") + sign(194, 16, 110, "Worry about sleep", fs=10, fill=HALDI)
               + sign(194, 104, 110, "Watch the clock", fs=10, fill=CORAL, color="#fff") + sign(16, 104, 110, "Harder to sleep", fs=10, fill=BLUE, color="#fff")
               + arrow(130, 26, 188, 26) + arrow(250, 40, 250, 98) + arrow(188, 114, 132, 114) + arrow(70, 98, 70, 42)
               + text(160, 72, "the loop", 12, weight=800, fill=TEAL),
               "Four boxes in a circle: a bad night, worry, clock watching, harder to sleep, and back", floor=False),
           [("Rohit", "The harder I try, the more awake I get. Why?"),
            ("chintu", f"After a few bad nights, people get anxious at the first sign of not falling asleep, and clock-watching makes it worse {P(42)}. Break the <b>loop</b>:")],
           after="<ol><li>Go to bed only when sleepy.</li><li>Not asleep within <b>20 minutes</b>? Get up, go to another room.</li>"
                 f"<li>Read or relax until you feel sleepy.</li><li>Then back to bed {P(42)}.</li></ol>",
           moral="Lying in bed fighting for sleep teaches your brain that bed means fighting.", badge="Picture it", key="loop")

ch.try_it("Relax your body, one muscle at a time",
          svg(person(70, 150, 1.0, mood="smile", shirt=GREEN, hair_col="#3b302b", arms="up")
              + text(228, 20, "RELAXATION", 10, weight=800, fill=TEAL)
              + sign(150, 30, 156, "1. Tense fists: 5 sec", fs=9, fill="#fff")
              + sign(150, 56, 156, "2. Let go: feel it", fs=9, fill="#fff")
              + sign(150, 82, 156, "3. Shoulders, legs...", fs=9, fill="#fff")
              + sign(150, 108, 156, "4. Breathe slow, deep", fs=9, fill=HALDI),
              "Rohit stretches beside four relaxation steps: tense, let go, move to the next muscle, breathe deeply"),
          f"<p><b>Relaxation therapy</b> helps some people with insomnia: meditation, deep breathing, or tensing then relaxing each muscle group before sleep {P(42)}. "
          f"It helps body and mind slow down {P(42)}.</p>"
          "<p><b>Try it</b> (our tip), tonight in bed:</p>"
          "<ol><li>Tense your fists for 5 seconds, then let go.</li><li>Do the same with your shoulders, then your legs.</li><li>Breathe slowly and deeply.</li></ol>"
          "<p>Where did you feel the most tension?</p>"
          "<details><summary>Answer</summary><p>There is no wrong answer. The point is to notice tension and let it go, one group at a time.</p></details>",
          "Tense, let go, breathe: it helps some people fall asleep.", key="relaxation")

ch.chat("Sleep restriction: Rohit's numbers",
           svg(text(160, 18, "SLEEP RESTRICTION: TIME IN BED VS ASLEEP", 9, weight=800, fill=TEAL)
               + bars([("In bed", 80, GREY, "8 h"), ("Asleep (avg)", 55, HALDI, "5.5 h"), ("New window", 55, TEAL2, "5.5 h")],
                      x=96, y=30, step=30, scale=1.8)
               + text(160, 136, "then add a little more each night", 9, weight=700),
               "Bars: 8 hours in bed, 5.5 hours asleep on average, and a new 5.5 hour window in bed", floor=False),
           [("Rohit", "8 hours in bed, about 5.5 asleep. What now?"),
            ("Doctor", f"Try <b>sleep restriction</b>, which works for some people {P(43)}:")],
           after=f"<ol><li>Find your average sleep over a week.</li><li>Limit your time in bed to that.</li><li>Slowly add more time each night {P(43)}.</li></ol>",
           points=[f"Meanwhile: no naps over 15 to 20 minutes, no driving or dangerous machines until you sleep enough {P(43)}"],
           moral="Shrink time in bed to the sleep you really get, then grow it slowly.", badge="Worked example", key="sleep restriction")

ch.chat("CBT: change the habit and the thought",
        svg(rohit(80, 150, 0.95, mood="sad")
            + bubble(8, 8, 150, "I will never sleep without a pill.", 80, 72, fs=10)
            + arrow(162, 26, 178, 26)
            + sign(182, 10, 132, ["CBT: A MORE", "REALISTIC THOUGHT"], fs=9, fill=GREEN, color="#fff")
            + doctor(250, 150, 0.9, arms="hold"),
            "Rohit says he will never sleep without a pill, and CBT turns it into a more realistic thought, with his doctor"),
        [("Rohit", "I will never sleep without a pill. Never."),
         ("chintu", f"That thought is what <b>CBT</b>, cognitive behavioural therapy, works on: it swaps negative thoughts about sleep for realistic ones. Reconditioning, relaxation and sleep restriction are part of it too {P(43)}"),
         ("sharma", f"Data says it is effective in most people with chronic insomnia {P(43)}")],
        moral="For long-term insomnia, CBT works for most people.", key="CBT")

ch.watch_out("A pill is not the first fix",
             svg(f'<rect x="40" y="56" width="56" height="80" rx="8" fill="#fff" stroke="{INK}" stroke-width="2"/>'
                 + f'<rect x="36" y="42" width="64" height="16" rx="4" fill="{CORAL}"/>'
                 + text(68, 92, "sedatives", 9, weight=800, fill=CORAL)
                 + text(68, 122, "?", 26, weight=800, fill=CORAL)
                 + stamp(196, 50, "ASK A DOCTOR", color=TEAL, rot=-6, fs=11)
                 + chintu(240, 150, 0.75, mood="flat", arms="hold"),
                 "A bottle of sedatives with a question mark, a stamp saying ask a doctor, and Chintu looking unsure"),
             talk(("Rohit", "My cousin takes a sleeping pill every night. Why not me?"),
                  ("chintu", f"Talk to a doctor first. Alcohol, <b>sedatives</b> over the counter or prescribed, and drowsy antihistamines have limited benefits and risks: some leave you groggy in the morning, some stop working over time {P(43)}"),
                  ("sharma", f"And some people not helped by behaviour therapy may need a prescription {P(43)}")),
             "For long-term insomnia, retrain the habit before you reach for the bottle.", key="sedatives")

ch.glance("Melatonin and valerian: the 'natural' fixes",
          svg(phone(14, 14, ["NATURAL", "SLEEP", "CURE!", "21 days"], fs=10, h=110, w=72)
              + stamp(138, 50, "NOT PROVEN", color=CORAL, rot=-8, fs=11)
              + f'<rect x="196" y="70" width="34" height="56" rx="6" fill="#fff" stroke="{INK}" stroke-width="1.6"/><rect x="194" y="60" width="38" height="12" rx="3" fill="{TEAL2}"/>'
              + sharma(276, 150, 0.9, "flat", "skeptic", arms="point"),
              "A phone ad promising a natural sleep cure in 21 days, stamped not proven, with Sharma ji pointing at a supplement bottle"),
          table2(["Remedy", "What the guide says"], [
              ["<b>Melatonin</b> for insomnia", f"little evidence it helps {P(44)}"],
              ["Melatonin for jet lag", f"seen as safe for days or weeks; results mixed; long-term safety unclear {P(17)}"],
              ["Valerian tea or extract", f"studies inconclusive; dose and purity vary {P(44)}"],
          ], first=36)
          + f"<p>In the US these remedies are not regulated, so their safety is not monitored {P(44)}. "
            "Natural is <b>not proven</b>: a \"21 din mein\" promise, like Phir Hera Pheri's (2006) scheme, deserves Sharma ji's red pen.</p>",
          "Natural does not mean proven. Ask your doctor first.", key="not proven")

ch.chat("What the doctor will ask Rohit",
        svg(doctor(62, 150, 1.0, arms="hold")
            + paper(100, 18, 114, 104, ["SLEEP HISTORY", "Hours slept?", "Times woken?", "Time to sleep?", "Rested?"], fs=9.5, anchor="start", fill="#fff")
            + rohit(266, 150, 0.95, mood="o")
            + bubble(220, 8, 94, "How will you know it is insomnia?", 266, 72, fs=9.5),
            "A doctor with a sleep-history list of questions, and Rohit asking how she will know it is insomnia"),
        [("Rohit", "How will you know it is insomnia?"),
         ("Doctor", f"Mainly from your <b>sleep history</b>, often a sleep diary {P(42)}: hours slept, how often and how long you wake, time to fall asleep, how rested you feel {P(50)}. Maybe an overnight test, if I suspect another disorder {P(42)}"),
         ("sharma", f"And the partner may be asked too, as you may not notice your own symptoms {P(50)}")],
        moral="Bring your diary; your doctor diagnoses insomnia mostly from your sleep story.", badge="Story", key="sleep history")

ch.try_it("Spot the problems in Rohit's sleep diary",
          svg(paper(14, 12, 182, 132, ["ROHIT'S SLEEP DIARY", "Chai: 1 cup, 8 pm", "Drinks: 2, at 9 pm", "Nap: 3:30 pm, 45 min",
                                       "Woke: 5 times, 2 hours", "Today: struggled to stay awake"], fs=9.5, anchor="start", fill="#fff")
              + sign(214, 10, 100, "FIND FOUR", fs=10, fill=HALDI)
              + sharma(262, 150, mood="flat", brow="skeptic", arms="point"),
              "A sleep diary with chai at 8 pm, 2 drinks at 9 pm and a long late nap, and Sharma ji pointing at it"),
          f"<p>Rohit's <b>sleep diary</b> copies the guide's own sample page {P(60)}. Find four habits spoiling his sleep.</p>"
          f"<details><summary>Answer</summary><p>Chai at 8 pm: caffeine can take up to 8 hours to wear off {P(33)}. "
          f"Two drinks at 9 pm: alcohol wakes you when it wears off {P(34)}. The nap is after 3 pm {P(34)} and longer than 20 minutes {P(29)}. "
          f"Waking often or for long spells, and struggling to stay awake, are signs to show a doctor if they keep happening {P(59)}.</p></details>",
          "A diary shows the habits that keep you from sleeping well.", key="sleep diary")

ch.myths([
    ("The main cause of insomnia is worry.", f"Illness, medicines or depression can cause it too {P(30)}."),
    ("Melatonin is a proven cure for insomnia.", f"Little evidence shows melatonin helps insomnia {P(44)}."),
    ("Stay in bed longer to catch more sleep.", f"Awake 20 minutes? Get up and do something relaxing {P(42)}."),
    ("Sleeping pills are the best long-term fix.", f"CBT is effective in most people with chronic insomnia {P(43)}."),
])

ch.redpen([f"Signs on 3+ nights a week: see a doctor {P(40)}.", f"Find the cause behind it {P(41)}.", f"Awake 20 minutes? Get up {P(42)}.",
           f"CBT before pills {P(43)}.", f"Natural is not proven {P(44)}."],
          where="the insomnia chapter",
          panel=svg(notes(12, 12, 180, 104, ["3 nights a week? Doctor", "Awake 20 min? Get up", "CBT before pills", "Natural is not proven"])
                    + paper(204, 30, 44, 56, ["SLEEP", "DIARY"], fs=8.5, fill="#fff", rot=5)
                    + sharma(282, 150, 1.0, "flat", "skeptic", arms="point"),
                    "Sharma ji points at his red-pen page next to a sleep diary: see a doctor, get up after 20 minutes, CBT before pills, natural is not proven"))

ch.oneliner("what actually fixes long-term insomnia?",
            f"Treat what is causing it {P(42)}, and use CBT: new sleep habits and calmer thoughts about sleep {P(43)}.",
            panel=svg(rohit(62, 150, 0.95, mood="o")
                      + bubble(8, 8, 116, "What actually fixes long-term insomnia?", 62, 72, fs=10)
                      + paper(132, 92, 50, 40, ["SLEEP", "DIARY"], fs=8.5, fill="#fff", rot=-4)
                      + doctor(256, 150, 0.95, arms="hold")
                      + bubble(136, 8, 178, "Treat what is causing it, and use CBT", 256, 66, fs=10),
                      "Rohit asks what fixes long-term insomnia and the doctor answers in one breath"))

ch.quizzes([
    ("Bad sleep 4 nights a week, for 6 weeks. What is it?",
     f"Chronic insomnia: symptoms at least 3 nights a week for more than a month {P(41)}.",
     "A few bad nights, or chronic?"),
    ("Rohit's cousin says melatonin will cure him. True?",
     f"Little evidence shows melatonin relieves insomnia, and in the US these supplements are not monitored for safety {P(44)}.",
     "Melatonin and valerian: the 'natural' fixes"),
])

ch.recall([
    ("Why can a 7 pm chai still keep you awake at 1 am?",
     f"Caffeine can take up to 8 hours to wear off fully {P(33)}, and it is thought to block adenosine's sleep signal {P(31)}.",
     "The 7 pm cutting chai"),
])

ch.done("Rohit sleeps through to 6",
        "Six weeks of CBT: a fixed window, the armchair when he cannot sleep, and no chai after 3 pm. "
        "Rohit now falls asleep in 20 minutes and sleeps through to 6. His doctor slowly widens his window.",
        panel=svg(sun(286, 30, 13) + bed(14, 150, 150, sleeper=True)
                  + clock(200, 50, 20, 6, 0) + text(200, 86, "6 am", 10, weight=700)
                  + chintu(262, 150, 0.8, mood="grin", arms="up"),
                  "Rohit asleep until 6 am as the sun rises, with Chintu cheering"))


# ======================= ADVANCED 3 =======================
ch = deck.chapter("advanced", "What are restless legs, narcolepsy and sleepwalking?", glossary=[
    ("Sleep disorder", "a medical problem that spoils your sleep."),
    ("REM", "rapid eye movement: the dreaming stage."),
    ("PSG", "the overnight sleep-lab test."),
    ("MSLT", "a daytime nap test."),
    ("Restless legs syndrome, RLS", "tingling legs you must move."),
    ("Narcolepsy", "sudden, overwhelming daytime sleep."),
])

ch.opener(
    svg(f'<rect x="10" y="10" width="300" height="56" rx="4" fill="{INK}"/><rect x="16" y="16" width="288" height="44" rx="2" fill="{BLUE}"/>'
        + text(160, 44, "MOVIE NIGHT", 12, weight=800, fill="#fff")
        + mausi(80, 150, 0.85, mood="sad", arms="up")
        + f'<rect x="20" y="124" width="290" height="26" rx="4" fill="{CORAL}" opacity=".35"/>'
        + pinky(170, 150, 0.8, mood="o") + chintu(260, 150, 0.75, mood="o")
        + text(30, 84, "again?", 10, weight=700, fill=CORAL),
        "Lata mausi stands up in the cinema row for the fourth time while Pinky and Chintu look puzzled"),
    scene("Movie night. Lata mausi stands up in the cinema row for the fourth time.")
    + talk(("Lata mausi", "My legs feel like ants are crawling inside. I have to move."),
           ("chintu", f"The four most common sleep disorders are <b>insomnia</b>, <b>sleep apnea</b>, restless legs syndrome and narcolepsy {P(39)}. "
                      "This chapter covers the last two, and the odd things some people do asleep.")),
    "Restless legs and narcolepsy are two of the four most common sleep disorders.")

ch.chat("Restless legs: the urge to move",
        svg(legs(60, 150) + text(80, 30, "RESTLESS LEGS", 10, weight=800, fill=CORAL) + text(80, 46, "tingle, crawl", 9, weight=700)
            + arrow(130, 96, 170, 96)
            + mausi(230, 150, 0.95, mood="smile", arms="hold")
            + text(230, 34, "move: relief", 10, weight=800, fill=GREEN),
            "Tingling restless legs, an arrow, and Lata mausi relieved after moving them"),
        [("pinky", "Ants in her legs? What is it?"),
         ("chintu", f"That can be <b>restless legs syndrome</b>: an unpleasant prickling or tingling in the legs, often the calves, eased by moving or rubbing them, so falling and staying asleep get hard {P(53)}"),
         ("sharma", f"Even the arms, sometimes. It can come on when you sit or lie still for long: a desk, a car, a movie {P(53)}")],
        moral="Creepy feelings in the legs that ease when you move them can be RLS.", key="restless legs")

ch.glance("RLS: who gets it, and why",
          svg(sign(14, 14, 120, "RUNS IN FAMILIES", fs=9, fill=HALDI)
              + sign(14, 44, 120, "PREGNANCY", fs=9, fill="#fff")
              + sign(14, 74, 120, "KIDNEY FAILURE", fs=9, fill="#fff")
              + sign(14, 104, 120, "LOW IRON", fs=9, fill=CORAL, color="#fff")
              + arrow(140, 114, 176, 114)
              + sign(182, 104, 84, "LOW DOPAMINE", fs=9, fill=BLUE, color="#fff")
              + doctor(286, 150, 0.6, arms="hold"),
              "Labels for family, pregnancy, kidney failure and low iron, with an arrow from low iron to low dopamine"),
          table2(["Fact", "From the guide"], [
              ["Causes", "often inherited; pregnancy, kidney failure, <b>low iron</b> or vitamins"],
              ["Why", "low iron may mean too little <b>dopamine</b>, a brain chemical that controls the limbs"],
              ["Diagnosis", "the symptoms, worse at rest and at night; maybe an iron blood test"],
          ], first=26)
          + f"<p>All from {P(53)}, which adds: more common with age and in women; children can have it too.</p>",
          "Low iron can be behind restless legs, and a blood test can check.", key="low iron")

ch.chat("RLS can be treated",
        svg(legs(40, 150) + text(58, 30, "TREATABLE", 10, weight=800, fill=GREEN)
            + sign(108, 14, 112, "STRETCH", fs=9, fill="#fff") + sign(108, 42, 112, "HOT BATH", fs=9, fill="#fff")
            + sign(108, 70, 112, "LEG MASSAGE", fs=9, fill="#fff") + sign(108, 98, 112, "NO CAFFEINE", fs=9, fill=HALDI)
            + doctor(276, 150, 0.95, arms="hold")
            + bubble(222, 8, 92, "Some doctors check iron.", 276, 56),
            "Four leg-care habits listed next to a doctor who says some doctors check iron: restless legs are treatable"),
        [("pinky", "Can Lata mausi's legs be fixed?"),
         ("chintu", f"RLS is <b>treatable</b> but not always curable: dopamine-like drugs or iron work fast, and milder cases may do well with sedatives or habits {P(53)}"),
         ("Doctor", f"Some doctors check iron with a blood test {P(53)}. Low iron or vitamins? Iron, B12 or folate may help. Stretching, a hot bath, leg massage and no caffeine help too; some antidepressants may cause RLS {P(54)}")],
        moral="Restless legs is treatable, often quickly, so see a doctor.", key="treatable")

ch.chat("Arjun falls asleep mid-sentence",
        svg(desk(14, 112, 150) + monitor(40, 46, 90, 58, ["Project", "update"], fs=9)
            + sign(10, 8, 104, "NARCOLEPSY?", fs=10, fill=HALDI)
            + person(196, 150, 0.9, mood="flat", shirt=BLUE, hair_col="#2b2320")
            + text(222, 70, "z", 14, fill=BLUE, weight=800) + text(234, 56, "z", 18, fill=BLUE, weight=800)
            + pinky(284, 150, 0.8, mood="o")
            + bubble(176, 8, 138, "Arjun just fell asleep mid-sentence!", 284, 74, fs=9.5),
            "Arjun falls asleep in the middle of his own sentence at his desk while Pinky stares"),
        [("pinky", "Arjun just fell asleep mid-sentence! Late night?"),
         ("chintu", f"<b>Narcolepsy</b> brings extreme, overwhelming daytime sleepiness even after enough night sleep, and night sleep may be broken by frequent waking {P(54)}"),
         ("sharma", f"Not a sitcom joke, then. Sleep attacks last seconds to over half an hour, come without warning and can cause injury {P(54)}")],
        intro="11 am: Arjun, after 8 hours of sleep, nods off mid-sentence.",
        moral="Falling asleep without warning after a full night is a reason to see a doctor.", badge="Story", key="narcolepsy")

ch.chat("Narcolepsy: often straight into REM",
           svg(text(14, 30, "Usual", 10, weight=800, anchor="start")
               + flow(["1", "2", "3", "REM"], y=16, x0=70, w=46, gap=16, h=26, fs=10)
               + text(14, 96, "Narcolepsy", 10, weight=800, anchor="start", fill=CORAL)
               + f'<rect x="112" y="82" width="10" height="26" rx="4" fill="{GREY}"/>'
               + arrow(126, 95, 238, 95, CORAL, 2.4)
               + f'<rect x="256" y="82" width="46" height="26" rx="6" fill="{BLUE}"/>' + text(279, 99, "REM", 10, weight=800, fill="#fff")
               + text(180, 128, "often skips the non-REM stages", 9, weight=700, fill="#6d675f"),
               "Usual sleep passes stages 1, 2 and 3 before REM; with narcolepsy an arrow goes straight to REM", floor=False),
           [("pinky", "Arjun says he dreams the moment he dozes off. How?"),
            ("chintu", f"Usually you pass through the <b>non-REM</b> stages before <b>REM</b>, the dreaming stage. People with narcolepsy tend to fall straight into dream-filled REM sleep {P(54)}"),
            ("sharma", f"So the line between asleep and awake blurs {P(54)}, and REM's muscle paralysis and vivid images can show up while awake {P(54)} {P(57)}")],
           moral="People with narcolepsy tend to fall straight into the dreaming stage.", badge="Picture it", key="REM")

ch.glance("Three more signs of narcolepsy",
          svg(person(60, 150, 0.95, mood="grin", shirt=HALDI, hair_col="#2b2320")
              + text(60, 40, "ha ha!", 11, weight=800, fill=CORAL)
              + arrow(96, 110, 126, 128)
              + f'<g transform="rotate(-70 170 140)">{person(170, 150, 0.8, mood="flat", shirt=HALDI, hair_col="#2b2320")}</g>'
              + text(176, 30, "CATAPLEXY", 10, weight=800, fill=CORAL)
              + text(176, 46, "knees give way", 9, weight=700)
              + bed(222, 150, 90) + text(268, 66, "cannot move", 9, weight=700),
              "A man laughs, then his knees give way in cataplexy; a person in bed cannot move on waking"),
          table2(["Sign", "What happens"], [
              ["<b>Cataplexy</b>", "sudden muscle weakness set off by anger, surprise, fear or laughter: a limp neck, buckling knees, even a full collapse"],
              ["<b>Sleep paralysis</b>", "you cannot talk or move for a moment when falling asleep or waking"],
              ["Vivid dreams", "so lifelike they can be confused with reality, on falling asleep or waking"],
          ], first=30)
          + f"<p>Not everyone with narcolepsy has these {P(54)} {P(56)}.</p>",
          "Weakness when you laugh can be a sign of narcolepsy.", key="cataplexy")

ch.chat("The missing wake-up chemical",
        svg(f'<ellipse cx="90" cy="80" rx="66" ry="50" fill="#f3d2c6" stroke="{INK}" stroke-width="2"/>'
            + f'<path d="M40 70 q20 -20 40 0 t40 0 M44 96 q20 -16 40 0 t40 0" fill="none" stroke="{SKIN2}" stroke-width="3"/>'
            + f'<circle cx="104" cy="82" r="9" fill="#fff" stroke="{CORAL}" stroke-width="2" stroke-dasharray="3 2"/>'
            + text(104, 146, "hypocretin cells", 9, weight=700)
            + sign(182, 18, 132, ["HYPOCRETIN:", "KEEPS YOU AWAKE"], fs=9, fill=HALDI)
            + sign(182, 60, 132, "MOSTLY MISSING", fs=9, fill=CORAL, color="#fff")
            + chintu(250, 150, 0.6, mood="o"),
            "A brain with an empty spot where hypocretin cells should be, and labels saying hypocretin keeps you awake but is mostly missing"),
        [("pinky", "Why does Arjun's brain do this?"),
         ("chintu", f"Most people with narcolepsy lack <b>hypocretin</b>, a wake-up chemical. Scientists believe the immune system destroys the cells that make it {P(56)}"),
         ("sharma", f"It usually starts in the teens or early adulthood, about 1 in 10 has a close relative with it, and it is often mistaken for depression, epilepsy or medicine side effects {P(56)}")],
        moral="Most people with narcolepsy lack hypocretin, a wake-up chemical.", key="hypocretin")

ch.chat("Living with narcolepsy",
        svg(clock(50, 46, 22, 11, 0) + text(50, 82, "nap 1", 9, weight=700)
            + clock(130, 46, 22, 2, 0) + text(130, 82, "nap 2", 9, weight=700)
            + clock(210, 46, 22, 5, 0) + text(210, 82, "nap 3", 9, weight=700)
            + text(130, 104, "10 to 15 minutes each", 10, weight=800, fill=TEAL)
            + person(40, 150, 0.6, mood="smile", shirt=BLUE, hair_col="#2b2320")
            + doctor(282, 150, 0.8, arms="hold"),
            "Three clocks marking three short naps a day of 10 to 15 minutes each, with a doctor beside them"),
        [("Arjun", "How do they even know it is narcolepsy?"),
         ("Doctor", f"An overnight recording, then a daytime <b>nap test</b>: both show falling asleep fast and reaching REM early {P(56)}. Medicines relieve some or all symptoms for most people: stimulants for sleepiness, REM-suppressing drugs for the weakness, paralysis and vivid dreams {P(57)}")],
        points=[f"Short naps of <b>10 to 15 minutes</b>, two or three times a day {P(57)}"],
        moral="Medicines and planned short naps help most people with narcolepsy.", key="10 to 15 minutes")

ch.glance("Parasomnias: things the body does asleep",
          svg(golu(50, 150, 0.6, mood="flat", arms="hold") + text(50, 46, "sleepwalk", 9, weight=700)
              + person(140, 150, 0.6, mood="o", shirt=GREEN) + text(140, 46, "sleep talk", 9, weight=700)
              + sign(190, 10, 92, "NIGHT TERROR", fs=9, fill=BLUE, color="#fff")
              + bed(196, 150, 116, sleeper=True)
              + text(266, 72, "acts out a dream", 9, weight=700),
              "A child sleepwalks, someone talks in their sleep, and a sleeper acts out a dream"),
          table2(["Type", "What it is"], [
              ["<b>Sleepwalking</b>, sleep talking, night terrors", "more common in children, who tend to outgrow them"],
              ["Sleep paralysis", "cannot move on waking; sleep loss can bring it on"],
              ["REM sleep behaviour disorder", "acting out dreams; may follow medicines or brain disorders; more in older people"],
          ], first=40)
          + f"<p>All from {P(57)}. Keeps happening? Talk with your doctor, and keep the family safe {P(57)}.</p>",
          "Repeated sleepwalking, paralysis or dream-acting needs a doctor and a safe home.", key="sleepwalk")

ch.example("Inside a sleep lab",
           svg(bed(14, 150, 140, sleeper=True)
               + f'<path d="M44 106 Q80 60 168 44" fill="none" stroke="{GREY}" stroke-width="2"/>'
               + monitor(168, 18, 140, 70, ["brain, eyes, muscles", "heart, breathing", "blood oxygen"], fs=9)
               + text(238, 120, "MSLT: 4 or 5 naps", 9, weight=800, fill=TEAL)
               + text(238, 136, "20 min, every 2 hours", 9, weight=700),
               "A sleeper wired to a monitor that records brain, eyes, muscles, heart, breathing and oxygen; the MSLT nap test follows"),
           f"<p><b>Night test (PSG):</b> sensors on your scalp, face, chest, limbs and finger record brain activity, eye movements, muscles, heart, blood pressure, "
           f"breathing and oxygen. It is painless {P(50)}.</p>"
           f"<p><b>Day test (MSLT):</b> four or five 20-minute naps, every 2 hours. People who fall asleep in under 5 minutes, or reach REM quickly, "
           f"likely need treatment. A specialist in sleep should read the results {P(51)}.</p>",
           "Falling asleep in under 5 minutes in a daytime nap test is a warning sign.", key="MSLT")

ch.myths([
    ("Narcolepsy is a funny sitcom habit.", f"Sleep attacks come without warning and can cause injury {P(54)}."),
    ("Narcolepsy just means you need more sleep.", f"With narcolepsy you are sleepy even after enough sleep {P(54)}."),
    ("Restless legs cannot be treated.", f"RLS is treatable, though not always curable {P(53)}."),
    ("Leg pain in kids is always growing pains.", f"Kids get RLS too; growing pains can be mistaken for it {P(53)}."),
])

ch.redpen([f"Creepy legs eased by moving: RLS? {P(53)}", f"Ask a doctor to check your iron {P(53)}.", f"Asleep without warning: see a doctor {P(40)} {P(54)}.",
           f"Weak when laughing: tell a doctor {P(40)} {P(54)}.", f"Sleepwalkers need a safe home {P(57)}."],
          where="the last chapter",
          panel=svg(notes(12, 12, 184, 104, ["Creepy legs? Ask a doctor", "Sudden sleep: see a doctor", "Weak when laughing: doctor", "Sleepwalker? Safe home"])
                    + moon(226, 28, 12)
                    + sharma(262, 150, 1.0, "flat", "skeptic", arms="point"),
                    "Sharma ji points at his red-pen page: check iron, see a doctor about sudden sleep or weakness, keep sleepwalkers safe"))

ch.oneliner("what are restless legs and narcolepsy?",
            f"RLS: tingling legs you must move {P(53)}. Narcolepsy: overwhelming daytime sleepiness {P(54)}. Both treatable {P(53)} {P(57)}.",
            panel=svg(person(62, 150, 0.95, mood="o", shirt=BLUE, hair_col="#2b2320")
                      + bubble(8, 8, 116, "What are restless legs and narcolepsy?", 62, 72, fs=10)
                      + chai(150, 150, 1.2)
                      + pinky(256, 150, 0.95, mood="grin", arms="wave")
                      + bubble(140, 8, 174, "RLS: tingling legs you must move", 256, 62, fs=10),
                      "Arjun asks what restless legs and narcolepsy are, and Pinky answers in one breath"))

ch.quizzes([
    ("Legs crawl at night; moving helps. What next?",
     f"Ask a doctor. RLS is diagnosed mainly from the symptoms; some doctors also check iron, since low iron can trigger it {P(53)}.",
     "RLS: who gets it, and why"),
    ("Arjun's knees buckle every time he laughs hard. Why worry?",
     f"Sudden muscle weakness set off by laughter is cataplexy, a common sign of narcolepsy {P(54)}.",
     "Three more signs of narcolepsy"),
])

ch.recall([
    ("How long should an everyday nap be, and by when?",
     f"20 minutes or less, and not after 3 pm {P(29)}. Longer naps make it hard to wake up {P(29)}.",
     "The office power nap, done right"),
])

ch.done("Everyone gets a plan",
        "Lata mausi's blood test shows low iron; with treatment, she watches a full movie sitting down. Arjun has a diagnosis, medicine and three 15-minute naps a day. "
        "Sharma ji reads every report, then finally smiles: \"Mogambo khush hua,\" as Mr. India (1987) put it.",
        panel=svg(paper(14, 14, 110, 50, ["IRON: treated", "NAPS: 3 a day"], fs=9, fill="#fff", rot=-3)
                  + mausi(64, 150, 0.85, mood="grin", arms="up")
                  + sharma(160, 150, 1.0, "smile", "flat", arms="hold")
                  + person(250, 150, 0.85, mood="grin", shirt=BLUE, hair_col="#2b2320", arms="up"),
                  "Lata mausi and Arjun cheer while Sharma ji, for the first time, smiles"))
