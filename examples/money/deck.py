"""Paisa kaise badhta hai: compound interest, in three levels.

Every rate here is an example rate for the maths. All sums were checked in Python:
lump sums compound yearly; monthly investing uses the yearly rate / 12, added each month.
"""
from samjha import *

R72 = src("https://en.wikipedia.org/wiki/Rule_of_72", "Rule of 72")
INFL = src("https://www.drishtiias.com/daily-updates/daily-news-analysis/india-retains-4-inflation-target-for-rbi/print_manually",
           "India's inflation target")
PONZI = src("https://en.wikipedia.org/wiki/Charles_Ponzi", "Charles Ponzi")
PHP = src("https://en.wikipedia.org/wiki/Phir_Hera_Pheri", "Phir Hera Pheri")
SEBI = src("https://thesouthfirst.com/pti/sebi-warns-investors-against-parking-money-with-unregistered-entities-promising-high-returns/",
           "SEBI, Feb 2024")
QI = src("https://quoteinvestigator.com/2011/10/31/compound-interest/", "Quote Investigator")
FRANKLIN = src("https://en.wikipedia.org/wiki/Benjamin_Franklin#Bequest", "Franklin's bequest")
ITGOV = src("https://www.incometax.gov.in/iec/foportal/help/individual/return-applicable-1", "Income Tax Dept")
NIFTY = src("https://en.wikipedia.org/wiki/NIFTY_50", "Nifty 50 yearly returns")
EIR = src("https://en.wikipedia.org/wiki/Effective_interest_rate", "Effective interest rate")
FDTAX = src("https://www.indusind.bank.in/iblogs/investment/how-is-income-tax-on-fixed-deposit-calculated/", "FD interest tax")

CLAY = "#c8693a"
MUTED = "#6d675f"


def gullak(x, y=150, s=1.0, crack=False):
    """A clay piggy bank (gullak) standing on y; crack=True draws it broken open."""
    c = (f'<path d="M-2 -57 L5 -47 L-3 -37 L6 -27 L-1 -17" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
         if crack else "")
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<ellipse cx="0" cy="-30" rx="30" ry="28" fill="{CLAY}" stroke="{INK}" stroke-width="1.4"/>'
            f'<rect x="-11" y="-64" width="22" height="9" rx="3" fill="#b45a2e" stroke="{INK}" stroke-width="1.3"/>'
            f'<rect x="-9" y="-50" width="18" height="3.5" rx="1.7" fill="{INK}"/>'
            f'<path d="M-26 -22 Q0 -12 26 -22" fill="none" stroke="{HALDI}" stroke-width="2.4"/>'
            f'<rect x="-16" y="-4" width="32" height="4" rx="2" fill="#9a4a24"/>{c}</g>')


def stack(x, n, label=None, under=None, fs=9):
    """A coin stack on the floor with an optional label above and a caption under it."""
    top = 150 - 4 - (n - 1) * 5 - 10
    return (coins(x, 150, n) + (text(x, top, label, fs, weight=700) if label else "")
            + (text(x, 164, under, 9, weight=600) if under else ""))


def pile(x, base, extra=0, r=12, label=None, under=None, fs=9):
    """A coin pile: `base` gold coins with `extra` coral coins (interest) on top."""
    out = "".join(f'<ellipse cx="{x}" cy="{146 - i * 5}" rx="{r}" ry="4.5" fill="{HALDI if i < base else CORAL}" '
                  f'stroke="{INK}" stroke-width="1"/>' for i in range(base + extra))
    top = 146 - (base + extra - 1) * 5 - 10
    return (out + (text(x, top, label, fs, weight=700) if label else "")
            + (text(x, 165, under, 9, weight=600) if under else ""))


def cal(x, y, top, big, w=40, h=44, color=CORAL, fs=18):
    """The kit's calendar, with a top label at fs 9.5 so it stays readable on a phone."""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#fff" stroke="{INK}" stroke-width="1.3"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="15" rx="4" fill="{color}"/><rect x="{x}" y="{y + 9}" width="{w}" height="6" fill="{color}"/>'
            + text(x + w / 2, y + 11.5, top, 9.5, fill="#fff", weight=800) + text(x + w / 2, y + h - 9, big, fs, weight=800))


def ruler(x, y, w):
    """A wooden ruler lying flat, with tick marks."""
    ticks = "".join(f'<path d="M{x + 6 + i * 10} {y} L{x + 6 + i * 10} {y + (7 if i % 5 == 0 else 4)}" stroke="{INK}" stroke-width="1"/>'
                    for i in range(int((w - 12) / 10) + 1))
    return f'<rect x="{x}" y="{y}" width="{w}" height="16" rx="2" fill="{HALDI}" stroke="{INK}" stroke-width="1.2"/>' + ticks


def plate(x, y):
    """A plate of rajma chawal on a table top at y."""
    return (f'<ellipse cx="{x}" cy="{y - 3}" rx="22" ry="5" fill="#fff" stroke="{INK}" stroke-width="1.2"/>'
            f'<ellipse cx="{x - 6}" cy="{y - 6}" rx="9" ry="3.2" fill="#fffdf9" stroke="{GREY}" stroke-width="0.8"/>'
            f'<ellipse cx="{x + 8}" cy="{y - 6}" rx="8" ry="3" fill="#8a3b22"/>')


