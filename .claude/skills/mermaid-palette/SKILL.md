---
name: mermaid-palette
description: Use when the user asks to make a mermaid diagram more readable, fix unreadable mermaid colors, or "align the colors with the rest of the blog". Applies the soft-pastel palette already used across `posts/*/index.qmd` mermaid blocks — light fills with darker matching strokes and dark text, plus a red palette for failure states. Triggers on prompts like "mermaid を見やすい色にして", "他の mermaid もこの配色に揃えて", "mermaid colors are unreadable".
---

# mermaid-palette

Mermaid diagrams in this repo use an explicit, repeating soft-pastel
palette via `classDef` lines. The palette is informal — there is no
shared `.mmdrc` or theme file — so consistency lives in posts.
When the user asks to fix mermaid colors, apply this palette;
don't invent new colors per diagram.

## The canonical palette (semantic, not arbitrary)

These four classes cover essentially every diagram in the repo.
Reuse the class names so future diagrams can be skimmed at a glance.

```mermaid
classDef app    fill:#e3eefc,stroke:#2c6cb0,color:#1a3c66
classDef proxy  fill:#fff4d6,stroke:#b8860b,color:#5a4209
classDef inside fill:#e2f0d9,stroke:#3a7d2b,color:#1f4d12
classDef fail   fill:#fde2e2,stroke:#c0392b,color:#7b1d1d
```

Semantics:

- `app` — *blue*. The client or the user-facing tool. Default for
  the leftmost / starting node in flowcharts.
- `proxy` — *amber*. Anything in the middle: tunnels, proxies,
  gateways, bridges, queues.
- `inside` — *green*. The "good" destination — the internal
  service, the successful end-state, the DB that responded.
- `fail` — *red*. Error nodes, failed paths, NXDOMAIN, 5xx.
  Use sparingly — only on nodes that represent failure.

## Rules of thumb

1. **Light fill + darker matching stroke + dark text.** Mermaid's
   default theme uses dark fills with white text, which is hard
   to read on the blog's light background and unreadable in any
   exported PDF. Always override.
2. **Three-color cap per diagram.** A diagram with all four
   classes plus extra one-off `style` lines becomes a colorbar.
   If you reach for a fifth color, you probably want to split
   the diagram instead.
3. **Use `classDef` + `class A,B,C app`** instead of per-node
   `style` lines, except for a single highlighted node. The
   compact `class A,B,C app` form is the dominant style in the repo.
4. **No `theme: dark`.** The site supports light/dark site themes
   but mermaid blocks stay in this palette either way — the dark
   strokes still read on a dark page.
5. **`gitGraph` uses a separate init-block convention.** `gitGraph`
   does not accept `classDef`, so the flowchart palette does not apply.
   Instead, every `gitGraph` in the repo opens with the same `%%{init}%%`
   header (see `posts/2024-11-05-when-do-i-use-git-rebase/` and
   `posts/2024-07-18-cannot-push-to-remote-branch/`):

   ```
   %%{init: { 'logLevel': 'debug', 'theme': 'base',
               'gitGraph': {'rotateCommitLabel': true,
                            'mainBranchName': 'main'}}}%%
   ```

   When a new gitGraph is unreadable (default mermaid dark fills
   clashing with the blog background), add the header above and,
   if the diagram has more than two branches, add `themeVariables`
   that map `git0` / `git1` / `git2` to the **flowchart palette
   stroke colors** so a reader skimming a post sees consistent
   semantics across diagram types:

   ```
   'themeVariables': {
       'git0': '#2c6cb0',   /* app blue       — main          */
       'git1': '#3a7d2b',   /* inside green   — develop / fix */
       'git2': '#b8860b',   /* proxy amber    — feature/hotfix */
       'gitBranchLabel0': '#ffffff',
       'gitBranchLabel1': '#ffffff',
       'gitBranchLabel2': '#ffffff',
       'commitLabelColor': '#1a3c66',
       'commitLabelBackground': '#e3eefc',
       'tagLabelColor': '#1f4d12',
       'tagLabelBackground': '#e2f0d9',
       'tagLabelBorder': '#3a7d2b'
   }
   ```

   Pre-existing gitGraphs that already have the plain `'theme': 'base'`
   header (e.g. `posts/2024-07-12-committed-on-a-wrong-branch/`) are
   intentionally left alone — don't recolor them unless the user
   specifically asks for git-graph styling.

## Applying the palette to an existing diagram

Workflow when the user says "this mermaid is unreadable" or
"align with the other diagrams":

1. Read the surrounding post to see whether it's a success-path
   diagram, a failure-path diagram, or both (some posts have a
   "works" diagram followed by a "doesn't work" diagram —
   see `posts/2026-05-21-poetry-add-from-gitlab-in-intra-server/`).
2. Map each node to one of the four classes by *role in the story*,
   not by visual variety. The leftmost actor is almost always `app`;
   anything that's actively failing is `fail`.
3. Replace any existing `style X fill:...` lines with
   `classDef`s and `class A,B,C <name>` lines. Keep at most one
   per-node `style` line, and only when one node needs special
   highlighting (e.g. the SOCKS tunnel node in the poetry post
   keeps an extra `style B fill:#fffbe9,stroke:#b8860b` to draw
   attention).
4. Don't introduce new hex values. If a node genuinely doesn't fit
   any class, ask the user before adding a fifth color.

## Example: before / after

Unreadable default:

````
```{mermaid}
flowchart LR
    A[git clone] --> B[localhost:1080] --> C[Step server] --> D[gitlab.internal:443]
```
````

Aligned with the blog:

````
```{mermaid}
flowchart LR
    A[git clone<br/>libcurl] -->|"socks5h CONNECT"| B[localhost:1080<br/>SSH -D tunnel]
    B -->|SSH-encrypted| C[Step server]
    C -->|"resolve via internal DNS"| D[gitlab.internal:443]

    classDef app    fill:#e3eefc,stroke:#2c6cb0,color:#1a3c66
    classDef proxy  fill:#fff4d6,stroke:#b8860b,color:#5a4209
    classDef inside fill:#e2f0d9,stroke:#3a7d2b,color:#1f4d12
    class A app
    class B,C proxy
    class D inside
```
````

## When the user says "fix the other mermaids too"

They mean: walk every `mermaid` fenced block in the current post
(or the file they named) and apply the palette where missing.
Workflow:

1. `grep -n '```{mermaid}'` to enumerate blocks.
2. For `flowchart` / `graph` / `sequenceDiagram` blocks: apply the
   four-class palette in-place with `Edit`.
3. For `gitGraph` blocks: apply the `%%{init}%%` header from rule 5
   (and the `themeVariables` block when there are 3+ branches).
4. Report which blocks you changed and which you skipped (and why).

Don't reflow node labels or change edge text while recoloring —
keep the diff to color/class lines so the user can review it cleanly.