# Picture cards for the plan of the day

When the user says in the intro what the day will be (»old town, then
shopping, then the airport«), a **card with a picture of each thing** flies in
from the side as they mention it, one at a time; the user stays visible. No
name on the card (they say it), no sound effect. Make them after the trailer,
when film times are final.

1. **Word timings**: with `prepis` installed, transcribe the intro (times are
   in the clip, not on the timeline; you need meaning and time, not perfect
   words). Without it, ask the user at which second they mention each thing, or
   skip the cards.
2. **Things**: places and activities the user actually mentions, at most six.
3. **Picture**: the user's own photo of that day (`_vlog/slike/`), else a sharp,
   bright frame from their later clip of the same day, taken from the original
   clip, not the proxy: `wayfare.ffmpeg.grab_frame(Path(clip), second,
   Path(out), 1920, 1080, hdr=<catalog>, rotacija=<rotation>)` (vertical:
   1080, 1920). Skip what they did not film; never download pictures without
   their OK. For the highlight show **the place, not the highlight**.
4. **Card**: picture 684×509, white 8 px border, 24 px rounded corners, shadow;
   PNG 780×605 with alpha in `<project>/_vstavki/uvod/` (the Studio offers it
   under **+ Insert**). Make it with the bundled ffmpeg:

   ```bash
   F="/Applications/Wayfare Studio.app/Contents/Resources/app/vendor/ffmpeg/bin"
   G="[0:v]scale=684:509:force_original_aspect_ratio=increase,crop=684:509,pad=700:525:8:8:white,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='if(lte(hypot(max(0,abs(X-W/2+0.5)-(W/2-24)),max(0,abs(Y-H/2+0.5)-(H/2-24))),24),255,0)',pad=780:605:40:40:color=black@0,split[k][s];[s]colorchannelmixer=rr=0:gg=0:bb=0:aa=0.45,gblur=sigma=14[s2];[s2][k]overlay=0:-8:format=auto"
   mkdir -p "<project>/_vstavki/uvod"
   "$F/ffmpeg" -v error -y -i <picture.jpg> -frames:v 1 -filter_complex "$G" "<project>/_vstavki/uvod/<n>-<thing>.png"
   ```

   The crop is `cover` — check the main thing stays in the picture.
5. **On the `insert` track**, one element per thing:
   `{"file": "_vstavki/uvod/3-old-town.png", "start": …, "dur": 2.3,
   "position": "right", "effect": "slide-left", "exit": "slide-right",
   "anim": 0.35}`
   - `start` = intro shot start + (word time − shot `in`) − 0.2 s;
   - on screen until 0.2 s before the next thing, 1.2–2.5 s; **one at a time**
     — under 1.2 s apart, drop the less important one;
   - **opposite the face and any screen**; face right: `position: left`,
     `effect: slide-right`, `exit: slide-left`; vertical output: `x 0.5`,
     `y 0.74`, `scale 0.85`, `slide-up`/`slide-down`.
6. **Check every card on the render**: face and screen stay free, the picture
   matches the word.
