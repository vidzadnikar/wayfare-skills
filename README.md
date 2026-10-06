# Wayfare skills for Claude

Skills that let [Claude](https://claude.com/claude-code) edit travel vlogs in
**Wayfare Studio**, the vlog editor for Mac.

| skill | what it does |
|---|---|
| [`vlog`](skills/vlog/SKILL.md) | Turns raw travel clips into a finished, publish-ready vlog: shooting-order edit with a story of the day, music that fits the place, animated captions, a trailer of the best moments, cutaways, J-cuts, speed ramps, a speech-first mix at −14.5 LUFS, and a full quality review before it calls anything done. |

## Requirements

- A Mac with Apple silicon (M1 or newer), macOS 12 or later
- Wayfare Studio installed in `/Applications` (download it from the Wayfare Studio website)
- [Claude Code](https://claude.com/claude-code)

## Install

**With the skills CLI** (needs Node.js):

```bash
npx skills add wayfare-studio/skills --skill vlog -g -a claude-code
```

**As a Claude Code plugin** (no Node.js needed), inside Claude Code:

```
/plugin marketplace add wayfare-studio/skills
/plugin install wayfare@wayfare
```

**By hand:** copy `skills/vlog` to `~/.claude/skills/vlog`.

## Use

Open Wayfare Studio, then in Claude Code:

> Make a vlog from my Lisbon clips in ~/Movies/Lisbon.

Claude asks for the project name and a few things it cannot see in the
footage — the music you want, the highlight of the day — and then edits,
renders and reviews the vlog. You can change anything in the Studio window
while it works.

## License

[MIT](LICENSE)
