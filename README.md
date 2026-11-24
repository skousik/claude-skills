# Claude skills for technical papers

Three [Claude Code](https://claude.com/claude-code) skills for writing and proofreading research papers in robotics, control, ML, and applied math.

| Skill | What it covers |
|---|---|
| [`technical-writing-style`](skills/technical-writing-style/SKILL.md) | Voice and structure for papers, proposals, and reports: a list of AI-sounding patterns to avoid, LaTeX source conventions, section architecture (introduction arc, contributions, related work, experiments, limitations), mathematical exposition, honest claims, and tone profiles for theory and systems papers. Includes `scripts/tone_check.py`, which measures a LaTeX draft against a profile. |
| [`proofreading`](skills/proofreading/SKILL.md) | A line-level audit of a LaTeX draft in seven checks (paper structure, math notation, statistical reporting, figures and tables, grammar, abbreviations, and house style), as a prioritized report or an interactive fix-it session. It defers to `technical-writing-style` for prose and structure rules and runs that skill's checklist as its seventh check. Includes scripts that render the report as a PDF and extract reviewer annotations from a PDF. |
| [`figure-making`](skills/figure-making/SKILL.md) | Layout, size, fonts, captions, renders, and photos for paper figures. Includes `scripts/figstyle.py`, a small matplotlib style helper (Times text, STIX math, embedded fonts, panel placement in inches). |

Claude loads a skill automatically when a task matches its description, for example "clean up the intro" or "make a plot of this for the paper". Run the proofreader with `/proofread path/to/paper` (add `--interactive` to fix issues one at a time).

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
- `proofreading` needs `pandoc`, a LaTeX engine, and `pymupdf` (see its `requirements.txt`) only for the PDF report and annotation extraction.
- `figure-making` points to a `dataviz` skill for chart-form and palette choices; it works without it.

## Credits

[Sundhar Vinodh-Sangeetha](https://github.com/sundharvs) wrote the early draft of the `technical-writing-style` skill.

The `proofreading` skill is adapted from [Jakob Thumm](https://jakob-thumm.com)'s [proofreading skill](https://github.com/JakobThumm/proofreading), which compiles the feedback he received on his Ph.D. paper drafts, and is used under its MIT license (kept in [`skills/proofreading/LICENSE`](skills/proofreading/LICENSE)). The changes here resolve its conflicts with `technical-writing-style` and add the house-style check.

## License

[MIT](LICENSE)
