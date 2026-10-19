# Trend: cut the vlog the way good travel vlogs are cut today

The Studio keeps a table of how current, successful travel vlogs are edited.
It is measured, not guessed: reference channels are sampled every week, each
new video that did better than the channel's average is watched by Gemini
(picture and sound, by its public YouTube link), and local meters measure the
user's own exports. The table holds medians and quartiles per style bucket:

| bucket | what it is |
|---|---|
| `hiter` | fast diary vlog: many cuts, talking to camera, text cards (the default) |
| `filmski` | cinematic travel film: long shots, voice-over or no speech, music |
| `pocasen` | slow or silent vlog: ambient sound, few cuts |
| `moji` | the user's own exported vlogs, measured locally |

Published rules of thumb (13–15 cuts per minute, median shot 4–5 s) come from
documentary channels, not travel vlogs; this table replaces them.

## When to read it

1. **Before you lay the story** (`W trend`): note
   the median shot length, cuts per minute by part (intro, middle, ending),
   when the first voice comes, when the hook lands, how long the trailer is,
   how much on-screen text there is. Use the bucket the user works in
   (`<studio>` block names it); the user's own exports (`moji`) say what they
   did last time — when the two differ, the user's own style wins unless the
   user asked to be "in step with the times".
2. **Critic step, before the first render** (`W trend --primerjaj <project>`): every measure outside the trend's
   quartiles is listed with the median and range. Fix what is a cut decision
   (shot lengths, a dead intro, too many punch-ins); leave what is the day
   itself (a long dinner, a quiet walk) and say so in the report.
3. **Review G1–G5** repeats the comparison as requirements: G1 tempo, G2
   intro, G3 on-screen text, G4 no overdoing (at most 4 punch-ins and 2
   whips or speed ramps per minute — editors' opinion, not a measurement),
   G5 length. None has a mechanical fix; they are your judgement, explained.

## How to use the numbers

- Medians are targets, quartiles are the room. A shot of 9 s is fine when the
  quartile goes to 8 s and the shot carries the climax.
- Intro: content on the first frame, no logo, a voice or a sound in the first
  second, the hook (highlight or open question) by the trend's `kavelj_s`.
- Pace falls through the video: intro fastest, ending slowest. Do not cut
  the ending like the intro.
- Text: location and time cards when the place changes, 3–4 s; constant
  captions only when the user's style has them.
- Lessons: `W trend --lekcije` lists short lessons Gemini wrote from the
  reference videos ("the hook shows the best shot of the day in the first
  five seconds"). Use them as ideas, not rules; never copy a reference
  video's content.

## What the measures mean

`kader_s` median shot length; `rezi_na_min[_uvod|_sredina|_konec]` cuts per
minute overall, in the first 30 s, in the middle, in the last 10 %;
`prvi_glas_s`, `kavelj_s`, `naslov_s` seconds until the first voice, the hook,
the title card; `napovednik_s` trailer length; `besedilo_delez` share of time
with text on screen; `napisov_na_min` titles and cards per minute;
`govor_v_kamero_delez`, `montaza_delez`, `glasba_delez` shares of talking head,
fast montage, music; `zoomov_na_min`, `whipov_na_min` punch-ins and
whips/ramps per minute; `konec_s` outro length; `trajanje_s` video length.
Local-only (own exports): `na_dobi_delez` cuts on the beat, `govor_delez`,
`lufs`, `mirnih_delez` still shots.

## Without a Gemini key

The table has only the `moji` bucket (the user's own exports) or nothing.
Say so once, edit by the review requirements and the user's style, and do
not ask the user to enter a key unless they ask how to turn the trend on
(menu ⋯ → Trend in the Studio, or `~/.wayfare/gemini.json`).
