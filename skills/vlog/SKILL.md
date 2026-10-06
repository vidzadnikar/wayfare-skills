---
name: vlog
description: Edit a travel vlog from raw clips in Wayfare Studio — catalog by shot time, a story of the day with an open loop, music that fits the place, animated captions, a trailer of the best moments, cutaways over long talking, J-cuts, speed ramps, a moment without music, sound accents, a film look, a day-in-numbers card, a speech-first mix measured to −14.5 LUFS, and a publishing package. Use when the user asks to make or edit a vlog, cut their travel clips, edit a video from a folder of clips, drops video clips into the conversation, asks for a trailer or an intro of the best moments, or works on a Wayfare Studio project.
license: MIT
---

# Wayfare Studio — vlog editing

Everything happens **in Wayfare Studio**, not in hand-written ffmpeg commands
and not in another editor. Each project is a folder of clips; the edit lives in
`<project>/edit.json` and every step goes through it. The user sees the same
edit in the Studio window (a local web app in their browser) and can change
anything there; you change it through the commands below.

## Setup — do this first in every session

Wayfare Studio is a Mac app. Its command-line tools are inside the app bundle:

```bash
R="/Applications/Wayfare Studio.app/Contents/Resources"
"$R/bin/wayfare" doctor
```

- If the app is not in `/Applications`, find it:
  `mdfind "kMDItemCFBundleIdentifier == 'studio.wayfare.app'"` and use
  `<that path>/Contents/Resources`. If it is not installed, tell the user to
  download it from the Wayfare Studio website — do not try to build it.
- Shell variables do not survive between your commands. Start every command
  with the `R=...` line, or use the full path.
- `"$R/bin/wayfare" <command>` runs the tool. `"$R/bin/wayfare-python"` is
  Python with the `wayfare` package importable (for the snippets below). Both
  put the bundled `ffmpeg`/`ffprobe` on `PATH` for that command.
- `doctor` lists what is available. Two things are optional and often missing:
  - **prepis** (speech transcription) — not bundled. Without it you cannot
    read *what* is said; `zvoki` still tells you *where* speech is. Never
    install models or packages without the user's permission.
  - **blender** — needed only for 3D map inserts (`vstavek`).
- **Never stop, restart or kill the Studio.** The user may be working in it.
  If you need a second Studio for testing, run it on a port above 8470 with
  `--no-open --no-reload`, and stop only that process by its PID.

Command names are Slovenian (the tool was built in Slovenia). The ones you use:

| command | what it does |
|---|---|
| `scan <folder>` | catalog clips: times, GPS, thumbnails, flags |
| `zvoki <clip> --strni Speech Music` | what is heard and when (speech, music, wind, laughter, vehicles…) |
| `music <track>` | tempo, beats, downbeats, energy |
| `prekrij <project>` | cutaways over long talking: proposal + contact sheet |
| `dih <project>` | where the music should step back for a moment |
| `napovednik <project>` | trailer of the best moments at the start |
| `pregled <project> [--pred] --popravi` | all quality requirements at once (review) |
| `render <project>/edit.json` | render + loudness measurement |
| `preveri <project>` | checks the edit and the render: LUFS, sync, frames |
| `barve <project>` | brightness and white balance per shot, on the render |
| `ocisti <clip> --primerjaj` | removes noise under speech and measures the difference |
| `objava <project>` | YouTube chapters and thumbnail candidates |
| `izvozi <project> --oblike 1080p,vertical` | several output formats at once |
| `vstavek …` | 3D inserts from templates: route map, departures board, city walk |
| `glasba dodaj <url> --skupina <group>` | add a CC BY / CC0 track to the music library |
| `studio [folder]` | open the editor (normally the user starts it from the app) |

Where `<project>` appears, pass the project folder path.

## The fast path

The user drops clips and says what they want. From there to a checked vlog it
always goes in this order. What can run in parallel runs in parallel; what can
be measured is measured by a command, not by you.

