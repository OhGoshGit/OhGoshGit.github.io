document.addEventListener("DOMContentLoaded", () => {

  const escapeHtml = (s) => s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");

  // Escape first, then re-introduce <code> for inline backticks.
  // Backticks survive escapeHtml unchanged, so the regex still matches.
  const renderInline = (s) => escapeHtml(s)
    .replace(/`([^`]+)`/g, "<code>$1</code>");

  const indentOf = (line) => {
    const m = line.match(/^[ \t]*/);
    return m ? m[0].length : 0;
  };

  document.querySelectorAll(".glossary-container").forEach(container => {

    const codeBlock = container.querySelector("pre code");
    if (!codeBlock) return;

    const rawLines = codeBlock.textContent.replace(/\s+$/, "").split(/\r?\n/);

    const glossary = [];
    let current = null;
    let descLines = null;       // raw lines collected for the active description
    let descBaseIndent = null;  // indent of the first non-blank description line
    let entryIndent = null;     // sibling-key indent for the active entry

    const flushDescription = () => {
      if (!current || descLines === null) return;
      while (descLines.length && descLines[descLines.length - 1].trim() === "") {
        descLines.pop();
      }
      const base = descBaseIndent ?? 0;
      current.description = descLines
        .map(l => (l.length >= base ? l.slice(base) : l.replace(/^\s+/, "")))
        .join("\n");
      descLines = null;
      descBaseIndent = null;
    };

    rawLines.forEach(line => {
      const trimmed = line.trim();
      const indent = indentOf(line);

      const defMatch = trimmed.match(/^-\s*def:\s*(.*)$/);
      if (defMatch) {
        flushDescription();
        current = { def: defMatch[1].trim(), description: "" };
        glossary.push(current);
        entryIndent = indent + 2; // sibling keys sit deeper than the dash
        return;
      }

      const descStart = trimmed.match(/^description:\s*([|>])\s*$/);
      if (descStart && current) {
        flushDescription();
        descLines = [];
        descBaseIndent = null;
        return;
      }

      // Inside a description: terminate when indent returns to entry level
      // (a sibling key like `category:` would land here). Blank lines stay.
      if (descLines !== null && current) {
        const isBlank = trimmed === "";
        if (!isBlank && entryIndent !== null && indent < entryIndent) {
          flushDescription();
        } else {
          if (!isBlank && descBaseIndent === null) descBaseIndent = indent;
          descLines.push(line);
          return;
        }
      }
    });

    flushDescription();

    const dl = document.createElement("dl");
    glossary.forEach(item => {
      const dt = document.createElement("dt");
      dt.textContent = item.def;
      dt.className = "glossary-term";

      const dd = document.createElement("dd");
      dd.className = "glossary-desc";
      dd.innerHTML = renderInline(item.description).trim();

      dl.appendChild(dt);
      dl.appendChild(dd);
    });

    container.innerHTML = "";
    container.appendChild(dl);

  });

});
