"""Kal se pakka: why we procrastinate, and how to stop. A samjha-kya example deck (topic mode)."""
from samjha import *

S_STEEL = "https://ucalgary.scholaris.ca/bitstreams/2376d7f2-d1c3-4ffe-ae50-4b9f7d88841a/download"
S_STEEL_NEWS = "https://sciencedaily.com/releases/2007/01/070110090851.htm"
S_SIROIS = "https://eprints.whiterose.ac.uk/91793/"
S_APS = "https://www.psychologicalscience.org/observer/why-wait-the-science-behind-procrastination"
S_PYCHYL = "https://carleton.ca/news/story/procrastination-problem-tim-pychyl/"
S_START = "https://thecorrespondent.com/113/first-eat-the-live-frog-and-two-other-good-habits-to-start-your-day/1737714-38627830"
S_TICE = "https://www.psychologicalscience.org/journals/psychological-science/j.1467-9280.1997.tb00460.x/"
S_SWEDEN = "https://neurosciencenews.com/procrastination-mental-physical-health-22317"
S_FUTURE = "https://www.uclahealth.org/news/release/the-stranger-within-connecting-with-our-future-selves"
S_BED = "https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2014.00611/full"
S_FRESH = "https://www.psychologicalscience.org/news/minds-business/why-monday-is-the-best-day-for-setting-new-goals.html"
S_META = "https://kops.uni-konstanz.de/entities/publication/2e749bfb-8533-437c-8203-7e788c910c5f"
S_XMAS = "https://sparq.stanford.edu/sites/g/files/sbiybj19021/files/media/file/gollwitzer_brandstatter_1997_-_implementation_intentions_effective_goal_pursuit.pdf"
S_FORGIVE = "https://bps.org.uk/research-digest/cure-procrastination-forgive-yourself"
S_BUNDLE = "https://knowledge.wharton.upenn.edu/article/researchers-used-hunger-games-encourage-healthier-choices/"
S_NHS_DEP = "https://www.nhs.uk/mental-health/conditions/depression-in-adults/symptoms/"
S_NHS_ADHD = "https://www.nhs.uk/conditions/adhd-adults/"


def dumbbell(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<rect x="-22" y="-3" width="44" height="6" rx="2" fill="{GREY}"/>'
            f'<rect x="-30" y="-12" width="10" height="24" rx="3" fill="{INK}"/>'
            f'<rect x="20" y="-12" width="10" height="24" rx="3" fill="{INK}"/></g>')


def bag(x, y, w=34, h=20, fill=TEAL):
    return (f'<path d="M{x + 9} {y} q{w / 2 - 9} -12 {w - 18} 0" fill="none" stroke="{INK}" stroke-width="2"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{INK}" stroke-width="1.2"/>')


def broom(x, y):
    return (f'<path d="M{x} {y} L{x + 14} {y + 62}" stroke="{WOOD}" stroke-width="3" stroke-linecap="round"/>'
            f'<path d="M{x + 4} {y + 60} L{x + 26} {y + 56} L{x + 30} {y + 76} L{x + 4} {y + 80} Z" fill="{HALDI}" stroke="{INK}" stroke-width="1.2"/>')


def checkbox(x, y, ticked=False):
    return (f'<rect x="{x}" y="{y}" width="9" height="9" rx="1.5" fill="#fff" stroke="{INK}" stroke-width="1.2"/>'
            + (tick(x + 4.5, y + 4.5, 0.5) if ticked else ""))


def shoes(x, y=150, fill=CORAL):
    """A pair of trainers on the floor, centred at x."""
    one = lambda cx: (f'<path d="M{cx - 11} {y} L{cx - 11} {y - 7} Q{cx - 6} {y - 11} {cx - 1} {y - 8} L{cx + 11} {y - 4} Q{cx + 13} {y} {cx + 11} {y} Z" fill="{fill}" stroke="{INK}" stroke-width="1"/>'
                      f'<path d="M{cx - 11} {y - 1.5} L{cx + 12} {y - 1.5}" stroke="#fff" stroke-width="2"/>')
    return one(x - 12) + one(x + 12)


def strike(x1, y, x2, color=CORAL):
    """A red-pen line through a word."""
    return f'<path d="M{x1} {y} L{x2} {y - 3}" stroke="{color}" stroke-width="2.6" stroke-linecap="round"/>'


def plate(x, y, rx=14):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="3.5" fill="#fff" stroke="{INK}" stroke-width="1.1"/>'
            f'<ellipse cx="{x}" cy="{y - 2}" rx="{rx * 0.5}" ry="2" fill="{HALDI}"/>')


deck = Deck(
    title="Kal se pakka: why we procrastinate",
    tagline="The gym from Monday, the night-before assignment, the 1 am scroll. And how to stop.",
    slug="procrastination",
    about="",
    caution="Not medical advice. If low mood or poor focus will not lift, see a doctor.",
)

# ================= Beginner =================
ch = deck.chapter("beginner", "Why do we put things off?", glossary=[
    ("ADHD", "a condition that makes focus and self-control hard"),
    ("Procrastination", "putting off what you meant to do, though you expect the delay to cost you."),
    ("Reel", "a short video in an endless feed."),
])

ch.opener(
    svg(pinky(70, 150, mood="grin", arms="up") + bag(96, 130, w=32, h=20)
        + calendar(138, 34, "MON", "1", w=44, h=46)
        + sharma(250, 150, mood="flat", brow="skeptic")
        + bubble(8, 10, 122, "Gym from Monday. Kal se pakka!", 70, 62, fs=10)
        + bubble(192, 10, 120, ["Third Monday", "this month."], 250, 62, fs=10),
        "Pinky holds her gym bag and promises to start on Monday; Sharma ji points out it is the third Monday this month"),
    scene("Sunday night. Pinky packs her gym bag.")
    + talk(("pinky", "Gym from Monday. Kal se pakka!"),
           ("sharma", "Third Monday this month."),
           ("chintu", "She is not lazy. She runs a team at work, plans every family trip and never misses a birthday."),
           ("sharma", "Then why does Monday never come?")),
    "Putting things off is not about being lazy. This chapter shows what it is about.")

ch.chat("The cleanest room in the city",
        svg(desk(14, 106, 112) + monitor(26, 42, 88, 54, ["ASSIGNMENT", "0 words"], fs=9)
            + clock(156, 44, 18, 11, 40)
            + pinky(230, 150, mood="grin", arms="hold") + broom(244, 72)
            + bubble(178, 8, 134, "So busy! Spices sorted, A to Z!", 230, 56, fs=10)
            + text(292, 104, "*", 20, fill=HALDI, weight=800) + text(300, 132, "*", 16, fill=HALDI, weight=800),
            "Pinky proudly sweeps at 11:40 pm, saying she is so busy, while her assignment on the screen still has 0 words"),
        [("pinky", "So busy! Spices sorted, A to Z! Fan cleaned too."),
         ("sharma", "And the assignment?"),
         ("chintu", "A title and 0 words. She worked hard all evening, on everything except the one task that felt bad.")],
        intro="11:40 pm. The assignment is due at 9 am.",
        points=["<b>Busy</b> is not the same as doing it"],
        moral="You can be busy all evening and still be putting off the one thing that matters.",
        badge="Story", key="busy")