def factboard(facts, who="", label="The facts pinned up, each with a tick"):
    """Myth-buster panel: the FACTS pinned up (a myth is printed once, in the body, never here).
    Three facts stack on the left beside a character; four sit in a 2 x 2 grid."""
    out = ""
    if len(facts) == 4:
        for i, f in enumerate(facts):
            x, y, w, h = 8 + (i % 2) * 154, 8 + (i // 2) * 72, 150, 64
            rows = wrap(f, w - 34, 9.5)[:3]
            out += (f'<g class="lbl" transform="rotate({[-1.5, 1.5, 1, -1][i]} {x + w / 2} {y + h / 2})">'
                    f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="#fff" stroke="{INK}" stroke-width="1.2"/>'
                    + lines(x + 10, y + 17, rows, 9.5, anchor="start") + "</g>" + tick(x + w - 14, y + h - 14, 1.1))
        return svg(out, label, floor=False)
    for i, f in enumerate(facts[:3]):
        x, y, w, h = 8, 8 + i * 47, 214, 43
        rows = wrap(f, w - 40, 9.5)[:2]
        out += (f'<g class="lbl" transform="rotate({[-1, 1, -0.5][i]} {x + w / 2} {y + h / 2})">'
                f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="#fff" stroke="{INK}" stroke-width="1.2"/>'
                + lines(x + 30, y + 18 if len(rows) > 1 else y + 25, rows, 9.5, anchor="start") + "</g>" + tick(x + 16, y + h / 2, 1.0))
    return svg(out + who, label)


def bucket():
    """A leaky bucket on the floor: water pours in at the top, three holes leak."""
    drop = lambda x, y: f'<path d="M{x} {y - 5} Q{x + 4} {y + 1} {x} {y + 3} Q{x - 4} {y + 1} {x} {y - 5} Z" fill="{TEAL2}"/>'
    return (f'<path d="M160 18 L160 52" stroke="{TEAL2}" stroke-width="6" stroke-linecap="round"/>'
            f'<path d="M112 58 L208 58 L194 148 L126 148 Z" fill="#e8e4dc" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M116 80 L204 80 L194 148 L126 148 Z" fill="#9fd0d6"/>'
            f'<path d="M112 58 L208 58" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
            + text(160, 122, "What", 9, weight=800, fill=TEAL) + text(160, 133, "grows", 9, weight=800, fill=TEAL)
            + f'<circle cx="119" cy="96" r="2.6" fill="{INK}"/><circle cx="123" cy="124" r="2.6" fill="{INK}"/>'
            f'<circle cx="200" cy="108" r="2.6" fill="{INK}"/>'
            + drop(110, 100) + drop(103, 108) + drop(114, 128) + drop(107, 136) + drop(209, 112) + drop(216, 120))


def bua(x, s=1.0, mood="smile"):
    return person(x, 150, s, mood=mood, shirt=HALDI, hair="bun", hair_col="#7a6a5e", bindi=True)


def bunty(x, s=1.0, mood="smile"):
    return person(x, 150, s, mood=mood, shirt=BLUE)


deck = Deck(
    title="Paisa kaise badhta hai: compound interest",
    tagline="How money grows, and why starting early beats starting big.",
    slug="money",
    about="Three levels: what interest is, why time beats amount, and what quietly eats your growth. No product or fund is recommended.",
    caution="Education, not financial advice. Rates are example rates, not forecasts. "
            "Market returns go up and down and can be negative.",
    left_out=[
        ("Picking a fund, stock or deposit", "this deck teaches the maths, not which product to buy"),
        ("Current tax slabs and rules", "they change most years and depend on your income"),
        ("Loans and EMIs, where compounding works against you", "worth a deck of its own"),
        ("Risk, asset mix and emergency funds", "beyond compound interest; learn them before investing in markets"),
    ],
)

# =====================================================================
# Beginner
# =====================================================================
ch = deck.chapter("beginner", "How does money left alone grow?", glossary=[
    ("Lakh", "1,00,000, Indian counting"),
    ("Interest", "what a bank pays you to use your money, as a % a year."),
    ("Compounding", "interest you leave in earns interest too."),
    ("FD", "fixed deposit: money left with a bank for a set time and rate."),
])

ch.opener(
    svg(phone(10, 36, ["SALARY", "Rs 25,000", "credited"], fs=9, h=86, w=60, screen="#e7f6e9")
        + pinky(100, 150, mood="grin", arms="up")
        + bubble(56, 8, 108, "Ab yeh badhega kaise?", 100, 56, fs=10)
        + gullak(176, 150, 0.5)
        + bua(250)
        + bubble(184, 8, 128, "Beta, FD best hai!", 250, 56, fs=10),
        "Pinky holds up her phone showing her first salary; a small gullak sits on the floor while Bua ji says FD best hai"),
    scene("Salary day: Rs 25,000, Pinky's first salary. The family WhatsApp group has opinions.")
    + talk(("pinky", "Ab yeh badhega kaise? How does money actually <b>grow</b>?"),
           ("Bua ji", "Beta, FD best hai!"),
           ("Mummy", "Gullak mein daal do."),
           ("sharma", "Data dikhao.")),
    "Before you pick where money goes, understand how it grows.")

ch.chat("The gullak that never grew",
        svg(gullak(70, 150, crack=True) + coin(26, 140, 10) + coin(114, 140, 10) + coin(128, 122, 9)
            + sign(18, 30, 104, "GULLAK, since class 6", fs=9, fill="#fff")
            + pinky(206, 150, mood="sad")
            + bubble(150, 8, 164, "10 saal, and still Rs 1,240?", 206, 56, fs=10),
            "Pinky stares at her cracked clay gullak, labelled since class 6, with the same few coins inside"),
        [("pinky", "10 saal, and still Rs 1,240? That is exactly what I put in."),
         ("chintu", "A <b>gullak</b> keeps money safe from your own hands. But nobody pays you for the wait.")],
        intro="Pinky cracks open the clay gullak she has fed since class 6.",
        points=["Safe is not the same as <b>growing</b>", "Money grows only when someone pays to use it"],
        moral="A gullak keeps money safe. It does not make it grow.", badge="Story", key="gullak")

ch.chat("Interest is rent for your money",
        svg(board(10, 14, 180, 96, ["Lend Rs 10,000.", "The bank pays rent:", "Rs 700 a year."], 11, title="INTEREST")
            + text(100, 130, "example rate: 7% a year", 9, fill=MUTED)
            + pinky(234, 150, 0.85, mood="o")
            + bubble(196, 8, 118, "Why would a bank pay me anything?", 234, 72, fs=9.5)
            + chintu(292, 150, 0.7, mood="smile", arms="wave"),
            "A whiteboard titled interest: lend Rs 10,000, the bank pays Rs 700 a year; Pinky asks why a bank would pay"),
        [("pinky", "Why would a bank pay me anything?"),
         ("chintu", "It lends your money onward and shares part of what it earns. That share is <b>interest</b>: rent for your money.")],
        points=["Written as a <b>% a year</b>", "Example rate 7%: Rs 10,000 earns Rs 700 in a year"],
        moral="Interest is the rent your money earns.", badge="Idea", key="interest")

ch.chat("Simple interest, flat as a ruler",
        svg(text(160, 22, "SIMPLE INTEREST: +Rs 700 every year", 10.5, weight=800, fill=CORAL)
            + text(160, 44, "Flat as a ruler", 11, weight=700)
            + f'<path d="M30 64 L290 64" stroke="{CORAL}" stroke-width="1.6" stroke-dasharray="5 4"/>'
            + "".join(coin(52 + i * 54, 82, 17, "700") + text(52 + i * 54, 114, f"Year {i + 1}", 9.5, weight=700) for i in range(5))
            + ruler(20, 126, 280),
            "Five equal Rs 700 coins for years 1 to 5 sit along a flat ruler under the words simple interest", floor=False),
        [("pinky", "Does my Rs 700 grow bigger next year?"),
         ("chintu", "Not with <b>simple interest</b>. It is paid only on the <b>principal</b>, the amount you first put in.")],
        intro="Rs 10,000 at an example 7% simple rate.",
        points=["Rs 700 in year 1, year 2 and year 20", "After 10 years: Rs 17,000, flat as a ruler"],
        moral="Simple interest never speeds up.", badge="Picture it", key="simple interest")

ch.chat("Compounding, year by year",
        svg(text(160, 22, "COMPOUND INTEREST: the interest stays in", 10, weight=700)
            + f'<path d="M50 96 L275 66" stroke="{TEAL2}" stroke-width="1.6" stroke-dasharray="5 4"/>'
            + pile(50, 10, 0, 15, "10,000", "Start", fs=10) + pile(125, 10, 2, 15, "10,700", "Year 1", fs=10)
            + pile(200, 10, 4, 15, "11,449", "Year 2", fs=10) + pile(275, 10, 6, 15, "12,250", "Year 3", fs=10)
            + sign(16, 34, 104, "coral = interest", fs=9, fill="#fff"),
            "Four coin piles grow taller as coral interest coins pile on top: 10,000, 10,700, 11,449 and 12,250"),
        [("pinky", "Same Rs 10,000, same example 7%, interest left in. Year 2 pays Rs 749. Why not Rs 700?"),
         ("chintu", "Because last year's Rs 700 stayed in and earns too. That is <b>compound interest</b>: interest on your interest.")],
        after=table(["Year", "Interest", "Balance"], [["1", "700", "10,700"], ["2", "749", "11,449"], ["3", "801", "12,250"]]),
        moral="Compound interest is interest on your interest.", badge="Worked example", key="compound interest")

ch.chat("The snowball",
        svg('<path d="M0 34 L320 150 L320 170 L0 170 Z" fill="#fff" stroke="#c9d6da" stroke-width="2"/>'
            + "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'
                      + text(cx, cy - r - 6, lab, 9, weight=700)
                      for cx, cy, r, lab in ((54, 47, 6, "Year 0"), (130, 69, 10, "Year 10"),
                                             (205, 92, 15, "Year 20"), (276, 106, 22, "Year 30")))
            + text(200, 18, "SNOWBALL", 11, weight=800, fill=TEAL)
            + text(200, 32, "bigger ball, more snow each turn", 9.5, weight=600)
            + pinky(42, 158, 0.6, mood="o"),
            "A snowball rolling down a slope gets bigger at year 0, 10, 20 and 30", floor=False),
        [("sharma", "Same example 7% every year, so it grows by the same amount each year."),
         ("chintu", "No. Think of a <b>snowball</b>: a bigger ball has more surface, so it picks up more snow each turn.")],
        points=["A bigger <b>balance</b> earns bigger interest", "That makes the balance bigger still"],
        moral="Compounding grows by its own size.", badge="Picture it", key="snowball")

