#!/usr/bin/env python3
"""Generate the NEW (non-migrated) workshop notebooks:
  - level-0-setup/00_welcome_and_verify.ipynb
  - level-4-real-inbox/40_connect_your_inbox.ipynb
Run from repo root: python3 scripts/generate_new_notebooks.py
"""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
COLAB = "https://colab.research.google.com/github/Abhijeet1520/langgraph-workshop/blob/main"
SITE = "https://github.com/Abhijeet1520/langgraph-workshop"

PROV_ROWS: list[str] = []

ENV_CELL = '''\
# --- Workshop provider config (edit ONLY these 3 values) ---------------------
import os

os.environ.setdefault("OPENAI_API_KEY", "")   # <- paste your key
os.environ.setdefault("OPENAI_API_BASE", "")  # <- paste your base URL
os.environ.setdefault("OPENAI_MODEL", "openai/gpt-4.1-mini")  # <- your model id

# Verify
for _v in ("OPENAI_API_KEY", "OPENAI_API_BASE", "OPENAI_MODEL"):
    print(_v, "=", "set" if os.getenv(_v) else "**MISSING — see docs/setup/providers.md**")
# -----------------------------------------------------------------------------\
'''

LLM_HELPER = '''\
from langchain_openai import ChatOpenAI
import os

def make_llm(**overrides):
    """Provider-agnostic LLM factory used across the workshop."""
    cfg = dict(
        model=os.environ["OPENAI_MODEL"],
        api_key=os.environ["OPENAI_API_KEY"],
        base_url=os.environ["OPENAI_API_BASE"],
        temperature=0,
    )
    cfg.update(overrides)
    return ChatOpenAI(**cfg)
'''


def md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": text}


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": text,
    }


def header(dest_rel: str, level: str, title: str) -> dict:
    badge = f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({COLAB}/{dest_rel})"
    return md(
        f"{badge}\n\n"
        f"# {title}\n\n"
        f"**Level {level}** · Part of the [LangGraph Workshop]({SITE}).\n\n"
        f"**Provider setup:** set `OPENAI_API_KEY` / `OPENAI_API_BASE` / `OPENAI_MODEL` first — "
        f"[docs/setup/providers.md]({SITE}/blob/main/docs/setup/providers.md). "
        f"The first cells install requirements and verify the connection."
    )