ch.chat("It is a mood fix, not laziness",
        svg(board(14, 14, 180, 104, "The task feels bad. Dodging it feels good. Right now.", 11, title="MOOD REPAIR")
            + chintu(262, 150, mood="smile", arms="wave")
            + bubble(204, 8, 110, "It is mood repair.", 262, 52, fs=10),
            "Chintu at a whiteboard titled mood repair: the task feels bad, dodging it feels good right now"),
        [("pinky", "If I am not lazy, why do I keep dodging it?"),
         ("chintu", "It is <b>mood repair</b>. Putting off an unpleasant task makes you feel better right away "
          + src(S_SIROIS, "Sirois and Pychyl 2013") + "."),
         ("sharma", "Then she needs a better timetable."),
         ("chintu", "No. Pychyl: \"It's not a time management problem.\" It is an emotion problem " + src(S_PYCHYL, "Carleton") + ".")],
        moral="You are not dodging the task. You are dodging the feeling the task gives you.",
        key="mood repair")

ch.picture("The ugh loop",
           svg(flow(["Task", "Ugh!", "Scroll", "Relief"], y=34, x0=14, w=60, gap=18, h=42, fs=12)
               + f'<path d="M278 78 L278 116 L44 116 L44 84" fill="none" stroke="{CORAL}" stroke-width="2.4"/>'
               + f'<path d="M38 91 L44 82 L50 91" fill="none" stroke="{CORAL}" stroke-width="2.4"/>'
               + text(161, 106, "Guilt", 11, fill=CORAL, weight=800)
               + text(161, 140, "...and the task feels even worse next time", 10.5, fill=CORAL, weight=700)
               + text(160, 22, "THE UGH LOOP", 10, fill=TEAL, weight=800),
               "A loop: task, ugh feeling, scroll, relief, then guilt sends you back to an even worse task", floor=False),
           "<p>The <b>ugh loop</b> has four steps:</p>"
           "<ol><li>A task gives you a small \"ugh\".</li><li>You grab the phone.</li>"
           "<li>The ugh vanishes, and that relief feels like a reward.</li>"
           "<li>Then the guilt arrives, so next time the task feels even worse.</li></ol>"
           "<p>Rewarded habits repeat, so the escape looks even better next time.</p>",
           "Every escape trains you to escape again.", key="ugh loop")

ch.chat("Data dikhao: how common is it?",
        svg(text(14, 22, "Who procrastinates?", 11, anchor="start", weight=800)
            + bars([("College students", 88, TEAL2, "80 to 95%"), ("Adults, chronic", 18, CORAL, "15 to 20%"),
                    ("Want to cut it", 95, HALDI, "over 95%")], x=104, y=36, step=30, scale=1.1)
            + sharma(290, 150, 0.75, mood="flat", brow="skeptic")
            + bubble(226, 56, 88, "Data dikhao.", 290, 92, fs=10),
            "Sharma ji asks for data beside bars: 80 to 95 percent of students procrastinate, 15 to 20 percent of adults chronically, and over 95 percent of procrastinators want to cut it"),
        [("sharma", "Everyone says they procrastinate. Data dikhao."),
         ("chintu", "Psychologist Piers Steel reviewed the research " + src(S_STEEL, "Steel 2007") + ".")],
        after=table(["Who", "How many"], [
            ["College students who do it", "<b>80 to 95%</b>"],
            ["Adults who do it chronically", "about 15 to 20%"],
            ["Delayers who wish to cut it", "over 95%"],
        ]),
        moral="If you procrastinate, you are in very large company.", badge="Data dikhao", key="80 to 95%")

ch.chat("Lazy, or procrastinating?",
        svg(sign(20, 12, 128, "LAZY", fs=10, fill="#fff") + sign(172, 12, 128, "PROCRASTINATING", fs=10)
            + think(30, 38, 108, "Don't want to.", 84, 84, fs=10)
            + think(172, 38, 128, "I want to. Just not now.", 236, 87, fs=10)
            + person(84, 150, 0.72, mood="flat", shirt=GREEN) + pinky(236, 150, 0.72, mood="sad"),
            "A lazy person who does not want to, beside Pinky who wants to but not now"),
        [("sharma", "Skipped the gym again. Lazy."),
         ("pinky", "I want to. Just not now."),
         ("chintu", "That is <b>procrastinating</b>: delaying what you intended to do, though you expect to be worse off "
          + src(S_STEEL, "Steel 2007") + ". Lazy is \"Don't want to.\"")],
        after=table(["", "Lazy", "Putting it off"], [
            ["Wants to do it?", "No", "Yes"],
            ["Plans to do it?", "No", "Yes, \"later\""],
        ]),
        moral="The intention is there. The start is what keeps slipping.", badge="At a glance", key="procrastinating")

ch.chat("The 1 am scroll",
        svg(bed(14, 150, 156) + f'<circle cx="40" cy="109" r="11" fill="{SKIN2}"/><path d="M29 107 Q40 93 51 107 Z" fill="#2b2320"/>'
            + f'<circle cx="36" cy="111" r="1.6" fill="{INK}"/><circle cx="44" cy="111" r="1.6" fill="{INK}"/>'
            + phone(22, 40, ["1:07", "am"], fs=9, h=54, w=38, screen="#dff1ff")
            + think(76, 10, 124, "Bas 5 minute aur", 44, 54, fs=10)
            + sign(186, 60, 84, "BEDTIME: 11 PM", fs=8.5, fill="#fff")
            + f'<rect x="206" y="124" width="44" height="26" rx="3" fill="{WOOD}"/>' + clock(228, 104, 18, 1, 7)
            + moon(288, 30, 14),
            "Pinky in bed at 1:07 am, phone held up, thinking five more minutes, though her bedtime was 11 pm"),
        [("pinky", "Bas 5 minute aur. Why can I never just stop?"),
         ("chintu", "It has a name: <b>bedtime procrastination</b>. You skip the bedtime you planned, though nothing outside you is stopping you "
          + src(S_BED, "Kroese et al. 2014") + "."),
         ("sharma", "So why does the feed win?"),
         ("chintu", "Because the feed pays you now. Sleep only pays you tomorrow.")],
        intro="1:07 am. Pinky got into bed at 11.",
        moral="Going to bed is a task too, and it gets put off like any other.", badge="Story", key="bedtime")

ch.chat("Which tasks get pushed?",
        svg(sign(14, 14, 90, "BORING", fs=10, fill="#fff") + sign(115, 14, 90, "CONFUSING", fs=10, fill="#fff") + sign(216, 14, 90, "SCARY", fs=10, fill="#fff")
            + books(59, 146, 6, 40)
            + text(160, 118, "?", 54, fill=BLUE, weight=800)
            + paper(226, 56, 70, 78, ["RESULT", "DAY"], fs=9) + text(261, 116, "!", 26, fill=CORAL, weight=800),
            "Three kinds of task: boring like a stack of books, confusing like a question mark, scary like a result day"),
        [("pinky", "Why do some tasks always get pushed?"),
         ("chintu", "The more unpleasant a task, the more we put it off, especially if it is <b>boring</b> or our energy is low. "
          "Tiredness is a top-three reason students give " + src(S_STEEL, "Steel 2007") + "."),
         ("sharma", "And confusing or scary ones?"),
         ("chintu", "Confusing, because you do not know step one. Scary, because of what the result might say about you.")],
        moral="Find the feeling and you have found the reason.", key="boring")

