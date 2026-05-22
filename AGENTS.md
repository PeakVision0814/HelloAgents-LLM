# Repository Guidelines

## Project Structure & Module Organization
This repository is a chapter-based learning project adapted from Hello-Agents. Root files such as `README.md`, `requirements.txt`, and `llm_clients.py` provide the main entry points and shared LLM configuration. Chapters `1_` through `6_` are mostly standalone teaching demos. `7_Building_Your_Agent_Framework/` is the most code-heavy area and contains both runnable examples (`my_*.py`) and the reusable `hello_agents/` package.

## Build, Test, and Development Commands
Use Python 3.10+.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Run a chapter script directly from the repo root, for example:

```bash
python "3_Fundamentals_of_LLMs\Call LLM.py"
python 1_Introduction_to_Agents\travel_agent.py
python 7_Building_Your_Agent_Framework\test_my_calculator.py
```

For Chapter 7 pytest-style checks, use `pytest 7_Building_Your_Agent_Framework -q` if `pytest` is available locally.

## Coding Style & Naming Conventions
Follow existing teaching-oriented Python style: 4-space indentation, readable control flow, and simple single-file execution. Keep comments, printed output, and user-facing text primarily in Chinese to match the repository. Reuse `llm_clients.py` for shared model setup instead of duplicating environment-loading logic. Existing files include spaces and mixed naming; when adding new files, prefer `snake_case.py` and avoid spaces.

## Testing Guidelines
There is no unified test suite for the whole repo. Validate changes by running the specific script you touched. For framework code in Chapter 7, add or update `test_*.py` files near the related module. If a script depends on external APIs, state clearly when it was not executed because keys or network access were unavailable.

## Commit & Pull Request Guidelines
Recent history uses Conventional Commit prefixes such as `feat:` and `fix:`. Keep messages short and scoped, for example `feat: add Gemini config example`. Pull requests should summarize the affected chapter, list behavior or dependency changes, and mention any `.env.example` or `README.md` updates. Include screenshots only when changing visual tools or exported workflow assets.

## Security & Configuration Tips
Store secrets in the root `.env` and never commit real API keys. Use `.env.example` as the template. If you change runtime behavior, also update the relevant chapter `README.md` or the root `README.md`.
