import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _write_svg(path: Path, content: str):
    path.write_text(content, encoding="utf-8")


def _svg_header(width, height):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'


def _svg_footer():
    return "</svg>"


def _svg_bar_chart(title, labels, values, max_value, width=900, height=320):
    padding = 50
    chart_w = width - padding * 2
    chart_h = height - padding * 2
    bar_gap = 16
    bar_width = (chart_w - bar_gap * (len(values) - 1)) / max(1, len(values))
    lines = [_svg_header(width, height)]
    lines.append(f'<rect width="100%" height="100%" fill="#0b0c10"/>')
    lines.append(f'<text x="{padding}" y="{padding - 16}" fill="#ffffff" font-size="16" font-family="Arial">{title}</text>')
    for i, (label, value) in enumerate(zip(labels, values)):
        x = padding + i * (bar_width + bar_gap)
        h = 0 if max_value <= 0 else (value / max_value) * chart_h
        y = padding + (chart_h - h)
        lines.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{bar_width:.2f}" height="{h:.2f}" fill="#66fcf1"/>')
        lines.append(f'<text x="{x + bar_width/2:.2f}" y="{padding + chart_h + 18}" fill="#c5c6c7" font-size="12" text-anchor="middle" font-family="Arial">{label}</text>')
        lines.append(f'<text x="{x + bar_width/2:.2f}" y="{y - 6:.2f}" fill="#ffffff" font-size="12" text-anchor="middle" font-family="Arial">{value}</text>')
    lines.append(_svg_footer())
    return "\n".join(lines)


def _svg_line_chart(title, labels, values, max_value, width=900, height=320):
    padding = 50
    chart_w = width - padding * 2
    chart_h = height - padding * 2
    lines = [_svg_header(width, height)]
    lines.append(f'<rect width="100%" height="100%" fill="#0b0c10"/>')
    lines.append(f'<text x="{padding}" y="{padding - 16}" fill="#ffffff" font-size="16" font-family="Arial">{title}</text>')
    points = []
    for i, value in enumerate(values):
        x = padding + (i / max(1, len(values) - 1)) * chart_w
        h = 0 if max_value <= 0 else (value / max_value) * chart_h
        y = padding + (chart_h - h)
        points.append((x, y))
    if points:
        path = "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in points)
        lines.append(f'<path d="{path}" fill="none" stroke="#45a29e" stroke-width="3"/>')
        for (x, y), label, value in zip(points, labels, values):
            lines.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5" fill="#66fcf1"/>')
            lines.append(f'<text x="{x:.2f}" y="{padding + chart_h + 18}" fill="#c5c6c7" font-size="12" text-anchor="middle" font-family="Arial">{label}</text>')
            lines.append(f'<text x="{x:.2f}" y="{y - 8:.2f}" fill="#ffffff" font-size="12" text-anchor="middle" font-family="Arial">{value}</text>')
    lines.append(_svg_footer())
    return "\n".join(lines)


def _bar(value, max_value, width=24):
    if max_value <= 0:
        return ""
    filled = int(round((value / max_value) * width))
    filled = max(0, min(width, filled))
    return "[" + ("#" * filled) + ("-" * (width - filled)) + "]"


def _table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |"]
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        lines.append("| " + " | ".join(str(v) for v in row) + " |")
    return "\n".join(lines)


def _section(title, body):
    return f"**{title}**\n{body}"