ch.watch_out("Calling yourself lazy",
             svg(pinky(80, 150, mood="sad")
                 + think(126, 12, 176, "I am so lazy. Again.", 104, 60, fs=10)
                 + f'<rect x="216" y="122" width="16" height="28" rx="2" fill="{HALDI}"/>'
                 + f'<rect x="240" y="104" width="16" height="46" rx="2" fill="#e07b3a"/>'
                 + f'<rect x="264" y="82" width="16" height="68" rx="2" fill="{CORAL}"/>'
                 + text(248, 58, "SELF-BLAME", 9.5, weight=800, fill=CORAL) + text(248, 72, "UGH METER", 9, weight=800),
                 "Pinky calls herself lazy while the self-blame pushes an ugh meter higher"),
             talk(("pinky", "Missed the gym. I am so lazy. Again."),
                  ("chintu", "Careful. Pychyl points to <b>self-blame</b> as part of what makes procrastination harmful "
                   + src(S_PYCHYL, "Carleton") + ". It sticks to the gym, so the gym feels worse."),
                  ("Mummy", "Jaadu ki jhappi first (a magic hug, as in Munna Bhai M.B.B.S., 2003). Then try again tomorrow.")),
             "Name-calling adds one more bad feeling to the task you are avoiding.", key="self-blame")

ch.idea("When it is more than putting off",
        svg(person(70, 150, mood="smile", shirt="#fff", hair="grey") + f'<path d="M62 116 q8 14 16 0" fill="none" stroke="{GREY}" stroke-width="2"/>'
            + f'<circle cx="70" cy="128" r="4" fill="{GREY}"/>'
            + pinky(160, 150, mood="o")
            + calendar(214, 30, "OVER 2 WEEKS", "!", w=74, h=50)
            + sign(212, 92, 82, ["See a", "doctor"], fs=10)
            + bubble(8, 10, 128, "How long has it felt like this?", 70, 74, fs=10),
            "Pinky visits a doctor, who asks how long the low mood has lasted; a calendar warns: over 2 weeks"),
        talk(("Doctor", "How long has it felt like this?"))
        + "<p>Most putting-off is ordinary. Steel's review links it to depression, mostly through <b>low energy</b> "
        + src(S_STEEL, "Steel 2007") + ". See a doctor if:</p>"
        "<ul><li>low mood, no interest in things or no energy lasts most of the day, every day, for <b>more than 2 weeks</b> " + src(S_NHS_DEP, "NHS") + "</li>"
        "<li>trouble focusing, planning or finishing tasks is hurting your studies, work or relationships. That can be <b>ADHD</b> " + src(S_NHS_ADHD, "NHS") + "</li></ul>",
        "Low mood most of the day, every day, for over 2 weeks, or focus trouble that hurts your studies, work or relationships: see a doctor.",
        badge="See a doctor when", key="2 weeks")

ch.myths([
    ("Procrastinators are lazy.", "Many are busy, just not with the one task that feels bad."),
    ("It is a time-management problem.", "It is mostly about handling feelings, says Tim Pychyl. " + src(S_PYCHYL, "Carleton")),
    ("Perfectionists delay the most.", "Steel's review found perfectionism is not the culprit. " + src(S_STEEL_NEWS, "ScienceDaily")),
])

ch.redpen(["Delay is a mood fix, not a character flaw.", "Notice the ugh. Name it.", "Bedtime is a task too.", "Name-calling makes the task heavier."],
          where="Why we put things off",
          panel=svg(sharma(50, 150, 1.0, "flat", "skeptic", arms="point")
                    + paper(100, 14, 150, 104, ["WHY PINKY SKIPS THE GYM"], 8.5, fill="#fff")
                    + text(175, 66, "LAZY", 18, weight=800) + strike(146, 61, 204)
                    + text(175, 100, "MOOD FIX", 15, weight=800, fill=CORAL)
                    + calendar(262, 30, "MON", "1", w=46, h=48),
                    "Sharma ji has struck out LAZY on Pinky's gym page and written MOOD FIX in red pen, beside the Monday calendar"))

ch.oneliner("is procrastination just laziness?",
            "No. It is dodging a bad feeling now and paying for it later.",
            panel=svg(person(60, 150, 0.95, mood="o", shirt=GREEN, hair="long", hair_col="#3a2c25")
                      + bubble(8, 8, 126, "Is procrastination just laziness?", 60, 62, fs=9.5)
                      + desk(104, 116, 112) + plate(132, 114) + plate(188, 114) + chai(160, 116, 0.8)
                      + pinky(258, 150, 0.95, mood="grin", arms="wave")
                      + bubble(144, 8, 170, "No. It is dodging a bad feeling now.", 258, 62, fs=10),
                      "At Sunday lunch, a cousin asks if procrastination is just laziness and Pinky answers in one breath"))

ch.quizzes([
    ("Pinky cleans her room the night before a deadline. Lazy?",
     "No. She is working hard, on the wrong thing. Cleaning gives her relief from the bad feeling the assignment gives.",
     "The cleanest room in the city"),
    ("Why does scrolling feel so good when a task is waiting?",
     "It switches off the task's bad feeling instantly. The relief is real, and it trains you to do it again.",
     "The ugh loop"),
    ("Does calling yourself useless help you stop delaying?",
     "Usually not. Self-blame adds one more bad feeling to the task, which makes escaping it even more tempting.",
     "Calling yourself lazy"),
])

ch.done("Monday, 6:30 am",
        "The alarm rings. Cold, sweaty, too early. This time Pinky names the feeling instead of calling herself lazy: "
        "\"Ugh. Shoes on anyway.\" Sharma ji, out for his paper, raises one eyebrow. One morning is not a habit yet, but it is a start.",
        panel=svg(sun(42, 128, 14) + clock(44, 40, 18, 6, 30)
                  + f'<rect x="96" y="40" width="54" height="110" rx="3" fill="{WOOD}" stroke="{INK}" stroke-width="1.2"/>'
                  + f'<rect x="102" y="46" width="42" height="98" rx="2" fill="#f5e6c8"/><circle cx="138" cy="98" r="3" fill="{INK}"/>'
                  + pinky(176, 150, mood="grin", arms="up") + shoes(176, 150)
                  + bubble(186, 10, 128, "Ugh. Shoes on anyway.", 182, 56, fs=10)
                  + sharma(278, 150, 0.85, mood="flat", brow="skeptic") + paper(254, 104, 46, 26, ["NEWS"], fs=9),
                  "At 6:30 am, Pinky steps out of the door in her gym shoes while Sharma ji watches over his newspaper"))