def write_nb(dest_rel: str, cells: list[dict], level: str, title: str) -> None:
    dest = REPO / "notebooks" / dest_rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    nb = {
        "cells": [header(dest_rel, level, title)] + cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11"},
            "langgraph_workshop": {"level": level},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    dest.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    PROV_ROWS.append(f"| `notebooks/{dest_rel}` | notebook | NEW (workshop original) | — | written for this repo |")


def welcome_nb() -> None:
    cells = [
        md(
            "## Welcome to the LangGraph Workshop 👋\n\n"
            "This notebook gets you running: install the stack, configure your LLM provider, and "
            "make one verified test call.\n\n"
            "**How this workshop works:**\n"
            "1. You need three values — **base URL**, **API key**, **model name** — from one provider. "
            "Get them from the instructor, or bring your own (OpenRouter / Hugging Face / Anthropic / "
            "any OpenAI-compatible endpoint): [providers.md](https://github.com/Abhijeet1520/langgraph-workshop/blob/main/docs/setup/providers.md).\n"
            "2. Set them in the cell below (it writes them into `os.environ` for this notebook).\n"
            "3. Run the **Verify** cell — a green ✅ means you're ready for Level 1.\n\n"
            "**Local users:** you can instead `export` the vars before starting Jupyter, or use a "
            "`.env` file — see [local.md](https://github.com/Abhijeet1520/langgraph-workshop/blob/main/docs/setup/local.md)."
        ),
        md("## Install (Colab) / already installed (local)"),
        code(
            "%pip install -q langgraph langchain langchain-core langchain-community langchain-openai "
            "langgraph-checkpoint ddgs beautifulsoup4 requests python-dotenv pydantic"
        ),
        md("## Configure your provider"),
        code(ENV_CELL),
        md(
            "## Verify\n\n"
            "One tiny call through the same code path every level uses. If this fails, the error "
            "message tells you which value to fix."
        ),
        code(
            LLM_HELPER
            + '''

llm = make_llm()
try:
    resp = llm.invoke("Say OK")
    print("✅ LLM reachable:", resp.content[:60])
    print("Model:", os.environ["OPENAI_MODEL"])
    print("Base URL:", os.environ["OPENAI_API_BASE"])
except Exception as e:
    print("❌ Connection failed:", type(e).__name__)
    print(str(e)[:500])
    print("\\nFix checklist:")
    print("  1. Key + base URL from the SAME provider (docs/setup/providers.md)")
    print("  2. Model id exact, including prefixes (openrouter/..., hf org/model)")
    print("  3. Rate-limited? wait 30s and retry")
'''
        ),
        md(
            "## Next\n\n"
            "You're set. Head to Level 1 — [01_introduction.ipynb]"
            "(https://github.com/Abhijeet1520/langgraph-workshop/blob/main/notebooks/level-1-basics/01_introduction.ipynb) "
            "(or open it from the workshop site)."
        ),
    ]
    write_nb("level-0-setup/00_welcome_and_verify.ipynb", cells, "0", "Welcome & Verify Your Setup")


def inbox_nb() -> None:
    cells = [
        md(
            "## Level 4 — Point the Agent at Your Real Inbox 📬\n\n"
            "Level 3's agent ran on two hardcoded sample emails. Now we load **your real emails** "
            "into the same `EmailState` and run the identical graph — no rebuild.\n\n"
            "**⚠️ Safety rules (read first):**\n"
            "- **Read-only + draft-only in this workshop.** We fetch, classify, and *draft* replies. "
            "Nothing is ever sent, moved, or deleted.\n"
            "- Use an app password + a **test label/folder**, not your main account if you can.\n"
            "- LLM calls cost money & your emails contain PII — start with 5–10 emails.\n\n"
            "**Steps:** (1) IMAP connect → (2) fetch a batch → (3) map to `EmailState` → (4) run the "
            "Level 3 graph → (5) review drafts."
        ),
        md("## Install"),
        code("%pip install -q langgraph langchain langchain-core langchain-openai"),
        md("## Provider + mailbox config"),
        code(
            ENV_CELL
            + '''

# --- Mailbox config ----------------------------------------------------------
IMAP_HOST = "imap.gmail.com"        # Gmail; outlook: outlook.office365.com
IMAP_USER = "you@gmail.com"
IMAP_PASSWORD = ""                  # <- Gmail: 16-char app password (not your login)
FOLDER = "INBOX"                    # safer: a test label like "workshop-test"
MAX_EMAILS = 5                      # start small
# -----------------------------------------------------------------------------\
'''
        ),
        code(
            LLM_HELPER
            + '''

llm = make_llm()
print("✅ LLM ready:", os.environ["OPENAI_MODEL"])
'''
        ),
        md(
            "## 1. Connect (read-only)\n\n"
            "Gmail app passwords: Google Account → Security → 2-Step Verification → App passwords. "
            "Requires 2FA. Outlook/others: any IMAP host works — just change `IMAP_HOST`."
        ),
        code(
            '''\
import imaplib

if not IMAP_PASSWORD:
    print("⚠️ Set IMAP_PASSWORD above first (Gmail: 16-char app password)")
else:
    mail = imaplib.IMAP4_SSL(IMAP_HOST)
    mail.login(IMAP_USER, IMAP_PASSWORD)
    mail.select(FOLDER, readonly=True)   # READ-ONLY
    print("✅ Connected:", IMAP_USER, "folder:", FOLDER)
'''
        ),
        md("## 2. Fetch a batch of emails"),
        code(
            '''\
import email
from email.header import decode_header

def fetch_emails(max_emails: int = 5) -> list[dict]:
    """Fetch latest emails as plain dicts: sender / subject / body."""
    typ, data = mail.search(None, "ALL")
    ids = data[0].split()[-max_emails:]
    out = []
    for eid in ids:
        typ, msg_data = mail.fetch(eid, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        def hdr(name: str) -> str:
            raw = msg.get(name, "")
            parts = decode_header(raw)
            return "".join(
                p.decode(enc or "utf-8", "replace") if isinstance(p, bytes) else p
                for p, enc in parts
            )

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode("replace", "ignore")
                    break
        elif msg.get_content_type() == "text/plain":
            body = msg.get_payload(decode=True).decode("replace", "ignore")

        out.append({"sender": hdr("From"), "subject": hdr("Subject"), "body": body[:4000]})
    return out

emails = fetch_emails(MAX_EMAILS)
print(f"✅ Fetched {len(emails)} emails")
for e in emails:
    print(" -", e["sender"][:40], "|", e["subject"][:50])
'''
        ),
        md(
            "## 3. The Level 3 graph, unchanged\n\n"
            "Copy of the EmailState graph from `30_email_agent_graph.ipynb` — same code, so you can "
            "see that **your inbox data just flows into it**."
        ),
        code(
            '''\
from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage

class EmailState(TypedDict):
    email: Dict[str, Any]
    is_spam: Optional[bool]
    draft_response: Optional[str]
    messages: List[Dict[str, Any]]

def read_email(state: EmailState):
    email = state["email"]
    print(f"Processing email from {email['sender']} — {email['subject']}")
    return {}

def classify_email(state: EmailState):
    email = state["email"]
    prompt = f"""You are an email triage assistant. Analyze this email and determine if it is spam.
Email:
From: {email['sender']}
Subject: {email['subject']}
Body: {email['body'][:1500]}
Answer with exactly SPAM or HAM (legitimate). Only return the answer."""
    response = llm.invoke([HumanMessage(content=prompt)])
    text = response.content.lower().strip()
    is_spam = "spam" in text and "ham" not in text
    return {"is_spam": is_spam}

def handle_spam(state: EmailState):
    print("  -> marked as spam (draft action only; nothing moved)")
    return {}

def drafting_response(state: EmailState):
    email = state["email"]
    prompt = f"""You are an email assistant. Draft a brief, professional reply to this email.
Email:
From: {email['sender']}
Subject: {email['subject']}
Body: {email['body'][:1500]}
Draft the reply only, ready for the human to review and send."""
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"draft_response": response.content}

email_graph = StateGraph(EmailState)
email_graph.add_node("read_email", read_email)
email_graph.add_node("classify_email", classify_email)
email_graph.add_node("handle_spam", handle_spam)
email_graph.add_node("drafting_response", drafting_response)

def route_email(state: EmailState) -> str:
    return "spam" if state["is_spam"] else "legitimate"

email_graph.add_edge(START, "read_email")
email_graph.add_edge("read_email", "classify_email")
email_graph.add_conditional_edges("classify_email", route_email, {
    "spam": "handle_spam",
    "legitimate": "drafting_response",
})
email_graph.add_edge("handle_spam", END)
email_graph.add_edge("drafting_response", END)

compiled = email_graph.compile()
print("✅ Graph compiled — identical structure to Level 3")
'''
        ),
        md("## 4. Run it on your inbox (drafts only)"),
        code(
            '''\
for e in emails:
    result = compiled.invoke({
        "email": e,
        "is_spam": None,
        "draft_response": None,
        "messages": [],
    })
    if result["is_spam"]:
        print(f"  [SPAM] {e['subject'][:50]}")
    else:
        print(f"  [DRAFT] {e['subject'][:50]}")
        print("   reply:", (result.get("draft_response") or "")[:200].replace("\\n", " "))
        print()

# ⚠️ Nothing was sent, moved, or deleted — drafts printed to your screen only.
'''
        ),
        md(
            "## Going further (carefully)\n\n"
            "- **Auto-apply after trust:** only after reviewing many runs would you write results to a "
            "label/folder (IMAP `STORE`), and even then start with copying, not moving.\n"
            "- **Reply sending (SMTP)** is possible but out of scope — always keep a human in the loop "
            "for anything that leaves your machine.\n"
            "- **Cost/PII hygiene:** each email = 2 LLM calls (classify + draft). Batch small, run "
            "selectively (e.g. `UNSEEN` or a label filter), and never paste sensitive mail into a "
            "shared endpoint you don't trust.\n\n"
            "Next: [Level 5 — what else can you automate?](https://github.com/Abhijeet1520/langgraph-workshop/blob/main/docs/levels/level-5-next-steps/what-next.md)"
        ),
    ]
    write_nb("level-4-real-inbox/40_connect_your_inbox.ipynb", cells, "4", "Connect Your Real Inbox")


def main() -> None:
    welcome_nb()
    inbox_nb()
    # append to PROVENANCE.md
    prov = REPO / "docs" / "PROVENANCE.md"
    text = prov.read_text(encoding="utf-8")
    insert_at = text.rfind("## Update policy")
    block = "## Workshop originals\n\n| Workshop file | Type | Source repo | Source file | Transformations |\n|---|---|---|---|---|\n" + "\n".join(PROV_ROWS) + "\n\n"
    text = text[:insert_at] + block + text[insert_at:]
    prov.write_text(text, encoding="utf-8")
    print("Generated:", len(PROV_ROWS), "new notebooks")


if __name__ == "__main__":
    main()
