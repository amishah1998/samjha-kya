# Contributing

Thanks for helping. Good first contributions:

- **New props and poses** for the cartoon kit (`skills/samjha-kya/scripts/art.py`): a flat SVG function that takes `x, y` and a few options, draws inside the 320 x 170 panel, and passes `check.py`.
- **Card types** in `skills/samjha-kya/scripts/deck.py`, with a line in `references/flow.md`.
- **Voice guides** for other languages or regions (`references/voice.md`).
- **Decks you made.** Open an issue with a link and the request you gave your agent.

Before you open a pull request:

```bash
python3 skills/samjha-kya/scripts/build.py skills/samjha-kya/assets/template_deck.py -o /tmp/starter.html
uv run --with playwright python skills/samjha-kya/scripts/check.py /tmp/starter.html
```

The check must print PASS. If you change the engine, rebuild the examples with `uv run --with playwright python tools/site.py` and check them too.

Keep text free of em and en dashes; use commas, colons or full stops.
