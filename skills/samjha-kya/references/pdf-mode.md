# PDF mode: from a document to a deck

## 1. Extract

```bash
uv run --with pypdf python $S/pdf_text.py file.pdf > pages.txt      # next to your deck.py
```

Each page starts with `=== page N ===`. The last line counts pages and flags pages with no text
(scanned images). For scanned pages, tell the user they need OCR first (for example `ocrmypdf`).

Long PDFs: read the contents page and headings first, then read the sections you will use in full.
Do not summarise a PDF you have only skimmed.

## 2. Map the PDF onto levels

Size by pages: up to 20 pages, 1 chapter per level; 20 to 80 pages, 2 to 3 per level; more, 3 to 4
per level. Put the page count in `source={"pages": N, ...}`; the build warns when a long PDF gets
too few chapters.

Levels follow difficulty, not the PDF's page order. Safety-critical points (warning signs, when to
see a doctor, deadlines, what not to do) go in the BEGINNER level, even if the PDF puts them at the
back; they can be repeated in more depth later.

- **Beginner:** the document's purpose and its 3 to 5 core ideas, in everyday terms.
- **Intermediate:** how its main processes, rules or numbers work, with its own examples.
- **Advanced:** exceptions, fine print, edge cases, and what people most often get wrong.

Information first: before writing cards, write an inventory file `facts.txt` next to deck.py, one
line per item: `p<page> | CORE or SUPPORTING or MINOR | the fact | card id or LEFT OUT: why`. Write of  it for every heading and every key fact, number and recommendation in the PDF, and tag the
guide's main messages CORE.
Every item must end up on a card or in `left_out=[(what, why), ...]` on the Deck, which the cover
shows as a "Left out of this deck" list. A CORE item is never left out. Before handing over, walk
the inventory once more and tick each item against a card id; anything unticked is a bug. A 20-page guide is one chapter per level. A 100-page book may need two to four
chapters per level; pick the sections that matter most and put the rest in `left_out`.

## 3. Cite every fact

- Put `pg(n)` at the end of any sentence whose fact comes from page n: `"Adults need 7 to 8 hours {pg(12)}."`
  That includes myths, red-pen notes, tables and quiz answers. n is the PDF's page (the
  `=== page N ===` number), not the number printed on the page.
- Fill `source=` on the deck so the cover credits the document:
  ```python
  deck = Deck(..., source={"title": "Your Guide to Healthy Sleep (NIH, 2011)", "url": "https://...", "note": "Page numbers refer to this PDF."})
  ```
- Stories and characters are yours; facts are the PDF's. If you add outside context, say so in the
  sentence ("Outside this guide, ...") with a `src()` link.
- Local examples of the PDF's own ideas are fine and encouraged (dal as an example of the guide's
  "pulses", rajma chawal next to its cottage pie). Mark them "our example" and keep the PDF's
  category or number unchanged.
- Your own practical tips are fine when labelled ("Our tip: compare per 100g"). Plain word or unit
  definitions (microgram, GP) need no source. If the document's advice is national (UK vitamin D,
  US hotlines), say so on the card ("UK advice; check what applies where you live").
- Keep quotes short (one sentence). Rephrase the rest in plain words.

## 4. Rights and credit

A deck made from a PDF copies its ideas, not its text, but it still credits the source. Before
publishing a deck online, check the PDF's licence: government publications in some countries
(for example most US federal works) are public domain; many others allow sharing with credit;
some forbid it. If the licence is unclear, keep the deck private. Put the licence name in the
`source=` note ("Open Government Licence v3.0"), so the cover credits it.
