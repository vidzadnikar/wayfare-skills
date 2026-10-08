# Trailer

Every vlog opens with a trailer: 10–15 s of the best moments, then the title.
Make it when shots, music and captions are done, before rendering. `W` is the
`wayfare` command (SKILL.md, Setup).

**Structure**: 1. **hook** — a moment with its own sound (reaction, laugh,
sentence; with speech the whole sentence), not in time order; 2. **jump** —
the montage starts on a downbeat where the track lifts; 3. **montage** — shots
across the day in time order, short transitions, calm 3 beats, moving 2;
4. **last shot** — mood or highlight, the longest; 5. **flash** into the title.
Shots must not all be the same length, and music must not be cut.

**Music**: one track without cuts, dramatic or energetic, **from the library,
not from the film** (`--glasba dramaticno | energicno | <path>`), set 3 dB
above the film's music. Swooshes, a riser into the flash and a hit on the
title are added automatically (`--zvoki brez` turns them off).

## Pick

```bash
W napovednik "<project>" --pregled
```

It prints the music, shots with beats and a proposal. Read
`_vlog/napovednik/pregled.jpg`: the first row are hooks, then one row per part
of the film (first frame = automatic pick, then candidates `clip@time`). The
automatic pick is a draft — it does not know what is in a shot or what is said.

- **Hook**: a face with a reaction, a laugh, someone showing or saying
  something — not a back, not an empty landscape. Find candidates by sound:
  `W zvoki <clip> --strni Laughter Speech Applause Cheering`. If the hook is
  speech, ask the user which sentence is good or to mark it in the Studio.
- People and action before objects; **every place of the day once**; sharp,
  bright, **60 fps** (30 fps stutters in a fast montage); consecutive shots
  differ in framing or color; **the last shot is mood**.

## Insert

```bash
W napovednik "<project>" --glasba dramaticno \
  --kavelj 005@4.2-6.4 --trenutki 002@4.0,006@7.7,008@8.7:3,009@1.6,011@1.1
```

- `005@4.8` searches for a sentence around that moment; `005@4.2-6.4` takes
  exactly that span; `:3` sets a shot's beats. Also
  `--ritem tekoce|pospesi|mirno`, `--prehodi zivahni|mehki|brez`,
  `--konec bliskavica|crnina`, `--dolzina` (12).
- Running it again replaces the old one; `--odstrani` removes it.
- Captions, inserts and music shift automatically — if the user is editing in
  the Studio, tell them the film moved.
- The review checks it (D1–D8; D2 is OKO on `napovednik.jpg`).