# ================= Intermediate =================
ch = deck.chapter("intermediate", "Why does \"later\" always win?", glossary=[
    ("UCLA", "a university in Los Angeles"),
    ("Procrastination", "putting off what you meant to do, though you expect the delay to cost you."),
    ("Future self", "you, later on, living with today's choices."),
    ("Reel", "a short video in an endless feed."),
])

ch.opener(
    svg(pinky(70, 150, 0.8, mood="grin") + calendar(108, 96, "DAY 1", "30", w=36, h=40)
        + arrow(152, 118, 200, 118)
        + pinky(240, 150, 0.8, mood="sad") + calendar(274, 96, "DAY 29", "1", w=38, h=40)
        + bubble(8, 30, 128, ["30 days?", "Plenty of time."], 70, 82, fs=10)
        + bubble(182, 30, 130, "How is it 1 am?", 240, 82, fs=10)
        + moon(159, 30, 9),
        "Pinky relaxed with 30 days left, then panicking at 1 am with one day left"),
    scene("Pinky's exam is 30 days away. The marks matter to her.")
    + talk(("pinky", "Day 1: 30 days? Plenty of time."),
           ("pinky", "Day 10: two chapters a day, from Monday."),
           ("pinky", "Day 29: how is it 1 am?"),
           ("sharma", "You knew the date all month. So why did the studying start on the last night?")),
    "There is a simple mechanism behind the last-night rush, and it can be used on purpose.")

ch.chat("Now beats later",
        svg(text(160, 18, "TEMPORAL MOTIVATION", 9.5, fill=TEAL, weight=800)
            + coin(70, 74, 34) + text(70, 128, "Fun, now", 11, weight=800)
            + arrow(116, 78, 226, 78) + text(170, 70, "30 days away", 9, weight=600)
            + coin(250, 78, 12) + text(250, 112, "Marks, later", 11, weight=800)
            + chintu(160, 150, 0.45, mood="o"),
            "A big coin labelled fun now, and a tiny far-away coin labelled marks later"),
        [("pinky", "The marks matter to me. So why does the reel win every evening?"),
         ("chintu", "Steel's <b>temporal motivation</b> theory: the longer you must wait for a reward, the smaller it feels today "
          + src(S_STEEL, "Steel 2007") + ". The reel pays now. The marks are 30 days off."),
         ("sharma", "Like a building far away. Huge, but it looks small.")],
        points=["<b>Near</b> rewards feel big", "<b>Far</b> rewards feel small, even huge ones"],
        moral="A reward feels smaller the further away it is.", key="temporal motivation")

_writing = [(40, 122), (100, 120), (160, 115), (210, 102), (240, 82), (262, 60), (290, 30)]
ch.example("Thomas Delay's semester",
           svg(f'<path d="M40 20 L40 128 L298 128" fill="none" stroke="{INK}" stroke-width="1.4"/>'
               + text(46, 22, "How much you want to do it", 9, anchor="start", weight=600)
               + f'<path d="M40 60 L290 60" stroke="{CORAL}" stroke-width="2.6"/>'
               + text(46, 54, "Going out: fun, always now", 9, anchor="start", fill=CORAL, weight=700)
               + '<path d="M' + " L".join(f"{x} {y}" for x, y in _writing) + f'" fill="none" stroke="{TEAL2}" stroke-width="2.6" stroke-linejoin="round"/>'
               + text(50, 112, "Writing the essay", 9, anchor="start", fill=TEAL, weight=700)
               + f'<path d="M262 60 L262 128" stroke="{INK}" stroke-width="1" stroke-dasharray="3 3"/>'
               + f'<circle cx="262" cy="60" r="4" fill="{INK}"/>' + text(250, 48, "Dec 3", 9, weight=800)
               + text(40, 142, "Sep 15", 9) + text(286, 142, "Dec 15", 9),
               "Chart: the urge to go out stays flat and high; the urge to write rises only near the deadline and crosses it on December 3",
               floor=False),
           "<p>Steel's paper uses a made-up student, <b>Thomas Delay</b>. His essay is set on September 15 and due December 15 " + src(S_STEEL, "Steel 2007") + ".</p>"
           "<ol><li>Going out is fun today, every day, so its pull stays high.</li>"
           "<li>The essay's reward is far off, so its pull starts low and climbs only as the deadline nears.</li>"
           "<li>The lines cross on <b>December 3</b>. That leaves 12 days for a 3-month essay.</li></ol>",
           "The deadline does not create the work. It just makes the reward finally feel close.", key="Dec 3")

ch.chat("Your future self is a stranger",
        svg(sign(14, 12, 112, "PINKY TODAY", fs=9) + sign(176, 12, 130, "FUTURE SELF, 10 YEARS ON", fs=9)
            + pinky(70, 150, mood="smile")
            + arrow(110, 104, 200, 104) + text(155, 94, "Who is she?", 10, weight=700)
            + person(246, 150, mood="flat", shirt=CORAL, hair_col=GREY),
            "Pinky today looks at her future self ten years ahead and wonders who she is"),
        [("pinky", "Why is it so easy to leave the dishes for tomorrow's me?"),
         ("chintu", "Hal Hershfield, now at UCLA, and his Stanford collaborators scanned brains while people thought about themselves now, "
          "in 10 years, and other people. In the scans, the <b>future self</b> looked like another person " + src(S_FUTURE, "UCLA Health") + "."),
         ("sharma", "So she hands her work to a stranger. Who happens to be her.")],
        moral="It is easy to dump work on someone you do not feel connected to, even if that someone is you.",
        badge="Picture it", key="future self")

ch.chat("Dear future Pinky",
        svg(paper(26, 14, 140, 114, ["Dear Future Pinky,", "You do the dishes.", "You will feel", "fresher. Promise.", "Love, Today Pinky"], fs=9, rot=-3)
            + pinky(244, 150, mood="grin", arms="wave")
            + bubble(188, 10, 118, "Kal ho naa ho!", 244, 62, fs=10),
            "Pinky leaves a cheerful note handing tonight's dishes to future Pinky"),
        [("pinky", "Kal ho naa ho! Future Pinky will feel fresher."),
         ("sharma", "Kal Ho Naa Ho (2003) means tomorrow may not come. When it does, <b>Future Pinky</b> is just as tired."),
         ("chintu", "Sirois explains the trap: \"We're trying to regulate our current mood and thinking our future self will be in a better state\" "
          + src(S_APS, "APS Observer") + ".")],
        intro="10 pm. Dishes in the sink, a note on the fridge.",
        moral="Future you is not a fresher person. Future you is you, plus today's dishes.", badge="Story", key="Future Pinky")

