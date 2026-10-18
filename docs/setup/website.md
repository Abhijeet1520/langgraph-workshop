# Setup — The Workshop Website

> **Goal:** use the companion site to follow along, keep your provider config, and jump into Colab fast.

**URL:** https://abhijeet1520.github.io/langgraph-workshop/

## What the site does

| Feature | Where | What |
|---|---|---|
| Level/task navigation | sidebar | the full journey (levels 0–5) with progress tracking |
| Teaching docs | main pane | every `docs/levels/**.md` rendered with Mermaid diagrams + code blocks w/ copy buttons |
| Follow-along text | under each doc | what to run next, and the notebook's **Open in Colab** badge |
| **Settings panel** | gear icon (topbar) | paste **base URL / API key / model** once — the site shows the export lines for local & `%env` lines for Colab, keeps values in your browser (localStorage), and generates a `settings.json` you can download/import |
| Verify connection | settings panel | 1-token test call against your endpoint (✓/✗ with reason) |
| Progress + completion | progress ring | check tasks done; 100% opens the celebration overlay (with LinkedIn share) |

## Using the settings panel during the workshop

1. Click the **gear icon** → paste the **base URL**, **API key**, and **model** announced by the instructor.
2. Hit **Verify** — a green check means you're set.
3. Use **Copy for Colab** to get the three `%env` lines; paste them into the notebook's provider-config cell.
4. (Local users) Use **Copy as exports** to get the `export OPENAI_...` lines for your terminal.
5. Values stay in your browser — re-open the panel anytime to update (e.g. if the instructor rotates the key or switches to OpenRouter/HF mid-session: [providers.md](providers.md)).

> The key value is shown masked (••••) with a **reveal** toggle — handy when the instructor says "check the key you pasted", and safe from shoulder-surfing by default.

## Where the site's content comes from

The site renders the repo's `docs/` folder directly (build-time copy) — there is a **single source of truth**: the same markdown you can read on GitHub. If the repo updates, the site rebuilds via GitHub Actions.

## Site settings backup (JSON)

The settings panel's **Download settings.json** writes:

```json
{
  "baseUrl": "https://…",
  "apiKey": "…",
  "model": "…",
  "providerHint": "instructor | openrouter | huggingface | anthropic | custom"
}
```

Import it back on another browser/machine. (It's your secret — keep it out of git and screenshots.)

→ Back to [README](../../README.md) · [All provider scenarios](providers.md)
