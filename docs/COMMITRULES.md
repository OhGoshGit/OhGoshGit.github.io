# Commit Rules

- This repository is a **Quarto site** — a blog, a book, or a mix of both: posts
  and chapters under content directories, reference material, and a build
  configured by `_quarto.yml`.
- It follows the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
  specification, adapted so that the `<type>` describes a change to **content**,
  not only to code.
- A consistent history makes it easy to answer "when did this page land?", "what
  changed in the reference material?", and "which commits touched the build?" —
  and it keeps the generated changelog readable.

## Commit Message Format

```text
<type>(<scope>): <description>   ← single line, mandatory

[optional body]

[optional footer(s)]
```

- The **header** is the first line and is mandatory — it is always a **single line**.
- The **scope** is optional but strongly encouraged; in a content repo it is
  usually the page slug or the section touched.
- A blank line separates the header from the body, and the body from the footer.

### Examples

A new page:

```text
post(lean4-setup): add Lean4 installation guide for Ubuntu

Covers elan as the version manager, VS Code extension setup, and the
mathlib cache warm-up step that is easy to miss on a fresh install.
```

An edit to an existing page:

```text
edit(shell-one-liner): clarify grep behaviour on empty lines
```

A reference-material change:

```text
ref(command): add realpath entry
```

Site-wide infrastructure:

```text
build: disable MathJax auto-injection via html-math-method plain
```

## Type

The `<type>` describes the kind of change and must be one of the following.
The first group is **content**; the second is **site and tooling**.

### Content types

| Type      | Description                                                                     |
| --------- | ------------------------------------------------------------------------------- |
| `post`    | Add a **new** page — a blog post, a book chapter, a standalone document          |
| `edit`    | Substantive edit to an existing page — new section, corrected explanation        |
| `ref`     | Reference material — glossaries, term/command lists, FAQ pages, link collections |
| `series`  | Restructure a multi-page series or book — reorder, re-thread, split, merge       |
| `fig`     | Figures and diagrams — SVG, TikZ, plots, screenshots                            |
| `typo`    | Typos, punctuation normalisation, wording touch-ups with no change in meaning    |
| `meta`    | Frontmatter only — `title`, `date`, `categories`, `description`, listing keys    |

> [!NOTE]
> Not every site has reference material or series. Drop the types you do not use
> rather than stretching them; a type nobody can place is worse than one fewer
> type.

### Site & tooling types

| Type       | Description                                                                  |
| ---------- | ---------------------------------------------------------------------------- |
| `style`    | Presentation only — CSS/SCSS, layout, fonts, theming                         |
| `feat`     | New site capability — filter, shortcode, generator script, Quarto extension  |
| `fix`      | A bug fix in site code, a generator, a filter, or a broken render            |
| `refactor` | Code or file reorganisation that neither fixes a bug nor adds a feature      |
| `perf`     | Faster build or render (e.g. `_freeze` caching, incremental render)          |
| `build`    | Quarto config, `_quarto.yml`, extensions, dependency manifests and lockfiles |
| `ci`       | CI workflows, `.pre-commit-config.yaml`, deployment automation               |
| `seo`      | Analytics, Open Graph, badges, sitemap, site verification files              |
| `docs`     | Repository documentation — `README.md`, `docs/`, agent instructions          |
| `chore`    | Housekeeping — `.gitignore`, cleanup of stray render artifacts, backups      |
| `revert`   | Reverts a previous commit                                                    |

> [!NOTE]
> `post` vs `edit` vs `typo` is the distinction that matters most here.
> Reach for `post` only when a new page is created; use `edit` when the reader
> would learn something new; use `typo` when they would not.

## Scope

The `<scope>` is optional and names the part of the site affected. Use a short,
lowercase noun. Omit it when the change is genuinely global.

- **For a page**, use the **slug**, dropping any date or number prefix the
  filename carries: `post(lean4-setup):`, `edit(shell-one-liner):`,
  `fig(wget-continue-flow):`
- **For a series or book part**, use its name: `series(set-and-topology):`
- **For reference material**, use the file or facet:
  `ref(command):`, `ref(regex):`, `ref(unicode):`
- **For site internals**, use the directory or subsystem:
  `style(dark-theme):`, `build(quarto):`, `ci(publish):`, `feat(glossary):`

## Description

- Keep the description on a **single line** — never wrap it onto multiple lines.
- Use the **imperative, present tense**: "add", not "added" or "adds".
- Do **not** capitalize the first letter.
- Do **not** end with a period.
- Keep the header concise — aim for **50 characters or fewer**, hard limit **72**.
- Wrap file, command, and option names in backticks, e.g. a header reading
  `edit(find): document -exec with +` becomes ``edit(find): document `-exec` with `+` ``
- Japanese is acceptable in the description when the change is about Japanese
  prose or terminology, but keep the `<type>(<scope>):` prefix in ASCII:
  `ref(term): パスカルケースの項目を追加`
- If more explanation is needed, put it in the **body**, not the description.

## Body

- Optional. Use it to explain **what** and **why**, not **how**.
- Wrap lines at **72 characters**.
- Separate from the header with one blank line.
- For a new page, a one-or-two-sentence summary of what it covers is more useful
  than a list of the sections you wrote.

## Footer

- Optional. Used for metadata such as issue references and breaking changes.
- Reference issues with `Closes #<id>`, `Fixes #<id>`, or `Refs #<id>`.
- Note when a change affects published URLs:
  `Refs: /posts/2026-07-31-lean4-setup/`

### Breaking Changes

In a content site, a "breaking change" is one that **breaks existing URLs or
inbound links** — renaming or deleting a page, changing a date or number prefix,
or moving a section. Indicate it with a `!` after the type/scope, a
`BREAKING CHANGE:` footer, or both.

```text
refactor(claude-code-setup)!: rename page to skill-ignition

BREAKING CHANGE: /posts/2025-06-14-claude-code-setup/ no longer resolves.
Inbound links and the RSS feed entry both change.
```

## One Change, One Commit

- Keep a page and its figures together in one commit — they are one change.
- Split unrelated work apart: adding a page and bumping a dependency are two
  commits, even when done in the same sitting.
- Do **not** commit build output. `_site/` (or the configured `output-dir`) and
  `_freeze/` are generated, and stray `*.quarto_ipynb` files are render artifacts.
- If `pre-commit` enforces file-size limits, compress or down-scale screenshots
  rather than raising the limit.

## Quick Reference

```text
post:     a new page — post, chapter, standalone document
edit:     substantive edit to an existing page
ref:      reference material — glossary, FAQ, link list
series:   restructure a multi-page series or book
fig:      figures, diagrams, screenshots
typo:     typos and wording, no change in meaning
meta:     frontmatter only

style:    CSS/SCSS, layout, fonts
feat:     new site capability
fix:      bug fix in site code or a broken render
refactor: reorganisation, no feature/fix
perf:     faster build or render
build:    Quarto config, extensions, dependencies
ci:       CI workflows, pre-commit, deployment
seo:      analytics, Open Graph, badges, sitemap
docs:     repo documentation
chore:    housekeeping
revert:   revert a previous commit
```
