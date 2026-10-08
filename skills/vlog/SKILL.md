---
name: vlog
description: Edit a travel vlog from raw clips in Wayfare Studio, up to a checked render at −14.5 LUFS with a publishing package — story of the day, music that fits, animated captions, place and time cards, a trailer of the best moments, cutaways over long talking, 3D route maps, and a full A–F review. Use when the user asks to make or edit a vlog, cut travel clips, edit a video from a folder of clips, drops video clips into the conversation, asks for a trailer or recap, or works on a Wayfare Studio project.
license: MIT
---

# Wayfare Studio — vlog editing

Everything happens **in Wayfare Studio**: the edit lives in
`<project>/edit.json` and every step goes through the tool — never
hand-written ffmpeg, never another editor. The user sees the same edit in the
Studio window and may change it there.

## Setup

The command-line tools are inside the Mac app:

- **`W`** below means `"/Applications/Wayfare Studio.app/Contents/Resources/bin/wayfare"`,
  **`WP`** means `".../Resources/bin/wayfare-python"` (Python with the
  `wayfare` package; run snippets as `WP - <<'EOF' … EOF`). Shell variables do
  not survive between your commands — write full paths.
- Not in `/Applications`? `mdfind "kMDItemCFBundleIdentifier == 'studio.wayfare.app'"`.
  Not installed? Tell the user to download it from the Wayfare Studio website.
- `W doctor` shows what is available. **prepis** (transcription) is not
  bundled — without it you know *where* speech is, not *what* is said.
  **blender** is needed only for 3D maps. Never install anything without the
  user's permission.
- **Never stop or restart the Studio.** A test Studio runs on a port above 8470
  with `--no-open --no-reload`; stop only that PID.

Commands are Slovenian (the tool was built in Slovenia):

| command | what it does |
|---|---|
| `scan <p>` | catalog clips: times, GPS, thumbnails, flags |
| `povzetek <p> [--zvoki] [--slika] [--edit\|--posnetki]` | clips with speech, the whole edit; `--slika` all clips on one image |
| `zvoki <clip> --strni Speech Music` | what is heard and when (detail) |
| `music <track>` | tempo, beats, downbeats, energy |
| `prekrij <p>` / `dih <p>` | cutaways over long talking / a moment without music |
| `napovednik <p> --pregled` | trailer (see `references/trailer.md`) |
| `pregled <p> [--pred] --popravi` | all requirements A–F, fixes, images to judge |
| `render <p>/edit.json` | render + loudness measurement |
| `preveri <p>` / `barve <p>` | edit and render checks / color per shot |
| `ocisti <clip> --primerjaj` | clean noise under speech and measure it |
| `objava <p>` | YouTube chapters and thumbnail candidates |
| `vstavek …` | 3D inserts (see `references/inserts.md`) |
| `glasba dodaj <url> --skupina <group>` | add a CC BY / CC0 track to the library |

## Working lean

Same quality, far fewer tokens:

1. **Read the catalog and the edit with `W povzetek <p>`** — the same fields in
   ~2,000 tokens instead of ~30,000. Never read `katalog.json` or `edit.json`
   whole; print a single field with one `WP` snippet. (An older app without
   `povzetek`: print only the fields you need with one snippet.)
2. **Speech for all clips in one command**: `W povzetek <p> --zvoki`, not a
   loop of `zvoki`. Use `zvoki` on one clip only for detail (laughter for the
   hook, a finer `--okno 1 --korak 0.5`).
3. **One `WP` snippet per round of changes**: load, change everything, save,
   print only what changed.
4. **Slow work in the background** (scan, render, inserts), output to a file.
   Do not sleep or poll; read `tail -5` of the log when it finishes.
   **Shorten every long output** (`2>&1 | tail -5`) — one ffmpeg error without
   it costs ~6,000 tokens.
5. **Read images only when they decide something** — `_vlog/posnetki.jpg`
   once at the start, contact sheets and the review's OKO images. Never read
   the same image twice; after a fix, check only the changed spots (a few
   render frames in one image).
6. **Read each reference at its step** (below), not up front.
7. **Do not repeat measurements `pregled` already makes** (checks, color,
   sound on the render, spectrum) — read its report.