1. **From the user's message take**: the project name, any 3D animation or
   map, the character of the music, the highlight and the complication of the
   day, special wishes. Ask for what is missing **in one message**, not one
   question at a time. Always confirm the name — it becomes the folder and the
   file name.
2. **Put the clips in the project folder** (see below) and run `scan` **in the
   background** right away (about 5 s per clip). Wait for answers meanwhile.
3. **Start a 3D insert immediately** if the user wants one (`vstavek …
   --pregled`, then the full render in the background). It can take over an
   hour; the edit does not wait for it.
4. **Edit**, section by section: Story of the day, Picture, Music, Sound,
   Captions, Trailer. `zvoki --strni Speech Music` tells you where speech is.
5. **Cutaways, breath, day in numbers**: `prekrij` (cover long talking), `dih`
   (at most two), `stevilke` before the end of the day. Cutaways come
   **before** step 6, which cuts whatever long talking remains with punch-ins.
6. **`pregled --pred --popravi`** before the first render. It sets speech
   markers, speech level, noise cleaning, motion on still shots, J-cuts at
   scene changes, punch-ins in long talking and the film look; it removes
   automatic subtitles. Whatever remains **NI** (not met), fix by hand using
   [review.md](references/review.md).
7. **Render** in the background.
8. **`pregled --popravi`** on the render (about 30 s); it also makes the
   publishing package. Then the **OKO** (eye) items: read the attached images
   with Read and judge them by `review.md`.
9. If anything was fixed: render again, repeat 8. At most three rounds.
10. **Report**: what was wrong, what you decided yourself, the music
    attribution and chapters for the video description
    (`_izris/objava/poglavja.txt`), thumbnail suggestion, and what you could
    not measure.

Why this order: rendering is the slowest step you repeat. Step 6 catches most
problems **before** it, so usually one render and one corrective render are
enough.

## Starting a project

1. **Ask for the project name.** Do not invent it or derive it from file
   names. The name is the folder name and the output file name.
2. **Project folder.** Projects live in the Studio's material folder:
   `~/Video` if it exists, otherwise `~/Movies` (check with
   `"$R/bin/wayfare-python" -c "from wayfare import studio; print(studio.home_dir())"`).
   Create `<material folder>/<name>/`. **Ask once whether to move or copy**
   the clips there. Moving avoids duplicates on disk; copying keeps the
   originals where they are. Before moving, say from where to where; after,
   list what landed in the folder. If a file with the same name already exists,
   do not overwrite it — ask.
3. **Catalog, then listen**:

   ```bash
   R="/Applications/Wayfare Studio.app/Contents/Resources"
   "$R/bin/wayfare" scan "<project>"
   for p in "<project>"/*.{MOV,mov,MP4,mp4}; do
     [ -e "$p" ] || continue; echo "== $p"; "$R/bin/wayfare" zvoki "$p" --strni Speech Music
   done
   ```

   The scanner skips its own folders (`_vlog`, `_vstavki`, `_izris`, `_glas`).
   Where someone talks, where there is only ambience and what it is (wind,
   water, animals, traffic, applause, laughter) decides where a shot may be
   shorter, where its own sound must stay in front, and what carries a shot
   when nobody talks. Without this those decisions are guesses from pictures.
4. **Show the project in the Studio** so the user can open it from the start
   page:

   ```bash
   "$R/bin/wayfare-python" -c "from pathlib import Path; from wayfare import studio; studio.remember(Path('<project>'), '<name>')"
   ```

5. **Ask three things** before editing — every time, unless the answer is
   already in the message the clips came with. Ask what is missing together
   with the name, in one message.

   **a) 3D animation or map.** *Do you want a 3D animation or map in this
   vlog — a route, a city walk, a departures board? If yes, what should it
   show and where?* A 3D insert is the one thing that cannot be added later
   without a new render, and it is made outside the edit (Blender). List the
   **moves of the day** you found in the catalog (»hotel → old town by tram«)
   and suggest short maps for them (see Animated graphics).

   **b) What music fits.** First look at the material yourself — catalog,
   thumbnails, times — and say what the vlog feels like. Then ask, and offer
   choices: *bright and bouncy, calm, driving, or cinematic for big views?* If
   the user has their own track, ask them to drop it into the project folder.
   The character of the music decides how the vlog reads, and you cannot guess
   it from pictures. Once they give the direction, choosing tracks, sections
   and changes within it is **your** job.

   **c) Highlight and complication.** *What was the highlight of the day? Was
   anything uncertain — a flight, tickets, weather, a route that went wrong?*
   This becomes the open loop (Story of the day).

   If the user says »up to you«, go straight to editing by the rules below.

