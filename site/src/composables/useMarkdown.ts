import { marked } from "marked";
import hljs from "highlight.js";
import mermaid from "mermaid";

let initialized = false;

function initOnce() {
  if (initialized) return;
  initialized = true;
  mermaid.initialize({ startOnLoad: false, theme: "dark", securityLevel: "loose" });
  marked.use({
    renderer: {
      code(code: string, lang: string) {
        if (lang === "mermaid") {
          const id = `mmd-${Math.random().toString(36).slice(2)}`;
          renderMermaid(id, code);
          return `<div class="mermaid-wrap"><div id="${id}">${escapeHtml(code)}</div></div>`;
        }
        let html: string;
        try {
          html =
            lang && hljs.getLanguage(lang)
              ? hljs.highlight(code, { language: lang }).value
              : escapeHtml(code);
        } catch {
          html = escapeHtml(code);
        }
        return `<div class="codeblock"><button class="copy-btn" data-code="${encodeURIComponent(code)}">⧉</button><pre><code class="hljs">${html}</code></pre></div>`;
      },
    } as any,
  });
}

async function renderMermaid(id: string, code: string) {
  requestAnimationFrame(async () => {
    const el = document.getElementById(id);
    if (!el) return;
    try {
      const { svg } = await mermaid.render(`${id}-svg`, code);
      el.innerHTML = svg;
    } catch (e) {
      el.innerHTML = `<pre class="mermaid-error">${escapeHtml(code)}</pre>`;
    }
  });
}

export function renderMarkdown(md: string): string {
  initOnce();
  return marked.parse(md) as string;
}

export function escapeHtml(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
