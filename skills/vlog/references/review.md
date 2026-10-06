# Review before done

The last step of every vlog. The edit is done, the render is on disk — and only
here is it decided whether the vlog is finished. While any requirement below
is not met, the vlog is **not** done and must not be called done.

A contact sheet of still frames is a sample, not a review: it has no motion and
no sound. The vlog must meet every requirement, and you fix it until it does.

## When

After `render`, before telling the user the vlog is finished. If the vlog has a
trailer, the review covers the **whole** render including it — the trailer is
the first 15 s, exactly where the viewer decides to stay.

## Tools

All commands below are run as `"$R/bin/wayfare" <command>` with
`R="/Applications/Wayfare Studio.app/Contents/Resources"` (see SKILL.md, Setup).

`pregled` runs everything below at once and in parallel; you need the single
tools only on the manual path or for an extra check.

| what | with | tells you |
|---|---|---|
| edit and render measurements | `preveri` | LUFS, true peak, sync, shots past clip end, double ducking |
| picture in motion | a video-watching skill if installed, else frames | what is really seen, where cuts land, how the pace reads |
| speech | `zvoki` + cleaned speech around cuts | where speech is and whether a cut falls on a word or in a pause |
| kind of sound | `zvoki` | speech, music, wind, laughter, water, vehicle, animal |
| spectrum | `ffmpeg showspectrumpic` + `astats` | clipping, noise floor, steady tones, gaps |
| noise under speech | `ocisti --primerjaj` | floor, peak, gap, RMS and noise before and after cleaning |
| color | `barve` | brightness, white balance, blown-out pixels per shot; `color` suggestion |

The bundled `ffmpeg`/`ffprobe` are in
`/Applications/Wayfare Studio.app/Contents/Resources/app/vendor/ffmpeg/bin`.
The `wayfare` command already puts them on `PATH`; for other tools add that
folder to `PATH` yourself. A `Fontconfig error: Cannot load default config
file` message is harmless.

Transcription (`prepis`) is not bundled and is **not used in the review**: word
timings are unreliable for cuts. A cut in the middle of a word is measured on
cleaned speech around the cut instead. Where the exact words matter — is the
sentence whole, is the hook understandable — ask the user.

## Procedure

```bash
R="/Applications/Wayfare Studio.app/Contents/Resources"
"$R/bin/wayfare" pregled "<project>" --popravi
```

About 30 s. The report is also in `_izris/pregled/porocilo.json`, images in
`_izris/pregled/`. Exit code 1 means something is **NI** (not met).

| status | meaning | what you do |
|---|---|---|
| izpolnjeno (met) | measured and fine | nothing |
| **NI** with a fix | measured, fix computed | `--popravi` already wrote it |
| **NI** without a fix | measured, no fix computable | fix it by the requirement below |
| **OKO** (eye) | cannot be measured | read the attached images and judge |
| ne velja (n/a) | e.g. a vlog without a trailer | nothing |

**Before the first render** run `pregled --pred --popravi`: it works on the
edit and the source clips and catches unmarked speech, noise under speech, cuts
in the middle of a word, still shots without motion, automatic subtitles,
music and trailer mistakes, long talking in one picture (B11, cut with
punch-ins), missing J-cuts (B12) and the film look (B15) — before any render
runs. Lay cutaways **before** this step; punch-ins are for what remains.

**OKO, in order:**

- **A8 spectrum** — steady horizontal lines that start and end on a cut are a
  tone; black vertical stripes are gaps.
- **B3** — a shot with no detected cut: look at the frames before and after the
  boundary; are they too similar?
- **B6 cut in a word** — the command says where the nearest pause is (e.g.
  `premor -0.11 s`). Move the cut by that much: outgoing shot and its sound
  +δ, incoming `start` and `in` +δ, `dur` −δ. Move music that changes on that
  cut with it (E2). Under 0.05 s is inaudible — leave it.
- **C4C5 captions** (`napisi.jpg`) — special characters, position, what is
  under the caption.
- **C8 inserts** (`vstavek-N.png`, full size) — estimate the height of the
  smallest letters in pixels.
- **D2 hook** (`napovednik.jpg`, 3 frames/s) — reaction, laugh, sentence.
- **B11 punch-in** — the frame in the middle of each piece marked `priblizano`:
  the face is in frame, no cut-off forehead or chin. If it is, fix `frame.y`
  (smaller raises the crop).
- **B13 speed ramp** — is there walking, driving or metro without speech
  longer than 4 s, and does it have `ramp`? If there is none, n/a.
- **B14 new places** (`kraji.jpg`) — the first shot of each new scene shows the
  place (wide), not a detail.
- **D8 story of the day** — is the sentence that opens the day's question in
  the first minute and whole? Is the highlight in the film, and do the picture
  cards not give it away?

Then render again and run `pregled` again. Done when there is no NI and every
OKO is judged.

### Manual path

Only if `pregled` does not run, or something needs a separate check.

1. **Measurements.** `preveri <project>`. Exit 1 means an error; errors are
   requirements A1–A4.
2. **Frames.** Extract about 1 frame/s from the render; the **trailer
   separately at 3 frames/s** — at 1/s, two-beat shots are almost invisible.
