---
name: write-blog-post
description: Use when the user asks to draft, rewrite, polish, or "align with the blog tone" a Quarto post under `posts/YYYY-MM-DD-slug/index.qmd`. Enforces the OhGoshGit voice (OGG-titled, problem→TL;DR→Goal→explanation→solution), frontmatter conventions, and structural callouts/mermaid usage seen across existing posts. Triggers on phrases like "blog全体のトーンと整合的な形でまとめて", "write a new post about X", "polish this draft", "summarize consistently with the rest of the blog".
---

# write-blog-post

This is a single-author Git-tips blog (`OhGoshGit!?!`) published with Quarto.
Every post under `posts/<DATE>-<slug>/index.qmd` follows a recognisable
voice and structure. When the user asks you to write a new post or
"align with the blog tone", reproduce that voice exactly — do **not**
invent new section names, emoji, or callout styles.

## Voice rules (non-negotiable)

- **Title starts with `OGG... `** and is phrased as a question the
  reader Googled in frustration. Examples actually in the repo:
  - `OGG... What's the difference between git diff, git diff --cached, and git diff HEAD?`
  - `OGG... How do I git add only files matching a pattern?`
  - `OGG... Why does poetry add fail through a SOCKS5h proxy when git clone works?`
- Second person, present tense, terse. No hedging ("it might be the case that...").
  No marketing language. No "let's dive in".
- English-only in the body. Code blocks and command output are verbatim.
- One concrete problem per post. No "everything you need to know about X" posts.

## Frontmatter template (copy verbatim, fill in)

```yaml
---
title: "OGG... <question phrased as the reader would Google it>"
author:
   - name: "Ryo Nakagami"
     url: https://github.com/RyoNakagami
date: "YYYY-MM-DD"
date-modified: "YYYY-MM-DD"
categories: [<lowercase, space-allowed, comma-separated>]
---
```

- `date` is the original publish date. `date-modified` is updated on
  every non-trivial edit — the RSS-to-social workflow keys off it
  (see [[rss-social-debug]]).
- `categories` use lowercase, can contain spaces (`git diff`, `git add`),
  and stay short (1–4 tags).

## Standard section order

Not every post uses every section, but they appear in this order when
they do appear. Pick the subset that fits.

1. **`::: {.callout-note}` TL;DR** — one paragraph or one code block.
   The reader who only reads this should walk away with the fix.
2. **`## 🎯 Goal`** — a markdown checklist of what the reader will be
   able to do by the end. 1–4 bullets, each starts with `- [ ] `.
3. **`## 🔎 Objective`** *(only when context needs setup)* — the
   situation that creates the problem. Often paired with a small
   ASCII diagram or mermaid graph.
4. **`## Why <thing> fails` / `## Diving into the pipeline`** — the
   explanation. Walk the reader through the moving parts. Diagrams
   (mermaid) are encouraged here (see [[mermaid-palette]]).
5. **`## Solution: using <command>`** — the actual commands, in a
   `bash` or `zsh` fenced block. Prefix narration with
   `<strong > &#9654;&nbsp; Steps</strong>` and
   `<strong > &#9654;&nbsp; Commands</strong>` when there are multiple.
6. **`::: {.callout-tip}` / `::: {.callout-warning}`** — gotchas,
   version notes, edge cases. Always have a `## <one-line heading>`
   on the first line inside the callout.

## Idioms to reuse

- `[Some inline section title]{.mini-section}` — used as a styled
  inline label before a code block or ASCII diagram. Reuse, don't
  invent new attribute classes.
- `:::{style="padding-left:1em;"}` — used to indent a block inside
  a callout. Stick to this exact style string.
- Tables for comparisons use
  `: {tbl-colwidths="[30,35,35]"}` underneath, and often sit inside
  `:::{.no-border-top-table}` ... `:::`.
- Mermaid diagrams use the shared palette — see [[mermaid-palette]].

## Anti-patterns to avoid

- Don't invent new emoji headings. The repo only uses 🎯 and 🔎 at
  H2 level. Don't add 💡, 🚀, ✨, etc.
- Don't add a "Conclusion" or "Summary" section. The TL;DR at the top
  is the summary.
- Don't add "References" / "Further reading" sections unless the
  user asks. Links go inline.
- Don't put the author's opinion in first person ("I think...",
  "In my experience..."). The post is a reference, not a diary.
- Don't change `freeze: true` or other `_metadata.yml` settings —
  these apply repo-wide.

## When the user says "align with the blog tone"

They mean: take an existing draft `index.qmd` and rewrite it so it
matches the rules above. Workflow:

1. Read the target file fully.
2. Read 2–3 recent posts (e.g. the most recent two `posts/2026-*`
   directories) to refresh your sense of the voice — the repo evolves.
3. Rewrite the file with `Edit` (preferred — only one file changed)
   or `Write` (only if the rewrite is near-total).
4. Preserve all factual content. The skill is voice, not research:
   never delete a code block, command, or claim the user wrote unless
   you are sure it's wrong — and if you change a claim, surface it
   in your end-of-turn message.
5. Update `date-modified` to today (the user's local date — check the
   `currentDate` context line, not `date +%Y-%m-%d`).

## When the user says "write a new post about X"

1. Confirm the directory slug with the user before creating files
   (`posts/<YYYY-MM-DD>-<kebab-slug>/index.qmd`). Don't invent
   a slug silently.
2. Scaffold `index.qmd` with the frontmatter template above.
3. Draft the body. Keep the draft tight — the user will iterate.