![Scrooge presentation image](ScroogeMcDuck.jpg)

# Scrooge

**Save millions of tokens. Understand any codebase in seconds.**

Scrooge scans a repository and builds a **function-level dependency graph** so AI agents and developers can instantly find the exact files and functions that matter — without reading the whole codebase and useless files.

Designed for AI coding tools like Claude Code. Available as a **CLI tool** and **MCP server**.

---

## The Problem

Modern AI coding tools burn through tokens reading thousands of lines of irrelevant code. Given a query like *"explain the run function"*, a classic keyword agent opens 6 files and sends **65,000+ tokens** to the model.

Most of that context is noise.

---

## The Result

Scrooge was benchmarked on [Brian2](https://github.com/brian-team/brian2), a large real-world neural simulator, against a classic keyword-based agent using Gemini 2.5 Flash.

**Query**: *"explain function run in brian2 simulator"*

![Benchmark chart: Scrooge vs Classic agent](benchmarks/results/benchmark_chart.png)

**Scrooge used 3.3× fewer tokens** and opened 3× fewer files — while producing an equally accurate, more detailed answer.

See the full agent responses comparison side by side: [brian_benchmark_output.md](brian_benchmark_output.md)


### How to reproduce

Classic agent:
```bash
python benchmarks/gemini_agent_benchmark.py --agents classic --agent-flow agent
```

Scrooge agent:
```bash
python benchmarks/gemini_agent_benchmark.py --agents scrooge --agent-flow agent --rank-keep-pct 0.4 --arch-filter connections
```

---

## Why it works

Instead of keyword-matching filenames, Scrooge builds a **structural graph of the repository**:

* which functions call which
* how modules depend on each other
* which symbols are most central to a query

Given a query, Scrooge ranks nodes by relevance and returns only the **key entry points** — the 2–3 files that actually contain the answer. The AI reads those, not everything.

### Smart query flow

Scrooge matches queries by **substring against code identifiers** (function names, class names, file names). To get the best results, the AI agent doesn't pass the user's raw question — it first **extracts keywords** that are likely to match symbol names in the codebase:

```
User: "how does the authentication flow work?"
         ↓
   LLM extracts keywords
         ↓
Scrooge query: "auth login authenticate user"
         ↓
   Matches: auth.py → authenticate(), login_user()
```

This keyword extraction step is built into the MCP tool descriptions, so AI agents like Claude Code automatically distill natural-language questions into symbol-oriented search terms before calling Scrooge.

At scale, across hundreds of agent runs, this saves **millions of tokens**.

---

## Example

```python
def login(user):
    authenticate(user)

def authenticate(user):
    get_user(user)

def get_user(user):
    pass
```

Scrooge builds:

```
login → authenticate → get_user
```

Query: *"what does login touch?"*
Scrooge returns: `auth.py` with `login`, `authenticate`, `get_user` — not every file in the repo.

---

## Features

* Function-level dependency graph
* Call graph generation
* Symbol ranking by query relevance
* `architecture` command — find symbols matching a query
* `connections` command — trace call paths around matched symbols
* Compact output mode (`--compact`) for minimal token footprint
* **MCP server** — plug directly into Claude Code and other AI agents
* **Python** — full AST parsing; JS/TS file scanning (parsers coming soon)

---

## How to Use

Scrooge has two modes. Pick the one that fits your workflow.

### As MCP Server (recommended)

This is the hands-off mode. After a one-time setup, **you don't do anything differently** — Claude Code uses Scrooge automatically behind the scenes.

1. Install Scrooge and add it to your Claude Code settings (see [Installation](#installation) and [MCP Setup](#setup-as-mcp-server-claude-code) below)
2. Restart Claude Code
3. Just use Claude Code as you normally would

That's it. When you ask Claude something like *"explain how authentication works in this repo"*, it will **automatically** call Scrooge's `architecture` tool instead of reading dozens of files. Scrooge returns only the 2–3 most relevant files, so Claude reads less, responds faster, and costs fewer tokens.

You don't need to mention Scrooge or change how you prompt — Claude sees the tools and decides when to use them.

### As CLI

Use this to explore a codebase from your terminal, or to integrate Scrooge into your own scripts and pipelines.

```bash
# Which files matter for "login"?
scrooge architecture path/to/repo login

# What does "login" call, and what calls it?
scrooge connections path/to/repo login 2
```

The output is JSON — designed to be piped into other tools or fed to an LLM as context.

---

## Installation

### Prerequisites

- **Python 3.11+** — check with `python --version`
- **Git** — to clone the repository
- **uv** (recommended) — install from [docs.astral.sh/uv](https://docs.astral.sh/uv/)

### Clone and install

```bash
git clone https://github.com/De-Cri/Scrooge.git
cd Scrooge
```

**With uv (recommended):**
```bash
uv pip install -e .
```

**With pip + venv:**
```bash
python -m venv .venv
```
Then activate the virtual environment:
- macOS / Linux: `source .venv/bin/activate`
- Windows (PowerShell): `.\.venv\Scripts\Activate.ps1`
- Windows (cmd): `.venv\Scripts\activate.bat`

```bash
pip install -e .
```

That's it! Both the **CLI** (`scrooge`) and the **MCP server** (`scrooge-mcp`) are installed.

---

## Setup as MCP Server (Claude Code)

Scrooge exposes its graph as an **MCP tool**, so AI agents like Claude Code can query it natively — calling `architecture`, `connections`, and `index` instead of reading entire files.

Open (or create) your Claude Code settings file:

| OS | Path |
|---|---|
| macOS / Linux | `~/.claude/settings.json` |
| Windows | `%USERPROFILE%\.claude\settings.json` |

Add the `Scrooge` MCP server inside the `mcpServers` block.

**With uv (recommended):**
```json
{
  "mcpServers": {
    "Scrooge": {
      "command": "uv",
      "args": ["run", "--directory", "SCROOGE_PATH", "scrooge-mcp"]
    }
  }
}
```

Replace `SCROOGE_PATH` with the absolute path to your Scrooge folder (e.g., `/home/yourname/Scrooge` or `C:/Users/yourname/Desktop/Scrooge`).

**Without uv (using venv python directly):**

macOS / Linux:
```json
{
  "mcpServers": {
    "Scrooge": {
      "command": "/home/yourname/Scrooge/.venv/bin/python",
      "args": ["-m", "mcp_server.scrooge_mcp"],
      "cwd": "/home/yourname/Scrooge"
    }
  }
}
```

Windows:
```json
{
  "mcpServers": {
    "Scrooge": {
      "command": "C:/Users/yourname/Desktop/Scrooge/.venv/Scripts/python.exe",
      "args": ["-m", "mcp_server.scrooge_mcp"],
      "cwd": "C:/Users/yourname/Desktop/Scrooge"
    }
  }
}
```

After saving, **restart Claude Code**. The Scrooge tools (`architecture`, `connections`, `index`) will appear automatically and Claude will use them when exploring codebases.

### Verify it works

In Claude Code, ask something like:

> *"Use the architecture tool to find the main entry points of this repo"*

If Scrooge is configured correctly, Claude will call the MCP tool instead of reading files manually.

---

## CLI Usage

### `architecture`

Find candidate files matching a query, ranked by relevance with their call connections:

```bash
scrooge architecture path/to/repo login
```

```json
{
  "candidates": [
    {
      "file": "auth.py",
      "relevance": 100,
      "calls": ["auth.audit_login", "auth.store_audit_entry"],
      "called_by": ["auth.audit_login", "auth.login_user"]
    }
  ]
}
```

### `connections`

Trace call paths around matched symbols:

```bash
scrooge connections path/to/repo login 2
```

```json
{
  "matched_nodes": ["auth.audit_login", "auth.login_user"],
  "ranked_nodes": ["auth.login_user", "auth.audit_login", "utils.normalize_username"],
  "connections": [
    { "from": "auth.audit_login", "to": "auth.store_audit_entry", "type": "calls", "depth": 1 },
    { "from": "auth.login_user", "to": "auth.audit_login", "type": "calls", "depth": 1 },
    { "from": "auth.login_user", "to": "utils.normalize_username", "type": "calls", "depth": 2 }
  ]
}
```

Compact output (fewer tokens):

```bash
scrooge connections path/to/repo login 2 --compact
```

```json
{
  "n": ["auth.audit_login", "auth.login_user"],
  "rn": ["auth.login_user", "auth.audit_login", "utils.normalize_username"],
  "e": [
    ["auth.audit_login", "auth.store_audit_entry", 1],
    ["auth.login_user", "auth.audit_login", 1],
    ["auth.login_user", "utils.normalize_username", 2]
  ]
}
```

---

## Architecture

```
repo
 └── Scanner        → finds all source files
      └── Parser    → extracts functions, calls, relationships
           └── Graph Builder  → builds dependency graph (NetworkX)
                └── Ranker    → scores nodes by query relevance
                     └── CLI / MCP  → returns minimal context to the agent
```

---

## Project Structure

```
Scrooge/
│
├── scanner/
│   └── scanner.py               # find all source files in the repo
│
├── parser/
│   └── ast_parser.py            # extract classes, methods, functions
│
├── indexer/
│   └── symbol_extractor.py      # symbol → file/line mapping
│
├── graph_builder/
│   ├── call_graph.py            # build the call graph
│   └── symbols_connections.py   # track connections between symbols
│
├── intelligence/
│   └── rank_graph_connections.py # rank nodes by relevance (PageRank + distance)
│
├── output/
│   └── output_writer.py         # format and write graph output
│
├── cli/
│   └── scrooge_cli.py           # CLI interface
│
├── mcp_server/
│   └── scrooge_mcp.py           # MCP server for AI agents
│
└── benchmarks/
    ├── gemini_agent_benchmark.py # benchmark vs classic keyword search
    └── bench_utils.py            # shared benchmark utilities
```

---

## Vision

Scrooge is the **structural memory layer for AI coding agents**.

Instead of reading entire repositories, agents:

1. Query the dependency graph
2. Get back only the relevant symbols and files
3. Read 2–3 files instead of 20
4. Reason about impact before editing

At the scale of real development — thousands of agent calls per day — this translates to **millions of tokens saved per project**, faster responses, and lower costs.

---

## Contributing

Contributions welcome. Open an issue or PR for:

* additional language parsers
* graph visualization
* AI agent integrations
* MCP improvements

---

## License

MIT
