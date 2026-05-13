# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Identity

Personal learning exercise based on [Datawhale Hello-Agents](https://github.com/datawhalechina/hello-agents). Code and prompts are in Chinese. Academic/teaching quality — not production-grade.

## Architecture

5 chapters, each with its own `README.md`. The root `README.md` is a hub pointing to them.

- **Ch1** `1_Introduction_to_Agents/` — LLM-driven travel agent (Thought-Action-Observation loop). Requires LLM API + Tavily key.
- **Ch2** `2_History_of_Agents/` — ELIZA rule-based chatbot. Zero dependencies, no API keys.
- **Ch3** `3_Fundamentals_of_LLMs/` — N-gram, BPE tokenizer, word embeddings, Transformer from scratch, calling a local Qwen model.
- **Ch4** `4_Agent_Classical_Paradigm_Construction/` — ReAct, Plan-and-Solve, Reflection agents. All share `llm_client.py` (OpenAI-compatible client `HelloAgentsLLM`) and `tools.py` (`calculate` + `search` via SerpApi). Must `cd` into this directory to run because of local imports.
- **Ch5** `5_Building_Agents_with_Low_Code_Platforms/` — Dify workflow exports (`.yml`, `.zip`) and an n8n workflow (`.json`). No Python code.

Recommended reading order: Ch2 → Ch3 → Ch1 → Ch4 → Ch5 (zero-dependency first, API-heavy later).

## Environment

Python 3.10+. Create `venv` at project root:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Key packages: `openai`, `python-dotenv`, `requests`, `tavily-python`, `google-search-results` (serpapi), `torch`, `modelscope`.

`.env` files go in the chapter directory that needs them (Ch1, Ch4). Template at `4_Agent_Classical_Paradigm_Construction/.env.example`. Never commit `.env` — it's in `.gitignore`.

## Git Conventions

Commit messages in English, imperative mood. When using the Bash tool for `git commit`, use `-m "message"` — do NOT use PowerShell here-strings (`@'...'@`), as they leak `@` artifacts into the message when run under Bash.

If API keys are accidentally committed, use `git filter-branch --index-filter` to purge the file from all history, then `git push --force`. Clean up with `git reflog expire --expire=now --all && git gc --aggressive --prune=now`.

## File Naming

Some filenames contain spaces (e.g., `Call LLM.py`, `超级智能个人助手.yml`). Quote them in commands.
