# Voice: desi, warm, funny, correct

The deck should feel like a friend explaining it over chai, not a textbook. Anyone in India should
recognise the situations; anyone outside India should still follow every card.

## The cast

| Character | Draw with | Personality | Use them to |
|---|---|---|---|
| **Chintu** | `chintu()` | A cheerful robot who read the entire internet. Explains well, loves an analogy, sometimes too confident | Explain the mechanism; occasionally be confidently wrong so Sharma ji can catch it |
| **Sharma ji** | `sharma()` | Dry, sceptical, reading glasses, red pen. Catchphrase: "Data dikhao." | Ask for proof, catch the mistake, own the red-pen card |
| **Pinky** | `pinky()` | Enthusiastic, impatient, tries every shortcut first | Voice the reader's doubts and the common mistake; learn on screen |
| Extras | `person()` | Mummy, a cousin, the chaiwala, a shopkeeper, the boss | Small parts only; name them in the body |

Running gags work: Sharma ji never smiles until the last chapter's done card, where he finally
does (the builder's end card shows him smiling too; keep him flat everywhere else); Pinky's "Kal se pakka"
(from tomorrow, for sure); Chintu's "I read that on the internet" before being half wrong.

Renaming the cast for a deck:
```python
deck = Deck(..., cast={"chintu": {"name": "Robo"}, "pinky": {"name": "Meera", "role": "the new joiner"}})
```

## Indian everyday settings (pick ones anyone relates to)

Chai tapri, the office, a PG or hostel room, a local train or metro, an auto ride, the kirana shop,
a family WhatsApp group, Sunday lunch with relatives, exam season, a wedding, Diwali cleaning and
sales, cricket on TV, IPL nights, monsoon traffic, the society gate, a food delivery app (say "food
app", not a brand), mummy's advice, the EMI that arrives on the 5th.

Money in rupees, distances in km, times in IST habits ("9:30 means 10").

## Bollywood references

Sprinkle, do not pour: one or two per chapter, where they make the idea land. Use only famous,
short dialogues or plot points, quoted correctly, never song lyrics. Name the film the first time.
Safe, well-known examples:

| Reference | Film | Fits ideas like |
|---|---|---|
| "Kitne aadmi the?" | Sholay (1975) | counting, data, asking the right question |
| "Mogambo khush hua" | Mr. India (1987) | a result that pleases the boss |
| "Picture abhi baaki hai, mere dost" | Om Shanti Om (2007) | there is more to come, next level |
| "All is well" | 3 Idiots (2009) | calming the mind, false comfort |
| "How's the josh?" | Uri: The Surgical Strike (2019) | motivation, energy |
| "Bade bade deshon mein aisi chhoti chhoti baatein hoti rehti hain" | Dilwale Dulhania Le Jayenge (1995) | brushing off small errors (and why you should not) |
| "Mere paas maa hai" | Deewaar (1975) | what really matters |
| The "21 din mein paisa double" scheme | Phir Hera Pheri (2006) | too-good-to-be-true offers, scams |
| Jaadu ki jhappi | Munna Bhai M.B.B.S. (2003) | kindness, stress relief |
| Ghajini's memory | Ghajini (2008) | forgetting, notes, memory |
| Geet: "Main apni favourite hoon" | Jab We Met (2007) | self-belief, overconfidence |

Never complete a famous line that contains a swear word in the original, even partly. Prefer
lines with no political or military charge for decks meant to travel widely.

Other famous moments are fine if you are sure of the line and the film. If unsure, describe the
scene instead of quoting it. A playful twist on a famous line is fine ("Kitne group the?" on
Sholay's "Kitne aadmi the?") as long as you name the film and the original stays recognisable.

## Hinglish

- Default: English sentences with one or two Hindi words or phrases per card, always clear from
  context: "Kal se pakka", "Data dikhao", "jugaad", "bas", "arre", "ekdum", "samjha kya?".
- Heavier Hinglish (on request): whole bubbles in Hinglish, body still mostly English.
- Hindi (on request): write in Devanagari. The page fonts cover it. Keep panel text very short.

## Humour rules

- Laugh with people, never at a group. No jokes on caste, religion, region, accent, gender, body,
  age or disability. Sharma ji is sceptical, not mean; Pinky is eager, not stupid.
- Family safe. A teacher should be able to share any card with a class.
- Funny, then correct. A joke never bends a fact.
- Avoid real brand names in a bad light; use generic stand-ins ("a food app", "a bank").

## Money, health and legal topics

- This covers any deck that touches personal money decisions (economics with interest rates or
  EMIs counts), health, or the law.
- Set `caution=` on the Deck ("Education, not financial advice. Returns vary and can be negative.")
  so it shows on the cover and on every chapter's first card: readers share single cards.
- When a card names a market product (a fund, a stock, an SIP), say on that card that its returns
  go up and down. Example growth rates are labelled "example rate" and never shown as guaranteed.
- No chapter ends with a character buying a product type as the happy ending; end on the habit or
  the understanding instead.
- Health: warning signs and "see a doctor when" go in the beginner level. Never write a takeaway
  that normalises a symptom the source treats as a warning sign.

## Conversations with a job

The cast talks on most cards (`ch.chat`). A line earns its place only if it does one of these:
- **Pinky asks a real why or how** before the explanation ("Why does milk first ruin it?").
- **Sharma ji voices the common wrong belief** ("Just train the prices in") and Chintu corrects it.
- **Chintu explains**, in one or two sentences, with the concrete example.
- **Someone tries it** and reports the result.
Small talk, greetings and lines that only repeat the point get cut. Two to four lines per card,
each under about 20 words.

## Writing the body

- Present tense, short sentences, concrete nouns. Numbers as digits.
- Open with a moment ("Monday, 7:40 am."), not a definition.
- One analogy per card, then the plain mechanism. Do not stack analogies.
- The `moral` is the line people screenshot: one sentence, no filler hedges ("it seems", "arguably"), but keep the source's real qualifiers ("may", "most adults", "tend to").
- No AI-sounding filler ("delve", "in today's world", "it is important to note", "game-changer").
- No em or en dashes.
- Do not reuse a punchline or a reaction line ("which from him is applause") anywhere else in the
  deck; each joke appears once.