3. **Cuts.** Scene detection at threshold 0.15; compare with shot times in
   `edit.json`. **Count first:** if far fewer cuts are found than shots in the
   edit, the threshold is to blame — lower it to 0.05 before claiming anything.
   At 1 frame/s one shot often spans two frames; two similar frames are **not**
   proof of two similar shots.
4. **Sound**, on the render:

   ```bash
   "$R/bin/wayfare" zvoki "<render>" --strni Speech Music
   ffmpeg -i "<render>" -lavfi "showspectrumpic=s=1600x800:legend=1:scale=log" spectrum.png
   ffmpeg -hide_banner -nostats -i "<render>" -af astats -f null -
   ```

   Compare `Speech` segments with `voice: true` in `edit.json` (A5). Read the
   spectrum (A8). From `astats` take the flat factor (clipping) and noise floor
   (A6, A7). Measure noise under speech on the **source clips** of speech
   shots, not on the render — music hides it there (A9):
   `zvoki <clip> --od <in> --dolzina <dur> --json`, then
   `zvoki.sum_pod_govorom` on the result.
5. **Color.** `barve <project>` (B9, B10). Look at both shots before applying a
   suggestion.
6. **Inserts.** For each insert, crop its area from the render at full size at
   a moment its text is visible, and read it (C8). A full-frame route: check
   the first, last and widest frames — no black, no model edge, no fade to
   black.
7. **Judge by requirements**, A to F, each separately: met / not met / cannot
   measure, with the time in the vlog and what you saw or measured.
8. **Fix everything at once**, not one by one. A render takes minutes.
9. **Render again and repeat.**

## Requirements

The standard is what was asked and what was measured. A requirement is not
softened to end a round sooner. If a requirement seems wrong, tell the user —
do not change it yourself.

### A. Sound (measure, recognize and clean — not listen)

1. Master **−14.5 LUFS ±1**, true peak **below −1 dBTP**.
2. Shots without speech are **not 6+ dB below** shots with speech.
3. No silent shot: where nobody talks, music carries it. Lowered music **and**
   lowered shot sound together are a mistake. A **breath** (in `dihi`) is not
   a silent shot: music drops, the place's sound comes forward and carries it.
4. No double ducking — `duck` in `envelope` mode **or** manually lowered
   pieces, never both.
5. **Ducking lies where speech is.** `Speech` segments from `zvoki` match the
   elements with `voice: true`.
6. **No clipping** — `astats` flat factor 0 and true peak below −1 dBTP.
7. **Noise floor not too high** (around −48 dB is good). Above −40 dB the
   review listens to the quietest spot: noise (wind, hum, traffic) is a
   mistake; music or speech is not.
8. **No steady tone in the spectrum** running through a shot and ending on a
   cut. If there is one, say where and at what frequency — whether it bothers,
   the user decides.
9. **No noise under speech.** For every `voice: true` shot,
   `zvoki.sum_pod_govorom` on the source is empty — or the shot has `ocisti`
   and `ocisti --primerjaj` shows the gap grew, `Speech` stayed above 0.9 and
   noise fell below 0.3. Its `gain_db` is computed from the cleaned copy's RMS.

### B. Cut

1. Shots go **in shooting order**, no jump back.
2. **Shot lengths differ.** All equal reads mechanical.
3. **Consecutive shots differ in framing or color.**
4. No shot runs past the end of its clip — no frozen last frame.
5. No duplicated frames in motion (30 fps material in a 60 fps vlog).
6. **A cut does not cut through speech.**
7. Still shots (view, castle, panorama) have `motion`; moving shots do not.
8. The output shape matches the material — vertical clips give a vertical
   vlog, no black side bars.
9. **Daylight shots are exposed correctly.** `barve`: brightness 90–175,
   blown-out pixels under 2 %. Evening and night shots are dark by nature.
10. **The same scene does not break in color.** Consecutive shots from the same
    day at most 10 minutes apart: brightness jump under 15 %, white balance
    jump (R/B on neutral pixels) under 0.08.
11. **Speech does not stay in the same picture longer than 12 s.** A cutaway, a
    punch-in or a card over speech is a change of picture. Fix: punch-ins in
    pauses (pieces up to 8 s).
12. **J-cuts at scene changes** where possible (no speech at the end of the
    previous shot, material available).
13. **Speed ramp on the way** (OKO): walking, driving, metro without speech
    longer than 4 s — at least one such shot has `ramp`.
14. **A new place starts wide** (OKO, `kraji.jpg`).
15. **The film look is on** — `videz` in the edit, the same across all days of
    a trip. Fix: `film`.

### C. Captions

1. A **title with the date** at the start, short event labels along the way.
2. Style: `din-cond`, upper case, white, border and shadow — not the most
   ordinary.
3. Entry and exit animate (`slide-up`).
4. **Special characters are right** — read them from the frame, do not assume.
5. A caption does not cover a face or what is readable in the shot.
6. A label stays long enough to read (about 3 s).
7. Place names only where the place is visible in the shot.
8. **Text in an insert is readable**: smallest letters at least 2 % of frame
   height (22 px at 1080p).
