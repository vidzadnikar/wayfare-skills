# Review before done

The vlog is done only when every requirement below is met — fix until it is.
The review covers the whole render, trailer included (the first 15 s decide
whether a viewer stays). `W` is the `wayfare` command (SKILL.md, Setup).

## Procedure

1. **Before the first render** `W pregled <p> --pred --popravi` (edit and
   source clips): unmarked speech, noise under speech, cuts in a word, still
   shots, automatic subtitles, music and trailer mistakes, long talking (B11,
   punch-ins), J-cuts (B12), film look (B15). Lay cutaways before this.
2. **After the render** `W pregled <p> --popravi` (~30 s, all in parallel,
   `preveri` included), output to a file; read only its `popravljeno` lines.
   Print the open items from `_izris/pregled/porocilo.json` (`zahteve`, status
   `ne` or `oko`, first ~200 characters). Images are in `_izris/pregled/`.
   Exit 1 means something is NI.

| status | you do |
|---|---|
| izpolnjeno (met) / ne velja (n/a) | nothing |
| **NI** with a fix | `--popravi` already wrote it |
| **NI** without a fix | fix it by the requirement below |
| **OKO** (eye) | read the attached image and judge |

3. **OKO** (read only these images):
   - **A8** spectrum: a horizontal line that starts and ends on a cut is a
     tone; a black vertical stripe is a gap;
   - **B3** a shot with no detected cut: are the neighbors too similar?
   - **B6** cut in a word: the command gives the nearest pause (`premor
     -0.11 s`). Move the cut by δ: outgoing shot and sound `dur` +δ, incoming
     `start` and `in` +δ, `dur` −δ; music changing there moves with it (one
     snippet for all cuts). Under 0.05 s, or where the neighbors' pauses
     disagree, leave it;
   - **C4/C5** `napisi.jpg`: special characters, position, what is underneath;
   - **C8** `vstavek-N.png`: height of the smallest letters in pixels; a route
     also first, last and widest frame without black;
   - **D2** `napovednik.jpg`: the hook is a reaction, laugh or sentence;
   - **B11** punch-in: face in frame, no cut-off forehead or chin (else a
     smaller `frame.y`);
   - **B13** speed ramp, **B14** `kraji.jpg`, **D8** story of the day.
4. **Fix everything at once** (one snippet), render, run again. Done when there
   is no NI and every OKO is judged. Claiming something works (ducking)?
   Measure it with a comparison render.

**Manual path** (only if `pregled` does not run): `W preveri` (A1–A4); frames
from the render (1/s, the trailer 3/s); scene detection at 0.15 (far fewer
cuts than shots → lower to 0.05); `W zvoki` on the render, ffmpeg
`showspectrumpic` and `astats` (flat factor, noise floor); noise under speech
on the source clips; `W barve`. The bundled ffmpeg is in
`…/Resources/app/vendor/ffmpeg/bin` (a Fontconfig warning is harmless).
Transcription tells **when** someone talks, not reliably **what** — where words
matter, ask the user.

## Requirements

Never softened to end a round sooner. If one seems wrong, tell the user.

**A. Sound**
1. Master **−14.5 LUFS ±1**, true peak below −1 dBTP.
2. Shots without speech are not 6+ dB below shots with speech.
3. No silent shot: lowered music **and** lowered shot sound together is a
   mistake. A breath is not silent — the place's sound carries it.
4. No double ducking (envelope **or** manual pieces).
5. Ducking lies on speech: `Speech` segments = elements with `voice: true`.
6. No clipping (flat factor 0, true peak below −1 dBTP).
7. Noise floor not too high (~−48 dB is good). Above −40 dB the review
   listens to the quietest spot: noise is a mistake, music or speech is not.
8. No steady tone running through a shot to a cut (if there is: where and at
   what frequency — the user decides whether it bothers).
9. No noise under speech — or the shot has `ocisti` with proof (`ocisti
   --primerjaj`) and `gain_db` from the cleaned copy.

**B. Cut**
1. Shooting order, no jump back.
2. Shot lengths differ.
3. Consecutive shots differ in framing or color.
4. No shot runs past its clip.
5. No duplicated frames in motion (30 fps in 60 fps).
6. A cut never cuts speech.
7. Still shots have `motion`, moving ones do not.
8. Output shape matches the material (vertical → vertical).
9. Daylight shots: brightness 90–175, blown-out under 2 % (`barve`).
10. The same scene (≤10 min apart) does not break in color: brightness under
    15 %, R/B under 0.08.