ch.chat("Simple versus compound, side by side",
        svg(text(160, 28, "Rs 10,000 at an example 7%, after 30 years", 10, weight=700)
            + bars([("Simple", 31, CORAL, "Rs 31,000"), ("Compound", 76.1, TEAL2, "Rs 76,123")],
                   x=90, y=52, step=34, scale=1.7)
            + chintu(292, 150, 0.5, mood="o"),
            "Two bars after 30 years: simple interest reaches Rs 31,000, compound reaches Rs 76,123"),
        [("sharma", "Simple or compound, it is a few rupees' difference."),
         ("chintu", "Rs 10,000 at an example 7%: in year 1, both end at Rs 10,700. After <b>30 years</b>, compound is about 2.5 times bigger.")],
        after=table(["After", "Simple, Rs", "Compound, Rs"], [
            ["10 years", "17,000", "19,672"],
            ["20 years", "24,000", "38,697"],
            ["30 years", "31,000", "76,123"],
        ]),
        moral="The gap is tiny at first and huge later.", badge="At a glance", key="30 years")

ch.chat("Year 1 is boring. Year 30 is not",
        svg(line_chart(26, 28, 170, 100, [round(10000 * 1.07 ** y) for y in range(0, 31, 3)],
                       labels=("Year 0", "Year 30"), fs=9)
            + chintu(262, 150, 0.85, mood="grin", arms="wave")
            + bubble(206, 8, 108, "Wait for year 30.", 262, 62, fs=10),
            "A curve that stays flat for years and then shoots up by year 30, with Chintu saying wait for year 30"),
        [("pinky", "Rs 700 more? That's it? I'm quitting."),
         ("chintu", "Wait for year 30. That is when you say \"Mogambo khush hua\", the villain's happy line from Mr. India (1987).")],
        intro="A year later, Pinky checks her deposit: Rs 10,000 at an example 7%.",
        points=["First 10 years add Rs 9,672", "<b>Years 21 to 30</b> add Rs 37,426, almost four times as much"],
        moral="With compounding, the biggest gains come in the last years.", badge="Story", key="year 30")

ch.true_story("Franklin's 200-year experiment",
              svg(cal(26, 16, "YEAR", "1790", w=62, h=50, color=BLUE) + arrow(98, 42, 196, 42)
                  + text(147, 32, "200 years", 9, weight=700)
                  + cal(206, 16, "YEAR", "1990", w=62, h=50, color=GREEN)
                  + pile(57, 2, 0, 16, "£1,000") + pile(237, 2, 9, 16, "$ millions"),
                  "A calendar for 1790 with two coins, an arrow marked 200 years, and a calendar for 1990 with a tall coin pile"),
              "<p>Benjamin Franklin died in 1790, leaving £1,000 each to Boston and Philadelphia (about $4,400 then), "
              "in trust to gather interest for <b>200 years</b>.</p>"
              f"<p>By 1990, Philadelphia's fund held over $2 million; Boston's had grown by almost $5 million {FRANKLIN}.</p>"
              + talk(("sharma", "So, a genius trade?"),
                     ("chintu", "No. The trusts lent it out, and Boston spent part at 100 years. Mostly, a very long wait.")),
              "A modest sum plus a very long wait did the heavy lifting.", key="200 years")

ch.watch_out("Pinky's Rs 58 food app habit",
             svg(pile(56, 10, 0, 16, "Rs 10,000", "Deposit", fs=10) + arrow(90, 100, 150, 100, color=CORAL)
                 + text(120, 91, "+Rs 58", 9, weight=700, fill=CORAL) + text(120, 114, "paid out", 9, weight=700, fill=CORAL)
                 + phone(156, 58, ["Food", "app", "order"], fs=9, h=80, w=48)
                 + pinky(255, 150, mood="o", arms="hold")
                 + bubble(208, 8, 100, "Smart, na?", 255, 58, fs=10),
                 "Each month's interest is paid out of the deposit straight into a food app order, and Pinky asks smart, na?"),
             scene("Pinky's deposit pays its interest out every month: about Rs 58 on Rs 10,000, at an example 7%.")
             + talk(("pinky", "Rs 58 a month, straight into one food app order. Smart, na?"),
                    ("chintu", "Nothing is lost, but nothing compounds. Interest that is <b>paid out</b> and spent cannot earn interest."),
                    ("sharma", "So her Rs 10,000 stays Rs 10,000 forever. Simple interest, with extra steps.")),
             "Only interest you leave in can compound.", key="paid out")

ch.myths([
    ("Compounding is only for people with lakhs.", "Compounding works the same on Rs 500. The rate and the years decide, not the size."),
    ("Einstein called compound interest the greatest invention.", f"The famous Einstein quote on compound interest has no good evidence behind it {QI}."),
    ("Simple and compound are nearly the same.", "Simple and compound match in year 1. After 30 years at an example 7%, compound is about 2.5 times bigger."),
], panel=factboard(["Compounding works the same on Rs 500", "No good evidence Einstein ever said the quote",
                    "30 years at an example 7%: compound about 2.5 times simple"],
                   sharma(272, 150, 0.85, "flat", "skeptic", arms="point"),
                   "Three facts pinned up with ticks, and Sharma ji pointing at them"))

ch.redpen(["Interest is rent your money earns.", "Simple: paid on the first amount only.",
           "Compound: interest earns interest.", "Leave the interest in.", "The big growth comes late."],
          where="Money left alone",
          panel=svg(gullak(62, 150, crack=True)
                    + paper(114, 16, 120, 64, ["PASSBOOK", "Rs 10,000", "+ interest"], 10, rot=-3, fill="#fff")
                    + text(174, 104, "LEAVE IT IN", 12, fill=CORAL, weight=800)
                    + sharma(278, 150, 1.0, "flat", "skeptic", arms="point"),
                    "Sharma ji points at Pinky's passbook, next to the cracked gullak, with LEAVE IT IN written in red"))

ch.oneliner("what is compound interest?",
            "Interest you leave in starts earning interest too, so the pile grows faster every year.",
            panel=svg(person(62, 150, 0.95, mood="o", shirt=GREEN, hair="bun", hair_col="#3a2c25", bindi=True)
                      + bubble(8, 8, 112, "What is compound interest?", 62, 60, fs=10)
                      + gullak(160, 150, 0.55)
                      + pinky(252, 150, 0.95, mood="grin", arms="wave")
                      + bubble(132, 8, 182, "Interest you leave in starts earning interest too.", 252, 60, fs=9.5),
                      "Mummy asks what compound interest is, and Pinky answers in one breath beside the old gullak"))

ch.quizzes([
    ("Rs 10,000 at an example 7% simple: how much after 2 years?",
     "Rs 11,400. Simple interest pays Rs 700 on the original Rs 10,000 each year, no more.",
     "Simple interest, flat as a ruler"),
    ("Interest paid out and spent every month: simple or compound?",
     "Simple, in effect. Interest that leaves the deposit cannot earn interest of its own.",
     "Pinky's Rs 58 food app habit"),
    ("Same rate every year. Why does year 30 add more than year 1?",
     "The rate is applied to a bigger balance. In year 30 you earn interest on 29 years of old interest too.",
     "The snowball"),
])

ch.done("Pinky's salary has a plan",
        "Pinky calls Bua ji back: \"Wherever my money goes, the interest stays in. And I start this month, not next year.\" "
        "Bua ji says she has been telling everyone this for 20 years. Sharma ji asks to see Pinky's numbers next month.",
        panel=svg(phone(16, 30, ["Bua ji", "calling..."], fs=9, h=80, w=54, screen="#e7f6e9")
                  + pinky(110, 150, mood="grin", arms="hold")
                  + bubble(64, 8, 150, "Wherever my money goes, the interest stays in.", 110, 54, fs=10)
                  + sign(176, 76, 66, ["THIS", "MONTH"], fs=10, fill="#d7eedb")
                  + bua(282, 0.8),
                  "Pinky on the phone to Bua ji, beside a sign marked this month"))