ch.chat("Why deadlines work",
        svg(text(100, 32, "Many small, near deadlines", 10, weight=800)
            + calendar(20, 52, "WK 1", "", w=44, h=44) + tick(42, 82)
            + calendar(78, 52, "WK 2", "", w=44, h=44) + tick(100, 82)
            + calendar(136, 52, "WK 3", "", w=44, h=44) + arrow(186, 76, 220, 76)
            + calendar(222, 50, "DUE", "15", w=66, h=66, color=INK)
            + pinky(160, 150, 0.45, mood="smile"),
            "Three weekly mini deadlines, two ticked, before the big due date"),
        [("pinky", "Why do I only really work just before a deadline?"),
         ("chintu", "Steel's theory predicts it: procrastinators work very hard, but only just before the deadline " + src(S_STEEL, "Steel 2007")
          + ". A <b>near deadline</b> makes the reward feel real."),
         ("pinky", "So how do I use that on purpose?"),
         ("chintu", "Break one far deadline into small, close ones, as Steel suggests. Say, one every week.")],
        moral="Many small, near deadlines bring the payoff close again and again.", key="near deadline")

ch.watch_out("\"I work best under pressure\"",
             svg(desk(14, 110, 150) + monitor(42, 50, 92, 52, ["DUE 9 AM", "3 pages left"], fs=9)
                 + chai(26, 110) + chai(150, 110) + chai(162, 110)
                 + pinky(226, 150, mood="o")
                 + bubble(176, 8, 136, "All is well. I work best under pressure.", 226, 56, fs=10),
                 "Pinky, at 2 am with three empty chai glasses, tells herself all is well, she works best under pressure"),
             scene("2 am. Pinky pats her heart like Rancho in 3 Idiots (2009).")
             + talk(("pinky", "All is well. I work best under pressure."),
                    ("sharma", "Do the studies agree?"),
                    ("chintu", "Two studies of students: delayers had less stress early in the term, but more <b>stress and illness</b> late. "
                     "They also got lower grades on all assignments " + src(S_TICE, "Tice and Baumeister 1997") + ".")),
             "Delayers felt calm early, then paid with more stress, more illness and lower grades.", key="under pressure")

ch.true_story("The long bill",
              svg(sharma(52, 150, mood="flat", brow="skeptic", arms="point")
                  + board(104, 14, 200, 102, ["3,525 students, 8 universities", "2,587 answered 9 months later:", "more stress, worse sleep,", "more loneliness"], 10, title="SWEDEN, 2023"),
                  "Sharma ji points at a board about a Swedish study of 3,525 students"),
              "<p>A Swedish team signed up <b>3,525 students</b> from 8 universities. Nine months later, 2,587 of them answered again.</p>"
              "<p>Students who procrastinated more reported a bit more depression, anxiety and stress. They also slept worse and felt lonelier "
              + src(S_SWEDEN, "Neuroscience News") + ".</p>"
              + talk(("sharma", "Fine print: no single health problem was strongly linked, and the authors say it is not proof of cause and effect.")),
              "The bill for delay rarely arrives on the day you delay.", key="3,525 students")

ch.chat("Now-you gets, later-you pays",
        svg(f'<path d="M160 150 L160 66" stroke="{INK}" stroke-width="5"/>'
            + f'<path d="M144 150 L176 150" stroke="{INK}" stroke-width="5"/>'
            + f'<path d="M70 92 L250 54" stroke="{WOOD}" stroke-width="5" stroke-linecap="round"/>'
            + f'<circle cx="160" cy="73" r="5" fill="{INK}"/>'
            + f'<path d="M70 92 L50 118 M70 92 L90 118 M250 54 L230 80 M250 54 L270 80" stroke="{INK}" stroke-width="1.2"/>'
            + f'<path d="M40 118 L100 118 Q70 132 40 118 Z" fill="{GREY}"/>'
            + f'<path d="M220 80 L280 80 Q250 94 220 80 Z" fill="{GREY}"/>'
            + phone(58, 72, (), h=44, w=26)
            + books(250, 78, 3, 30)
            + text(70, 146, "Now-you: fun", 10, weight=800) + text(250, 112, "Later-you pays", 10, weight=800),
            "A scale tipped down by a phone labelled now-you fun, with the books labelled later-you pays floating up"),
        [("pinky", "So every delay is a trade?"),
         ("chintu", "These four are. Now-you gets something, and <b>later-you</b> pays for it.")],
        after=table(["Choice", "Now-you gets", "Later-you pays"], [
            ["1 am scroll", "Fun, right now", "A foggy morning"],
            ["Skip the gym", "A cosy sofa", "Another \"from Monday\""],
            ["Delay the bill", "No boring form", "A late fee"],
            ["Cram at the end", "Free evenings", "Stress, weaker work"],
        ]),
        moral="The scale always tips toward now, unless you put something on the other side.", badge="At a glance", key="later-you")

ch.try_it("Find your \"later\" feeling",
          svg(paper(24, 12, 156, 112, ["My task: _________", "Which feeling?", "Bored", "Confused", "Scared", "Tired"], fs=11, anchor="start")
              + checkbox(110, 46) + checkbox(110, 59) + checkbox(110, 73, True) + checkbox(110, 86)
              + pinky(248, 150, mood="o", arms="hold"),
              "A checklist: my task, which feeling, then bored, confused, scared or tired"),
          "<ol><li>Pick one task you keep pushing to tomorrow.</li><li>Imagine starting it right now, for 10 seconds.</li>"
          "<li>Which <b>feeling</b> shows up: bored, confused, scared or tired?</li></ol>"
          "<details><summary>What each feeling needs</summary>"
          + table(["Feeling", "Try this"], [
              ["Bored", "Pair it with music or a friend"],
              ["Confused", "Make step one \"find out how\""],
              ["Scared", "Aim for a bad first draft"],
              ["Tired", "Move it to your high-energy hour"],
          ]) + "</details>",
          "Once the feeling has a name, the fix gets obvious.", key="feeling")

ch.myths([
    ("Deadlines are the enemy.", "Near deadlines make the reward finally feel real."),
    ("Future you will feel more like it.", "Future you is the same person, just as tired."),
    ("Pressure gives better work.", "Delayers got lower grades on all assignments. " + src(S_TICE, "Tice and Baumeister")),
])

ch.redpen(["Far rewards feel small.", "Future you is still you.", "Make deadlines small and near.", "Calm now, stress later."],
          where="Why later wins",
          panel=svg(sharma(50, 150, 1.0, "flat", "skeptic", arms="point")
                    + paper(98, 14, 156, 104, ["PINKY'S EXAM PLAN"], 8.5, fill="#fff")
                    + text(176, 58, "Day 29: cram", 13, weight=700) + strike(128, 54, 224)
                    + lines(176, 86, ["4 weekly", "mini deadlines"], 12, fill=CORAL, weight=800)
                    + calendar(264, 30, "EXAM", "30", w=46, h=48),
                    "Sharma ji has struck out day 29 cramming on Pinky's exam plan and written four weekly mini deadlines in red pen"))