## Before you touch edit.json

1. **Make a copy** in `_vlog/zgodovina/edit-<time>-before-<what>.json`.
2. **Check whether the user changed something meanwhile.** They may be
   dragging sliders in the Studio while listening. Compare the latest files in
   `_vlog/zgodovina/`; if values differ from yours, the user's setting is the
   reference — start from it, do not overwrite it.
3. Save through the project, never by writing the file directly:

   ```python
   from pathlib import Path
   from wayfare import spec, studio
   p = studio.Project(Path("<project>").expanduser()); s = p.load_edit()
   # ... change s ...
   p.save_edit(s, base_mtime=p.mtime())   # refuses if the Studio saved in between
   ```

   Run snippets with `"$R/bin/wayfare-python" - <<'EOF' … EOF`.

## Story of the day

A viewer stays because there is an open question (»will they make the
flight?«, »what is it like inside the arena?«) and leaves when there is none.
A vlog is a record of the day in time order, so you do not rebuild the story —
you make sure the question opens and closes.

- **The user opens the question.** A sentence from their intro that announces
  the day or the highlight (»tonight we're going to the bullfight«) stays
  whole and within the first minute. Picture cards for the plan of the day show
  **the place, not the highlight**; the trailer shows it only for a moment.
- **The complication stays.** What was uncertain (question c) is not cut out,
  even if the shot is weaker — it is the tension of the day.
- **The question closes.** The highlight is in the film and gets the longest
  shots of the day; after it comes the wind-down (evening, »good night«).
- **A new loop before the highlight.** When the user says on camera what is
  coming (»now we're going in«), that sentence stays right before it.
- Do not add narration, and do not write captions that promise something the
  user did not say. A label of what happens stays a label.

## Picture

- **Build shots from the catalog, not from memory.** Take `hdr`, `src_w`,
  `src_h` for each clip from `_vlog/katalog.json`.
- **A shot must not run past the end of its clip** (`in + dur ≤ duration`).
  `preveri` reports it as an error; fix it before rendering.
- **Check orientation.** Phones also shoot vertically; the catalog then shows
  `2160x3840`. If the clips are vertical, the output must be vertical
  (`1080x1920`), otherwise you get a narrow strip between black bars. A new
  project takes format and frame rate from most clips — still check `output`
  before rendering. For vertical output, scale caption sizes (title ~112
  instead of 132, labels 52 instead of 58).
- **Shots go in shooting order, start to end.** No jumps back in time; a
  viewer reads them as a mistake. Two moments from the same clip: merge them
  into one shot or put a dissolve between them — never insert a clip from
  another time.
- **Trim only where nobody talks**, or where speech ends early enough. A cut
  must not cut speech. Be moderate.
- **J-cut at scene changes.** Where place or time changes, the new scene's
  sound starts 0.5 s before its picture. `pregled --pred --popravi` makes them
  (B12); not where someone is talking at the end of the previous shot.
- When you shorten a shot, re-lay the timeline and **move its sound (and any
  narration above it) by the same offset** (they are linked by the `clip`
  field).
- To remove a shot (»drop 007«) do not delete by hand:
  `spec.ripple_delete(s, spec.clip_index(s, {"start": …, "clip": "007"}))`.
  The gap closes on all tracks, the music loses its end instead of its middle,
  speech stays aligned; `message` says what went with the shot.
- **A new place starts wide.** When the scene changes (new place or more than
  10 minutes later), the first shot shows where we are — square, arena,
  street; then medium and detail. If the first shot of a place is a detail,
  drop or shorten it and start with the first wide one (B14, `kraji.jpg`).
- **Speed ramps on the way.** Walking, driving, metro, escalators without
  speech, longer than 4 s, get variable speed — `ramp` with `v` 2–3,
  `prehod` 0.3, start and end on a music beat. Find candidates with `zvoki`
  (*Vehicle, Train, Walk, footsteps*) and high `frame_diff`. A ramp mutes the
  shot's own sound, so use it only where music carries the shot. One to three
  per vlog:

  ```python
  i = next(k for k, v in enumerate(s["video"]) if v["clip"] == "<id>")
  spec.set_ramp(s, i, {"v": 2.5, "od": 1.0, "do": 3.0, "prehod": 0.3},
                studio.trajanja_posnetkov(p))
  ```

- **Cutaways over talking.** Talking to camera does not stay in the same
  picture longer than 12 s (B11). `prekrij <project>` lists long talking,
  pauses and clips shot close in time, and makes `_vlog/prekrivke/pregled.jpg`.
  Over the part where the user talks about something, lay a clip of that
  thing: `--na <from>-<to> --z <clip>@<time>`. The segment lies inside one
  shot, 3–6 s, edges in a pause. What stays too long, `pregled --pred
  --popravi` cuts with punch-ins (118 %) in pauses. Keep the speaker's face at
  least at the start and end of the talk — the viewer must know who speaks.
- **Film look.** Every vlog gets `"videz": {"ime": "film"}` — soft S-curve,
  cool shadows, warm lights, vignette, a little grain, captions stay white. It
  comes **after** per-shot color fixes (`barve`), not instead of them. All
  days of one trip and their recap share the look. The user can switch it in
  the Studio (Film, Warm, Clean, None) — their choice wins.
- **Color after the first render.** `barve <project>` measures brightness and
  white balance of each shot on the render and reports where the same scene
  does not match or a daylight shot is too dark, with a `color` suggestion for
  each finding. Look at both shots before applying — the measurement cannot
  tell a sunny meadow from a blown-out sky. Dark interiors (opera, museum,
  dawn) are dark by nature, not a mistake.
- **Each shot has its own link** (`link`) shared only with its own sound —
  even two shots from the same clip. Split with `spec.split`/`split_times`.
- **Still shots move.** `motion` with `zoom-in`, `zoom-out`, `left`, `right`,
  `up`, `down` and `amount` ~0.12 brings views, castles, panoramas and photos
  to life; do not add it to shots that already move.
- **Contact sheets lie about orientation** if you scale thumbnails to a fixed
  box — check the ratio in the catalog, not by eye.

## Music

- **The user picks the character** (bright, calm, driving, cinematic); you
  pick tracks, sections and changes within it.
- **Library.** The Studio's music library is the folder `_glasba/` in the
  material folder, with `knjiznica.json` (groups, license, attribution). A new
  user's library is usually empty. Then: use the user's own tracks, or add
  tracks with `glasba dodaj <free-stock-music.com link> --skupina <group>`. It
  downloads the MP3 and records license and attribution, and accepts only
  **CC BY and CC0**. **Every download needs the user's OK first** — say what,
  from where, and how many MB.
- **Licenses.** If the vlog will earn money (ads, sponsors), only tracks whose
  license allows commercial use go in. CC BY needs attribution in the video
  description — always.
- **Three to four tracks** per video, all from the **same group**, tempos
  close together. Six tracks from different genres is a shock; the limit is the
  rhythm of changes (five tracks in two minutes is a change every 26 s and gets
  restless).
- **Local color.** For a vlog from a country with a matching group (French,
  Italian, Spanish, Japanese…), offer **one** local track under the arrival in
  the place; the bed stays from the general group. A whole vlog in local music
  feels like a theme park.
- **Pick the section by the energy curve**, not from the start of the track —
  starts are intros. Use `music.detail()`, find a window of the wanted length
  with the right average energy and align it to a **downbeat**.
- **Tracks do not overlap.** A change is a cut **on a picture cut**, with a
  **0.7 s** fade on each side. The film may fade in (1.2 s) and ring out
  (2.5 s). Two tracks at once sound like a mistake.
- Put the change where **the day turns** — from the top downhill, towards
  home. Let tempo rise through the day and settle at the end.

## Sound

Starting points, measured — not dogma:

| what | level |
|---|---|
| music where nobody talks | `−14 dB` |
| music under speech | `−25 dB` |
| shot sound where nobody talks | 8 dB below full |
| shot sound with speech | stays in front: raise the shot's `gain_db`, `voice: true` |
| TV or film inside the shot | −5 dB |
| master | **−14.5 LUFS**, true peak below −1 dBTP |

- **Measure where speech is.** `zvoki <clip> --strni Speech Music` gives speech
  and music segments in seconds (window 3 s, step 1.5 s; lower `--okno` and
  `--korak` for finer edges). Set `voice: true` and ducking from them. Where no
  `Speech` segment is found, music carries the shot.
- **Clean noise under speech.** If `zvoki` finds wind, traffic, an engine, rain
  or hum under speech (`zvoki.sum_pod_govorom`, threshold 0.3), give the
  element on the shot-sound track `"ocisti": true` — the render takes a
  cleaned copy, noise drops ~12 dB, ambience stays. Measure with
  `ocisti <clip> --primerjaj --od <in> --dolzina <dur>`: the peak–floor gap
  must grow, `Speech` stay above 0.9, noise fall below threshold. **RMS
  drops** — compute that shot's `gain_db` from the cleaned copy's RMS. Do not
  clean where there is no noise.
- **Speech stays in the shot's own sound.** Raise the shot's `gain_db`, set
  `voice: true`, lower the music. Do not cut speech out onto a separate track
  (that track is for the user's voice-overs).
- **Where someone talks, the music steps back**, and the level change sits on
  a picture cut.
- **Automatic ducking**: `"duck": {"mode": "envelope", "depth_db": 11}` lowers
  music under `voice: true` by a steady 11 dB and pins the edge to the picture
  cut. New projects have it. Never combine it with manually lowered music
  pieces (double ducking; `preveri` warns).
- **Where nobody talks, it must not go silent.** Lowering both music and shot
  sound makes the shot silent; there, music carries the shot.
- **Always measure the master** with `preveri` (and the render log): LUFS, true
  peak and how much to change `master_db`. The Studio's master slider changes
  the render — check `master_db` before rendering. If raising `master_db` no
  longer raises LUFS, the limiter is cutting: lower the peaks (`gain_db` of
  speech shots) instead.
- **Speech level for a fixed shot**: compute `source RMS + gain_db` for all
  elements that already have `voice: true` in **this** edit and use the median.
  For a cleaned shot use the cleaned copy's RMS.
- **Breath — a moment without music.** At a reveal — the arena opens, a view,
  bells, live music — the music steps back 18 dB for 2–4 s and the place is
  heard. `dih <project>` suggests shots without speech whose sound carries the
  scene; `--na <s> --dolzina <s>` inserts it. **At most two per vlog.** Where
  live music carries the sound throughout, there is no library music there and
  no breath needed.
- **Sound accents.** A riser (peak at its end) before the highlight and a hit
  (peak at its start) on it, on the Effects track:
  `spec.dodaj_poudarek(s, "dvig", <time>)` and `"udarec"`. The trailer places
  its own. Elsewhere **at most four per vlog**, only on highlights.

## Captions

- **A title with the date at the start**, short labels of what happens along
  the way. Write captions in the user's language.
- The style must **not be the most ordinary**: `din-cond`, `case: upper`,
  white, `border 0.06` `black@0.45`, `shadow 3`.
- Title centered (`x 0.5`, `y 0.435` and `0.55`, sizes 132 and 44); labels
  bottom-left (`bottom-left`, size 58, 3 s).
- **Entry and exit animate**: `effect: slide-up`, `exit: slide-up`.
- A caption must not cover what is already readable in the shot (a screen, a
  face).
- **Place names only when you can see the place in the shot.** Otherwise
  describe (»Castle above the valley«).
- **Place and time on glass.** At the start of each part of the day — arrival
  somewhere new, morning, lunch, evening — add a `kraj` element on track `G1`:
  two glass tiles bottom-left, a pin with the place name and a dial with the
  shooting time. It **replaces** a separate place label and a separate clock.
  Add it with the tool, which takes the time from the catalog:

  ```python
  from wayfare import kraj
  kraj.dodaj(s, p.catalog, <time>, "Plaza Mayor")   # 4 s, bottom-left
  ```

  About 4–7 per vlog, 0.3–0.5 s after the cut to the first (wide) shot of the
  new place; `position: "top-left"` if a face is bottom-left; empty `value`
  keeps only the clock. Event labels (»First churros«) stay ordinary captions
  and never appear at the same time as `kraj`.

## Motion rules

- **Nothing just fades.** Captions and graphics slam, slide, tear or click into
  place. (Cuts between shots keep their dissolves.)
- **One accent for the whole film.** All motion runs on at most three easing
  curves — keep one `effect` for entry and one for exit through the vlog.
- **A small kit, composed forward**: title, label, place+time, number, insert.
  A new effect for every scene means the kit is not chosen yet.
- **No shot stands on flat black.** The first frames are the YouTube
  thumbnail; if it must be dark, give it texture.
- **Scene changes happen under motion**, not in emptiness.
- **Times derive from scene offsets.** `edit.json` stores absolute `start`
  times, so moving one scene means shifting every later element on every track
  — recompute the whole tail, then check captions and sound still match.

## Animated graphics

**Every travel animation is made in the tool.** When the user asks for a route
animation, »a map from X to Y«, a departures board or a city walk, the answer
is `vstavek` — not a hand-built HTML/Remotion composition.

```bash
R="/Applications/Wayfare Studio.app/Contents/Resources"
"$R/bin/wayfare" vstavek seznam                         # templates
"$R/bin/wayfare" vstavek primer pot > "<work>/pot.json" # example; edit it
"$R/bin/wayfare" vstavek pot "<work>/pot.json" -p "<project>" --pregled
"$R/bin/wayfare" vstavek pot "<work>/pot.json" -p "<project>" --na 12.5
```

1. Requires **Blender** (`doctor` shows it). Without Blender, say so and offer
   the edit without the insert.
2. **Look up** coordinates of places, airports and stops — never guess.
3. Always `--pregled` first and read `pregled.jpg` with Read — a full render
   takes 10–90 minutes.
4. If the command reports `manjkajo podatki` (missing map data), **ask the
   user's permission** — what, from where, how many MB (the command prints
   it) — and only then `--prenesi`.
5. Run the full render in the background; `--na <s>` writes it into
   `edit.json` through the editor's save. Put the attribution it prints into
   the video description.
6. **City walk from clips**: `vstavek posnetki -p <project> --dan YYYY-MM-DD`
   prints `mesto` parameters with stops from the clips' GPS and name
   suggestions from OSM. Check names against the thumbnails.
7. **Trains run on real tracks**: a stage `{"vozilo": "vlak", "postaje": [...],
   "do": ...}` follows OpenStreetMap rails through the stations where the
   train stopped.
8. **A route fills the whole frame from the first to the last frame** — never
   the edge of the model, black around it, or a fade to black. If the command
   prints `OPOZORILO … rob makete`, the insert is not good even if it rendered.
   Check the first, last and widest frames.
9. **Every route has places and landmarks** (`kraji`): names of larger towns
   along the way (one per 40–100 km), porcelain landmark figures at start,
   transfer and destination (`grad`, `svetilnik`, `zvonik`, `arena`,
   `katedrala`; `vstavek kipi -o <folder>` shows them). Landmarks without a
   town (cave, lake, mountain) get `ime` and `pod`; lakes and mountains
   `"pika": false`.
10. An interrupted render continues with `--nadaljuj` and the same `--ime`.
11. A full-frame route goes **on the picture track between shots**
    (`spec.vstavek_na_sliko`), not over clips. Transparent inserts (board,
    walk, relief) go over clips.
12. **Text in an insert must be readable on a phone**: the smallest letters at
    least 2 % of the frame height (22 px at 1080p). If it is too small, put the
    text as a `kartica` on `G1` over the insert instead of re-rendering.

**Map at a move.** When the day moves to another part of town or another place
— metro, car, train, plane — a short from–to map goes between the last shot of
the old place and the first of the new: inside a city `vstavek mesto` with two
stops, 4–6 s, `nadnaslov` by transport (»METRO«, »TAXI«); between cities
`vstavek pot`. At most three per vlog; a short walk gets none.

Track `G1` also carries `pas` (place name in a corner), `kartica` (title +
time in the accent color) and `naslov` (big centered letters), each with an
entry and exit (`left`, `right`, `up`, `down`, `grow`, `fade`) and `anim`
(0.45 s is a good start).

**Day in numbers.** Before the end of each day, on a calm shot without speech,
a `stevilke` card on `G1` for 5 s: clips, hours on the way, kilometers (if the
clips have GPS), minutes filmed. The tool computes the numbers:

```python
from wayfare import stevilke
s["graphics"].append({"kind": "stevilke", "start": <time>, "dur": 5.0,
                      "value": "Day 3 in numbers",
                      "ploscice": stevilke.izracunaj(s, p.catalog)})
```

## Trailer

A vlog opens with a **trailer**: 10–15 s of the best moments, then the title.
Make it when the edit is done (shots, music, captions) and before rendering.

**Structure:** 1. **Hook** — a moment with its own sound: a reaction, a laugh,
a sentence; with speech, **the whole sentence**, never half. 2. **Jump** — the
montage starts on a downbeat where the track lifts. 3. **Montage** — shots
across the whole day in time order, short transitions, calm shots 3 beats,
moving ones 2. 4. **Last shot** — mood or highlight, the longest. 5. **Flash**
into the film's title.

**Music:** one track without cuts, **dramatic or energetic, from the library,
not from the film** (`--glasba dramaticno | energicno | <path>`); the command
sets it 3 dB above the film's music. Swooshes, a riser into the flash and a hit
on the title are added automatically (`--zvoki brez` turns them off).

**The automatic pick is only a draft:**

```bash
"$R/bin/wayfare" napovednik "<project>" --pregled
```

Read `_vlog/napovednik/pregled.jpg`: the first row are hooks, then one row per
part of the film — the first frame is the automatic pick, then candidates
labeled `clip@time`. Choose:

- **Hook:** a face with a reaction, a laugh, someone showing or saying
  something. Find candidates by sound: `zvoki <clip> --strni Laughter Speech
  Applause Cheering`. You cannot know *what* is said — if the hook is speech,
  ask the user which sentence is good, or ask them to mark it in the Studio.
- **People and action before objects**; **every place of the day once**;
  **sharp, bright, 60 fps** (30 fps material stutters in a fast trailer);
  consecutive shots differ in framing or color; **the last shot is mood**.

Then insert:

```bash
"$R/bin/wayfare" napovednik "<project>" --glasba dramaticno \
  --kavelj 005@4.2-6.4 --trenutki 002@4.0,006@7.7,008@8.7:3,009@1.6,011@1.1
```

`--kavelj 005@4.8` searches for a sentence around that moment; `005@4.2-6.4`
takes exactly that span; `:3` sets a shot's beats. Also `--ritem tekoce |
pospesi | mirno`, `--prehodi zivahni | mehki | brez`, `--konec bliskavica |
crnina`, `--dolzina` (12 s). Running it again replaces the old one;
`--odstrani` removes it. After inserting, render the trailer and a few seconds
of the film and check frames every quarter second, no duplicated frames in
motion, hook and montage within 2 dB, montage 3–4 dB above the film. Captions,
inserts and music shift automatically; tell the user the film moved if they
are editing in the Studio.

## Picture cards for the plan of the day

When the user says in the intro what the day will be (»old town, then
shopping, then the airport«), a **card with a picture of each thing** flies in
from the side as they mention it, one at a time. The user stays visible; no
name on the card (they say it), no sound effect.

This needs word timings. If `prepis` (transcription) is installed, use it;
otherwise ask the user at which second of the intro they mention each thing,
or skip the cards.

1. Pick only things the user actually mentions, at most six.
2. Picture: the user's own photo of that day (`_vlog/slike/`), else a sharp
   frame from their later clip of the same day:
   `wayfare.ffmpeg.grab_frame(Path(clip), second, Path(out), 1920, 1080,
   hdr=<from catalog>, rotacija=<rotation>)`. Show **the place, not the
   highlight**. Never download pictures without the user's OK.
3. Card: picture 684×509, white 8 px border, 24 px rounded corners, shadow;
   PNG 780×605 with alpha, saved in `<project>/_vstavki/uvod/` so the Studio
   offers it under **+ Insert**.
4. Insert on the `insert` track:
   `{"file": "_vstavki/uvod/3-old-town.png", "start": …, "dur": 2.3,
   "position": "right", "effect": "slide-left", "exit": "slide-right",
   "anim": 0.35}` — start 0.2 s before the word; 1.2–2.5 s on screen; only one
   at a time; opposite the face (face right: `position: left`, `effect:
   slide-right`, `exit: slide-left`); vertical output: `x 0.5`, `y 0.74`,
   `scale 0.85`, `slide-up`/`slide-down`.
5. Check every card on the render — face and screen stay free, the picture
   matches the word.

## Recap of several days

- **Clips stay in the day folders.** The recap project gets a catalog built
  from paths (`scan.scan_files(paths, <project>/_vlog)`, `scan.merge`,
  `scan.write_catalog`, then `proxy.build_all` and `proxy.build_waves`); shots
  carry `dir`. Run it in the background. Move nothing.
- **Pick from the day films**, not raw material — shots there are already
  chosen, colors fixed, cuts checked. Speech shots keep `in` and `dur` from the
  day film.
- **One day, one track**, changing at the day boundary. Where live music
  carries the sound, no library music.
- Each day starts with `Day N` + date, a sentence from that day's intro and
  its picture cards.
- **Speech from different days differs in loudness** — measure LUFS of each
  speech shot on the render and bring outliers above 2 dB towards the median.
- **Limiter ceiling −2.0 dB** when there are sharp transients (applause).

## What I do not do

- **No narration.** The voice-over track is the user's.
- **No copying speech onto the voice track** — raise the shot, lower the music.
- **No choosing the music's character alone** — ask, then choose within it.
- **No downloads, installs or deletions without the user's OK** — music, map
  data, models, pictures. When a requirement makes you remove the user's own
  material (a shot, photo, their caption, their track), keep a copy in
  `_vlog/zgodovina/` and explain it in the report.

## Check before saying it is done

The edit does not end with the render but with the review. The procedure and
the **list of all requirements** are in [references/review.md](references/review.md)
— read it when the render exists and complete it. While any requirement is
open, the vlog is not done and you do not call it done.

The review runs on its own: assess, decide, fix, render again, and report at
the end what you decided — do not ask about every finding. What you may fix
yourself and what only when a requirement demands it is in `review.md`.

Say plainly what you could not check. You **recognize** the kind of sound
(`zvoki`), **measure** loudness (`preveri`), **see** the spectrum. You cannot
say whether it **sounds good** — whether the track fits, the voice is pleasant
or the mix is pleasing. That stays the user's judgment; present it that way.

## Attribution and publishing package

Library tracks under CC BY **require attribution**. The **Attribution** button
in the Studio's Music window lists the tracks used and copies them; tell the
user to put them in the video description.

`objava <project>` makes YouTube chapters and six thumbnail candidates in
`_izris/objava/`. Paste the chapters into the report under the attribution;
read the thumbnails with Read and suggest one — with a face and a reaction,
not an empty landscape.