# =====================================================================
# Intermediate
# =====================================================================
ch = deck.chapter("intermediate", "Why does starting early beat starting big?", glossary=[
    ("Lakh, crore", "1 lakh = 1,00,000; 1 crore = 100 lakh"),
    ("FD", "fixed deposit: a bank deposit at a set rate"),
    ("Compounding", "growth on growth: what you leave in earns too."),
    ("SIP", "a monthly sum into a market fund; returns go up and down."),
    ("Inflation", "prices rising, so each rupee buys a little less."),
])

ch.opener(
    svg(sign(10, 12, 140, "PINKY: Rs 5,000 a month, age 25 to 35", fs=9, fill="#fff")
        + sign(170, 12, 140, "BUNTY: Rs 5,000 a month, age 35 to 60", fs=9)
        + pinky(80, 150, mood="grin") + bunty(240)
        + text(160, 104, "?", 40, weight=800, fill=CORAL),
        "Two signs compare Pinky's 10 years of investing with cousin Bunty's 25 years"),
    scene("Sunday lunch, rajma chawal. Pinky is 25; cousin Bunty is 35.")
    + talk(("pinky", "Rs 5,000 a month from 25 to 35, then I stop and leave it. Rs 6 lakh in."),
           ("Bunty", "Rs 5,000 a month from 35 to 60. Rs 15 lakh in. Obviously I win <b>at 60</b>."),
           ("sharma", "The whole table votes Bunty. Calculator lao.")),
    "Before you vote, count the years, not just the rupees.")

ch.chat("The rule of 72",
        svg(sign(14, 12, 124, "RULE OF 72", fs=12, fill="#fff")
            + text(76, 60, "72 ÷ 8 = 9 years", 12, weight=800, fill=TEAL)
            + pile(36, 4, 0, 14, "Rs 1L", fs=10) + arrow(58, 128, 98, 128) + text(78, 120, "8%", 9, weight=700)
            + pile(122, 8, 0, 14, "Rs 2L", fs=10) + cal(148, 90, "YEAR", "9", w=40, h=44)
            + chintu(252, 150, 0.9, mood="smile", arms="wave", hat="grad")
            + bubble(194, 8, 120, "Divide 72 by the yearly rate.", 252, 60, fs=9.5),
            "Rs 1 lakh doubles to Rs 2 lakh by year 9 at 8%; Chintu in a graduation cap says divide 72 by the yearly rate"),
        [("pinky", "How long does money take to double?"),
         ("chintu", f"Use the <b>rule of 72</b>: divide 72 by the yearly rate {R72}. At an example 8%, 72 ÷ 8 = 9 years.")],
        points=["Example 6%: about 12 years. 9%: about 8", f"Most accurate around 6 to 10%; it drifts at very high rates {R72}"],
        moral="Divide 72 by the rate to get roughly how many years money takes to double.", badge="Idea", key="rule of 72")

ch.example("Checking the rule with real numbers",
           svg(text(160, 24, "Rs 1 lakh at an example 8% a year", 10, weight=700)
               + bars([("Start", 100, GREY, "Rs 1,00,000"), ("3 years", 126, TEAL2, "Rs 1,25,971"),
                       ("6 years", 158.7, TEAL2, "Rs 1,58,687"), ("9 years", 199.9, GREEN, "Rs 1,99,900")],
                      x=58, y=38, step=26, scale=0.95),
               "Four bars grow from Rs 1 lakh to almost Rs 2 lakh by 9 years"),
           talk(("sharma", "I do not trust shortcuts. Show me Rs 1 lakh at an example 8%, added once a year."))
           + table(["After", "Balance"], [["3 years", "Rs 1,25,971"], ["6 years", "Rs 1,58,687"], ["9 years", "Rs 1,99,900"]])
           + talk(("sharma", "The rule said 9. Real answer: <b>9 years and a few days</b>. Theek hai, calculator down.")),
           "At 8%, the rule of 72 is off by only a few days.", key="9 years")

ch.chat("Doubling, every 9 years",
        svg(text(160, 30, "DOUBLING every 9 years, example 8%", 10, weight=800, fill=TEAL)
            + flow([["Rs 1L", "age 25"], ["Rs 2L", "age 34"], ["Rs 4L", "age 43"], ["Rs 8L", "age 52"]], y=50, h=40)
            + text(160, 118, "then Rs 16 lakh at 61", 11, weight=800, fill=GREEN)
            + chintu(292, 150, 0.4, mood="grin"),
            "Four boxes doubling from Rs 1 lakh at 25 to Rs 8 lakh at 52, then Rs 16 lakh at 61", floor=False),
        [("pinky", "Which doubling adds the most?"),
         ("chintu", "The last one. From 52 to 61 it adds about Rs 8 lakh: more than all the earlier <b>doublings</b> combined.")],
        intro="Rs 1 lakh put away at 25, never topped up, at an example 8% a year.",
        points=["Rs 2 lakh at 34, Rs 4 lakh at 43, Rs 8 lakh at 52"],
        moral="Each doubling is bigger than all the ones before it.", badge="Picture it", key="doubling")

ch.chat("Monthly investing, Rs 2,000 at a time",
        svg(text(160, 24, "Rs 2,000 a month SIP, 20 years, example 8%", 10, weight=700)
            + bars([("You put in", 48, GREY, "Rs 4.8 lakh"), ("It becomes", 117.8, TEAL2, "Rs 11.8 lakh")],
                   x=92, y=48, step=34, scale=1.3)
            + text(196, 128, "real fund returns go up and down", 9, weight=700, fill=CORAL)
            + pinky(36, 150, 0.5, mood="grin", arms="up"),
            "Two bars: Rs 4.8 lakh put in grows to Rs 11.8 lakh, with a note that real fund returns go up and down"),
        [("pinky", "No lakh, just a salary. Does Rs 2,000 a month compound too?"),
         ("chintu", "Yes. For 20 years at an example 8% (÷ 12, added monthly), Rs 4.8 lakh in becomes about Rs 11.8 lakh. Almost 60% is growth."),
         ("sharma", "So an <b>SIP</b> pays 8% every year?"),
         ("chintu", "No. A market fund has no fixed rate: returns go up and down, and some years are negative.")],
        moral="Small monthly amounts compound like a lump sum, just in instalments.", badge="Worked example", key="SIP")

JAG = [(34, 118), (56, 100), (76, 110), (98, 84), (118, 96), (140, 70), (160, 104), (184, 62), (206, 44)]
ch.chat("8% on paper, bumpy in real life",
        svg(f'<path d="M30 26 L30 124 L212 124" fill="none" stroke="{INK}" stroke-width="1.4"/>'
            + f'<path d="M34 118 Q130 108 206 44" fill="none" stroke="{TEAL2}" stroke-width="2.8" stroke-linecap="round"/>'
            + '<path d="M' + " L".join(f"{x} {y}" for x, y in JAG) + f'" fill="none" stroke="{CORAL}" stroke-width="2.4" stroke-linejoin="round"/>'
            + text(120, 18, "Example rate: smooth", 10, weight=800, fill=TEAL)
            + text(120, 142, "Real market: up and down", 10, weight=800, fill=CORAL)
            + pinky(274, 150, 0.85, mood="o")
            + bubble(220, 8, 94, "So will my fund give 8% every year?", 274, 72, fs=9),
            "A smooth teal line for an example rate beside a jagged coral line for real market returns; Pinky asks if her fund gives 8% every year", floor=False),
        [("pinky", "So will my fund give 8% every year?"),
         ("chintu", f"No. A bank FD fixes its rate for its term. A market fund does not: in 2008, India's Nifty 50 share index fell about 52% {NIFTY}.")],
        intro="These cards use one steady rate, so the maths stays easy.",
        points=["<b>Example rate</b>: for understanding the maths", "<b>Market returns</b>: up and down, never promised"],
        moral="An example rate is for the maths; a market fund's actual return goes up and down.", badge="Plot twist", key="example rate")