ch.oneliner("why do I always leave it for the last night?",
            "Fun is always now. The payoff only feels real once the deadline is close.",
            panel=svg(f'<path d="M0 16 L320 16" stroke="{GREY}" stroke-width="3"/>'
                      + "".join(f'<path d="M{x} 16 L{x} 26" stroke="{GREY}" stroke-width="1.6"/><circle cx="{x}" cy="30" r="4" fill="none" stroke="{GREY}" stroke-width="1.6"/>' for x in (150, 170))
                      + f'<rect x="114" y="62" width="92" height="44" rx="8" fill="#d7eef0" stroke="{INK}" stroke-width="1.2"/>'
                      + f'<path d="M160 62 L160 106" stroke="{INK}" stroke-width="1.2"/>'
                      + person(64, 150, 0.95, mood="o", shirt=BLUE)
                      + bubble(8, 34, 120, "Why do I always leave it for the last night?", 64, 70, fs=9.5)
                      + pinky(256, 150, 0.95, mood="smile", arms="wave")
                      + bubble(196, 40, 118, "Fun is always now.", 256, 70, fs=10),
                      "On the metro, a colleague asks why he always leaves things for the last night and Pinky answers in one breath"))

ch.quizzes([
    ("Why do exam marks feel unimportant 30 days before the exam?",
     "Because the reward is far away. The longer the wait for a reward, the smaller it feels today.",
     "Now beats later"),
    ("How do small weekly deadlines help with a big project?",
     "Each one brings a payoff close, so the last-night push happens every week in small doses instead of once in a panic.",
     "Why deadlines work"),
    ("\"I work best under pressure.\" What did the studies find?",
     "Delayers felt calmer early in the term, but more stressed and sicker later, and got lower grades.",
     "\"I work best under pressure\""),
])

ch.recall([("Why do researchers call putting things off mood repair?",
            "Putting off an unpleasant task makes you feel better right away. You are dodging the feeling the task gives you.",
            "It is a mood fix, not laziness")])

ch.done("Day 29, done differently",
        "Next exam, Pinky splits the 30 days into four weekly mini deadlines and ticks one off each Sunday. "
        "On day 29 she revises, eats dinner and sleeps by 11. Sharma ji reads the planner twice and, for once, finds nothing to correct.",
        panel=svg(paper(14, 20, 124, 72, ["EXAM PLAN", "Wk 1: ch 1 to 3", "Wk 2: ch 4 to 6", "Wk 3: ch 7 to 9", "Wk 4: revise"], fs=9, anchor="start", fill="#fff")
                  + tick(122, 42, 0.6) + tick(122, 53, 0.6) + tick(122, 64, 0.6) + tick(122, 75, 0.6)
                  + bed(156, 150, 120, sleeper=True) + clock(296, 34, 15, 11, 0) + moon(226, 30, 11),
                  "A four-week exam plan with every week ticked, and Pinky asleep in bed at 11 pm the night before the exam"))

# ================= Advanced =================
ch = deck.chapter("advanced", "So how do you stop?", glossary=[
    ("Procrastination", "putting off what you meant to do, though you expect the delay to cost you."),
    ("If-then plan", "deciding in advance: when a set moment comes, I do a set action."),
    ("Temptation bundling", "allowing a treat only while doing the dull task."),
])

ch.opener(
    svg(phone(12, 30, ["RISE AT", "5 AM!"], fs=9, h=76, w=54)
        + paper(78, 22, 86, 92, ["MY 20-PAGE", "MASTER", "PLAN"], fs=9, rot=-6)
        + pinky(200, 150, mood="sad")
        + sharma(274, 150, mood="flat", brow="skeptic")
        + bubble(222, 8, 92, "Data dikhao.", 274, 64, fs=10),
        "Pinky surrounded by a 5 am routine video and a 20-page plan, still stuck; Sharma ji asks for data"),
    scene("Pinky has tried it all: motivation videos, a 5 am routine, a 20-page colour-coded master plan.")
    + talk(("pinky", "The plan took a whole weekend to make. The assignment is still at 0 words."),
           ("sharma", "Enough tips from the internet. Data dikhao. What actually works?")),
    "A few simple tools have real evidence behind them. Most motivation tricks do not.")

ch.true_story("The Christmas Eve report",
              svg(calendar(16, 14, "DEC", "24", w=46, h=48)
                  + text(186, 34, "Report written within 2 days", 10, weight=800)
                  + bars([("When + where", 71, GREEN, "71%"), ("No plan", 32, GREY, "32%")], x=106, y=72, step=32, scale=1.9)
                  + chintu(292, 150, 0.5, mood="grin"),
                  "Bars: 71 percent of students with a when-and-where plan wrote the report in time, against 32 percent without"),
              "<p>In 1997, Peter Gollwitzer and Veronika Brandstätter asked students to write a report on how they spent Christmas Eve, within 2 days after it.</p>"
              "<p>Some students also wrote down exactly <b>when and where</b> they would write it. 71% of them wrote it in time, against 32% of the others. "
              "It was a small study: the result rests on 36 students " + src(S_XMAS, "Gollwitzer and Brandstätter 1997") + ".</p>",
              "In one small study, deciding when and where more than doubled the share who got it done.", key="when + where")

ch.chat("If-then plans",
        svg(text(160, 22, "IF-THEN PLAN", 10.5, fill=TEAL, weight=800)
            + sign(14, 46, 124, ["IF it is 7 am", "and I have brushed"], fs=10, fill="#fff")
            + arrow(144, 60, 176, 60)
            + sign(182, 46, 124, ["THEN I put on", "my gym shoes"], fs=10)
            + chintu(76, 150, 0.7, mood="smile", arms="wave") + pinky(244, 150, 0.75, mood="grin", arms="up"),
            "An if-then plan: an IF sign leading to a THEN sign, if it is 7 am and I have brushed, then I put on my gym shoes"),
        [("sharma", "\"I will exercise more.\" There, a plan."),
         ("chintu", "That is a wish. \"If it is 7 am and I have brushed, then I put on my gym shoes\" is an <b>if-then plan</b>."),
         ("pinky", "Does it really work?"),
         ("chintu", "A review of 94 tests found a medium-to-large effect on reaching goals " + src(S_META, "Gollwitzer and Sheeran 2006")
          + ". The moment itself becomes the reminder.")],
        moral="Decide once, in advance, so the moment does the deciding.", key="if-then")

ch.picture("Make the first step tiny",
           svg(flow([["Open", "laptop"], ["Open", "the file"], ["Type", "the title"], ["One ugly", "line"]], y=24, x0=14, w=58, gap=18, h=40, fs=9.5)
               + paper(18, 90, 112, 40, ["THE WHOLE", "ASSIGNMENT"], fs=9, rot=-4) + cross(148, 110, 1.6)
               + text(236, 92, "Just the next action", 11, weight=800, fill=TEAL)
               + pinky(238, 150, 0.55, mood="grin", arms="up"),
               "Four tiny steps from opening the laptop to one ugly line, instead of the whole assignment, which is crossed out"),
           "<p>\"Do the assignment\" is huge, vague and scary, so it gets delayed. Pychyl's trick is one question: "
           "\"What's the <b>next action</b> I need to do, if I was to get started?\" " + src(S_PYCHYL, "Carleton") + "</p>"
           "<ol><li>Open the laptop.</li><li>Open the file.</li><li>Type the title.</li><li>Write one ugly line.</li></ol>"
           "<p>Steel's review agrees that small, near goals shorten the delay " + src(S_STEEL, "Steel 2007") + ".</p>",
           "Make step one so small it would be silly to skip.", key="next action")

