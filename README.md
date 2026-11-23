# Claude skills for technical papers

Two [Claude Code](https://claude.com/claude-code) skills for writing research papers in robotics, control, ML, and applied math.

| Skill | What it covers |
|---|---|
| [`technical-writing-style`](skills/technical-writing-style/SKILL.md) | Voice and structure for papers, proposals, and reports: a list of AI-sounding patterns to avoid, LaTeX source conventions, section architecture (introduction arc, contributions, related work, experiments, limitations), mathematical exposition, honest claims, and tone profiles for theory and systems papers. Includes `scripts/tone_check.py`, which measures a LaTeX draft against a profile. |
| [`figure-making`](skills/figure-making/SKILL.md) | Layout, size, fonts, captions, renders, and photos for paper figures. Includes `scripts/figstyle.py`, a small matplotlib style helper (Times text, STIX math, embedded fonts, panel placement in inches). |

Claude loads a skill automatically when a task matches its description, for example "clean up the intro" or "make a plot of this for the paper".

## Install

As a plugin, from inside Claude Code:

```
/plugin marketplace add skousik/claude-skills
/plugin install paper-writing@skousik-skills
```

Or copy (or symlink) the folders in `skills/` into `~/.claude/skills/` for personal use, or into a project's `.claude/skills/`.

## Using the tone checker

```bash
python3 skills/technical-writing-style/scripts/tone_check.py path/to/paper --profile theory
```

It needs only the Python standard library. Use `--profile systems` for empirical papers and `--section intro` (or `related`, `method`, `experiments`, `conclusion`) to check one section. Rates on fewer than about 1,500 words are noisy.

## Notes

- These are one lab's house rules, not universal ones. Where a project has its own style guide, the skills defer to it.
- `figure-making` points to a `dataviz` skill for chart-form and palette choices; it works without it.

## License

[MIT](LICENSE)