ch.chat("Your starting age decides your ending",
        svg(text(160, 22, "STARTING AGE: Rs 3,000 a month to 60, example 8%", 9.5, weight=700)
            + stack(52, 14, "68.8L", "From 25") + stack(124, 9, "44.7L", "From 30")
            + stack(196, 6, "28.5L", "From 35") + stack(268, 2, "10.4L", "From 45"),
            "Four coin stacks shrink as the starting age moves from 25 to 45"),
        [("pinky", "Does my <b>starting age</b> really matter that much?"),
         ("chintu", "Yes. Rs 3,000 a month to 60, example 8%, added monthly: each 5 years you wait cuts the ending by <b>about a third</b>.")],
        after=table(["Start", "Put in", "At 60"], [
            ["25", "Rs 12.6 lakh", "Rs 68.8 lakh"],
            ["30", "Rs 10.8 lakh", "Rs 44.7 lakh"],
            ["35", "Rs 9.0 lakh", "Rs 28.5 lakh"],
            ["45", "Rs 5.4 lakh", "Rs 10.4 lakh"],
        ]),
        moral="Each 5 years you wait cuts the ending by about a third.", badge="At a glance", key="starting age")

ch.chat("Time beats amount",
        svg(text(160, 24, "TIME beats amount: both put in Rs 7.2 lakh", 10, weight=700)
            + bars([("Rs 2,000 x 30 yrs", 29.8, GREEN, "Rs 29.8 lakh"), ("Rs 4,000 x 15 yrs", 13.8, CORAL, "Rs 13.8 lakh")],
                   x=112, y=40, step=30, scale=4.4)
            + pinky(70, 150, 0.5, mood="grin", arms="up") + person(250, 150, 0.5, mood="o", shirt=BLUE),
            "Rs 2,000 a month for 30 years ends at Rs 29.8 lakh; Rs 4,000 for 15 years ends at Rs 13.8 lakh"),
        [("sharma", "Two friends, Rs 7.2 lakh in each. Double the monthly amount, double the money."),
         ("chintu", "Not when the years are halved. <b>Time</b> beats amount: at an example 8%, half the amount for double the years ends more than double.")],
        after=table(["Plan", "Ends at"], [["Rs 2,000 a month, 30 years", "Rs 29.8 lakh"],
                                          ["Rs 4,000 a month, 15 years", "Rs 13.8 lakh"]]),
        moral="Doubling the years beats doubling the amount.", badge="Worked example", key="time")

ch.chat("The cousins, solved",
        svg(sharma(50, 150, 0.9, mood="flat", brow="skeptic", arms="point")
            + bubble(8, 8, 96, "Kitne saal the?", 50, 74, fs=10.5)
            + sign(116, 8, 150, "10-YEAR HEAD START", fs=9.5, fill="#d7eedb")
            + "".join(text(x, 46, a, 9, weight=700) for x, a in ((124, "25"), (176, "35"), (306, "60")))
            + text(120, 64, "Pinky: 35 years", 9.5, anchor="start", weight=800)
            + f'<rect x="124" y="68" width="52" height="14" rx="3" fill="{CORAL}"/><rect x="176" y="68" width="130" height="14" rx="3" fill="{TEAL2}"/>'
            + text(120, 102, "Bunty: 25 years", 9.5, anchor="start", weight=800)
            + f'<rect x="176" y="106" width="130" height="14" rx="3" fill="{CORAL}"/>'
            + text(215, 140, "coral: paying in, teal: just growing", 8.5, fill=MUTED),
            "Sharma ji asks how many years; two timelines show Pinky's money growing from 25 to 60 and Bunty's from 35 to 60, a 10-year head start"),
        [("sharma", "Kitne saal the?"),
         ("pinky", "Mine compound for 35 years. Bunty's never get more than 25."),
         ("chintu", "At an example 8%, added monthly: Pinky's Rs 6 lakh grows to about Rs 67 lakh at 60, Bunty's Rs 15 lakh to about Rs 48 lakh. "
                    "Bunty did well; Pinky had a 10-year <b>head start</b>.")],
        intro="Back at Sunday lunch, Sharma ji borrows a line from Sholay (1975).",
        moral="Pinky's 10-year head start beat Bunty's extra Rs 9 lakh of deposits.", badge="Story", key="head start")

ch.chat("Inflation: the chai price test",
        svg(chai(50, 112, 1.6) + sign(22, 122, 56, "Rs 10", fs=10, fill="#fff")
            + arrow(96, 80, 214, 80) + text(155, 70, "12 years at 6% (example)", 9, weight=700)
            + chai(258, 112, 1.6) + sign(230, 122, 56, "Rs 20", fs=10)
            + text(160, 22, "INFLATION: same glass, double the price", 11, weight=800, fill=CORAL),
            "A Rs 10 glass of chai becomes a Rs 20 glass after 12 years of 6% inflation"),
        [("pinky", "Do prices compound too?"),
         ("chintu", "Yes. At an example 6% a year, prices double in about 12 years: a Rs 10 glass of chai becomes Rs 20. That is <b>inflation</b>.")],
        points=[f"India's central bank targets <b>4%</b>, within a band of 2 to 6% {INFL}",
                f"Since 2016 it has averaged about 4.9% {INFL}. At 4%, prices double in about 18 years"],
        moral="Prices compound too, quietly, against you.", badge="Idea", key="inflation")

ch.chat("What \"FD best hai\" leaves out",
        svg(text(160, 22, "REAL RETURN, example rates per year", 10, weight=800, fill=TEAL)
            + bars([("FD pays", 7, TEAL2, "7%"), ("Prices rise", 6, CORAL, "6%"), ("Real return", 0.94, GREEN, "about 0.9%")],
                   x=110, y=36, step=28, scale=20)
            + bua(286, 0.6),
            "Bars: a 7% FD minus 6% inflation leaves a real return of about 0.9%, with Bua ji beside them"),
        [("Bua ji", "FD best hai! 7% every year."),
         ("pinky", "But if prices rise 6%, how much richer am I really?"),
         ("chintu", "At those example rates, about 0.9% a year in what your money can buy: 1.07 ÷ 1.06 = 1.009. That is your <b>real return</b>.")],
        points=["FDs are low risk and useful", "Judge every rate <b>after inflation</b>, not before"],
        moral="Real return = what your money can buy, not what the passbook says.", badge="Worked example", key="real return")

ch.watch_out("The Rs 1 crore brochure",
             svg(paper(16, 14, 150, 54, ["Rs 1 CRORE", "in 30 years!"], fs=14, fill="#fff") + coins(36, 66, 5, r=9)
                 + stamp(96, 106, "TODAY: Rs 17.4 LAKH", fs=11, rot=-6)
                 + pinky(210, 150, mood="o") + bubble(178, 8, 92, "Sign me up!", 210, 58, fs=10)
                 + sharma(278, 150, 0.85, "flat", "skeptic", arms="point"),
                 "A brochure promising Rs 1 crore is stamped with what it buys today, Rs 17.4 lakh, while Pinky says sign me up"),
             scene("A brochure on the bank counter: \"Rs 1 crore in 30 years!\"")
             + talk(("pinky", "Rs 1 crore! Sign me up!"),
                    ("sharma", "At an example 6% inflation, prices in 30 years are about 5.7 times today's."),
                    ("chintu", "So that crore buys what about Rs 17.4 lakh buys now. Useful money, just not a crore in <b>today's prices</b>.")),
             "Always ask what a future amount buys in today's prices.", key="today")

ch.try_it("Rule of 72 on your own numbers",
          svg(paper(18, 18, 156, 92, ["YEARS TO DOUBLE?", "72 ÷ 7.5 = ?", "72 ÷ 5 = ?", "1L to 4L at 8%?"], fs=12, fill="#fff", rot=-3)
              + pinky(240, 150, mood="flat", arms="hold") + think(196, 8, 118, "Grab a pen.", 236, 56),
              "Pinky works out years-to-double sums on a sheet of paper"),
          "<p>Grab a pen. Use the rule of 72: 72 ÷ yearly rate = <b>years to double</b>.</p>"
          "<ol><li>A deposit at an example 7.5% a year: how long to double?</li>"
          "<li>Prices rising 5% a year: when does your Rs 100 grocery bag cost Rs 200?</li>"
          "<li>At an example 8%, how many years for Rs 1 lakh to reach Rs 4 lakh?</li></ol>"
          "<details><summary>Answers</summary><p>1. About 9.6 years. 2. About 14.4 years. "
          "3. Two doublings of 9 years each: about 18 years.</p></details>",
          "One division tells you roughly how long any rate takes to double.", key="years to double")

