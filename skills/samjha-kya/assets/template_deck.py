"""Starter deck: copy this file, keep the structure, replace the content.

One chapter shows every card type in the standard order. A real deck has at least one chapter per
level (beginner, intermediate, advanced). Build it with:
    python3 <skill>/scripts/build.py deck.py
"""
from samjha import *

deck = Deck(
    title="Cutting chai, explained",
    tagline="Why the tapri chai tastes better than yours, in 30-second stories.",
    slug="cutting-chai",
    about="Chintu, Sharma ji and Pinky try to crack the perfect glass of chai.",
)

# ---------------- Beginner ----------------
ch = deck.chapter("beginner", "Why does tapri chai taste better?", glossary=[
    ("Tapri", "a roadside tea stall."),
    ("Cutting", "half a glass of chai, Mumbai style."),
])

ch.opener(
    svg(chintu(60, 150, mood="grin", arms="hold") + chai(60, 116)
        + pinky(160, 150, mood="o", arms="up")
        + bubble(92, 10, 120, "Mine tastes like hot water. Why?", 160, 58)
        + sign(222, 14, 90, "RAJU TEA STALL", fs=8) + sharma(262, 150, 0.95, "flat", "skeptic"),
        "Pinky holds up her sad homemade chai while Chintu holds a tapri glass"),
    scene("Monday, 7:40 am, outside Raju's tea stall.")
    + talk(("pinky", "Mine tastes like hot water. Why?"),
           ("chintu", "Same leaves as the stall. The difference is <b>time and heat</b>."),
           ("sharma", "Prove it.")),
    "Good chai is not a secret recipe. It is three simple rules done in order.")

# The default teaching card: the picture's bubble is a line of the chat, word for word.
ch.chat("Milk blocks the brew",
        svg(board(24, 18, 150, 96, ["Leaves + boiling water", "= flavour out fast", "", "Milk = cooler pot,", "coated leaves"], 9.5, title="WHY")
            + pinky(240, 150, mood="o")
            + bubble(196, 8, 118, "Why does milk first ruin it?", 240, 58, fs=9.5),
            "A whiteboard explaining why milk slows brewing, with Pinky asking why"),
        [("pinky", "Why does milk first ruin it?"),
         ("chintu", "Leaves give out flavour fastest in water at a <b>rolling boil</b>. Milk cools the pot and coats the leaves, so the brewing slows."),
         ("sharma", "So the order matters, not the brand.")],
        points=["<b>Water first</b>: leaves boil alone", "<b>Milk second</b>: it slows the brew"],
        moral="Water first, milk second. Always.", key="Milk")

ch.story("The four-minute experiment",
         svg(clock(60, 56, 22, 7, 44) + arrow(92, 56, 128, 56) + clock(160, 56, 22, 7, 48)
             + sign(40, 92, 160, "4 MINUTES APART", fs=9)
             + bubble(196, 18, 116, "Boil the leaves longer before the milk", 250, 58, fs=10)
             + chintu(250, 150, 0.9, mood="smile", arms="wave"),
             "Two clocks four minutes apart, with Chintu explaining"),
         "<p>Chintu makes two pots side by side. Pot A: leaves, water and milk together for two minutes. "
         "Pot B: leaves boil in water alone for <b>4 minutes</b>, then the milk goes in.</p>"
         "<p>Sharma ji tastes both with his eyes closed and points at B without a pause.</p>",
         "Leaves need time in plain boiling water before milk joins in.", key="4 minutes")

ch.glance("Home chai versus tapri chai",
          svg(sign(30, 30, 110, "HOME", fs=10, fill="#fff") + sign(180, 30, 110, "TAPRI", fs=10)
              + cross(85, 90, 1.6) + tick(235, 90, 1.6), "A cross under home chai, a tick under tapri chai"),
          table(["", "Home", "Tapri"], [
              ["Leaves boiled alone", "No", "<b>4 min</b>"],
              ["Heat", "Medium", "Full"],
              ["Milk boils", "Once", "Two or three times"],
          ]),
          "The stall is not magic. It just does not skip steps.", key="Tapri")

ch.watch_out("Boiling it for 20 minutes",
             svg(clock(70, 64, 26, 9, 20) + sign(36, 102, 70, "20 MIN", fs=10, fill=CORAL, color="#fff")
                 + chai(170, 140, 1.6) + pinky(260, 150, mood="sad"),
                 "A clock at 20 minutes next to a dark, bitter glass"),
             talk(("pinky", "I boiled it for 20 minutes. Now it is bitter."),
                  ("chintu", "Past six or seven minutes the <b>tannins</b> take over, so it turns bitter."))
             + keys("<b>Four minutes</b> is brewing; twenty is punishment"),
             "Stop before seven minutes.", key="20 min")

ch.myths([
    ("Expensive leaves make good chai.", "Method matters more than price."),
    ("More sugar fixes weak chai.", "Sugar hides weak chai; it does not fix it."),
    ("Adrak goes in at the end.", "Crushed ginger goes in with the leaves so it can boil."),
])

ch.redpen(["Leaves boil alone first.", "Four minutes, full heat.", "Milk second, boil it up twice.", "Stop before seven minutes."],
          where="the chai chapter",
          panel=svg(chai(70, 140, 1.8) + sharma(170, 150, 1.0, "smile", "flat", arms="hold")
                    + paper(206, 30, 100, 60, ["4 MIN", "MILK 2ND"], 10, rot=4, fill="#fff"),
                    "Sharma ji holds up his note card next to a perfect glass"))

ch.oneliner("why does tapri chai taste better?", "They boil the leaves alone first, then let the milk rise twice.",
            panel=svg(pinky(80, 150, 0.95, mood="o") + chintu(240, 150, 0.95, mood="grin", arms="wave")
                      + bubble(110, 12, 200, "Leaves alone first, then milk, twice.", 240, 58, fs=10),
                      "Chintu answers Pinky in one breath"))

# Each quiz names the card it tests: that card's picture is shown again as a memory cue.
ch.quizzes([
    ("What goes in first: milk or leaves?", "Leaves, in plain boiling water.", "Milk blocks the brew"),
    ("Your chai is bitter. What went wrong?", "It boiled too long; tannins took over after about seven minutes.", "Boiling it for 20 minutes"),
])

ch.done("You can now out-chai your office",
        "Water, leaves, four minutes, then milk. Sharma ji has asked for a second glass, which is the highest honour he gives.",
        panel=svg(sign(200, 14, 100, "RAJU TEA STALL", fs=8) + chai(80, 140, 1.6) + pinky(160, 150, 0.95, mood="grin", arms="up")
                  + sharma(250, 150, 0.95, "smile", "flat"), "Pinky's chai finally matches the stall's; Sharma ji smiles"))

# ---------------- Intermediate and Advanced ----------------
# Add at least one chapter for each, same structure. From the second chapter on, add one
# 'Yaad hai?' question about an EARLIER chapter, naming the card it tests:
#   ch.recall([("Why does milk go in second?", "Milk cools the pot and coats the leaves.", "Milk blocks the brew")])
