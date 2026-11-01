# The chapter rhythm

Every chapter follows the same beat, so readers always know where they are. The builder adds the
"Before you start" card (cast plus glossary) at the top of each chapter and a level card before the
first chapter of each level. You write everything from the opener on.

```
[Before you start]  auto: cast + the chapter's glossary
1. opener            the hook scene: a relatable problem that raises the chapter's question
2..n middle          9 to 14 cards mixing the types below, one idea each, mostly ch.chat
   myths             2 to 4 common beliefs: the fact first, the myth once
   redpen            3 to 5 lines worth remembering, as Sharma ji's margin notes
   oneliner          the chapter in one sentence
   quizzes           2 or 3 quick checks, each naming the card it tests
   recall            from chapter 2 on: 1 "Yaad hai?" question about an earlier chapter
   done              the payoff scene and a callback to the opener
[Mixed review]       auto, at the end of each level: one question from each of its chapters
                     (a one-chapter level adds the chapters before it, so level 1 needs 2 chapters)
[Level done]         auto: what the level taught, and what the next level adds
```

Card ids are `c<chapter>-<n>`. The auto "Before you start" card is n=1, so a chapter's opener is
`c1-2`, its next card `c1-3`, and so on. Build warnings and check.py use the same ids. Card counts
in this guide ("14 to 20 per chapter") count the cards you write, not the auto ones.

## Middle card types

| Method | Badge | Use it for | Panel idea |
|---|---|---|---|
| `ch.chat(title, panel, lines, points=[...], moral, key=)` | Talk | **The default.** The idea as a 2 to 4 line conversation, then 2 or 3 points to remember | The moment of the conversation; its bubble is one of the lines |
| `ch.story(title, panel, body, moral)` | Story | A scene where a character hits the idea in real life | Characters mid-action, one bubble |
| `ch.true_story(...)` | True story | A real, sourced event (needs `src()` in the body) | The event, simply drawn |
| `ch.idea(...)` | Idea | The mechanism, stated plainly with an analogy | A board, a diagram, an analogy object |
| `ch.picture(...)` | Picture it | A diagram: flow, layers, before/after | `flow()`, `layers()`, arrows |
| `ch.glance(...)` | At a glance | A small comparison table, use `table(head, rows)` | Two signs with tick and cross |
| `ch.example(...)` | Worked example | Real numbers worked step by step | `bars()`, `line_chart()`, coins |
| `ch.watch_out(...)` | Watch out | The common mistake and what it costs | A character's face when it goes wrong |
| `ch.try_it(...)` | Try it yourself | A 1-minute task the reader can do now; answer in `<details>` | Phone, paper, calendar |
| `ch.card(kind, badge, title, panel, body, moral)` | any | Anything else; reuse a kind above for styling | |

Any card's `badge` can be renamed ("Plot twist", "The maths", "Cheat sheet 1 of 2"). Every teaching
card takes `key="term"`: the one term it teaches, bold in the body and labelled in the picture.
The other card types can carry a conversation too: put `talk(...)` and `keys(...)` inside any body.

A chat card, in full:

```python
ch.chat("Milk blocks the brew",
        svg(board(24, 18, 150, 96, ["Leaves + boiling water", "= flavour out fast"], 9.5, title="WHY")
            + pinky(240, 150, mood="o") + bubble(196, 8, 118, "Why does milk first ruin it?", 240, 58, fs=9.5),
            "A whiteboard on brewing, with Pinky asking why"),
        [("pinky", "Why does milk first ruin it?"),
         ("chintu", "Leaves give out flavour fastest at a <b>rolling boil</b>. Milk cools the pot, so the brewing slows."),
         ("sharma", "So the order matters, not the brand.")],
        points=["<b>Water first</b>: leaves boil alone", "<b>Milk second</b>: it slows the brew"],
        moral="Water first, milk second. Always.", key="Milk")
```

Speakers are "chintu", "sharma", "pinky", or any other name for an extra. `scene("Monday, 7:40 am.")`
adds an italic stage direction before the talk.

## A good middle, by level (standard size, 14 to 20 cards per chapter)