ch.chat("A great speech, and still no start",
        svg(chintu(66, 150, mood="grin", arms="up") + f'<path d="M100 150 L118 96" stroke="{WOOD}" stroke-width="4" stroke-linecap="round"/>'
            + f'<path d="M100 150 q-8 0 -10 -6" fill="none" stroke="{WOOD}" stroke-width="4" stroke-linecap="round"/>'
            + bubble(8, 8, 124, ["Sattar minute!", "Give it everything!"], 66, 50, fs=10)
            + f'<rect x="196" y="112" width="104" height="26" rx="8" fill="{BLUE}"/><rect x="190" y="104" width="14" height="40" rx="5" fill="{BLUE}"/>'
            + f'<rect x="292" y="104" width="14" height="40" rx="5" fill="{BLUE}"/>'
            + pinky(246, 136, 0.9, mood="flat")
            + bubble(176, 8, 138, "Nice speech. I'll start when I feel like it.", 246, 62, fs=10),
            "Chintu gives a big pep talk holding a hockey stick; Pinky, on the sofa, says she will start when she feels like it"),
        [("chintu", "Sattar minute! Give it everything!"),
         ("pinky", "Nice speech. I'll start when I <b>feel like it</b>."),
         ("chintu", "Pychyl calls waiting for the mood a common trap. His fix: \"I don't feel like it right now, but I'm just going to get started anyway\" "
          + src(S_START, "The Correspondent") + ".")],
        intro="Chintu tries a pep talk in the style of coach Kabir Khan's \"Sattar minute\" (70 minutes) speech in Chak De! India (2007).",
        moral="Do not wait for the mood. Get started anyway.", badge="Story", key="feel like it")

ch.example("Audiobooks only at the gym",
           svg(dumbbell(42, 30) + text(186, 20, "TEMPTATION BUNDLING", 9.5, weight=800, fill=TEAL)
               + text(186, 40, "Gym visits", 11, weight=800)
               + bars([("Gym-only books", 151, TEAL2, "+51%"), ("Gift card only", 100, GREY, "usual")], x=104, y=56, step=34, scale=1.0)
               + pinky(284, 150, 0.7, mood="grin"),
               "Temptation bundling bars: the group whose audiobooks were locked to the gym visited 51 percent more than the comparison group"),
           "<p>Katy Milkman's team studied 226 students and staff at a university gym for nine weeks. One group got gripping audiobooks that played only at the gym. "
           "That group went <b>51% more</b> often than a comparison group, though the boost weakened over the weeks.</p>"
           "<p>Researchers call this <b>temptation bundling</b>. Afterwards, 61% of participants were willing to pay to lock their audiobooks to the gym " + src(S_BUNDLE, "Wharton") + ".</p>"
           "<p>Desi version: that one web series only on the treadmill.</p>",
           "Lock a treat to the dull task, so the reward arrives now.", badge="The study", key="temptation bundling")

ch.chat("Fix the room, not your willpower",
        svg(text(86, 24, "STIMULUS CONTROL", 10, fill=TEAL, weight=800)
            + desk(14, 104, 110) + books(48, 104, 3, 30) + bag(80, 84, w=30, h=20)
            + pinky(160, 150, 0.85, mood="smile")
            + f'<rect x="206" y="40" width="50" height="110" rx="3" fill="{WOOD}" stroke="{INK}" stroke-width="1.2"/>'
            + f'<circle cx="248" cy="98" r="3" fill="{INK}"/>'
            + sign(262, 50, 52, ["OTHER", "ROOM"], fs=9, fill="#fff")
            + f'<rect x="264" y="132" width="48" height="6" rx="2" fill="{WOOD}"/>'
            + phone(274, 84, ["zzz"], fs=9, h=48, w=30),
            "Stimulus control: a desk with books and the gym bag ready; the phone sits charging outside the door in another room"),
        [("sharma", "She just needs more willpower."),
         ("chintu", "Steel calls the fix <b>stimulus control</b>: keep cues for your goal close, remove reminders of temptation. "
          "Students who always studied in the same place procrastinated less " + src(S_STEEL, "Steel 2007") + "."),
         ("pinky", "So: gym clothes on the chair, phone charging outside the bedroom.")],
        points=["Willpower is a fight you repeat every few minutes", "A room can win it for you"],
        moral="Make the good choice the easy choice, before the moment comes.", key="stimulus control")

ch.watch_out("Scolding yourself after a slip",
             svg(think(10, 12, 138, "Useless! Again!", 70, 56, fs=10) + think(168, 12, 142, "Slipped. Next: 7 pm.", 240, 56, fs=10)
                 + pinky(70, 150, mood="sad") + pinky(240, 150, mood="smile")
                 + cross(130, 104, 1.4) + tick(296, 104, 1.4)
                 + text(130, 132, "SCOLD", 9, weight=800, fill=CORAL) + text(296, 132, "FORGIVE", 9, weight=800, fill=GREEN),
                 "Two Pinkys: one scolds herself after a slip, the other forgives herself and sets the next time"),
             talk(("pinky", "Skipped again. Useless! Again!"),
                  ("chintu", "Careful. In a study of 134 first-year students, those who forgave themselves for delaying before their first exams "
                   "procrastinated less before the second ones, and did better on them " + src(S_FORGIVE, "BPS Research Digest") + "."),
                  ("pinky", "Okay. Slipped. Next: 7 pm."))
             + "<p>It was a questionnaire study, not a trial, but it fits: <b>forgiveness</b> takes the extra bad feeling off the task.</p>",
             "Forgive the slip, then set the next if-then.", key="forgive")

ch.chat("Even Sharma ji does it",
        svg(shelf(12, 64, 56, 3) + sharma(104, 150, mood="o", brow="flat")
            + think(66, 8, 112, "I am unsure I'll get it right.", 104, 60, fs=9.5)
            + paper(186, 30, 120, 108, ["TAX FORM"], fs=11)
            + "".join(f'<rect x="198" y="{y}" width="{w}" height="4" rx="2" fill="#ddd6ca"/>' for y, w in ((56, 96), (68, 78), (80, 90), (124, 60)))
            + stamp(246, 104, "UNTOUCHED", fs=11, rot=-10),
            "Sharma ji, next to a perfectly organised shelf, feels unsure about a tax form stamped untouched"),
        [("pinky", "Your files are labelled. So why has your tax form sat untouched for three weeks?"),
         ("sharma", "Hmm. I am unsure I'll get it right."),
         ("chintu", "Very common. Steel notes many people would likely finish their taxes sooner if they felt more "
          "<b>confident</b> of getting them right " + src(S_STEEL, "Steel 2007") + ". The fix: a small first win, or help for the hard part.")],
        moral="Being organised hides procrastination. It does not cure it.", badge="Plot twist", key="unsure")