def main():
    results_path = REPO_ROOT / "benchmarks" / "results" / "benchmark_results.json"
    if not results_path.exists():
        raise SystemExit("Run benchmarks first: python benchmarks/run_benchmarks.py")

    data = json.loads(results_path.read_text(encoding="utf-8"))
    report_lines = []

    report_lines.append("# RepoGraph Benchmark Report")
    report_lines.append("")
    report_lines.append(f"Source: `{results_path}`")
    report_lines.append("")

    agent = data.get("agent_comparison", {})
    diagnostics = data.get("diagnostics", {})
    results_dir = results_path.parent

    agent_repos = agent.get("repos", [])
    for repo in agent_repos:
        repo_name = repo.get("name", "repo")
        agent_rows = []
        for item in repo.get("results", []):
            agent_rows.append(
                (
                    item.get("query"),
                    item.get("baseline", {}).get("tokens_estimate"),
                    item.get("repograph", {}).get("tokens_estimate"),
                    item.get("savings", {}).get("token_reduction"),
                    item.get("savings", {}).get("read_time_reduction"),
                    item.get("repograph", {}).get("architecture_time_s"),
                    item.get("repograph", {}).get("connections_time_s"),
                )
            )
        agent_table = _table(
            [
                "query",
                "baseline_tokens",
                "repograph_tokens",
                "token_reduction",
                "read_time_reduction",
                "arch_time_s",
                "conn_time_s",
            ],
            agent_rows,
        )
        report_lines.append(_section(f"Agent Comparison ({repo_name})", agent_table))
        report_lines.append("")

        # Agent comparison charts per repo
        agent_labels = [r.get("query") for r in repo.get("results", [])]
        token_reduction_vals = [r.get("savings", {}).get("token_reduction", 0) for r in repo.get("results", [])]
        token_reduction_svg = _svg_bar_chart(
            f"Token Reduction ({repo_name})",
            agent_labels,
            token_reduction_vals,
            1.0,
        )
        token_reduction_path = results_dir / f"agent_token_reduction_{repo_name}.svg"
        _write_svg(token_reduction_path, token_reduction_svg)
        report_lines.append(f'![Agent Token Reduction {repo_name}]({token_reduction_path.as_posix()})')
        report_lines.append("")

        read_time_reduction_vals = [r.get("savings", {}).get("read_time_reduction", 0) for r in repo.get("results", [])]
        read_time_svg = _svg_bar_chart(
            f"Read Time Reduction ({repo_name})",
            agent_labels,
            read_time_reduction_vals,
            1.0,
        )
        read_time_path = results_dir / f"agent_read_time_reduction_{repo_name}.svg"
        _write_svg(read_time_path, read_time_svg)
        report_lines.append(f'![Agent Read Time Reduction {repo_name}]({read_time_path.as_posix()})')
        report_lines.append("")

        total_time_vals = [
            (r.get("repograph", {}).get("architecture_time_s", 0) + r.get("repograph", {}).get("connections_time_s", 0))
            for r in repo.get("results", [])
        ]
        total_time_svg = _svg_bar_chart(
            f"RepoGraph CLI Time ({repo_name})",
            agent_labels,
            total_time_vals,
            max(total_time_vals) if total_time_vals else 0,
        )
        total_time_path = results_dir / f"agent_cli_time_{repo_name}.svg"
        _write_svg(total_time_path, total_time_svg)
        report_lines.append(f'![Agent CLI Time {repo_name}]({total_time_path.as_posix()})')
        report_lines.append("")

    correctness = diagnostics.get("example_repo_correctness", {})
    correctness_table = _table(
        ["Metric", "Value"],
        [
            ("node_precision", correctness.get("node_precision")),
            ("node_recall", correctness.get("node_recall")),
            ("edge_precision", correctness.get("edge_precision")),
            ("edge_recall", correctness.get("edge_recall")),
            ("nodes_expected", correctness.get("nodes_expected")),
            ("nodes_actual", correctness.get("nodes_actual")),
            ("edges_expected", correctness.get("edges_expected")),
            ("edges_actual", correctness.get("edges_actual")),
        ],
    )
    report_lines.append(_section("Correctness", correctness_table))
    report_lines.append("")

    # Correctness chart
    correctness_labels = ["node_prec", "node_rec", "edge_prec", "edge_rec"]
    correctness_values = [
        correctness.get("node_precision", 0),
        correctness.get("node_recall", 0),
        correctness.get("edge_precision", 0),
        correctness.get("edge_recall", 0),
    ]
    correctness_svg = _svg_bar_chart(
        "Correctness (Precision/Recall)",
        correctness_labels,
        correctness_values,
        1.0,
    )
    correctness_path = results_dir / "correctness.svg"
    _write_svg(correctness_path, correctness_svg)
    report_lines.append(f'![Correctness]({correctness_path.as_posix()})')
    report_lines.append("")

    query_utility = diagnostics.get("query_utility", [])
    query_rows = []
    for item in query_utility:
        query_rows.append(
            (
                item.get("query"),
                item.get("hit_count"),
                item.get("expected_count"),
                item.get("recall"),
            )
        )
    report_lines.append(
        _section(
            "Query Utility",
            _table(["query", "hit", "expected", "recall"], query_rows),
        )
    )
    report_lines.append("")

    context = diagnostics.get("context_reduction", [])
    context_rows = []
    max_total = max((c.get("total_loc", 0) for c in context), default=0)
    for item in context:
        bar = _bar(item.get("selected_loc", 0), max_total)
        context_rows.append(
            (
                item.get("query"),
                item.get("selected_loc"),
                item.get("total_loc"),
                item.get("selected_ratio"),
                bar,
            )
        )
    report_lines.append(
        _section(
            "Context Reduction",
            _table(["query", "selected_loc", "total_loc", "ratio", "bar"], context_rows),
        )
    )
    report_lines.append("")

    # Context reduction chart
    context_labels = [c.get("query") for c in context]
    context_values = [c.get("selected_ratio") for c in context]
    context_svg = _svg_bar_chart(
        "Context Selected Ratio (Lower is Better)",
        context_labels,
        context_values,
        1.0,
    )
    context_path = results_dir / "context_reduction.svg"
    _write_svg(context_path, context_svg)
    report_lines.append(f'![Context Reduction]({context_path.as_posix()})')
    report_lines.append("")

    end_to_end = diagnostics.get("end_to_end", {})
    e2e_rows = []
    for item in end_to_end.get("results", []):
        e2e_rows.append(
            (
                item.get("task"),
                item.get("query"),
                item.get("recall"),
                item.get("selected_loc"),
                item.get("total_loc"),
                item.get("estimated_selected_read_min"),
                item.get("estimated_full_read_min"),
            )
        )
    e2e_table = _table(
        [
            "task",
            "query",
            "recall",
            "selected_loc",
            "total_loc",
            "est_selected_min",
            "est_full_min",
        ],
        e2e_rows,
    )
    assumptions = end_to_end.get("assumptions", {})
    report_lines.append(
        _section(
            "End To End",
            e2e_table
            + "\n\n"
            + f"Assumptions: read_wpm={assumptions.get('read_wpm')}, "
            + f"words_per_loc={assumptions.get('words_per_loc')}",
        )
    )
    report_lines.append("")

    # End-to-end time chart
    e2e_labels = [r.get("task") for r in end_to_end.get("results", [])]
    e2e_values = [r.get("estimated_selected_read_min") for r in end_to_end.get("results", [])]
    e2e_svg = _svg_bar_chart(
        "Estimated Reading Time (Selected Context, minutes)",
        e2e_labels,
        e2e_values,
        max(e2e_values) if e2e_values else 0,
    )
    e2e_path = results_dir / "end_to_end_time.svg"
    _write_svg(e2e_path, e2e_svg)
    report_lines.append(f'![End To End Time]({e2e_path.as_posix()})')
    report_lines.append("")

    perf = diagnostics.get("performance_scaling", [])
    perf_rows = []
    max_time = max((p.get("time_s", 0) for p in perf), default=0)
    for item in perf:
        bar = _bar(item.get("time_s", 0), max_time)
        perf_rows.append(
            (
                item.get("repo"),
                item.get("files"),
                item.get("funcs_per_file"),
                item.get("fanout"),
                item.get("nodes"),
                item.get("edges"),
                item.get("time_s"),
                bar,
            )
        )
    report_lines.append(
        _section(
            "Performance Scaling",
            _table(
                ["repo", "files", "funcs", "fanout", "nodes", "edges", "time_s", "bar"],
                perf_rows,
            ),
        )
    )
    report_lines.append("")

    # Performance chart
    perf_labels = [p.get("repo") for p in perf]
    perf_values = [p.get("time_s") for p in perf]
    perf_svg = _svg_line_chart(
        "Performance Scaling (seconds)",
        perf_labels,
        perf_values,
        max(perf_values) if perf_values else 0,
    )
    perf_path = results_dir / "performance_scaling.svg"
    _write_svg(perf_path, perf_svg)
    report_lines.append(f'![Performance Scaling]({perf_path.as_posix()})')
    report_lines.append("")

    out_path = REPO_ROOT / "benchmarks" / "results" / "benchmark_report.md"
    out_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Report written to: {out_path}")


if __name__ == "__main__":
    main()