- **Beginner:** opener, chat, picture, chat, glance, story, chat, watch_out, example, try_it, then the closing run.
- **Intermediate:** opener, chat, example, picture, chat, glance, watch_out, story, chat, try_it, then the closing run.
- **Advanced:** opener, true_story, chat, picture, example, watch_out, chat ("The nuance"), glance, story, try_it, then the closing run.

Vary the panel style between neighbouring cards. Never three "two people talking" panels in a row.

## Closing run details

- `ch.myths([(myth, reality), ...], moral=None)`: the card shows the fact first and the myth once,
  struck through (repeating a myth makes it feel true). The default picture pins up the facts.
- `ch.redpen([...], where=None, panel=None)`: give it `panel=`, a real scene (Sharma ji with the
  chapter's key object); the default notepad only reprints the text. imperatives or crisp facts, under 10 words each. `where=` is the short name written on Sharma ji's page ("the FD chapter"); long chapter titles get cut, so pass one.
- `ch.oneliner(question, line, bubble_text=None, panel=None)`: the question a friend asks; the line
  answers it in under 20 words. Give it `panel=`, the moment the friend asks and gets the answer;
  `bubble_text` is an optional shorter version of the line for the drawing.
- `ch.quizzes([(q, a, "title of the card it tests"), ...])`: test understanding, not recall of a
  number. Answers in one or two sentences that also teach. The named card's picture is shown again
  with all its words removed: the scene is the memory cue, and the words would give the answer away.
  `panels=` replaces it with your own drawing of the question's situation (never its answer; the
  build warns when a quiz picture shows words of the answer).
- `ch.recall([(q, a, "title of a card in an earlier chapter")])`: from the second chapter on, one
  "Yaad hai?" question about an earlier chapter. Coming back after a gap (spacing) is one of the
  strongest memory effects known; the build warns when a chapter has none.
- `ch.done(title, body, moral="Samjha kya? Keep swiping.", panel=svg(...))`: close the opener's story,
  in words and in the drawing (the same place and people as the opener, now sorted out).
- Length limits the drawings need: each myth under 54 characters (the myth panel prints it), each
  red-pen note under 44 characters and at most 5 notes, the one-liner's question under 45 characters
  (its card title is `If someone asks "<question>"`). `ch.myths(..., panel=)` and `ch.redpen(..., panel=)`
  take your own drawing if you prefer.

## Sizes

- One idea or a short guide: 3 chapters (one per level), about 50 to 60 cards with the auto cards.
- A subject ("economics 101") or a long PDF: 2 to 3 chapters per level. A course or book: 3 to 4.
- Each chapter: 14 to 20 cards you write (the build warns below 12 or above 24), of which at least 9
  are teaching cards (story, true story, idea, picture, glance, example, watch out, try it).

## Cards that stand alone

Readers jump in from the Menu search. So:
- Never refer to another chapter ("as we saw", "remember Ch 2"). Re-explain in one clause or add the
  term to that chapter's `glossary`.
- The opener of each chapter re-introduces the situation in its first sentence.
- `glossary=[("Term", "plain one-line meaning"), ...]` on `deck.chapter(...)`: only terms the
  chapter uses without explaining. Two to five is typical.

## Built on how memory works

| Rule | Why (evidence) |
|---|---|
| Picture and text are one story; the panel labels the key term | Pictures that only decorate lower learning on average; a picture tied to the text beats no picture (several meta-analyses on "seductive details" and multimedia learning) |
| Talk between the cast, with a job | A conversational tone helps (meta-analysis); watching a dialogue beats a monologue when the learner asks deep questions or a wrong belief is corrected |
| Bold 1 to 3 key terms | Cues that point at what matters improve recall (meta-analysis); too many cues stop working |
| Tables for comparisons, sentences for cause and effect | Tables beat prose and outlines for comparing; "because" and "so" help understanding |
| Quick checks that bring back the picture | Retrieval practice is one of the strongest learning effects (meta-analysis); the same picture at test aids recall |
| "Yaad hai?" and the mixed review | Spacing and mixing questions from different chapters improve long-term memory (meta-analysis) |
| Myths: fact first, myth once | Repeating a myth makes it feel familiar, and familiar feels true |