ch.myths([
    ("Start when you earn more.", "In our example, starting earlier beat doubling the monthly amount."),
    ("A 7% FD makes you 7% richer every year.", "With a 7% FD, your buying power grows by only about 7% minus inflation."),
    ("The rule of 72 is exact.", f"The rule of 72 is a shortcut, most accurate for rates around 6 to 10% {R72}."),
], panel=factboard(["Our example: starting early beat doubling the amount", "Buying power grows by about 7% minus inflation",
                    "Rule of 72: a shortcut, most accurate at 6 to 10%"],
                   pinky(272, 150, 0.85, mood="o"),
                   "Three facts pinned up with ticks, and Pinky reading them"))

ch.redpen(["72 ÷ rate = years to double, roughly.", "Start early, even small.", "Doubling the years beat doubling the amount.",
           "Always subtract inflation.", "Ask what a future sum buys today."],
          where="Start early",
          panel=svg(paper(18, 12, 168, 56, ["WHO HAS MORE AT 60?", "Bunty: Rs 15 lakh in", "Pinky: Rs 6 lakh in"], 10.5, fill="#fff", anchor="start")
                    + text(102, 90, "Count the years: 35 vs 25", 10.5, fill=CORAL, weight=800)
                    + desk(14, 122, 176) + plate(60, 122) + chai(166, 122, 0.9, steam=False)
                    + sharma(262, 150, 1.0, "flat", "skeptic", arms="point"),
                    "At the Sunday lunch table, Sharma ji has written count the years, 35 versus 25, in red under the cousins' sums"))

ch.oneliner("why does starting early matter so much?",
            "Starting early gives compounding more years, and the last years add the most.",
            panel=svg(bunty(62, 0.95, mood="o")
                      + bubble(8, 8, 118, "Why does starting early matter so much?", 62, 60, fs=9.5)
                      + desk(128, 120, 64) + plate(160, 120)
                      + pinky(252, 150, 0.95, mood="grin", arms="wave")
                      + bubble(140, 8, 174, "Starting early gives compounding more years.", 252, 60, fs=9.5),
                      "Over rajma chawal, Bunty asks why starting early matters, and Pinky answers in one breath"))

ch.quizzes([
    ("At an example 9% a year, how long does money take to double?",
     "About 8 years: 72 ÷ 9. The exact answer is about 8.04 years.",
     "The rule of 72"),
    ("Pinky invests 10 years, Bunty 25 but later. Why can Pinky win?",
     "Her money gets 10 extra years of compounding at the end, and those late years add more than Bunty's extra deposits.",
     "The cousins, solved"),
    ("Your FD pays an example 7% and prices rise 7%. Are you richer?",
     "In buying power, no. Your real return is about zero: the money grew, but so did prices.",
     "What \"FD best hai\" leaves out"),
])

ch.recall([("At an example 7%, why does year 2 earn Rs 749, not Rs 700?",
            "Last year's Rs 700 stayed in and earned 7% too. Growth on growth: that is compounding.",
            "Compounding, year by year")])

ch.done("Not kal se. Aaj se.",
        "Pinky had planned to start \"kal se pakka\". After the cousin maths she puts aside her first Rs 2,000 that same evening "
        "and sets a reminder to do it every month. Where it goes, she will choose slowly, after asking about risk and costs. "
        "The start date she fixes today. Bunty starts too: late beats never. Sharma ji asks for the spreadsheet, to check it.",
        panel=svg(sign(14, 16, 120, "KAL SE PAKKA", fs=11, fill="#fff")
                  + f'<path d="M30 26 L118 26" stroke="{CORAL}" stroke-width="2.4"/>'
                  + sign(186, 16, 120, "AAJ SE", fs=11, fill="#d7eedb") + tick(286, 25, 0.9)
                  + pinky(90, 150, mood="grin", arms="up") + coins(160, 150, 4)
                  + bunty(240, 0.9),
                  "Kal se pakka is crossed out and Aaj se is ticked; Pinky and Bunty start today"))

# =====================================================================
# Advanced
# =====================================================================
ch = deck.chapter("advanced", "What quietly eats your compounding?", glossary=[
    ("Lakh, crore", "1 lakh = 1,00,000; 1 crore = 100 lakh"),
    ("FD, SEBI", "fixed deposit; India's market regulator"),
    ("Compounding", "what you leave in earns too."),
    ("Interest", "what you earn for lending money, % a year."),
    ("Inflation", "prices rising, so each rupee buys a little less."),
    ("Fee", "a yearly charge, as a % of your money."),
])

ch.opener(
    svg(phone(10, 14, ["DOUBLE YOUR", "MONEY IN", "21 DAYS!", "", "Only 10", "seats left"], fs=9.5, h=128, w=90, screen="#e7f6e9")
        + pinky(150, 150, mood="grin", arms="up")
        + sharma(258, 150, mood="flat", brow="skeptic")
        + bubble(196, 8, 116, "Data dikhao.", 258, 56, fs=11),
        "A phone shows a double-your-money-in-21-days forward; Pinky is excited and Sharma ji says data dikhao"),
    scene("Sunday, 4 pm. A forward in Pinky's office group: \"Double your money in 21 days!\" She starts typing \"interested\".")
    + talk(("Colleague", "My friend doubled his money twice!"),
           ("chintu", "Our example rate is 8% a year, and even that is not promised. This promises <b>100% in three weeks</b>."),
           ("sharma", "Data dikhao.")),
    "Next to 8% a year, 100% in 21 days should make anyone stop and check.")

ch.chat("21 din mein paisa double? Run the maths",
        svg(text(160, 26, "Double every 21 days, starting with Rs 1 lakh", 10, weight=700)
            + flow([["Rs 1L", "day 0"], ["Rs 2L", "day 21"], ["Rs 4L", "day 42"], ["Rs 1,700", "crore"]], y=42, h=40,
                   cols=[TEAL2, HALDI, CORAL, "#a5302a"])
            + text(160, 102, "...about 17 doublings in one year", 10, weight=700, fill=CORAL)
            + chintu(46, 150, 0.6, mood="o", eyes="x") + pinky(276, 150, 0.6, mood="o", arms="up"),
            "Doubling boxes run from Rs 1 lakh to Rs 1,700 crore within a year, and Chintu and Pinky are stunned"),
        [("pinky", "What if it really doubles every 21 days?"),
         ("chintu", "A year holds about 17.4 spans of 21 days, so Rs 1 lakh becomes about <b>Rs 1,700 crore</b> in a year."),
         ("sharma", "No business grows like that. So the money paying you comes from somewhere else.")],
        intro=f"In Phir Hera Pheri (2006), Raju falls for a 21-day doubling pitch, and the trio lose everything {PHP}.",
        moral="If the maths turns a lakh into a fortune in a year, it is not maths, it is bait.", badge="Idea", key="1,700 crore")

ch.true_story("The man who gave the scam its name",
              svg(text(160, 22, "Boston, 1920: 50% profit in 45 days", 11, weight=800, fill=CORAL)
                  + flow([["New", "investors"], ["Ponzi"], ["Old", "investors"]], y=48, x0=20, w=80, gap=24, h=40,
                         cols=[TEAL2, INK, HALDI])
                  + text(160, 112, "the 'profit' was the next person's money", 9, weight=600)
                  + stamp(160, 140, "COLLAPSED", fs=12, rot=-5),
                  "New investors' money flows through Ponzi to old investors until it collapses", floor=False),
              "<p>In 1920, <b>Charles Ponzi</b> promised Boston investors 50% profit in 45 days, from trading postal reply coupons.</p>"
              f"<p>In reality he paid early investors with <b>later investors' money</b>. It collapsed that August. "
              f"Investors lost about $20 million and got back less than 30 cents per dollar {PONZI}.</p>"
              + talk(("pinky", "But the early investors really were paid!"),
                     ("chintu", "Yes. That is exactly why their friends joined.")),
              "Being paid early does not prove a scheme is real.", key="Ponzi")