9. **Place and time on glass at each new place** — a `kraj` element on `G1`,
   time from the catalog (`kraj.dodaj`). No separate clock top-left and no
   place label bottom-left at the same time. It must not cover a face; if it
   does, use `top-left`.

### D. Trailer (if there is one)

1. **10–15 s**, ends with a flash into the film's title.
2. **The hook has its own sound** — reaction, laugh, sentence. With speech, the
   **whole sentence**; if in doubt, ask the user.
3. Music is **one track without cuts**, dramatic or energetic, from the library
   and not from the film.
4. **Shots are not all the same length** — calm 3 beats, moving 2.
5. Hook and montage within 2 dB of each other, montage 3–4 dB above the film.
6. No 30 fps material unless there is no other option.
7. The montage starts on a downbeat.
8. **Story of the day** (OKO): the sentence that opens the day's question is in
   the first minute and whole; the highlight is in the film; the picture cards
   do not give it away. N/a for a day without an intro.

### E. Music

1. **Three to four tracks**, all from the same group, tempos close together.
2. Tracks **do not overlap**. A change is a cut on a picture cut, with a 0.7 s
   fade on each side.
3. The change lies where the day turns.
4. The track section is aligned to a downbeat.
5. **Accents and breaths are rare**: at most four sound accents outside the
   trailer and at most two breaths.

### F. Finish

1. Attribution for CC BY tracks is written out and given to the user.
2. What you could not measure is said plainly. You recognize the kind of
   sound, measure loudness, see the spectrum — **whether it sounds good, you do
   not know**. Whether the track fits, the voice is pleasant, the mix is
   pleasing: that stays the user's judgment.
3. **Publishing package from this render** — `_izris/objava/poglavja.txt` is
   newer than the render; chapters are in the report. Fix: `objava`.
4. **Day in numbers** — `stevilke` on `G1` before the end of the day (in a
   recap, one at the end).

## Deciding alone

The review **does not ask about every finding**. Assess, decide, fix, render,
assess again — and at the end say what you decided and why.

Fix without asking:

- **any value**: `gain_db`, `voice`, caption position, size, style, effect,
  `motion`, color fix, `master_db`, music level;
- **anything the user did not make** — automatic subtitles, automatically
  picked trailer shots, anything marked `samodejno` (automatic).

Remove only when a requirement A–F demands it, always with a copy in
`_vlog/zgodovina/` and an explanation in the report:

- **the user's own material**: a shot, a photo, their hand-written caption,
  their track.

Never invent new content (narration, new music, new shots), and never soften a
requirement to finish a round. If a requirement stays open, say so.

## Decisions that already apply

| finding | decision | why |
|---|---|---|
| automatic subtitles with wrong words | remove | wrong text on screen is worse than none |
| caption on a screen, face or text in the shot | move to a clean part of the frame | C5 |
| close speech pushed down | raise it and mark `voice: true` | A5 |
| one vertical clip or screenshot among horizontal ones | **leave** | one vertical insert does not change the output shape |
| `preveri` reports a time jump for a photo or screenshot | **leave** | shooting order applies to clips; a still has no visible time |
| noise under speech (wind, traffic, engine) | `"ocisti": true`, then `gain_db` from the cleaned copy | A9 |
| `barve` reports a jump or bad exposure | `color` suggestion, render, measure again | B9, B10; look at both shots first |
| text in an insert too small | text as a `kartica` on `G1` over the insert | C8; a 3D re-render takes up to an hour and a half |
| long talking in one picture | cutaway first (`prekrij`), punch-ins for the rest (`--popravi`) | B11 |
| missing J-cut | `--popravi` makes it | B12 |
| no film look | `film` | B15; the user can change it in the Studio |
| a day without day-in-numbers | `stevilke` on the last calm shot without speech | F4 |
| `--popravi` brightens dark interiors (opera, museum, dawn) | restore the previous colors; B9/B10 stay a judgment | dark is the place, not a mistake |
| B10 keeps chasing brightness shot after shot | stop after one fix; the rest is judgment | sun and shade in the same place are real |
| true peak above −1 dBTP | `limit_db` −3 | the limiter catches sample peaks, not true peaks |

### What level to raise speech to

Do not guess. In **this** edit compute `source RMS + gain_db` for all elements
that already have `voice: true` and take the median; give a fixed shot
`gain_db = median − its RMS`. For a shot with `ocisti`, use the **cleaned
copy's** RMS (`ocisti --primerjaj` prints it) — cleaning removes energy, and
the source RMS would leave the shot several dB too quiet.

## How many rounds

Up to three. Each round: assess everything, fix everything, render, assess
again. After the third, do not keep going: tell the user which requirement
stayed open, what you tried and why it did not work.

Before every new round: a copy in `_vlog/zgodovina/`, and if the user changed
something in the Studio meanwhile, their setting is the starting point.

## Report

When every requirement is met, write the user a short report: what was wrong,
what you fixed, and **which decisions you made yourself** — especially where
you removed something or judged a finding not to be a mistake. No list of
everything that was fine. Also say what you could not measure.
