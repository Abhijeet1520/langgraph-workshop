# Provenance — where every notebook/doc came from

This repo teaches with material migrated from other repositories (with permission of their licenses).
Each migrated file carries a source header; this table is the full mapping. Sources are pinned
to the commits listed below so later updates can be diffed cleanly.

## Source repositories (pinned)

| Source repo | Local path | Pinned commit | License |
|---|---|---|---|
| [Abhijeet1520/LangGraph-Basics](https://github.com/Abhijeet1520/LangGraph-Basics) | `tools/harness/langgraph-docs/LangGraph Basics` | `ff39740` | MIT |
| [snehotosh/langgraph-notebooks](https://github.com/snehotosh/langgraph-notebooks) | `tools/harness/langgraph-docs/langgraph-notebooks` | `999d6e6` | (check repo) |
| [iamvaibhavmehra/LangGraph-Course-freeCodeCamp](https://github.com/iamvaibhavmehra/LangGraph-Course-freeCodeCamp) | `tools/harness/langgraph-docs/LangGraph-Course-freeCodeCamp` | `9f172bf` | (check repo) |
| [langfuse/langfuse-docs](https://github.com/langfuse/langfuse-docs) | `tools/harness/langgraph-docs/langfuse-docs` | `3441a24` | CC-BY (docs) |

## File mapping

| Workshop file | Type | Source repo | Source file | Transformations |
|---|---|---|---|---|
| `docs/levels/level-0-setup/task1-setup.md` | doc | `Abhijeet1520/LangGraph-Basics` | [`docs/task1-setup.md`](https://github.com/Abhijeet1520/LangGraph-Basics/blob/main/docs/task1-setup.md) | verbatim |
| `docs/levels/level-1-basics/task2-sequential-vs-stateful.md` | doc | `Abhijeet1520/LangGraph-Basics` | [`docs/task2-sequential-vs-stateful.md`](https://github.com/Abhijeet1520/LangGraph-Basics/blob/main/docs/task2-sequential-vs-stateful.md) | verbatim |
| `docs/levels/level-1-basics/task3-stategraph.md` | doc | `Abhijeet1520/LangGraph-Basics` | [`docs/task3-stategraph.md`](https://github.com/Abhijeet1520/LangGraph-Basics/blob/main/docs/task3-stategraph.md) | verbatim |
| `docs/levels/level-1-basics/task4-nodes.md` | doc | `Abhijeet1520/LangGraph-Basics` | [`docs/task4-nodes.md`](https://github.com/Abhijeet1520/LangGraph-Basics/blob/main/docs/task4-nodes.md) | verbatim |
| `docs/levels/level-1-basics/task5-edges-routing.md` | doc | `Abhijeet1520/LangGraph-Basics` | [`docs/task5-edges-routing.md`](https://github.com/Abhijeet1520/LangGraph-Basics/blob/main/docs/task5-edges-routing.md) | verbatim |
| `docs/levels/level-1-basics/task6-loops.md` | doc | `Abhijeet1520/LangGraph-Basics` | [`docs/task6-loops.md`](https://github.com/Abhijeet1520/LangGraph-Basics/blob/main/docs/task6-loops.md) | verbatim |
| `docs/levels/level-2-tools-memory-capstone/task7-tools.md` | doc | `Abhijeet1520/LangGraph-Basics` | [`docs/task7-tools.md`](https://github.com/Abhijeet1520/LangGraph-Basics/blob/main/docs/task7-tools.md) | verbatim |
| `docs/levels/level-2-tools-memory-capstone/task8-memory.md` | doc | `Abhijeet1520/LangGraph-Basics` | [`docs/task8-memory.md`](https://github.com/Abhijeet1520/LangGraph-Basics/blob/main/docs/task8-memory.md) | verbatim |
| `docs/levels/level-2-tools-memory-capstone/task9-research-assistant.md` | doc | `Abhijeet1520/LangGraph-Basics` | [`docs/task9-research-assistant.md`](https://github.com/Abhijeet1520/LangGraph-Basics/blob/main/docs/task9-research-assistant.md) | verbatim |
| `notebooks/level-1-basics/01_introduction.ipynb` | notebook | `snehotosh/langgraph-notebooks` | [original](https://github.com/snehotosh/langgraph-notebooks/blob/main/1_introduction.ipynb) | outputs cleared, header added, env-var LLM config |
| `notebooks/level-1-basics/02_simple_graph.ipynb` | notebook | `snehotosh/langgraph-notebooks` | [original](https://github.com/snehotosh/langgraph-notebooks/blob/main/2_simple_graph.ipynb) | outputs cleared, header added, env-var LLM config |
| `notebooks/level-1-basics/03_more_on_states.ipynb` | notebook | `snehotosh/langgraph-notebooks` | [original](https://github.com/snehotosh/langgraph-notebooks/blob/main/7_more_on_states.ipynb) | outputs cleared, header added, env-var LLM config |
| `notebooks/level-1-basics/04_chat_tool_graph.ipynb` | notebook | `snehotosh/langgraph-notebooks` | [original](https://github.com/snehotosh/langgraph-notebooks/blob/main/3_build_chat_tool_graph.ipynb) | outputs cleared, header added, env-var LLM config |
| `notebooks/level-1-basics/05_basic_agent.ipynb` | notebook | `snehotosh/langgraph-notebooks` | [original](https://github.com/snehotosh/langgraph-notebooks/blob/main/4_BasicAgent.ipynb) | outputs cleared, header added, env-var LLM config |
| `notebooks/level-1-basics/06_agent_memory_checkpointing.ipynb` | notebook | `snehotosh/langgraph-notebooks` | [original](https://github.com/snehotosh/langgraph-notebooks/blob/main/5_BasicAgent-with-memory-checkpointing.ipynb) | outputs cleared, header added, env-var LLM config |
| `notebooks/level-1-basics/07_controllability_breakpoints_timetravel.ipynb` | notebook | `snehotosh/langgraph-notebooks` | [original](https://github.com/snehotosh/langgraph-notebooks/blob/main/9_controllability-breakpoints-and-timetravel.ipynb) | outputs cleared, header added, env-var LLM config |
| `notebooks/level-1-basics/08_parallelization_subgraph.ipynb` | notebook | `snehotosh/langgraph-notebooks` | [original](https://github.com/snehotosh/langgraph-notebooks/blob/main/10_controllability- parallelization_subgraph.ipynb) | outputs cleared, header added, env-var LLM config |
| `notebooks/level-1-basics/09_more_on_messages.ipynb` | notebook | `snehotosh/langgraph-notebooks` | [original](https://github.com/snehotosh/langgraph-notebooks/blob/main/6_more_on_messages.ipynb) | outputs cleared, header added, env-var LLM config |
| `notebooks/level-1-basics/10_chatbot_summarization_stream.ipynb` | notebook | `snehotosh/langgraph-notebooks` | [original](https://github.com/snehotosh/langgraph-notebooks/blob/main/8_build_chatbot_summarization_and_stream.ipynb) | outputs cleared, header added, env-var LLM config |
| `notebooks/level-2-tools-memory-capstone/11_research_assistant.ipynb` | notebook | `snehotosh/langgraph-notebooks` | [original](https://github.com/snehotosh/langgraph-notebooks/blob/main/11_build_research_assistant.ipynb) | outputs cleared, header added, env-var LLM config |
| `notebooks/level-2-tools-memory-capstone/12_memory.ipynb` | notebook | `snehotosh/langgraph-notebooks` | [original](https://github.com/snehotosh/langgraph-notebooks/blob/main/12_memory.ipynb) | outputs cleared, header added, env-var LLM config |
| `notebooks/level-2-tools-memory-capstone/13_memory_profile_collection.ipynb` | notebook | `snehotosh/langgraph-notebooks` | [original](https://github.com/snehotosh/langgraph-notebooks/blob/main/13_memory_with_profile-and-collection.ipynb) | outputs cleared, header added, env-var LLM config |
| `notebooks/level-2-tools-memory-capstone/14_chatbot_agent.ipynb` | notebook | `snehotosh/langgraph-notebooks` | [original](https://github.com/snehotosh/langgraph-notebooks/blob/main/14_Building_Chatbot_Agent.ipynb) | outputs cleared, header added, env-var LLM config |
| `notebooks/level-3-email-agent/30_email_agent_graph.ipynb` | notebook | `langfuse/langfuse-docs` | [example_langgraph_agents.ipynb](https://github.com/langfuse/langfuse-docs/blob/main/cookbook/example_langgraph_agents.ipynb) | split (graph part), outputs cleared, workshop env cell added |
| `notebooks/level-3-email-agent/31_email_agent_observability.ipynb` | notebook | `langfuse/langfuse-docs` | [example_langgraph_agents.ipynb](https://github.com/langfuse/langfuse-docs/blob/main/cookbook/example_langgraph_agents.ipynb) | split (full source w/ evaluation), outputs cleared, workshop env cell added |

## Workshop originals

| Workshop file | Type | Source repo | Source file | Transformations |
|---|---|---|---|---|
| `notebooks/level-0-setup/00_welcome_and_verify.ipynb` | notebook | NEW (workshop original) | — | written for this repo |
| `notebooks/level-4-real-inbox/40_connect_your_inbox.ipynb` | notebook | NEW (workshop original) | — | written for this repo |

## Update policy

To pull updates from a source repo: bump its pinned commit above, re-run
`python3 scripts/migrate_sources.py` (from repo root), and review the diff. The script is
idempotent and never edits files under `site/`.
