# Benchmarks for RepoGraph

This folder contains an automated benchmark suite that evaluates RepoGraph on:

- Agent comparison (baseline repo scan vs RepoGraph CLI for time + token estimate)
- Correctness (nodes + edges vs expected graph on `example_repo`)
- Query utility (symbol matches for real queries)
- Context reduction (how much code is filtered out by queries)
- Performance scaling (time vs repo size on synthetic repos)

## How To Run

From the repo root:

```bash
python benchmarks/run_benchmarks.py
```

Results are printed to stdout and saved to:

`benchmarks/results/benchmark_results.json`

Generate a markdown report:

```bash
python benchmarks/report.py
```

The report is saved to:

`benchmarks/results/benchmark_report.md`

SVG charts are saved to:

- `benchmarks/results/agent_token_reduction_<repo>.svg`
- `benchmarks/results/agent_read_time_reduction_<repo>.svg`
- `benchmarks/results/agent_cli_time_<repo>.svg`
- `benchmarks/results/correctness.svg`
- `benchmarks/results/context_reduction.svg`
- `benchmarks/results/end_to_end_time.svg`
- `benchmarks/results/performance_scaling.svg`

## What The Benchmarks Mean

- `example_repo_correctness`: precision/recall of nodes and edges compared to the expected ground-truth graph.
- `query_utility`: recall for a few representative queries (`login`, `profile`, `email`).
- `context_reduction`: percentage of LOC selected by the query vs total LOC in `example_repo`.
- `performance_scaling`: time to parse + build graph on synthetic repos of increasing size.
- `end_to_end`: task-level recall plus estimated reading time saved by using RepoGraph filtering.
- `agent_comparison`: baseline vs RepoGraph CLI for token estimates, read-time estimates, and CLI runtime.

## Notes

- The expected graph for `example_repo` lives in `benchmarks/fixtures/expected_example_repo.json`.
- Synthetic repos are created under `benchmarks/tmp/` and can be deleted safely.
- End-to-end time uses a simple estimate based on words per line and reading speed.
- Token estimates use a simple chars-per-token heuristic.

## Real Repos

To benchmark real repositories, copy `benchmarks/real_repos.sample.json` to
`benchmarks/real_repos.json` and edit the paths + queries.

If `benchmarks/real_repos.json` exists, it will be used. Otherwise the benchmark
falls back to `example_repo`.