11. Speech never stays in one picture longer than 12 s (a cutaway, punch-in or
    card is a change). Fix: punch-ins in pauses, pieces up to 8 s.
12. J-cuts at changes of place or time where possible.
13. OKO: walking, driving, metro without speech over 4 s — at least one `ramp`.
14. OKO: a new place starts wide (`kraji.jpg`).
15. Film look on, the same across all days. Fix: `film`.

**C. Captions**
1. Title with the date at the start, short labels along the way.
2. `din-cond`, upper case, white, border and shadow.
3. Entry and exit animate (`slide-up`).
4. Special characters right — read them from the frame.
5. Never over a face or readable text.
6. A label stays ~3 s.
7. Place names only where the place is visible.
8. Letters in an insert at least 2 % of frame height (22 px at 1080p).
9. `kraj` on `G1` at each new place, time from the catalog; no separate clock
   or place label at the same time; readable and not over a face (else
   `top-left`).

**D. Trailer** (if there is one)
1. 10–15 s, ends with a flash into the title.
2. The hook has its own sound; speech is a whole sentence (if in doubt, ask).
3. One track without cuts, dramatic or energetic, from the library.
4. Shots differ in length (calm 3 beats, moving 2).
5. Hook and montage within 2 dB, montage 3–4 dB above the film.
6. No 30 fps unless there is no other option.
7. The montage starts on a downbeat.
8. OKO story of the day: the sentence opening the question is whole in the
   first minute; the highlight is in the film; cards do not give it away. N/a
   without an intro.

**E. Music**
1. 3–4 tracks from one group, tempos close.
2. No overlap; a change on a picture cut, 0.7 s fade each side.
3. The change where the day turns.
4. Section aligned to a downbeat.
5. At most four accents outside the trailer and two breaths.

**F. Finish**
1. CC BY attribution written out and given to the user.
2. What you could not measure, said plainly (whether it sounds good is the
   user's judgment).
3. Publishing package from this render (`poglavja.txt` newer than the
   render). Fix: `W objava`.
4. Day in numbers before the end of the day (recap: one at the end).

## Deciding alone

Do not ask about every finding — assess, decide, fix, render; at the end say
what you decided.

- **Without asking**: any value (`gain_db`, `voice`, position, size, style,
  effect, `motion`, color, `master_db`, music level) and anything the user did
  not make (automatic subtitles, automatically picked trailer shots).
- **Only when a requirement demands it**, with a copy in `_vlog/zgodovina/` and
  an explanation: the user's own material (shot, photo, their caption, track).
- **Never**: new content (narration, music, shots), softened requirements.

| finding | decision |
|---|---|
| automatic subtitles with wrong words | remove |
| caption on a screen, face or text in the shot | move to a clean part (C5) |
| close speech pushed down | raise, `voice: true` (A5) |
| one vertical clip or screenshot among horizontal ones | leave |
| `preveri` time jump for a photo or screenshot | leave |
| noise under speech | `ocisti`, `gain_db` from the cleaned copy (A9) |
| `barve` jump or bad exposure | `color` suggestion after looking at both shots |
| text in an insert too small | `kartica` on `G1` over the insert (C8) |
| long talking in one picture | cutaway first (`prekrij`), punch-ins for the rest |
| missing J-cut / film look | `--popravi` / `film` |
| no day in numbers | `stevilke` on the last calm shot without speech |
| `--popravi` brightens dark interiors | restore the previous colors; B9/B10 stay a judgment |
| B10 keeps chasing brightness pair after pair | stop after one fix |
| true peak above −1 dBTP | `limit_db` −3 |

## Rounds and report

At most three rounds (assess, fix everything, render, assess). Before each, a
copy in `_vlog/zgodovina/`; a change the user made in the Studio is the
starting point. After the third, say which requirement stayed open, what you
tried and why it did not work.

**Report** (short): what was wrong, what you fixed, which decisions you made
yourself (especially removals and »not a mistake«), attribution, chapters
(`_izris/objava/poglavja.txt`), a thumbnail suggestion with a face, and what
you could not measure. No list of what was fine.