ch.chat("The red flag formula",
        svg(sign(18, 18, 122, "GUARANTEED", fs=12, fill="#fff") + text(160, 34, "+", 20, weight=800)
            + sign(180, 18, 122, "VERY HIGH", fs=12, fill="#fff") + text(120, 82, "=", 24, weight=800)
            + stamp(190, 82, "RED FLAG", fs=18, rot=-6)
            + sharma(52, 150, 0.7, mood="flat", brow="skeptic", arms="point")
            + pinky(276, 150, 0.6, mood="o"),
            "Guaranteed plus very high equals a red flag stamp, with Sharma ji pointing"),
        [("pinky", "Guaranteed, and very high too? Double good, na?"),
         ("chintu", f"In February 2024, SEBI, India's market regulator, warned that high returns usually come with high risk, including fraud. "
                    f"It said there can be no assured returns in the securities market {SEBI}."),
         ("sharma", "So guaranteed plus very high is a <b>red flag</b>.")],
        moral="Guaranteed plus very high equals walk away.", badge="Idea", key="red flag")

ch.chat("A 1% fee, over 30 years",
        svg(text(160, 26, "Rs 10 lakh for 30 years, example rates", 10, weight=700)
            + bars([("10%, no fee", 174.5, TEAL2, "Rs 1.74 Cr"), ("9% after fee", 132.7, CORAL, "Rs 1.33 Cr")],
                   x=96, y=48, step=34, scale=0.92)
            + text(160, 136, "The 1% fee took about Rs 42 lakh", 11, weight=800, fill=CORAL),
            "Two bars: Rs 1.74 crore with no fee versus Rs 1.33 crore with a 1% fee"),
        [("sharma", "A 1% fee? Too small to matter."),
         ("chintu", "Rs 10 lakh at an example 10% for 30 years: about Rs 1.74 crore. With a <b>1% fee</b>, 9%: about Rs 1.33 crore.")],
        intro="Real fund returns go up and down; these are example rates.",
        points=["Taken every year from a growing pile",
                "Fee money never compounds for you: here about <b>Rs 42 lakh</b>, nearly a quarter"],
        moral="Small yearly fees compound too, in someone else's favour.", badge="Worked example", key="1% fee")

ch.chat("The leaky bucket",
        svg(bucket() + text(58, 24, "LEAKY BUCKET", 11, weight=800, fill=TEAL)
            + sign(180, 14, 126, "IN: you earn 10%", fs=9, fill="#d7eedb")
            + sign(8, 74, 84, "Fee: 1%", fs=9, fill="#f9d6cf") + sign(8, 112, 84, "Tax: a slice", fs=9, fill="#f9d6cf")
            + sign(226, 82, 88, "Inflation: 6%", fs=9, fill="#f9d6cf")
            + text(268, 140, "example rates", 9, weight=600, fill=MUTED),
            "A leaky bucket filling from a tap at 10% loses water through three holes labelled fee, tax and inflation"),
        [("pinky", "Two offers both say 10%. Same ending, right?"),
         ("chintu", "Not once you count the leaks. Picture a <b>leaky bucket</b> with three holes, and each leak compounds, like the water.")],
        points=["Fee: a little every year", "Tax: a slice of the gains", "Inflation: shrinks what the rest buys"],
        moral="Judge any return after fees, tax and inflation.", badge="Picture it", key="leaky bucket")

ch.example("Tax every year shrinks what compounds",
           svg(sign(96, 14, 128, "Interest: Rs 7,000", fs=10, fill="#fff")
               + arrow(130, 38, 82, 72, color=CORAL) + arrow(190, 38, 238, 72, color=GREEN)
               + sign(20, 76, 120, "Tax: Rs 2,100", fs=10, fill="#f9d6cf")
               + sign(180, 76, 120, ["Stays: Rs 4,900", "= 4.9% compounds"], fs=10, fill="#d7eedb")
               + chintu(160, 150, 0.5, mood="o"),
               "Rs 7,000 of interest splits into Rs 2,100 of tax and Rs 4,900, or 4.9%, that stays to compound"),
           f"<p>FD interest is taxed as \"Income from Other Sources\", and the tax depends on your income that year {FDTAX}. "
           f"The tax return lists interest under other sources {ITGOV}.</p>"
           "<p>Example: Rs 1 lakh at 7%, for someone paying an example 30% tax. Of Rs 7,000 interest, Rs 2,100 goes as tax, "
           "so only <b>4.9%</b> stays to compound.</p>"
           "<p>Over 20 years, Rs 1 lakh grows to about Rs 3.87 lakh with no tax, but only about Rs 2.60 lakh with tax paid every year.</p>",
           "Tax paid every year lowers the rate that compounds.", key="4.9%")

ch.chat("How often it compounds",
        svg(text(160, 22, "Rs 1 lakh, quoted 8%, after 10 years", 10, weight=700)
            + bars([("Yearly", 115.9, GREY, "Rs 2,15,892"), ("Quarterly", 120.8, TEAL2, "Rs 2,20,804"),
                    ("Monthly", 122.0, GREEN, "Rs 2,21,964")], x=84, y=36, step=28, scale=1.2)
            + chintu(290, 150, 0.45, mood="o"),
            "Three bars: the same 8% added yearly, quarterly and monthly ends a little higher each time"),
        [("pinky", "Two deposits, both 8% a year. Why does one pay more?"),
         ("chintu", f"It adds 2% every 3 months (<b>quarterly</b>), and each 2% earns on the last. So it really earns 8.24% a year {EIR}.")],
        after=table(["Interest added", "Earns a year"], [["Yearly", "8.00%"], ["Quarterly", "8.24%"], ["Monthly", "8.30%"]])
        + '<p class="small">This deck adds lump sums yearly and monthly plans monthly.</p>',
        moral="Same quoted rate, more frequent compounding, a slightly bigger ending.", badge="Worked example", key="quarterly")

ch.chat("The nuance: up 50%, then down 50%",
        svg(line_chart(34, 30, 170, 90, [100, 150, 75], color=CORAL)
            + text(34, 136, "Start", 9) + text(119, 136, "Year 1", 9) + text(204, 136, "Year 2", 9)
            + text(62, 112, "Rs 1L", 9, weight=700) + text(119, 22, "Rs 1.5L", 9, weight=700)
            + text(236, 116, "Rs 75K", 9, weight=700) + text(238, 100, "down 25%", 10, weight=800, fill=CORAL)
            + chintu(292, 150, 0.6, mood="sad"),
            "A line goes from Rs 1 lakh up to Rs 1.5 lakh and down to Rs 75,000, down 25%"),
        [("sharma", "Up 50%, down 50%. Average zero, so I am back where I started."),
         ("chintu", "No. Rs 1 lakh becomes Rs 1.5 lakh, then Rs 75,000. You are <b>down 25%</b>.")],
        points=["A fall needs a bigger rise to undo it: from Rs 75,000, +100% just to get back to Rs 1.5 lakh",
                "Market funds move like this: judge by what you <b>end with</b>"],
        moral="Ups and downs cost you, even when the average return is 0%.", badge="The nuance", key="down 25%")

ch.watch_out("Pausing for 5 years costs far more than 5 years",
             svg(cal(24, 26, "PAUSE", "30-35", w=76, h=54) + cross(62, 104, 1.6)
                 + bars([("No pause", 68.8, GREEN, "68.8L"), ("Paused", 52.6, CORAL, "52.6L")], x=172, y=30, step=30, scale=1.3)
                 + pinky(210, 150, 0.6, mood="sad"),
                 "A calendar marked pause, age 30 to 35, and bars showing 68.8 lakh versus 52.6 lakh"),
             scene("Plan: Rs 3,000 a month from 25 to 60, example 8% a year. Ending: about Rs 68.8 lakh.")
             + talk(("pinky", "I'll pause from 30 to 35, for a wedding and a bike. I skip only Rs 1.8 lakh."),
                    ("chintu", "But you end with about Rs 52.6 lakh: about Rs 16 lakh less. Early rupees have the most years ahead, "
                               "so a <b>pause</b> skips their whole future.")),
             "A pause costs the missed rupees and every year of growth they would have had.", key="pause")

