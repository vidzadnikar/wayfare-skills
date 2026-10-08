# Recap of several days

One video from several days that are already edited.

- **Clips stay in the day folders**; move nothing. The recap project gets a
  catalog built from paths, in the background (~150 files take ~20 min):
  `scan.scan_files(paths, <project>/_vlog)`, `scan.merge`,
  `scan.write_catalog`, then `proxy.build_all` and `proxy.build_waves`. Shots
  carry `dir`.
- **Pick from the day films**, not raw material — shots, colors and cuts are
  already checked there. Speech shots keep `in` and `dur` (their cuts are in
  pauses, B6); shots without speech can be trimmed freely.
- **Copy the sound descriptions** from each day's `_vlog/zvoki/` under the new
  numbers (the key is the file path, so they stay valid).
- **One day, one track**, changing at the day boundary; where live music
  carries the sound, no library music.
- Each day starts with `Day N` + date, a sentence from that day's intro and its
  picture cards (`intro-cards.md`). One day-in-numbers card at the end.
- **Speech from different days differs in loudness**: measure LUFS of each
  speech shot on the render and bring outliers above 2 dB towards the median.
- **Limiter ceiling −2 dB** (or −3, see `review.md`) when there are sharp
  transients (applause).
