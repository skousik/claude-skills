---
name: figure-making
description: House rules for making and revising figures in technical papers and documents (robotics, control, ML, applied math). Covers layout and composition (left-to-right panels, timestep panels plus a summary plot, equal panel heights, panel labels on one baseline, tight crops, direct labels at curve ends), size and fonts (final printed width, the paper's font family such as Times New Roman for IEEE, embedded fonts), figure captions, figures for key constructions, front figures, simulation renders and timelapses, photos and video frames under double-blind review, and provenance from scripts. Includes a matplotlib style helper (scripts/figstyle.py). Use this skill whenever you create, edit, restyle, or review any figure, plot, render, timelapse, diagram, or figure caption for a paper, proposal, report, or slide, even if the user only says "make a plot of this", "fix the whitespace", or "the labels look off". For the choice of chart form and color palette validation, also use the dataviz skill.
---

# Figure Making

These rules apply to every figure in a technical paper or document, whatever tool draws it (matplotlib, TikZ, a renderer, a photo).
The `technical-writing-style` skill covers the prose around figures; this skill covers the figure itself and its caption.
For the chart form and for validating a color palette, also follow the `dataviz` skill.

## Before making a figure

1. **Read the paper's format.** Find the document class, the column and text widths, the body and caption font family and size, and whether review is double-blind. IEEE two-column: column width about 3.5 in, text width about 7.16 in, Times body text, 8 pt captions.
2. **Find the claim.** Name the one point a reader should take from the figure, and the text that will cite it. A figure with no claim in the text is cut or moved to the appendix.
3. **Use a script.** Every figure comes from a script in the repository, which writes to a gitignored output folder. Leave a LaTeX comment next to `\includegraphics` naming the script and the commit, so numbers in the caption and text can be traced back.

## Layout and composition

**Panels.** A multi-panel figure reads entirely left to right, with no panel order the reader has to work out.
For a result that evolves over time, show at most three or four timestep panels, then put the plot of the measured quantity (e.g. ground truth vs. computed probability over time) as the rightmost panel, beside the visualization it summarizes, instead of in a separate figure or in place of yet another timestep.
Run only as many steps as the figure and the claim need.

**Whitespace.** Minimize it.
- Panels share axes and a legend where they can, and no panel is included just to fill a grid.
- Give side-by-side panels the same height and bottom edge. In matplotlib, place axes by size in inches (`figstyle.inches`) instead of relying on a grid with fixed-aspect panels, which leaves gaps around square images and equal-aspect plots.
- Size an image panel to the image's own aspect ratio at the shared panel height, and crop the image itself to its content.
- Crop margins tightly, especially at the top and bottom and above the caption (`bbox_inches="tight"` with a small pad, or explicit figure dimensions that fit the panels).

**Panel labels.** Put the labels ((a), (b), …) on one baseline, all aligned the same way (`figstyle.panel_titles`). Never let per-axes titles float at different heights.

**Labels on the data.** Label curves directly at their right-hand ends, or beside a marker, instead of with text floating in the middle of the plot. Use a legend only when direct labels would collide. Keep text in ink colors (black or dark grey), never in the series color.

**Annotations.** Use otherwise-empty space for annotations that help the reader (an equation relating the panels, such as $Z = Z_1 \oplus Z_2$, or an operator symbol between inputs and output).
Separate panels with thin light-grey rules where adjacent panels could be read as one.
Drop a plot whose curves coincide and carry no information; report it in a sentence or a table instead.

**Consistency.** Use one color per object across the whole paper (the same blue for the same set in every figure), and keep method figures in the same visual conventions (colors, symbols) as result figures.

## Size and fonts

**Final printed width.** Make each figure at its final printed width (a one-column figure at the column width, about 3.5 in. in IEEE two-column format; a two-column figure at the text width) and include it at that same width, so text in the figure appears at the same size as the caption.
Do not stretch a column-sized figure across the page or shrink a page-sized one into a column.
A figure that does not need two columns goes in a one-column `figure`.

**Font family.** Match the paper.
- For IEEE and other Times-based classes, use Times New Roman for text and STIX for math (`mathtext.fontset = "stix"`).
- For a paper in Computer Modern, use Computer Modern (`text.usetex` or the `cm` math font set).
- Never leave matplotlib's default DejaVu Sans in a paper figure.

**Sizes.** Use about 8 pt for labels and 7 pt for tick labels, so figure text matches the 8 pt caption.

**Embedding.** Embed TrueType fonts (`pdf.fonttype = 42`), since some publishers reject Type 3 fonts.

**Vectors.** Save PDF for plots and diagrams. Rasterize only dense parts (heatmaps, renders, photos) inside the PDF (`rasterized=True`), at 300 dpi or more.

`scripts/figstyle.py` sets all of this: `use_paper_style()`, `inches(fig, x, y, w, h)`, and `panel_titles(fig, axes, labels, y_in)`. Copy it next to the figure scripts.

## Captions

Figure captions are short. They say what is shown: the objects, the encoding by color, line style, or panel, and the one point to take away.
Definitions, derivations, limiting cases, and parameter values belong in the text that cites the figure.
The exception is the front figure, whose caption may be self-contained so it can be read before the paper.

Start with a noun phrase naming the figure ("Impulse cone at the hammer face for the current strike."), then give one sentence per panel ("(a) …", "(b) …"). Panel labels inside captions may take a colon.

## Figures for key constructions

Aim for a figure for every key construction or proof idea (a decomposition, a covering, a geometric bound, an operation on the paper's objects), placed beside the text that develops it.
Make them first and cut later if space requires.
This matters especially in theory papers, whose method sections otherwise have no figures.

## Front figures

In IEEE two-column format, the usual front figure is one column wide and sits at the top of the second column on page one, beside the abstract, not above it in the first column. `\suppressfloats[t]` before the figure at the start of the introduction achieves this.
A two-column teaser figure is also welcome when the content suits it. It goes between the title and authors and the text, above both the abstract and the introduction.

## Renders, timelapses, and photos

**Renders.**
- **Camera:** choose a view perpendicular to the main motion and frame the subject tightly. Try a few angles at low resolution and pick one by looking.
- **Occluders:** make tools and other occluders translucent so a construction drawn inside them (a cone, a set, an arrow) stays visible.
- **Overlays:** draw constructions with thick lines and arrows in the paper's colors, and check that lighting has not shifted those colors.

**Timelapses.** Ghost earlier poses with increasing opacity and draw the key pose (e.g. contact) opaque. Use three or four poses, and place the summary plot to the right, as in the timestep rule above.

**Photos and video frames.**
- **Double-blind review:** crop out faces, and blur logos, badges, name tags, lab signage, and anything else that identifies the authors or institution. Check every frame in the figure.
- **Disclosure:** say in the caption if a background was removed or edited.
- **Source:** use the original capture, not a re-encoded or slowed export.

## Final check

Render the figure at its printed size and look at it before handing it over. Check:
- panels have equal heights and labels sit on one baseline;
- no text collides or floats away from what it labels;
- margins are tight;
- the font matches the paper;
- colors are consistent with the other figures;
- double-blind anonymity holds;
- every number in the caption or the citing text matches the script's output.
