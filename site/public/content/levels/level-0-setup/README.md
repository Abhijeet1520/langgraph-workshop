# Level 0 — Setup & Verify

> **Goal:** install the LangGraph stack and confirm your LLM provider works — one verified test call and you're ready for Level 1.

## The three ways to run the workshop

| Way | Best for | Guide |
|---|---|---|
| **Google Colab** | zero install, workshop default | [docs/setup/colab.md](../../setup/colab.md) |
| **Local** | your own machine, offline-ish | [docs/setup/local.md](../../setup/local.md) |
| **Workshop site** | following along, keeping your config | [docs/setup/website.md](../../setup/website.md) |

## The notebook

[00_welcome_and_verify.ipynb](../../notebooks/level-0-setup/00_welcome_and_verify.ipynb) — welcome, install, configure provider, verify.

## The three env vars (everything hinges on these)

```bash
export OPENAI_API_KEY="<key>"
export OPENAI_API_BASE="<base-url>"
export OPENAI_MODEL="<model>"
```

Every notebook reads the same three — set once, done. Where to get values for every provider scenario (instructor endpoint, OpenRouter, Hugging Face, Anthropic, local proxies): [providers.md](../../setup/providers.md).