ch.chat("The nuance: \"from Monday\" is not the enemy",
        svg(calendar(22, 26, "MON", "1", w=64, h=70) + text(54, 118, "Fresh start", 10, weight=800)
            + text(118, 66, "+", 26, weight=800, fill=TEAL)
            + sign(146, 36, 160, ["IF Monday, 7 am", "THEN shoes on"], fs=10)
            + pinky(226, 150, 0.72, mood="grin", arms="up"),
            "A Monday calendar labelled fresh start, plus an if-then sign: if Monday 7 am, then shoes on"),
        [("sharma", "\"From Monday\" is just an excuse."),
         ("chintu", "Not always. Gym records showed visits jump at the start of a new week, a new semester and right after a birthday "
          + src(S_FRESH, "APS") + ". Researchers call it the <b>fresh start</b> effect."),
         ("pinky", "So I keep Monday as fuel, and add an if-then and a tiny first step.")],
        moral="A fresh start is fuel. It still needs a plan to burn in.", badge="The nuance", key="fresh start")

ch.chat("What works, what backfires",
        svg(sign(30, 14, 110, "WORKS", fs=11) + sign(180, 14, 110, "BACKFIRES", fs=11, fill="#fff")
            + tick(130, 90, 1.8) + cross(282, 90, 1.8)
            + chintu(80, 150, 0.8, mood="grin", arms="up") + pinky(232, 150, 0.8, mood="sad"),
            "A tick under works and a cross under backfires"),
        [("pinky", "Give me the cheat sheet."),
         ("chintu", "Left side works. Right side <b>backfires</b>.")],
        after=table(["Works", "Backfires"], [
            ["If-then plan", "No when or where"],
            ["Tiny first step", "Waiting for the mood"],
            ["Phone in another room", "Willpower alone"],
            ["Treat only during the task", "Treat first, task later"],
            ["Forgive, then replan", "Calling yourself lazy"],
        ]),
        moral="Change the plan, the step and the room. Not your character.", badge="At a glance", key="backfires")

ch.try_it("Write your if-then, now",
          svg(paper(20, 14, 196, 112, ["MY IF-THEN", "IF it is ________", "and I am at ________,", "THEN I will ________."], fs=12, anchor="start")
              + pinky(266, 150, mood="smile", arms="hold"),
              "A sheet titled my if-then, with blanks: if it is, and I am at, then I will"),
          "<ol><li>Pick the task you delay most.</li>"
          "<li>Fill in your <b>if-then</b> with a real time, a real place and the tiniest first action.</li>"
          "<li>Say it out loud once.</li></ol>"
          "<details><summary>Three examples</summary><p>If it is 9 pm and dinner is done, then I open the assignment file and type the title.</p>"
          "<p>If it is 11 pm, then the phone goes to charge in the kitchen.</p>"
          "<p>If it is Sunday 10 am, then I fill in page 1 of the tax form.</p></details>",
          "A real time, a real place and one tiny action: that is a plan.", key="if-then")

ch.myths([
    ("You must feel motivated to start.", "You can start without the mood, says Tim Pychyl. " + src(S_START, "The Correspondent")),
    ("Being hard on yourself keeps you in line.", "Students who forgave themselves delayed less the next time. " + src(S_FORGIVE, "BPS")),
    ("Disciplined people never procrastinate.", "Organised people delay tasks they feel unsure about. " + src(S_STEEL, "Steel 2007")),
])

ch.redpen(["Decide when and where, in advance.", "Shrink the first step.", "Start before you feel like it.",
           "Move the phone, not your willpower.", "Forgive the slip, then replan."],
          where="So how do you stop?",
          panel=svg(sharma(50, 150, 1.0, "flat", "skeptic", arms="point")
                    + paper(100, 20, 92, 100, ["MY 20-PAGE", "MASTER", "PLAN"], 9, rot=-4)
                    + cross(146, 92, 2.4)
                    + arrow(200, 70, 222, 70, CORAL)
                    + paper(228, 36, 84, 62, ["IF 7 AM,", "THEN", "SHOES ON"], 10, rot=3, fill=HALDI),
                    "Sharma ji has crossed out Pinky's 20-page master plan and swapped it for one if-then card"))

ch.oneliner("so what actually works?",
            "Plan the when and where, make step one tiny, move the temptation, and forgive the slips.",
            panel=svg(monitor(118, 50, 84, 50, ["IF 9 PM,", "OPEN FILE"], fs=9) + desk(104, 116, 112)
                      + person(60, 150, 0.95, mood="o", shirt=GREEN)
                      + bubble(8, 8, 104, "So what actually works?", 60, 62, fs=10)
                      + pinky(258, 150, 0.95, mood="grin", arms="wave")
                      + bubble(150, 8, 164, "Plan the when and where, make step one tiny.", 258, 62, fs=9.5),
                      "At the office, a colleague asks what actually works and Pinky answers in one breath"))

ch.quizzes([
    ("\"Study more\" or \"If it is 8 pm, open chapter 3\": which wins?",
     "The second. Tying the action to a time and a place means the moment itself reminds you, so you do not have to decide again.",
     "If-then plans"),
    ("Pinky skipped the gym twice. What should she do first?",
     "Forgive herself and set the next if-then. Scolding adds a bad feeling to the gym, which makes the next skip more likely.",
     "Scolding yourself after a slip"),
    ("Why does a phone in another room beat a promise?",
     "It removes the cue. You stop fighting the temptation every few minutes, so there is far less to resist.",
     "Fix the room, not your willpower"),
])

ch.recall([("Why does Thomas Delay's essay only win near the deadline?",
            "Going out pays every day, but the essay's reward is far off, so its pull starts low. It wins only on December 3, when the deadline is close.",
            "Thomas Delay's semester")])

ch.done("Monday, take three",
        "A sticky note on the fridge: \"If it is 7 am and I have brushed, then shoes on.\" The shoes wait by the door, and a podcast is saved for the walk only. "
        "Three weeks in, Pinky has missed two days and forgiven both. Sharma ji, smiling for the first time, holds up his tax form: "
        "\"Help me write one for my tax form?\"",
        panel=svg(f'<rect x="12" y="24" width="72" height="126" rx="6" fill="#fff" stroke="{INK}" stroke-width="1.4"/><path d="M12 70 L84 70" stroke="{INK}" stroke-width="1.2"/>'
                  + f'<rect x="74" y="38" width="4" height="22" rx="2" fill="{GREY}"/><rect x="74" y="80" width="4" height="30" rx="2" fill="{GREY}"/>'
                  + paper(18, 80, 52, 50, ["IF 7 AM,", "THEN", "SHOES"], 9, rot=-3, fill=HALDI)
                  + pinky(132, 150, mood="grin", arms="wave") + shoes(132, 150)
                  + f'<path d="M124 80 q-6 18 0 34" fill="none" stroke="{INK}" stroke-width="1.4"/><circle cx="124" cy="80" r="2.5" fill="{INK}"/>'
                  + sharma(250, 150, mood="smile", brow="flat", arms="hold") + paper(226, 112, 48, 30, ["TAX", "FORM"], 9, fill="#fff")
                  + bubble(170, 8, 142, ["Help me write", "one for my tax form?"], 250, 64, fs=10),
                  "Pinky heads out in gym shoes past an if-then note on the fridge, while Sharma ji, smiling, holds up his tax form and asks for help"),
        moral="Samjha kya? Kal se nahi, aaj se.")
