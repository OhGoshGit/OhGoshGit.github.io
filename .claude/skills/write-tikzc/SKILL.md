---
name: write-tikzc
description: Use when the user asks for a conceptual diagram in a blog post drawn with TikZ/tikzc — "tikzcを用いて概念図を表現して", "この違いを図にして", "draw the difference between X and Y", "add a diagram to this post". Produces a `.tikz` source next to the post's `index.qmd`, compiles it to SVG only with `tikzc`, verifies it visually, and embeds it. Not for mermaid (see mermaid-palette) or for slide block diagrams (see tikz-block-diagram).
---

# write-tikzc

Conceptual diagrams in this blog are hand-written TikZ compiled to SVG by
`tikzc`. They explain *a distinction* — what two commands each look at,
which store holds which version, which commits a flag selects. They are
not decoration and not architecture diagrams.

One diagram per post, placed right after the section that introduces the
distinction it clarifies.

## Scope

| Ask | Skill |
|---|---|
| Conceptual diagram for a blog post | **this skill** |
| Sequence / flow that mermaid renders fine | `mermaid-palette` |
| 1600×900 slide block diagram (control systems, dataflow) | `tikz-block-diagram` |

`tikz-block-diagram` is a general slide skill and its defaults (PNG proofing,
16:9 aspect, Japanese labels) are wrong for this repo. When the target is a
post under `posts/`, this skill wins.

## Output rules (non-negotiable)

- **SVG only.** Compile with `--format svg`. Never `--format both` or `png`.
  Every committed diagram in `posts/` is a lone `.svg`; a stray `.png`
  doubles the repo weight for a file Quarto never serves.
- Both the `.tikz` source and the `.svg` are committed, side by side in
  the post directory. The source is the editable original — never ship an
  SVG whose `.tikz` is missing.
- Name the file after the **distinction**, not the post:
  `grep-head-vs-cached.tikz`, `pickaxe-vs-diff-regex.tikz`,
  `find-vs-lsfiles.tikz`, `key-id-anatomy.tikz`.
- Never overwrite an existing diagram with different content. New idea,
  new filename.

## Fonts

Put this header on the first line of every `.tikz`:

```latex
#| mainfont: Noto Sans CJK JP
```

`_quarto.yml` sets `mainfont: "Noto Sans JP"` for the site, but that name
is a **Google Fonts web build and is not installed locally**. `tikzc`
compiles through lualatex, which needs a real font file — passing
`Noto Sans JP` makes lualatex fall back to its serif default *silently*,
and the diagram ships in the wrong typeface. `Noto Sans CJK JP` is the
same typeface, installed system-wide, and matches the rendered page.

Verify before trusting any font name:

```bash
fc-list : family | tr ',' '\n' | grep -i "<name>" | sort -u
```

Older diagrams carry `#| mainfont: IPAGothic` or no header at all. Leave
them alone unless the user asks; don't bulk-rewrite.

## Compile and verify

```bash
cd posts/<YYYY-MM-DD-slug>
tikzc <name>.tikz --format svg
```

**Compiling is not finishing.** `tikzc` exits 0 on diagrams that are
visually broken. To check the result, render a throwaway PNG into the
scratchpad — outside the repo, so it never gets committed:

```bash
tikzc <name>.tikz --format png -o "$SCRATCHPAD/<name>.png"
```

Then `Read` that PNG and confirm:

- [ ] No text overflows its node; no label collides with a wire or box
- [ ] Arrow direction matches the real data flow — in Git diagrams,
      edits move working tree → index → HEAD, so `git add` and
      `git commit` arrows point **leftward** toward HEAD
- [ ] Color encodes the axis the reader cares about. Green = found/hit,
      red = absent/miss — never green for "row 1" and red for "row 2"
- [ ] Bold text is legible (serif fallback makes `\textbf` nearly
      invisible — a sign the font header failed)
- [ ] No `` `` `` quotes: they render CJK-width under a CJK font. Use
      `\textit{}` instead

Re-render and re-read after every fix.

## Shared style vocabulary

Existing diagrams converge on one palette. Reuse these; don't invent a new
scheme per post.

```latex
\begin{tikzpicture}[
    >={Latex[length=2.0mm]}, font=\footnotesize, line width=0.6pt,
    % a colored box: pass the color as an argument -> box=blue
    box/.style={draw=#1!55!black, fill=#1!12, rounded corners=3pt,
                align=center, minimum height=0.85cm, inner sep=4pt,
                font=\ttfamily\small, text=#1!30!black},
    % neutral content panel
    panel/.style={draw=black!35, fill=white, rounded corners=2pt,
                  align=left, inner sep=4pt, font=\ttfamily\scriptsize,
                  text=black!70},
    note/.style={font=\scriptsize, text=black!62, align=center},
    hit/.style={font=\scriptsize, text=green!25!black},
    miss/.style={font=\scriptsize, text=red!45!black},
  ]
```

Conventions worth keeping:

- Stroke `#1!55!black` over fill `#1!12` — dark outline, pale interior
- Explanatory prose is `black!62`; never pure black
- Connector arrows are `draw=black!45`, thinner than node strokes
- Color-code stores consistently: `gray` = HEAD/committed,
  `orange` = index/staged, `blue` = working tree
- Close with a `text width=12cm` takeaway note spelling out the point
  in a sentence — the figure should stand alone

## Layout

- Horizontal for pipelines (three Git stores left to right), vertical
  rows for per-case comparison (one row per flag, one column per commit)
- Keep it wider than tall; these render at 78–96% of a 1200px body column
- Reach for `\coordinate` + `(a |- b)` to lock rows and columns into
  alignment rather than eyeballing offsets
- See `tikz.dev` for TikZ syntax questions

## Embedding

```markdown
![](<name>.svg){fig-align="center" width="92%"}
```

Width is per-diagram: 78% for a compact two-column figure, 96% for a
dense three-column one. Pick what keeps the text readable at body size.
No caption — the surrounding prose introduces the figure, matching every
existing post.

## Anti-patterns

- Don't emit PNG into the repo
- Don't add a `\documentclass` — `tikzc` wraps the file in `standalone`
- Don't leave a `.tikz` uncompiled or an `.svg` sourceless
- Don't put Japanese in a post diagram; this blog's body text is English
- Don't restate the caption inside the figure *and* the prose — the
  in-figure note carries the mechanism, the prose carries the argument
- Don't compile with `--format both` out of habit
