#!/usr/bin/env python3
"""Migrate task docs + notebooks into the langgraph-workshop repo structure.

Sources (read-only):
  ../LangGraph Basics/          (own repo: Abhijeet1520/LangGraph-Basics @ ff39740)
  ../langgraph-notebooks/       (snehotosh/langgraph-notebooks @ 999d6e6)
  ../LangGraph-Course-freeCodeCamp/ (iamvaibhavmehra/... @ 9f172bf)
  ../langfuse-docs/cookbook/    (langfuse/langfuse-docs @ 3441a24)

Outputs:
  docs/levels/level-{0..5}-*/   teaching md (copied + provenance header)
  notebooks/level-{0..4}-*/     ipynb (copied, outputs cleared, header cell added)
  docs/PROVENANCE.md            full mapping table
Run from repo root: python3 scripts/migrate_sources.py
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO.parent

BASICS = SRC / "LangGraph Basics"
NB_SRC = SRC / "langgraph-notebooks"
FCC = SRC / "LangGraph-Course-freeCodeCamp"
LF = SRC / "langfuse-docs" / "cookbook"

PROVENANCE_ROWS: list[str] = []

SITE = "https://github.com/Abhijeet1520/langgraph-workshop"
COLAB = "https://colab.research.google.com/github/Abhijeet1520/langgraph-workshop/blob/main"


def colab_link(path_in_repo: str) -> str:
    return f"{COLAB}/{path_in_repo}"


def md_header(src_rel: str, src_repo: str, src_url: str) -> str:
    return (
        f"> **Source:** migrated from [`{src_rel}`]({src_url}) "
        f"({src_repo}). See [PROVENANCE.md](../../PROVENANCE.md) for the full mapping.\n\n"
    )


def copy_doc(src: Path, dest: Path, src_repo: str, repo_url: str, src_rel: str) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)
    rel_out = dest.relative_to(REPO).as_posix()
    PROVENANCE_ROWS.append(
        f"| `{rel_out}` | doc | `{src_repo}` | [`{src_rel}`]({repo_url}/blob/main/{src_rel}) | verbatim |"
    )


def nb_header_md(dest_rel: str, level: str, title: str, src_repo: str, src_url: str) -> str:
    badge = f"[![Open In Colab]({colab_png()})]({colab_link(dest_rel)})"
    return (
        f"{badge}\n\n"
        f"# {title}\n\n"
        f"**Level {level}** · Part of the [LangGraph Workshop]({SITE}).\n\n"
        f"**Provider setup:** set `OPENAI_API_KEY` / `OPENAI_API_BASE` / `OPENAI_MODEL` first — "
        f"[docs/setup/providers.md]({SITE}/blob/main/docs/setup/providers.md). "
        f"The first cells install requirements and verify the connection."
    )


def colab_png() -> str:
    return "https://colab.research.google.com/assets/colab-badge.svg"


def write_nb(
    src: Path,
    dest: Path,
    level: str,
    title: str,
    src_repo: str,
    src_url: str,
    fix_llm: bool = False,
) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    nb = json.loads(src.read_text(encoding="utf-8"))
    # clear outputs + execution counts
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
    # fix model config: normalize to env-var-driven ChatOpenAI
    if fix_llm:
        nb = normalize_llm(nb)
    dest_rel = dest.relative_to(REPO).as_posix()
    header = {
        "cell_type": "markdown",
        "metadata": {},
        "source": nb_header_md(dest_rel, level, title, src_repo, src_url),
    }
    nb["cells"] = [header] + nb.get("cells", [])
    nb["metadata"] = nb.get("metadata", {})
    nb["metadata"]["langgraph_workshop"] = {
        "level": level,
        "source_repo": src_repo,
        "source_url": src_url,
    }
    dest.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    PROVENANCE_ROWS.append(
        f"| `{dest_rel}` | notebook | `{src_repo}` | [original]({src_url}) | outputs cleared, header added"
        + (", env-var LLM config" if fix_llm else "")
        + " |"
    )


MAKE_LLM_ENV = '''\
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

MAKE_LLM_HELPER = '''\
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

llm = make_llm()

# Connection check (1 token)
resp = llm.invoke("Say OK")
print("✅ LLM reachable:", resp.content[:60])
'''


def workshop_env_cell() -> dict:
    """The provider-config cell every workshop notebook gets."""
    return {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": MAKE_LLM_ENV,
    }


def make_llm_helper_cell() -> dict:
    """The make_llm() factory + 1-token connection check cell."""
    return {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": MAKE_LLM_HELPER,
    }


def normalize_llm(nb: dict) -> dict:
    """Replace hardcoded model constructions with env-var driven ones.

    Conservative: only touches known-safe patterns from the source repos
    (gpt-4o ChatOpenAI constructors). Provider config + helper are prepended
    right after the header cell.
    """
    import re

    cells = nb.get("cells", [])
    config_cell = {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": MAKE_LLM_ENV,
    }
    helper_cell = {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": MAKE_LLM_HELPER,
    }
    # patterns: llm = ChatOpenAI(model="gpt-4o"...) / model = ChatOpenAI(...)
    ctor = re.compile(
        r'^(?P<var>\w+)\s*=\s*ChatOpenAI\(\s*(?P<args>[^)]*)\)\s*(\.bind_tools\((?P<tools>[^)]*)\))?\s*$',
        re.M,
    )

    def repl(m: re.Match) -> str:
        var, args, tools = m.group("var"), m.group("args"), m.group("tools")
        extra = ""
        # keep temperature if present
        t = re.search(r"temperature\s*=\s*([\d.]+)", args)
        if t:
            extra = f", temperature={t.group(1)}"
        line = f"{var} = make_llm({extra.strip(', ')})"
        if tools:
            line += f".bind_tools({tools})"
        return line

    changed = False
    for cell in cells:
        if cell.get("cell_type") != "code":
            continue
        src = "".join(cell["source"])
        new, n = ctor.subn(repl, src)
        if n:
            cell["source"] = new
            changed = True

    # Insert config+helper after position 0 (header) only if we replaced something
    # or the notebook has no provider config at all.
    has_env = any(
        "OPENAI_API_BASE" in "".join(c["source"]) for c in cells if c.get("cell_type") == "code"
    )
    if changed or not has_env:
        nb["cells"] = [cells[0], config_cell, helper_cell] + cells[1:] if cells else [
            config_cell,
            helper_cell,
        ]
    return nb


def main() -> None:
    # ------------------------------------------------------------------ docs
    # Level 1-2 docs: task2..task9 from LangGraph Basics
    doc_map = [
        # (src, dest, repo, repo_url, src_rel)
        (BASICS / "docs/task1-setup.md", "levels/level-0-setup/task1-setup.md"),
        (BASICS / "docs/task2-sequential-vs-stateful.md", "levels/level-1-basics/task2-sequential-vs-stateful.md"),
        (BASICS / "docs/task3-stategraph.md", "levels/level-1-basics/task3-stategraph.md"),
        (BASICS / "docs/task4-nodes.md", "levels/level-1-basics/task4-nodes.md"),
        (BASICS / "docs/task5-edges-routing.md", "levels/level-1-basics/task5-edges-routing.md"),
        (BASICS / "docs/task6-loops.md", "levels/level-1-basics/task6-loops.md"),
        (BASICS / "docs/task7-tools.md", "levels/level-2-tools-memory-capstone/task7-tools.md"),
        (BASICS / "docs/task8-memory.md", "levels/level-2-tools-memory-capstone/task8-memory.md"),
        (BASICS / "docs/task9-research-assistant.md", "levels/level-2-tools-memory-capstone/task9-research-assistant.md"),
    ]
    for src, rel in doc_map:
        copy_doc(
            src,
            REPO / "docs" / rel,
            "Abhijeet1520/LangGraph-Basics",
            "https://github.com/Abhijeet1520/LangGraph-Basics",
            f"docs/{Path(rel).name}",
        )

    # Level 3-5 docs are NEW content, not migrations.
    # ------------------------------------------------------------- notebooks
    # Level 1-2: langgraph-notebooks (snehotosh) — concept coverage order
    nb_map = [
        # src, dest, level, title, fix_llm
        (NB_SRC / "1_introduction.ipynb", "level-1-basics/01_introduction.ipynb", "1", "Introduction to LangGraph", True),
        (NB_SRC / "2_simple_graph.ipynb", "level-1-basics/02_simple_graph.ipynb", "1", "Simple Graph", True),
        (NB_SRC / "7_more_on_states.ipynb", "level-1-basics/03_more_on_states.ipynb", "1", "More on States", True),
        (NB_SRC / "3_build_chat_tool_graph.ipynb", "level-1-basics/04_chat_tool_graph.ipynb", "1", "Chat + Tool Graph", True),
        (NB_SRC / "4_BasicAgent.ipynb", "level-1-basics/05_basic_agent.ipynb", "1", "Basic Agent", True),
        (NB_SRC / "5_BasicAgent-with-memory-checkpointing.ipynb", "level-1-basics/06_agent_memory_checkpointing.ipynb", "1", "Agent with Memory & Checkpointing", True),
        (NB_SRC / "9_controllability-breakpoints-and-timetravel.ipynb", "level-1-basics/07_controllability_breakpoints_timetravel.ipynb", "1", "Controllability: Breakpoints & Time Travel", True),
        (NB_SRC / "10_controllability- parallelization_subgraph.ipynb", "level-1-basics/08_parallelization_subgraph.ipynb", "1", "Parallelization & Subgraphs", True),
        (NB_SRC / "6_more_on_messages.ipynb", "level-1-basics/09_more_on_messages.ipynb", "1", "More on Messages", True),
        (NB_SRC / "8_build_chatbot_summarization_and_stream.ipynb", "level-1-basics/10_chatbot_summarization_stream.ipynb", "1", "Chatbot: Summarization & Streaming", True),
        (NB_SRC / "11_build_research_assistant.ipynb", "level-2-tools-memory-capstone/11_research_assistant.ipynb", "2", "Research Assistant Capstone", True),
        (NB_SRC / "12_memory.ipynb", "level-2-tools-memory-capstone/12_memory.ipynb", "2", "Memory Architectures", True),
        (NB_SRC / "13_memory_with_profile-and-collection.ipynb", "level-2-tools-memory-capstone/13_memory_profile_collection.ipynb", "2", "Memory: Profiles & Collections", True),
        (NB_SRC / "14_Building_Chatbot_Agent.ipynb", "level-2-tools-memory-capstone/14_chatbot_agent.ipynb", "2", "Chatbot Agent End-to-End", True),
    ]
    for src, rel, level, title, fix in nb_map:
        write_nb(
            src,
            REPO / "notebooks" / rel,
            level,
            title,
            "snehotosh/langgraph-notebooks",
            f"https://github.com/snehotosh/langgraph-notebooks/blob/main/{src.name}",
            fix_llm=fix,
        )

    # Level 3: langfuse email agent — split into graph + observability
    split_email_notebook()

    # ------------------------------------------------------------ PROVENANCE
    prov = [
        "# Provenance — where every notebook/doc came from",
        "",
        "This repo teaches with material migrated from other repositories (with permission of their licenses).",
        "Each migrated file carries a source header; this table is the full mapping. Sources are pinned",
        "to the commits listed below so later updates can be diffed cleanly.",
        "",
        "## Source repositories (pinned)",
        "",
        "| Source repo | Local path | Pinned commit | License |",
        "|---|---|---|---|",
        "| [Abhijeet1520/LangGraph-Basics](https://github.com/Abhijeet1520/LangGraph-Basics) | `tools/harness/langgraph-docs/LangGraph Basics` | `ff39740` | MIT |",
        "| [snehotosh/langgraph-notebooks](https://github.com/snehotosh/langgraph-notebooks) | `tools/harness/langgraph-docs/langgraph-notebooks` | `999d6e6` | (check repo) |",
        "| [iamvaibhavmehra/LangGraph-Course-freeCodeCamp](https://github.com/iamvaibhavmehra/LangGraph-Course-freeCodeCamp) | `tools/harness/langgraph-docs/LangGraph-Course-freeCodeCamp` | `9f172bf` | (check repo) |",
        "| [langfuse/langfuse-docs](https://github.com/langfuse/langfuse-docs) | `tools/harness/langgraph-docs/langfuse-docs` | `3441a24` | CC-BY (docs) |",
        "",
        "## File mapping",
        "",
        "| Workshop file | Type | Source repo | Source file | Transformations |",
        "|---|---|---|---|---|",
        *PROVENANCE_ROWS,
        "",
        "## Update policy",
        "",
        "To pull updates from a source repo: bump its pinned commit above, re-run",
        "`python3 scripts/migrate_sources.py` (from repo root), and review the diff. The script is",
        "idempotent and never edits files under `site/`.",
        "",
    ]
    (REPO / "docs" / "PROVENANCE.md").write_text("\n".join(prov), encoding="utf-8")
    print("Migration complete.")
    print(f"Docs migrated: {len(doc_map)}")
    print(f"Notebooks migrated: {len(nb_map)}")


def split_email_notebook() -> None:
    """Split langfuse example_langgraph_agents.ipynb into graph + observability parts.

    Source layout (43 cells):
      0: NOTEBOOK_METADATA comment     1: "Step 0 Install" md    2: %pip install
      3: "Step 1 env" md                4: Langfuse+OpenAI env     5: md
      6: get_client                    7: "Step 2" md             8: chat graph test
      9: CallbackHandler test         10: md traces
     11: "Step 3" md                   12: imports  13: EmailState  14: nodes+LLM
     15: add edges                    16: compile  17: example emails
     18: run with Langfuse handler    19: "### Trace Structure" md
     20+: "## Online Evaluation" ... offline evaluation ... end
    """
    src = LF / "example_langgraph_agents.ipynb"
    nb = json.loads(src.read_text(encoding="utf-8"))
    cells = nb["cells"]

    # normalize the LLM init in the graph cells to workshop env vars
    import copy

    def envify_llm_cell(cell: dict) -> dict:
        c = copy.deepcopy(cell)
        if c.get("cell_type") != "code":
            return c
        c["source"] = [
            line.replace(
                'model = ChatOpenAI( model="gpt-4o",temperature=0)',
                "model = make_llm()  # env-var driven: OPENAI_MODEL / OPENAI_API_KEY / OPENAI_API_BASE",
            )
            for line in c["source"]
        ]
        return c

    graph_cells_env = [envify_llm_cell(c) for c in (cells[12], cells[13], cells[14], cells[15], cells[16], cells[17])]

    # --- graph notebook: install md + pip cell + workshop env + graph cells ---
    graph_nb_cells = [
        cells[1],   # "## Step 0: Install the Required Libraries"
        cells[2],   # %pip install ...
        workshop_env_cell(),
        make_llm_helper_cell(),
        *graph_cells_env,
        email_run_cell(),  # run the graph on both emails (no Langfuse)
    ]

    # --- observability notebook: full source flow ---
    obs_cells = [c.copy() for c in cells]

    def build_nb(cells_out: list[dict], dest_rel: str, level: str, title: str) -> Path:
        out = {
            "cells": [],
            "metadata": {
                "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                "language_info": {"name": "python", "version": "3.11"},
                "langgraph_workshop": {"level": level},
            },
            "nbformat": 4,
            "nbformat_minor": 5,
        }
        dest = REPO / "notebooks" / dest_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        # clear outputs
        for c in cells_out:
            if c.get("cell_type") == "code":
                c["outputs"] = []
                c["execution_count"] = None
        # header cell
        header = {
            "cell_type": "markdown",
            "metadata": {},
            "source": nb_header_md(
                dest_rel, level, title,
                "langfuse/langfuse-docs",
                "https://github.com/langfuse/langfuse-docs/blob/main/cookbook/example_langgraph_agents.ipynb",
            ),
        }
        out["cells"] = [header] + cells_out
        dest.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        return dest

    g = build_nb(
        graph_nb_cells,
        "level-3-email-agent/30_email_agent_graph.ipynb",
        "3",
        "Email Automation Agent — The Graph",
    )
    o = build_nb(
        obs_cells,
        "level-3-email-agent/31_email_agent_observability.ipynb",
        "3",
        "Email Automation Agent — Observability & Evaluation (Langfuse, optional)",
    )
    for dest, label in ((g, "graph part"), (o, "full source w/ evaluation")):
        rel = dest.relative_to(REPO).as_posix()
        PROVENANCE_ROWS.append(
            f"| `{rel}` | notebook | `langfuse/langfuse-docs` | [example_langgraph_agents.ipynb](https://github.com/langfuse/langfuse-docs/blob/main/cookbook/example_langgraph_agents.ipynb) | split ({label}), outputs cleared, workshop env cell added |"
        )


def email_run_cell() -> dict:
    """Run the compiled email graph on both sample emails (no Langfuse dependency)."""
    return {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": (
            "# Run the email agent on both sample emails\n"
            "print(\"\\nProcessing legitimate email...\")\n"
            "legitimate_result = compiled_graph.invoke(\n"
            "    input={\n"
            "        \"email\": legitimate_email,\n"
            "        \"is_spam\": None,\n"
            "        \"spam_reason\": None,\n"
            "        \"email_category\": None,\n"
            "        \"draft_response\": None,\n"
            "        \"messages\": [],\n"
            "    },\n"
            ")\n"
            "print(\"\\nProcessing spam email...\")\n"
            "spam_result = compiled_graph.invoke(\n"
            "    input={\n"
            "        \"email\": spam_email,\n"
            "        \"is_spam\": None,\n"
            "        \"spam_reason\": None,\n"
            "        \"email_category\": None,\n"
            "        \"draft_response\": None,\n"
            "        \"messages\": [],\n"
            "    },\n"
            ")\n"
            "print(\"\\n--- Legitimate email result ---\")\n"
            "print(\"is_spam:\", legitimate_result[\"is_spam\"])\n"
            "print(\"draft_response:\", legitimate_result.get(\"draft_response\", \"\")[:300])\n"
            "print(\"\\n--- Spam email result ---\")\n"
            "print(\"is_spam:\", spam_result[\"is_spam\"])\n"
        ),
    }


if __name__ == "__main__":
    main()
