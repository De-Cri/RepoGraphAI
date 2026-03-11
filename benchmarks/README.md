# Benchmarks for RepoGraph

This folder contains an automated benchmark suite that evaluates RepoGraph on:

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

## What The Benchmarks Mean

- `example_repo_correctness`: precision/recall of nodes and edges compared to the expected ground-truth graph.
- `query_utility`: recall for a few representative queries (`login`, `profile`, `email`).
- `context_reduction`: percentage of LOC selected by the query vs total LOC in `example_repo`.
- `performance_scaling`: time to parse + build graph on synthetic repos of increasing size.
- `end_to_end`: task-level recall plus estimated reading time saved by using RepoGraph filtering.

## Notes

- The expected graph for `example_repo` lives in `benchmarks/fixtures/expected_example_repo.json`.
- Synthetic repos are created under `benchmarks/tmp/` and can be deleted safely.
- End-to-end time uses a simple estimate based on words per line and reading speed.
