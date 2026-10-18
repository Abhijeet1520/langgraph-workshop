# Setup — Run Locally

> **Goal:** a working local Python environment with the LangGraph stack and your LLM provider configured. ~10 minutes.

## 1. Prerequisites

- **Python 3.10+** — check: `python3 --version`
- **git** — check: `git --version`
- A terminal (bash/zsh on macOS/Linux, PowerShell on Windows)

## 2. Clone the repo

```bash
git clone https://github.com/Abhijeet1520/langgraph-workshop.git
cd langgraph-workshop
```

## 3. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows PowerShell
python3 -m pip install --upgrade pip
```

> Colab already has most packages — this section is only for local runs.

## 4. Install the workshop requirements

```bash
pip install -r notebooks/requirements.txt
```

<details>
<summary>What gets installed (click to expand)</summary>

| Package | Purpose |
|---|---|
| `langgraph`, `langgraph-checkpoint` | Stateful graph orchestration + persistence |
| `langchain`, `langchain-core`, `langchain-community` | Chains, prompts, community integrations |
| `langchain-openai` | OpenAI-compatible LLM access (works with any base URL) |
| `langchain-anthropic` | Anthropic direct provider (one scenario) |
| `ddgs` | DuckDuckGo web search for tools/capstone (no API key) |
| `beautifulsoup4`, `requests` | HTML parsing helpers |
| `ipython`, `ipykernel`, `jupyter` | Run the notebooks locally |
| `python-dotenv`, `pydantic` | Config & validation |

</details>

## 5. Configure your provider (pick ONE scenario)

All notebooks read the **same three env vars** — set them once and every level works:

```bash
export OPENAI_API_KEY="<key>"
export OPENAI_API_BASE="<base-url>"
export OPENAI_MODEL="<model>"
```

If you don't have values yet, see [providers.md](providers.md) — it covers the instructor-provided workshop endpoint, OpenRouter, Hugging Face, Anthropic, and generic OpenAI-compatible proxies, with exact values to paste.

> **Tip:** put the three `export` lines in a `.env` file at repo root and run `cp .env.example .env` — the `python-dotenv` we install makes notebooks pick them up automatically.

```bash
cp .env.example .env
# then edit .env with your values
```

## 6. Start Jupyter and open Level 0

```bash
jupyter lab          # or: jupyter notebook
```

Open `notebooks/level-0-setup/00_welcome_and_verify.ipynb` and run all cells — it verifies your provider config with a live test call.

## 7. Verify

```bash
python3 - << 'EOF'
import os
for v in ("OPENAI_API_KEY", "OPENAI_API_BASE", "OPENAI_MODEL"):
    val = os.getenv(v)
    print(f"{v}: {'✅ set' if val else '❌ missing — see docs/setup/providers.md'}")
EOF
```

## Troubleshooting

| Symptom | Fix |
|---|---|
| `OPENAI_API_BASE` set but 401/invalid key | Key and base URL must come from the **same** provider — see [providers.md](providers.md) |
| `model not found` | Model name must be the provider's exact ID (with prefix, e.g. `openrouter/...`) — check the provider's model page |
| Long timeouts during the workshop | Instructor endpoint may be rate-limited; wait 30s, retry; the verify cell tells you if the endpoint is alive |
| pip resolution conflicts | recreate the venv: `rm -rf .venv && python3 -m venv .venv && source .venv/bin/activate && pip install -r notebooks/requirements.txt` |

→ Next: [Level 0 notebook](../../notebooks/level-0-setup/00_welcome_and_verify.ipynb) · Back to: [README](../../README.md)