8. Ask the user everything **in one message**. Do not narrate while working;
   report at the end.

## The fast path

What can be measured is measured by a command; what can run in parallel runs
in parallel.

1. **From the user's message take** the project name, any 3D animation or map,
   the character of the music, the highlight and complication of the day, and
   wishes. Ask for what is missing in one message. Always confirm the name.
2. **Project folder, clips, `W scan` in the background** (~5 s per clip), then
   `W povzetek <p> --zvoki --slika` and read `_vlog/posnetki.jpg` **once**
   (what is where: wide shots, places, the highlight).
3. **3D insert or map right away**, in the background → read
   `references/inserts.md`. It can take over an hour; the edit does not wait.
4. **Edit** by the sections below: story, picture, music, sound, captions.
5. **Cutaways, breath, day in numbers** — cutaways come before step 7, which
   cuts remaining long talking with punch-ins (118 %) in pauses.
6. **Trailer** → `references/trailer.md`. If the intro announces the day,
   picture cards → `references/intro-cards.md`. A recap of several days →
   `references/recap.md`.
7. **`W pregled <p> --pred --popravi`** before the first render: speech
   markers and level, noise cleaning, motion on still shots, J-cuts,
   punch-ins, film look; automatic subtitles out. Fix what stays **NI** (not
   met) with `references/review.md`.
8. **Render** in the background.
9. **`W pregled <p> --popravi`** on the render (~30 s, also makes the
   publishing package) → judge the **OKO** (eye) items with `review.md`. Fix
   everything at once, render, repeat — at most three rounds.
10. **Report** as in `review.md`.

Step 7 catches most problems before the slowest step, so one render and one
corrective render are usually enough.

## Starting a project

1. **Ask for the project name** — do not derive it from file names. It
   becomes the folder and the output file name.
2. **Folder**: the Studio's material folder (`~/Video` if it exists, else
   `~/Movies`; `WP -c "from wayfare import studio; print(studio.home_dir())"`),
   then `<material>/<name>/`. **Ask once whether to move or copy** the clips.
   Say from where to where; afterwards list what landed. Never overwrite a file
   with the same name — ask.
3. **`W scan "<p>"`, then `W povzetek "<p>" --zvoki`**: where someone talks,
   where there is only ambience and what it is (wind, water, traffic,
   laughter). That decides where a shot may be shorter and what carries it when
   nobody talks.
4. **Show it in the Studio**:
   `WP -c "from pathlib import Path; from wayfare import studio; studio.remember(Path('<p>'), '<name>')"`.
5. **Ask three things** — every time, unless the answer came with the clips;
   together with the name, in one message:
   - **a) 3D or map:** *Do you want a 3D animation or map — a route, a city
     walk, a departures board? What should it show, and where?* List the
     **moves of the day** from the catalog (»hotel → old town by tram«) and
     suggest short maps. 3D is the one thing that cannot be added without a
     new render.
   - **b) Music:** first say what the vlog feels like, then offer *bright and
     bouncy, calm, driving, or cinematic*; their own track goes into the
     project folder. Once they choose, tracks, sections and changes are yours.
   - **c) Highlight and complication:** *What was the highlight? Was anything
     uncertain — a flight, tickets, weather, a route?* This becomes the open
     loop.

   If the user says »up to you«, go straight to editing.

## Before you touch edit.json

1. **A copy** in `_vlog/zgodovina/edit-<time>-before-<what>.json`.
2. **Did the user change something?** Compare the latest files in
   `_vlog/zgodovina/`; if values differ from yours, the user's setting is the
   starting point — never overwrite it.
3. **Save through the project** (it refuses if the Studio saved in between):

   ```python
   from pathlib import Path
   from wayfare import spec, studio
   p = studio.Project(Path("<project>").expanduser()); s = p.load_edit()
   # ... all changes of this round ...
   p.save_edit(s, base_mtime=p.mtime())
   ```

## Story of the day

A viewer stays while there is an open question. A vlog is the day in time
order — you do not rebuild the story, you make sure the question opens and
closes (D8):

- **The user opens it**: a sentence from the intro that announces the day or
  the highlight stays whole in the first minute. Picture cards show the place,
  not the highlight; the trailer shows the highlight only for a moment.
