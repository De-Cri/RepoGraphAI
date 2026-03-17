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
python benchmarks/gemini_agent_benchmark.py --agents repograph --agent-flow agent --rank-keep-pct 0.4 --arch-filter connections
```

---

## Why it works

Instead of keyword-matching filenames, Scrooge builds a **structural graph of the repository**:

* which functions call which
* how modules depend on each other
* which symbols are most central to a query

Given a query, Scrooge ranks nodes by relevance and returns only the **key entry points** — the 2–3 files that actually contain the answer. The AI reads those, not everything.

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
* **All programming languages** — Python, TypeScript, JavaScript, Go, Java, and more

---

## Installation

```bash
git clone https://github.com/yourname/repograph
cd repograph
python -m venv .venv
source .venv/bin/activate
pip install typer networkx
```

---

## CLI Usage

Index a repository:

```bash
python cli.py index path/to/repository
```

### `architecture`

Find all symbols matching a query:

```bash
python cli/repograph_cli.py architecture path/to/repo login
```

```json
{
  "auth.py": {
    "functions": ["login_user", "audit_login"]
  },
  "auth_service.py": {
    "classes": {
      "AuthService": {
        "methods": ["authenticate"]
      }
    }
  }
}
```

### `connections`

Trace call paths around matched symbols:

```bash
python cli/repograph_cli.py connections path/to/repo login 2
```

```json
{
  "matched_nodes": ["auth.login_user"],
  "connections": [
    { "from": "auth.login_user", "to": "utils.normalize_username", "type": "calls", "depth": 1 },
    { "from": "auth.login_user", "to": "models.AuthService.issue_token", "type": "calls", "depth": 1 }
  ]
}
```

Compact output (fewer tokens):

```bash
python cli/repograph_cli.py connections path/to/repo login 2 --compact
```

```json
{
  "n": ["auth.login_user"],
  "e": [
    ["auth.login_user", "utils.normalize_username", 1],
    ["auth.login_user", "models.AuthService.issue_token", 1]
  ]
}
```

---

## MCP Server

Scrooge exposes its graph as an **MCP tool**, so AI agents can query it natively.

Add it to your Claude Code config and agents will automatically call `repograph.connections` or `repograph.architecture` instead of reading entire files.

```json
{
  "mcpServers": {
    "repograph": {
      "command": "python",
      "args": ["server/api.py", "--repo", "path/to/repo"]
    }
  }
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
repograph/
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
│   ├── architecture_detector.py  # match symbols to a query
│   └── rank_graph_connections.py # rank nodes by relevance
│
├── output/
│   └── output_writer.py         # format and write graph output
│
├── cli/
│   └── repograph_cli.py         # CLI interface
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
