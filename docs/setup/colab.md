# Setup — Run in Google Colab

> **Goal:** run every workshop notebook with zero local install. Colab gives you a free (small) GPU-less VM with Jupyter preinstalled.

## 1. Open a notebook in Colab

Every notebook in `notebooks/` has a Colab badge in its first cell (and on the workshop site). Two equivalent ways:

- **From the site (recommended during the workshop):** click **"Open in Colab"** on any task page.
- **From GitHub:** go to the repo's `notebooks/` folders, open a notebook, and use the **Colab badge/link** in its header cell — or construct it directly:
  `https://colab.research.google.com/github/Abhijeet1520/langgraph-workshop/blob/main/notebooks/<level>/<file>.ipynb`

## 2. Install the stack (first cell does it for you)

The first code cell of every notebook runs:

```python
%pip install -q langgraph langchain langchain-core langchain-community langchain-openai langgraph-checkpoint ddgs beautifulsoup4 requests python-dotenv pydantic
```

Just run it (takes ~1 minute). Colab resets this on reconnect, so re-run it if your VM recycles.

## 3. Configure your provider (pick ONE scenario)

In Colab you set env vars with `%env` magic in a cell:

```python
%env OPENAI_API_KEY=<your-key>
%env OPENAI_API_BASE=<your-base-url>
%env OPENAI_MODEL=<your-model>
```

Paste the values your instructor gives you, **or** pick your own provider from [providers.md](providers.md) (instructor endpoint, OpenRouter, Hugging Face, Anthropic, generic proxy).

> **Workshop flow:** the workshop site's **Settings panel** (gear icon) is where you paste base URL / API key / model once. It shows you the exact `%env` lines and the `os.environ[...]` snippet to copy into Colab, and keeps them in your browser so you can re-copy later.

## 4. Verify the connection

Every notebook's **"Verify connection"** cell does a 1-token test call and prints ✓/✗ with the reason on failure. If you see ✗:

- Re-check the three values — key and base URL must come from the same provider.
- `model not found` → wrong model id; check the provider's model page for the exact string (prefixes matter, e.g. `openrouter/...`).
- 429/timeout during the workshop → the instructor endpoint may be rate-limited; wait 30s and retry.

## 5. Colab-specific notes

- **Everything is ephemeral** — files you write in Colab disappear when the VM recycles. Notebooks are designed so only the provider config needs re-pasting after a recycle.
- **Secrets (safer, optional):** instead of `%env` lines, use the 🔑 **Secrets** sidebar in Colab and read them in a cell:
  ```python
  from google.colab import userdata
  import os
  os.environ["OPENAI_API_KEY"] = userdata.get("OPENAI_API_KEY")
  os.environ["OPENAI_API_BASE"] = userdata.get("OPENAI_API_BASE")
  os.environ["OPENAI_MODEL"]    = userdata.get("OPENAI_MODEL")
  ```
- **No local files needed** — notebooks that need extra files fetch them from the repo's raw URLs.

## 6. Where to go next

| After setup... | Go to |
|---|---|
| Basics level | [Level 1](../levels/level-1-basics/) notebooks |
| Full local setup instead | [local.md](local.md) |
| All provider scenarios & values | [providers.md](providers.md) |

→ Back to: [README](../../README.md)
