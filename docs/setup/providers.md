# Setup — LLM Providers & Credentials

> **Goal:** get the three values every notebook needs — `OPENAI_API_KEY`, `OPENAI_API_BASE`, `OPENAI_MODEL` — for **any** scenario. Pick the one that matches where your access comes from.

All workshop code is provider-agnostic: it uses `ChatOpenAI(base_url=..., api_key=..., model=...)` from `langchain-openai`, which speaks the OpenAI-compatible chat API. If a provider offers an OpenAI-compatible endpoint (nearly all do), it works here.

## Scenario A — Instructor-provided endpoint (workshop default)

During the workshop, the instructor hands out a proxy/endpoint. The values are announced at the session (they may be rotated live):

```bash
export OPENAI_API_KEY="<announced at the session>"
export OPENAI_API_BASE="<announced at the session>"
export OPENAI_MODEL="openai/gpt-4.1-mini"   # or as announced
```

- The **workshop site's Settings panel** (gear icon) is the fastest path: paste the three values once, and it generates the exact export/env lines for local and Colab.
- If the endpoint is slow/limited mid-session, the instructor may switch to a fallback — see B/C/D below, which you can self-serve.

## Scenario B — OpenRouter (many models, one key)

1. Create an account at <https://openrouter.ai> and create an API key.
2. Values:

```bash
export OPENAI_API_KEY="sk-or-v1-..."
export OPENAI_API_BASE="https://openrouter.ai/api/v1"
export OPENAI_MODEL="openai/gpt-4.1-mini"    # any vendor/... id from openrouter.ai/models
```

- Model IDs include the vendor prefix (e.g. `anthropic/claude-sonnet-4`, `google/gemini-2.5-flash`, `meta-llama/llama-3.3-70b-instruct`).
- Some models are free (`:free` suffix) — good workshop fallback.

## Scenario C — Hugging Face (with organization)

1. Create a token at <https://huggingface.co/settings/tokens> (a **fine-grained** token with *Inference* scope; read-only is fine).
2. Values:

```bash
export OPENAI_API_KEY="hf_..."
export OPENAI_API_BASE="https://router.huggingface.co/v1"
export OPENAI_MODEL="meta-llama/Llama-3.3-70B-Instruct"   # any Inference Providers model id
```

- HF's OpenAI-compatible endpoint: `https://router.huggingface.co/v1` routes to Inference Providers using your HF token.
- Model ids look like `meta-llama/Llama-3.3-70B-Instruct`, `Qwen/Qwen2.5-72B-Instruct`, etc. (see <https://huggingface.co/models?inference_provider=all>).
- If you belong to a Hugging Face **organization**, use its Inference credits via a token with the *org* scope.

## Scenario D — Anthropic (direct)

Two options:

**D1. OpenAI-compatible gateway (works with the same 3 env vars):** Anthropic exposes an OpenAI-compatible endpoint:

```bash
export OPENAI_API_KEY="sk-ant-..."
export OPENAI_API_BASE="https://api.anthropic.com/v1"
export OPENAI_MODEL="claude-sonnet-4-5"       # e.g. claude-sonnet-4-5, claude-haiku-4-5
```

> Check the Anthropic docs for current model ids and OpenAI-compat endpoint availability — if this route errors, use D2.

**D2. Native Anthropic provider (requires a small code change in the notebook):**

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export ANTHROPIC_MODEL="claude-sonnet-4-5"
```

```python
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-sonnet-4-5")
```

Every notebook marks its `make_llm()` helper cell — swapping the single construction line is the only change needed.

## Scenario E — Any OpenAI-compatible proxy / vLLM / Ollama / LM Studio

```bash
export OPENAI_API_KEY="whatever-the-proxy-needs"     # e.g. "ollama" for local Ollama
export OPENAI_API_BASE="http://localhost:11434/v1"   # Ollama example
export OPENAI_MODEL="llama3.2"
```

- vLLM: `http://localhost:8000/v1`; LM Studio: `http://localhost:1234/v1`.
- Great for fully offline workshops — bring your own model.

## What to set — summary

| Scenario | OPENAI_API_BASE | Key | Model id style |
|---|---|---|---|
| A. Instructor endpoint | announced at session | announced at session | `openai/gpt-4.1-mini` (example) |
| B. OpenRouter | `https://openrouter.ai/api/v1` | `sk-or-v1-...` | `vendor/model` |
| C. Hugging Face | `https://router.huggingface.co/v1` | `hf_...` | `org/model` |
| D. Anthropic | `https://api.anthropic.com/v1` | `sk-ant-...` | `claude-*` |
| E. Local proxy | `http://host:port/v1` | proxy-specific | proxy-specific |

## Safety rules

- **Never commit keys.** `.env` is git-ignored (`.gitignore` includes it); in Colab prefer Secrets (🔑) over pasted `%env` cells; on the site, keys live only in your browser's localStorage.
- Keys and base URL must come from the **same** provider.
- Rotate anything exposed in screenshots/shares.

→ Next: [local.md](local.md) · [colab.md](colab.md) · Back to [README](../../README.md)