ch.chat("Red flags and green flags",
        svg(sign(30, 26, 110, "RED FLAG", fs=10, fill="#f9d6cf") + sign(180, 26, 110, "GREEN FLAG", fs=10, fill="#d7eedb")
            + cross(85, 80, 1.8) + tick(235, 80, 1.8)
            + text(85, 124, "\"Only 10 seats!\"", 9, weight=600) + text(235, 124, "\"Take your time.\"", 9, weight=600),
            "A red flag sign with a cross and a green flag sign with a tick"),
        [("pinky", "So what does a better offer look like?"),
         ("chintu", "Like the <b>green flag</b> column. Nobody rushes you.")],
        after=table(["", "Red flag", "Green flag"], [
            ["Returns", "Guaranteed, high", "Vary, explained"],
            ["Hurry", "Only 10 seats!", "Take your time"],
            ["Pays from", "New members", "A business or loans"],
            ["Paperwork", "Screenshots", "Registered, in writing"],
        ]),
        moral="Pressure and big promises are red flags. Paperwork and patience are green ones.", badge="At a glance", key="green flag")

ch.try_it("The 1-minute offer check",
          svg(cal(14, 14, "DOUBLES", "3 yrs", w=64, h=46, color=CORAL)
              + paper(88, 16, 104, 46, ["Yearly rate", "= 72 ÷ 3 ?"], 11, fill="#fff", rot=-2)
              + pile(36, 4, 0, 14, "Rs 1L", fs=10) + arrow(58, 128, 100, 128)
              + pile(124, 8, 0, 14, "Rs 2L", fs=10)
              + pinky(250, 150, mood="flat", arms="hold") + think(202, 8, 112, "Who earns that safely?", 246, 56),
              "An offer doubles Rs 1 lakh to Rs 2 lakh in 3 years; Pinky works out the yearly rate and wonders who earns that safely"),
          "<p>The rule of 72 works backwards too: <b>yearly rate</b> ≈ 72 ÷ years to double.</p>"
          "<p>A cousin's friend offers a plan that \"doubles in 3 years, guaranteed\". What yearly rate is that? "
          "Then ask: who earns that safely every year, and why share it with you?</p>"
          "<details><summary>Answer</summary><p>72 ÷ 3 = about 24% a year (exactly about 26%), guaranteed. "
          "That is far above the example rates in this deck. Ask for registration and paperwork, or walk away.</p></details>",
          "Turn every \"double in X\" into a yearly rate before you believe it.", key="yearly rate")

ch.chat("Sharma ji's four questions",
        svg(board(10, 10, 206, 118, ["1. After fees?", "2. After tax?", "3. After inflation?", "4. How does it earn?"],
                  13, title="FOUR QUESTIONS FIRST")
            + sharma(262, 150, mood="flat", brow="skeptic", arms="point")
            + bubble(222, 8, 92, "Four questions.", 262, 58, fs=10),
            "Sharma ji points at a board of four questions to ask before investing"),
        [("pinky", "How do you decide on an offer, Sharma ji?"),
         ("sharma", "<b>Four questions</b>. After fees? After tax? After inflation? And how exactly does it earn, and who checks?"),
         ("pinky", "And if it answers all four, in plain words?"),
         ("sharma", "Still only a maybe, till I check the seller is <b>registered</b>. No plain answers, no money.")],
        moral="Four questions first: after fees, after tax, after inflation, and how it earns.", badge="Story", key="four questions")

ch.myths([
    ("A guarantee means it is safe.", f"SEBI says there can be no assured returns in the securities market {SEBI}."),
    ("A 1% fee is too small to matter.", "In our 30-year example, a 1% yearly fee took nearly a quarter of the ending."),
    ("Pausing only costs what I did not put in.", "A pause also costs all the growth the skipped rupees would have made."),
    ("If friends are being paid, it is real.", "Ponzi schemes pay early people with new people's money."),
], panel=factboard(["SEBI: no assured returns in the securities market", "Our 30-year example: a 1% fee took nearly a quarter",
                    "A pause also costs the growth those rupees would make", "Ponzi schemes pay early people with new people's money"],
                   label="Four facts pinned up, each with a tick"))

ch.redpen(["Guaranteed plus very high: walk away.", "Check the fee. 1% is big over decades.",
           "Judge returns after tax and inflation.", "Protect the early years.", "Turn any doubling time into a yearly rate."],
          where="What eats compounding",
          panel=svg(phone(18, 14, ["DOUBLE", "IN 21", "DAYS!"], fs=11, h=112, w=78, screen="#e7f6e9")
                    + "".join(f'<path d="M28 {y} L86 {y - 3}" stroke="{CORAL}" stroke-width="2.6" stroke-linecap="round"/>' for y in (32, 46, 59))
                    + cross(57, 96, 1.6)
                    + paper(114, 18, 122, 66, ["Guaranteed", "+ very high", "= walk away"], 11, rot=-3, fill="#fff", color=CORAL)
                    + sharma(278, 150, 1.0, "flat", "skeptic", arms="point"),
                    "Sharma ji has crossed out the doubling forward in red and written: guaranteed plus very high equals walk away"))

ch.oneliner("what eats compounding?",
            "Fees, tax and inflation take a slice every year; a pause skips growth, and a scam can take it all.",
            panel=svg(person(62, 150, 0.95, mood="o", shirt=GREEN)
                      + bubble(8, 8, 112, "What eats compounding?", 62, 60, fs=10)
                      + desk(122, 122, 80) + monitor(134, 76, 56, 36, [])
                      + pinky(252, 150, 0.95, mood="grin", arms="wave")
                      + bubble(136, 8, 178, "Fees, tax and inflation take a slice every year.", 252, 60, fs=9.5),
                      "At the office, a colleague asks what eats compounding and Pinky answers in one breath"))

ch.quizzes([
    ("An offer doubles money in 2 years. What yearly rate is that?",
     "About 36% by the rule (72 ÷ 2), and really about 41%: the rule drifts at high rates. Ask how any business earns that safely, year after year.",
     "The 1-minute offer check"),
    ("Why does a 1% yearly fee cost much more than 1% of your money?",
     "It is taken every year from a growing pile, and the fee money also loses all its future compounding.",
     "A 1% fee, over 30 years"),
    ("Your investment goes up 50%, then down 50%. Where are you?",
     "Down 25%. Rs 1 lakh becomes Rs 1.5 lakh, then Rs 75,000. Averages hide the path.",
     "The nuance: up 50%, then down 50%"),
])

ch.recall([("A brochure says Rs 1 crore in 30 years. What do you ask?",
            "What it buys in today's prices. At an example 6% inflation, that crore buys what about Rs 17.4 lakh buys now.",
            "The Rs 1 crore brochure")])

ch.done("Pinky replies to the forward",
        "Pinky types one line in the office group: \"Doubling every 21 days turns Rs 1 lakh into Rs 1,700 crore in a year. "
        "Kaun deta hai?\" Then she saves Sharma ji's four questions on her phone, ready for the next offer that sounds too good. "
        "Sharma ji forwards her reply to his own family group, without changing a word, and for once he smiles.",
        panel=svg(phone(12, 12, ["1 lakh to", "1,700 crore", "in a year?", "Kaun deta", "hai?"], fs=9.5, h=128, w=82, screen="#fff")
                  + pinky(140, 150, mood="grin", arms="hold")
                  + paper(186, 12, 126, 70, ["1. After fees?", "2. After tax?", "3. After inflation?", "4. How does it earn?"], fs=9.5, fill="#fff", anchor="start")
                  + sharma(268, 150, 0.8, "smile", "flat", arms="hold"),
                  "Pinky's phone reply asks who pays 1,700 crore a year, beside a note of the four questions; Sharma ji smiles"))
