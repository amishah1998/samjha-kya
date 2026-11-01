# Drawing panels with the kit

Every panel is `svg(inner, label)`: a 320 x 170 canvas with a cream background and a floor band
from y=150 down. `inner` is SVG strings added together; `label` is the alt text (describe what the
picture shows, one sentence). `svg(..., floor=False)` drops the floor for diagrams.

```
(0,0) ------------------------------------------ (320,0)
  |   bubbles and titles live up here (y 8 to 70)   |
  |   characters' heads around y 60 to 90            |
  |------------- floor line y = 150 ----------------|
(0,170) ---------------------------------------- (320,170)
```

## Characters (feet at x, y; y=150 stands them on the floor)

| Call | Options |
|---|---|
| `chintu(x, y, s=1.0, mood, hat, arms, eyes, tint)` | mood: smile, grin, o, sad, flat. hat: None, "grad", "chef". arms: down, up, wave, hold. eyes: dot, up, x, shades |
| `sharma(x, y, s=1.0, mood, brow, arms)` | mood: flat, smile, o, sad, grin. brow: skeptic, flat. arms: down, up, point, hold |
| `pinky(x, y, s=1.0, mood, arms)` | same moods and arms as sharma |
| `person(x, y, s=1.0, mood, shirt, arms, hair_col)` | an extra: any colour shirt and hair |

At scale 1 a character is about 50 wide and 95 tall (Chintu's antenna reaches y about 55).
Three characters fit at x = 60, 160, 260. Two fit at x = 70 and 240. Use `s=0.6` to 0.8 for a
small figure beside a big prop.

## Text

- `bubble(x, y, w, text, tx, ty, fs=11)`: speech bubble, top-left at (x, y), width w, tail points
  at (tx, ty), just above the speaker's head: for anyone standing at y=150 at scale 1, aim at
  y=58 (Chintu's antenna and Pinky's bun both end around y=65). Pass a string; it wraps to the
  width, with balanced rows so a bubble never ends on one lonely word. To force your own line
  breaks, pass a list of rows.
  Rows are about fs*1.22 tall, so a 3-row bubble at fs 10 is about 47 tall.
- `think(x, y, w, text, tx, ty, fs=10)`: thought cloud.
- `text(x, y, s, fs, anchor, fill, weight)`: one line. `lines(x, y, rows, fs)`: several.
- `board(x, y, w, h, text, fs=9, title=None)`: a whiteboard on legs.
- `sign(x, y, w, text, fs=9, fill)`: a label box (shop board, tag). `sticky(x, y, label)`.
- `paper(x, y, w, h, text, fs=8, rot=0)`: a sheet of paper. `monitor(x, y, w, h, text)`: a screen on a stand.
- `phone(x, y, text, fs=7, h=64, w=36)`: a phone with text on its screen.
- `stamp(x, y, label, color, rot, fs)`: a rubber stamp ("BUSTED", "PAID", "WRONG").

Keep panel text to about 12 words in total. The body carries the detail.

## Props

`chai(x, y, s)`, `coin(x, y, r, label)`, `coins(x, y, n)`, `clock(x, y, r, hour, minute)`,
`calendar(x, y, top, big)`, `bed(x, y=150, w, sleeper)`, `moon(x, y, r)`, `sun(x, y, r)`,
`bulb(x, y, on)`, `plant(x, y=150)`, `heart(x, y, s)`, `books(x, y, n)`, `shelf(x, y, w, rows)`,
`desk(x, y, w)`, `tick(x, y, s)`, `cross(x, y, s)`, `arrow(x1, y1, x2, y2)`.

## Charts and diagrams

- `bars([(label, value, colour, value_text), ...], x=110, y=28, step=24, scale=1.6)`: horizontal bars.
  `value * scale` is the bar length, so keep `x + max(value) * scale` under about 290.
- `line_chart(x, y, w, h, values, labels=("Year 1", "Year 10"))`: axes and a line.
- `flow(["Step", ["Two", "rows"], "Step"], y=60, w=56, gap=20)`: boxes joined by arrows; four boxes fit at the default size.
- `layers([(label, colour, note), ...])`: stacked bands with notes to the right.
- `duo(left_svg, (text, fs), right_svg, (text, fs), label)`: two characters with a bubble each. `text` is a string (wrapped for you) or a list of rows (each row is wrapped too if it is too long).

Colours: `INK, TEAL, TEAL2, HALDI (turmeric yellow), CORAL, CREAM, FLOOR, PAPER, BLUE, GREEN, GREY, WOOD, SKIN, SKIN2`.

## Recipes

Two people talking:
```python
svg(pinky(70, 150, mood="o") + chintu(240, 150, mood="grin", arms="wave")
    + bubble(10, 10, 130, "Bas 5 minute aur?", 70, 70) + bubble(178, 10, 132, "That is what you said at 6 am.", 240, 52),
    "Pinky pleads for five more minutes; Chintu points out the time")
```

Explainer at a board:
```python
svg(board(20, 16, 170, 100, "Money earns money, then that money earns money too.", 10, title="COMPOUNDING")
    + chintu(250, 150, mood="smile", arms="wave"),
    "Chintu explains compounding at a whiteboard")
```

Before and after:
```python
svg(sign(30, 20, 110, "BEFORE", fill="#fff") + sign(180, 20, 110, "AFTER")
    + pinky(85, 150, 0.8, mood="sad") + pinky(235, 150, 0.8, mood="grin", arms="up") + arrow(130, 100, 190, 100),
    "Pinky sad before, happy after")
```

Numbers:
```python
svg(bars([("Age 25", 100, TEAL2, "Rs 1 crore"), ("Age 35", 38, CORAL, "Rs 38 lakh")], x=70, y=50, step=34, scale=1.6)
    + chintu(280, 150, 0.6, mood="o"), "Two bars: starting at 25 ends far higher than starting at 35")
```

## Composition rules

- Draw the card's turning point, not its setup: the moment the idea lands (the bitter glass, the
  price tag changing), not two people standing before it happens.
- Label the key term in the picture (`key=` must appear in the panel's text; the build checks it).
- A speech bubble or thought cloud is a line of the card's conversation, word for word; on a quiz
  card the picture is the tested card's picture, shown again with every word removed and a "?"
  badge over its top-right corner (about x 272 to 312, y 8 to 48). So a card that a quiz names
  draws its idea with objects, not words on a board, and keeps that corner clear.

- The panel must show the idea: the object, the comparison, the mistake. A row of characters
  smiling is not a panel.
- Leave 6 units of margin at every edge. Bubbles must not overlap each other or a sign (the check fails).
- Point bubble tails at the speaker's head, not their feet.
- Keep the floor clear for characters; put labels in the top half.
- Vary layouts between neighbouring cards.
- Run `check.py --shots` and look at the contact sheets: the check catches overlaps and spills,
  not ugliness.
