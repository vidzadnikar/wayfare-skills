# 3D inserts and maps

Read when the user wants a 3D animation, a route map or a map at a move, a
departures board or a city walk. `W` is the `wayfare` command (SKILL.md,
Setup). Needs **Blender** (`W doctor`); without it, say so and offer the edit
without the insert.

**Every travel animation is made with `W vstavek`**, never as a hand-built
HTML/Remotion composition: real roads (OSRM), a 3D model with a tilted camera,
the plane's shadow. A clock running through the day can be added as a caption
on `G1` over the insert.

## Procedure

```bash
W vstavek seznam                                   # templates
W vstavek primer pot > "<work>/pot.json"           # example; edit it
W vstavek pot "<work>/pot.json" -p "<project>" --pregled
W vstavek pot "<work>/pot.json" -p "<project>" --na 12.5
```

1. **Look up** coordinates of places, airports, stations and landmarks (OSM,
   Wikipedia) — never guess.
2. Always `--pregled` first and read `pregled.jpg`. Full render: board ~10
   min, city ~15, a 16 s route with landmarks ~85.
3. `manjkajo podatki` (missing map data) → **ask permission** (what, from
   where, how many MB — the command prints it), then `--prenesi`.
4. Full render in the background; `--na <s>` writes it into the edit through
   the editor's save. The attribution it prints goes into the description.
   Judge quality on the render, not the Studio preview.
5. Interrupted: `--nadaljuj` with the same `--ime`; after changing parameters
   or code, start again without it.
6. City walk from clips: `W vstavek posnetki -p <project> --dan YYYY-MM-DD`
   prints `mesto` parameters from the clips' GPS with OSM names — check the
   names on the thumbnails. Clips without GPS give nothing.

## Route

- **Fills the whole frame from the first to the last frame** — no model edge,
  no black, no fade. `OPOZORILO … rob makete` means the insert is not good
  even if it rendered. Check first, last and widest frames. Never hide it with
  `scale` or cropping.
- **On the picture track between shots** (`spec.vstavek_na_sliko`), not over
  clips.
- **Trains on real tracks**: a stage `{"vozilo": "vlak", "postaje": [...],
  "do": ...}` (also `[avto, vlak]`); stations from OSM `railway=station` — ask
  which train the user took. A vehicle that jitters is a tool bug, not a
  parameter problem.
- **Places and landmarks on every route** (`kraji`):
  - start, transfer, destination: only `kip` (they already have labels);
  - larger towns and train stops: `ime`, at most one per 40–100 km; a famous
    landmark adds `kip` and `pod` (VENICE / ST MARK'S BELL TOWER);
  - landmarks without a town (cave, lake, mountain): `ime` and `pod`; lakes and
    mountains `"pika": false`;
  - figures: `grad`, `svetilnik`, `zvonik`, `arena`, `katedrala`
    (`W vstavek kipi -o <folder>`); never download figures;
  - in `--pregled`: each figure by its town, labels do not overlap, the last
    frame shows the whole route. `OPOZORILO kip … nima prostega mesta` → move
    or drop it.
- **Output**: a route is HEVC 10-bit `.mp4`, BT.709, no alpha, 24 samples. Do
  not switch it to ProRes or raise samples without measuring. Transparent
  inserts (board, walk, relief) stay ProRes 4444 with alpha and go over clips.

## Map at a move

When the day moves by metro, car, train or plane, a short from–to map goes
between the last shot of the old place and the first of the new, on the
picture track: inside a city `vstavek mesto` with two stops, `trajanje` 4–6 s,
`nadnaslov` by transport (»METRO«, »TAXI«); between cities `vstavek pot`. A
short walk gets none; at most three per vlog. Suggest them in question a and
start them right after the user agrees.

## Readability

The smallest letters in an insert must be at least **2 % of the frame height**
(22 px at 1080p). If they are smaller, put the text as a `kartica` on `G1` over
the insert instead of re-rendering; a bigger `scale` helps only until it
covers the shot.