- **The complication stays**, even if the shot is weaker.
- **The highlight** gets the longest shots of the day, then a wind-down.
- A sentence before the highlight saying what is coming (»now we're going in«)
  stays right before it.
- No narration; no caption promising what the user did not say.

## Picture

- **Shooting order**, no jumps back. Two moments of one clip: one shot or a
  dissolve between them, never another clip in between.
- **Lay shots with `spec.polozi(s, p.catalog, [("001", in, dur), {"clip": "020",
  "dur": 2.5, "motion": {...}}, …])`** — catalog fields, link and the shot's
  sound are added for you, length is limited to the clip. Never build the JSON
  by hand. Run `WP` snippets via `- <<'EOF'` (a script file elsewhere does
  not find the module).
- **Vertical material** (`2160x3840`) → vertical output `1080x1920`; title ~112,
  labels 52. Check `output` before rendering. Contact sheets with a fixed box
  lie about orientation — trust the catalog.
- **Trim only where nobody talks**, moderately. A cut never cuts speech.
- When you shorten a shot, re-lay the timeline and **move its sound by the same
  offset** (linked by `clip`). **Each shot has its own `link`**, shared only
  with its sound — split with `spec.split`/`split_times`.
- **»Drop 007«**: `spec.ripple_delete(s, spec.clip_index(s, {"start": …,
  "clip": "007"}))` — the gap closes on all tracks.
- **A new place starts wide** (square, arena), then medium and detail (B14).
- **J-cut at a change of place or time**: the new sound starts 0.5 s before its
  picture — `pregled --pred --popravi` makes them (B12).
- **Speed ramps on the way**: walking, driving, metro without speech, longer
  than 4 s (`zvoki`: Vehicle, Train, Walk; high `frame_diff`) — 1–3 per vlog,
  only where music carries the shot (a ramp mutes it):
  `spec.set_ramp(s, i, {"v": 2.5, "od": 1.0, "do": 3.0, "prehod": 0.3},
  studio.trajanja_posnetkov(p))`, start and end on a beat.
- **Cutaways over talking** (B11): talking to camera does not stay in one
  picture longer than 12 s. `W prekrij <p>` lists long talking, pauses and
  clips shot nearby, with `_vlog/prekrivke/pregled.jpg`. Over the part where
  the user talks about something, lay a clip of it: `--na <from>-<to> --z
  <clip>@<time>` — inside one shot, 3–6 s, edges in a pause. Keep the face at
  the start and end of the talk.
- **Still shots move**: `motion` (`zoom-in`, `zoom-out`, `left` …, `amount`
  ~0.12) on views, castles, panoramas, photos — not on shots that move.
- **Film look**: every vlog `"videz": {"ime": "film"}`, after per-shot color
  fixes, the same for all days of a trip. The user's choice in the Studio wins.
- **Color** after the first render is measured by `pregled` (`barve`,
  B9/B10); apply a `color` suggestion only after looking at both shots. Dark
  interiors are dark by nature.

## Music

- **The user picks the character**; you pick tracks, sections and changes.
- **Library**: `_glasba/` in the material folder with `knjiznica.json`. A new
  user's library is usually empty: use their tracks or `W glasba dodaj
  <free-stock-music.com link> --skupina <group>` (CC BY and CC0 only).
  **Every download needs the user's OK** — what, from where, how many MB.
- If the vlog earns money, only licenses that allow commercial use. CC BY
  always needs attribution in the description.
- **3–4 tracks** from the **same group**, tempos close; tempo rises through the
  day and settles at the end. More than one change per ~30 s is restless.
- **Local color**: for a country with a matching group, offer **one** local
  track under the arrival; the bed stays general.
- **Section by energy** (`music.detail()`), aligned to a **downbeat** — track
  starts are intros.
- **Level per track**: library tracks differ a lot in loudness (−7 to −17
  LUFS). `gain_db = −24 − napovednik.glasnost_odseka(path, in, length)`, not one
  gain for all.
- **Tracks never overlap**: a change is a cut on a picture cut with a 0.7 s
  fade each side; the film fades in 1.2 s and rings out 2.5 s. Change where the
  day turns.

## Sound

| what | starting point |
|---|---|
| music without / under speech | −14 dB / −25 dB |
| shot sound without speech | 8 dB below full |
| shot sound with speech | in front: raise `gain_db`, `voice: true` |
| TV or film inside the shot | −5 dB |
| master | **−14.5 LUFS**, true peak below −1 dBTP |

- **Measure speech** (`povzetek --zvoki`, `zvoki`); it stays in the shot's own
  sound — never cut it onto a separate track (that is for voice-overs).
- **Ducking**: `"duck": {"mode": "envelope", "depth_db": 11}` (new projects have
  it) lowers music under `voice: true`, edges on picture cuts. Never together
  with manually lowered pieces.
- **Where nobody talks it must not go silent** — music carries the shot.
- **Noise under speech** (`ŠUM` in `povzetek`, threshold 0.3): `"ocisti": true`
  on the shot-sound element; prove it with `W ocisti <clip> --primerjaj --od
  <in> --dolzina <dur>` (peak–floor gap grows, Speech above 0.9). RMS drops —
  compute `gain_db` from the cleaned copy. No noise, no cleaning.
- **Speech level**: median of `source RMS + gain_db` over all `voice: true`
  elements in this edit; a fixed shot gets `gain_db = median − its RMS`.
- **Master**: measure (`preveri`, render log); the Studio's master slider
  changes the render, so check `master_db` before rendering. If raising it no
  longer raises LUFS, the limiter is cutting — lower speech peaks instead.
- **Breath** (at most two): at a reveal the music steps back 18 dB for 2–4 s —
  `W dih <p>` suggests, `--na <s> --dolzina <s>` inserts. Where live music
  carries the sound, no library music there.
- **Sound accents** (at most four outside the trailer): a riser before the
  highlight, a hit on it — `spec.dodaj_poudarek(s, "dvig"|"udarec", <time>)`.

## Captions and graphics

- **Title with the date** at the start (`x 0.5`, `y 0.435` and `0.55`, sizes 132
  and 44), short labels bottom-left (`bottom-left`, 58, 3 s), in the user's
  language.
- Style: `din-cond`, `case: upper`, white, `border 0.06` `black@0.45`,
  `shadow 3`; entry and exit `slide-up`. One entry and one exit for the film.
- Never over a face or readable text in the shot. **Place names only when
  visible in the shot**, otherwise describe (»Castle above the valley«).
- **Place and time on glass** at each new place or part of the day (4–7 per
  vlog, 0.3–0.5 s after the cut to the first wide shot; `top-left` if a face is
  bottom-left; empty `value` = clock only). It replaces a place label and a
  separate clock; event labels never appear at the same time:
  `from wayfare import kraj; kraj.dodaj(s, p.catalog, <time>, "Plaza Mayor")`.
- **Day in numbers** before the end of each day, on a calm shot without speech,
  5 s (in a recap, one at the end):
  `s["graphics"].append({"kind": "stevilke", "start": <t>, "dur": 5.0,
  "value": "Day 3 in numbers", "ploscice": stevilke.izracunaj(s, p.catalog)})`.
- `G1` also carries `pas`, `kartica`, `naslov`, each with entry and exit
  (`left`, `right`, `up`, `down`, `grow`, `fade`) and `anim` ~0.45 s.
- **Motion**: nothing just fades; at most three easing curves; a small kit of
  elements; no shot on flat black (the first frames are the thumbnail); scene
  changes under motion. Times are absolute — moving a scene means
  recomputing the whole tail on every track.

## What I do not do

- No narration; no copying speech onto the voice track.
- No choosing the music's character alone.
- No downloads, installs or deletions without the user's OK. If a requirement
  removes the user's own material (shot, photo, their caption, track), keep a
  copy in `_vlog/zgodovina/` and explain it in the report.

## Done only after the review

The procedure, requirements A–F, what you decide alone and the report are in
`references/review.md` — read it at step 7. While any requirement is open, the
vlog is not done. The review runs on its own: assess, decide, fix, render; do
not ask about every finding. You recognize sound, measure loudness and see the
spectrum — whether it **sounds good** stays the user's judgment.

**Attribution and publishing**: the CC BY attribution (Studio → Music →
Attribution) and the chapters from `_izris/objava/poglavja.txt` go into the
report; suggest a thumbnail with a face and a reaction.
