from __future__ import annotations

import csv
import html
import math
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT / "src"
RESULTS_DIR = ROOT / "results"
BUILD_DIR = RESULTS_DIR / "build" / "classes"
RAW_DIR = RESULTS_DIR / "raw-data"
CHART_DIR = RESULTS_DIR / "charts"
CSV_PATH = RAW_DIR / "benchmark_results.csv"

INPUT_SIZES = [5000, 10000, 30000, 50000, 70000, 100000]
ALGORITHMS = [
    ("FibonacciSequence", "Fibonacci Sequence"),
    ("Factorial", "Factorial"),
    ("BinarySearch", "Binary Search"),
    ("FastExponentiation", "Fast Exponentiation"),
]
METHODS = ["Recursive", "Iterative"]
COLORS = {
    "Recursive": "#c2410c",
    "Iterative": "#0f766e",
}


def ensure_directories() -> None:
    for directory in (BUILD_DIR, RAW_DIR, CHART_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def compile_sources() -> None:
    ensure_directories()
    source_files = sorted(str(path) for path in SRC_DIR.glob("*.java"))
    if not source_files:
        raise FileNotFoundError(f"No Java files found in {SRC_DIR}")

    subprocess.run(
        ["javac", "-d", str(BUILD_DIR), *source_files],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )


def run_java_program(class_name: str, num_runs: int, timeout_seconds: int = 600) -> str:
    completed = subprocess.run(
        ["java", "-cp", str(BUILD_DIR), class_name],
        cwd=ROOT,
        input=f"{num_runs}\n",
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
        check=True,
    )

    stdout_path = RAW_DIR / f"{class_name}_stdout.txt"
    stdout_path.write_text(completed.stdout, encoding="utf-8")
    return completed.stdout


def parse_benchmark_output(class_name: str, algorithm_label: str, num_runs: int, stdout: str) -> list[dict]:
    pattern = re.compile(r"(Recursive|Iterative).*?of\s+(\d+):\s+(-?\d+)")
    rows: list[dict] = []

    for method, input_size, avg_time_ns in pattern.findall(stdout):
        avg_time = int(avg_time_ns)
        rows.append(
            {
                "algorithm_class": class_name,
                "algorithm_label": algorithm_label,
                "method": method,
                "input_size": int(input_size),
                "avg_time_ns": avg_time,
                "status": "stack_overflow" if avg_time < 0 else "ok",
                "num_runs": num_runs,
            }
        )

    expected_rows = len(INPUT_SIZES) * len(METHODS)
    if len(rows) != expected_rows:
        raise ValueError(
            f"Expected {expected_rows} benchmark rows for {class_name}, found {len(rows)}.\n"
            f"Program output was:\n{stdout}"
        )

    rows.sort(key=lambda row: (row["method"], row["input_size"]))
    return rows


def save_results_csv(rows: list[dict], csv_path: Path = CSV_PATH) -> Path:
    ensure_directories()
    fieldnames = [
        "algorithm_class",
        "algorithm_label",
        "method",
        "input_size",
        "avg_time_ns",
        "status",
        "num_runs",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return csv_path


def load_results(csv_path: Path = CSV_PATH) -> list[dict]:
    with csv_path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = []
        for row in reader:
            rows.append(
                {
                    "algorithm_class": row["algorithm_class"],
                    "algorithm_label": row["algorithm_label"],
                    "method": row["method"],
                    "input_size": int(row["input_size"]),
                    "avg_time_ns": int(row["avg_time_ns"]),
                    "status": row["status"],
                    "num_runs": int(row["num_runs"]),
                }
            )
    return rows


def run_all_benchmarks(num_runs: int = 10, timeout_seconds: int = 600) -> list[dict]:
    compile_sources()
    all_rows: list[dict] = []
    for class_name, algorithm_label in ALGORITHMS:
        stdout = run_java_program(class_name, num_runs, timeout_seconds=timeout_seconds)
        all_rows.extend(parse_benchmark_output(class_name, algorithm_label, num_runs, stdout))
    save_results_csv(all_rows)
    return all_rows


def rows_for_algorithm(rows: list[dict], algorithm_label: str) -> list[dict]:
    return [row for row in rows if row["algorithm_label"] == algorithm_label]


def row_lookup(rows: list[dict], algorithm_label: str, method: str, input_size: int) -> dict | None:
    for row in rows:
        if (
            row["algorithm_label"] == algorithm_label
            and row["method"] == method
            and row["input_size"] == input_size
        ):
            return row
    return None


def format_ns(value: int) -> str:
    if value < 0:
        return "overflow"
    return f"{value:,}"


def input_label(value: int) -> str:
    return f"{value // 1000}k" if value >= 1000 else str(value)


def value_label(value: float) -> str:
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}B"
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"{value / 1_000:.1f}K"
    return f"{value:.0f}"


def safe_log10(value: int) -> float:
    return math.log10(max(1, value))


def pairwise(values: list[tuple[float, float]]) -> list[tuple[tuple[float, float], tuple[float, float]]]:
    return list(zip(values, values[1:]))


def summary_markdown(rows: list[dict]) -> str:
    lines = [
        "| Algorithm | Method | 5k | 10k | 30k | 50k | 70k | 100k |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for algorithm_label in [label for _, label in ALGORITHMS]:
        for method in METHODS:
            values = []
            for size in INPUT_SIZES:
                row = row_lookup(rows, algorithm_label, method, size)
                values.append(format_ns(row["avg_time_ns"]) if row else "n/a")
            lines.append(
                f"| {algorithm_label} | {method} | " + " | ".join(values) + " |"
            )
    return "\n".join(lines)


def summary_html(rows: list[dict]) -> str:
    table_rows = [
        "<table>",
        "<thead><tr><th>Algorithm</th><th>Method</th>"
        + "".join(f"<th>{html.escape(input_label(size))}</th>" for size in INPUT_SIZES)
        + "</tr></thead>",
        "<tbody>",
    ]
    for algorithm_label in [label for _, label in ALGORITHMS]:
        for method in METHODS:
            cells = []
            for size in INPUT_SIZES:
                row = row_lookup(rows, algorithm_label, method, size)
                cells.append(f"<td>{html.escape(format_ns(row['avg_time_ns']) if row else 'n/a')}</td>")
            table_rows.append(
                f"<tr><td>{html.escape(algorithm_label)}</td><td>{html.escape(method)}</td>"
                + "".join(cells)
                + "</tr>"
            )
    table_rows.append("</tbody></table>")
    return "\n".join(table_rows)


def write_svg(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    return path


def chart_title_block(title: str, subtitle: str, x: int = 60, y: int = 44) -> str:
    return (
        f'<text x="{x}" y="{y}" font-size="26" font-weight="700" fill="#111827">{html.escape(title)}</text>'
        f'<text x="{x}" y="{y + 28}" font-size="15" fill="#4b5563">{html.escape(subtitle)}</text>'
    )


def badge(x: float, y: float, text: str, fill: str, text_fill: str = "#ffffff", stroke: str | None = None) -> str:
    width = max(106, int(len(text) * 7.2) + 24)
    stroke_attr = f' stroke="{stroke}" stroke-width="1"' if stroke else ""
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="28" rx="14" fill="{fill}"{stroke_attr}/>'
        f'<text x="{x + 12}" y="{y + 18}" font-size="13" font-weight="700" fill="{text_fill}">{html.escape(text)}</text>'
    )


def draw_overflow_x(x: float, y: float, color: str, size: float = 7) -> str:
    return (
        f'<line x1="{x - size}" y1="{y - size}" x2="{x + size}" y2="{y + size}" stroke="{color}" stroke-width="3" stroke-linecap="round"/>'
        f'<line x1="{x - size}" y1="{y + size}" x2="{x + size}" y2="{y - size}" stroke="{color}" stroke-width="3" stroke-linecap="round"/>'
    )


def first_overflow_size(rows: list[dict], algorithm_label: str, method: str = "Recursive") -> int | None:
    overflow_sizes = [
        row["input_size"]
        for row in rows
        if row["algorithm_label"] == algorithm_label
        and row["method"] == method
        and row["avg_time_ns"] < 0
    ]
    return min(overflow_sizes) if overflow_sizes else None


def largest_safe_size(rows: list[dict], algorithm_label: str, method: str = "Recursive") -> int | None:
    safe_sizes = [
        row["input_size"]
        for row in rows
        if row["algorithm_label"] == algorithm_label
        and row["method"] == method
        and row["avg_time_ns"] > 0
    ]
    return max(safe_sizes) if safe_sizes else None


def largest_shared_comparison(rows: list[dict], algorithm_label: str) -> tuple[int | None, float | None]:
    for size in reversed(INPUT_SIZES):
        recursive_row = row_lookup(rows, algorithm_label, "Recursive", size)
        iterative_row = row_lookup(rows, algorithm_label, "Iterative", size)
        if recursive_row and iterative_row and recursive_row["avg_time_ns"] > 0 and iterative_row["avg_time_ns"] > 0:
            return size, recursive_row["avg_time_ns"] / iterative_row["avg_time_ns"]
    return None, None


def ratio_label(ratio: float) -> str:
    if ratio >= 1:
        return f"{ratio:.2f}x slower"
    return f"{(1 / ratio):.2f}x faster"


def file_slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def make_individual_algorithm_svg(rows: list[dict], algorithm_label: str) -> Path:
    width = 1500
    height = 900
    panel_x = 70
    panel_y = 88
    panel_width = width - 140
    panel_height = height - 152
    plot_margin_left = 108
    plot_margin_right = 34
    plot_margin_top = 112
    plot_margin_bottom = 90
    plot_x = panel_x + plot_margin_left
    plot_y = panel_y + plot_margin_top
    plot_width = panel_width - plot_margin_left - plot_margin_right
    plot_height = panel_height - plot_margin_top - plot_margin_bottom

    algorithm_rows = rows_for_algorithm(rows, algorithm_label)
    positive_values = [row["avg_time_ns"] for row in algorithm_rows if row["avg_time_ns"] > 0]
    if not positive_values:
        raise ValueError(f"No positive benchmark values found for {algorithm_label}")

    overflow_at = first_overflow_size(rows, algorithm_label)
    compared_size, ratio = largest_shared_comparison(rows, algorithm_label)

    min_log = min(safe_log10(value) for value in positive_values)
    max_log = max(safe_log10(value) for value in positive_values)
    if math.isclose(min_log, max_log):
        min_log -= 0.5
        max_log += 0.5
    else:
        padding = (max_log - min_log) * 0.12
        min_log -= padding
        max_log += padding

    def x_pos(input_size: int) -> float:
        idx = INPUT_SIZES.index(input_size)
        if len(INPUT_SIZES) == 1:
            return plot_x + plot_width / 2
        return plot_x + idx * plot_width / (len(INPUT_SIZES) - 1)

    def y_pos(value: int) -> float:
        normalized = (safe_log10(value) - min_log) / (max_log - min_log)
        return plot_y + plot_height - normalized * plot_height

    pieces = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f8fafc"/>',
        f'<rect x="{panel_x}" y="{panel_y}" width="{panel_width}" height="{panel_height}" rx="30" fill="#ffffff" stroke="#dbe4ee" stroke-width="1.5"/>',
        f'<text x="{panel_x + 26}" y="{panel_y + 40}" font-size="34" font-weight="700" fill="#0f172a">{html.escape(algorithm_label)}</text>',
        badge(panel_x + 26, panel_y + 58, "Recursive", COLORS["Recursive"]),
        badge(panel_x + 154, panel_y + 58, "Iterative", COLORS["Iterative"]),
    ]

    if overflow_at is not None:
        pieces.append(badge(panel_x + 282, panel_y + 58, f"Recursive overflow at {input_label(overflow_at)}", "#fff7ed", text_fill="#9a3412", stroke="#fdba74"))
    else:
        pieces.append(badge(panel_x + 282, panel_y + 58, f"Recursive safe through {input_label(INPUT_SIZES[-1])}", "#ecfdf5", text_fill="#065f46", stroke="#86efac"))

    if ratio is not None and compared_size is not None:
        pieces.append(
            f'<text x="{panel_x + panel_width - 26}" y="{panel_y + 77}" text-anchor="end" font-size="18" fill="#475569">'
            f'At {input_label(compared_size)}: recursion is {html.escape(ratio_label(ratio))}</text>'
        )

    tick_min = math.floor(min_log)
    tick_max = math.ceil(max_log)
    for exponent in range(tick_min, tick_max + 1):
        tick_value = 10 ** exponent
        if exponent < -1:
            continue
        y = y_pos(tick_value)
        pieces.append(f'<line x1="{plot_x}" y1="{y}" x2="{plot_x + plot_width}" y2="{y}" stroke="#e2e8f0" stroke-width="1.2"/>')
        pieces.append(f'<text x="{plot_x - 16}" y="{y + 5}" text-anchor="end" font-size="16" fill="#64748b">{value_label(tick_value)}</text>')

    for size in INPUT_SIZES:
        x = x_pos(size)
        pieces.append(f'<line x1="{x}" y1="{plot_y}" x2="{x}" y2="{plot_y + plot_height}" stroke="#f1f5f9" stroke-width="1"/>')
        pieces.append(f'<text x="{x}" y="{plot_y + plot_height + 34}" text-anchor="middle" font-size="16" fill="#64748b">{input_label(size)}</text>')

    pieces.append(f'<line x1="{plot_x}" y1="{plot_y + plot_height}" x2="{plot_x + plot_width}" y2="{plot_y + plot_height}" stroke="#334155" stroke-width="2"/>')
    pieces.append(f'<line x1="{plot_x}" y1="{plot_y}" x2="{plot_x}" y2="{plot_y + plot_height}" stroke="#334155" stroke-width="2"/>')

    if overflow_at is not None:
        overflow_x = x_pos(overflow_at)
        pieces.append(
            f'<line x1="{overflow_x}" y1="{plot_y}" x2="{overflow_x}" y2="{plot_y + plot_height}" '
            f'stroke="#fb923c" stroke-width="2.5" stroke-dasharray="8 8" opacity="0.95"/>'
        )
        pieces.append(
            f'<text x="{overflow_x + 12}" y="{plot_y + 24}" font-size="16" font-weight="700" fill="#9a3412">'
            f'Overflow starts at {input_label(overflow_at)}</text>'
        )

    pieces.append(f'<text x="{plot_x + plot_width / 2}" y="{plot_y + plot_height + 68}" text-anchor="middle" font-size="18" fill="#334155">Input Size</text>')
    pieces.append(
        f'<text x="{plot_x - 78}" y="{plot_y + plot_height / 2}" text-anchor="middle" font-size="18" fill="#334155" '
        f'transform="rotate(-90 {plot_x - 78} {plot_y + plot_height / 2})">Average Runtime (ns, log scale)</text>'
    )

    for method in METHODS:
        method_rows = [row for row in algorithm_rows if row["method"] == method]
        ok_rows = [row for row in method_rows if row["avg_time_ns"] > 0]
        color = COLORS[method]
        points = [(x_pos(row["input_size"]), y_pos(row["avg_time_ns"])) for row in ok_rows]

        for start, end in pairwise(points):
            pieces.append(
                f'<line x1="{start[0]}" y1="{start[1]}" x2="{end[0]}" y2="{end[1]}" '
                f'stroke="{color}" stroke-width="5" stroke-linecap="round"/>'
            )

        for point_x, point_y in points:
            pieces.append(f'<circle cx="{point_x}" cy="{point_y}" r="7" fill="{color}" stroke="#ffffff" stroke-width="2.5"/>')

        if method == "Recursive":
            overflow_rows = [row for row in method_rows if row["avg_time_ns"] < 0]
            for overflow_row in overflow_rows:
                pieces.append(draw_overflow_x(x_pos(overflow_row["input_size"]), plot_y + 36, "#c2410c", size=11))

    pieces.append("</svg>")
    filename = f"poster_{file_slug(algorithm_label)}.svg"
    return write_svg(CHART_DIR / filename, "\n".join(pieces))


def generate_individual_algorithm_charts(rows: list[dict]) -> list[Path]:
    return [make_individual_algorithm_svg(rows, algorithm_label) for _, algorithm_label in ALGORITHMS]


def make_poster_runtime_svg(rows: list[dict]) -> Path:
    width = 1600
    height = 1120
    outer_margin_x = 70
    outer_margin_y = 132
    panel_gap_x = 46
    panel_gap_y = 52
    panel_width = (width - 2 * outer_margin_x - panel_gap_x) / 2
    panel_height = (height - outer_margin_y - 122 - panel_gap_y) / 2
    plot_margin_left = 80
    plot_margin_right = 28
    plot_margin_top = 74
    plot_margin_bottom = 64

    pieces = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f8fafc"/>',
        chart_title_block(
            "How Runtime Changes as Input Size Grows",
            "Main poster figure. Lower is better. The y-axis uses a log scale so all four algorithms can be read on the same page.",
            x=outer_margin_x,
            y=54,
        ),
        badge(width - 286, 42, "Recursive", COLORS["Recursive"]),
        badge(width - 158, 42, "Iterative", COLORS["Iterative"]),
        badge(width - 286, 78, "X = stack overflow", "#ffffff", text_fill="#991b1b", stroke="#fca5a5"),
    ]

    algorithm_labels = [label for _, label in ALGORITHMS]
    for index, algorithm_label in enumerate(algorithm_labels):
        col = index % 2
        row = index // 2
        panel_x = outer_margin_x + col * (panel_width + panel_gap_x)
        panel_y = outer_margin_y + row * (panel_height + panel_gap_y)
        plot_x = panel_x + plot_margin_left
        plot_y = panel_y + plot_margin_top
        plot_width = panel_width - plot_margin_left - plot_margin_right
        plot_height = panel_height - plot_margin_top - plot_margin_bottom

        pieces.append(
            f'<rect x="{panel_x}" y="{panel_y}" width="{panel_width}" height="{panel_height}" rx="24" fill="#ffffff" stroke="#dbe4ee" stroke-width="1.5"/>'
        )
        pieces.append(f'<text x="{panel_x + 22}" y="{panel_y + 30}" font-size="22" font-weight="700" fill="#0f172a">{html.escape(algorithm_label)}</text>')

        overflow_at = first_overflow_size(rows, algorithm_label)
        largest_safe = largest_safe_size(rows, algorithm_label)
        compared_size, ratio = largest_shared_comparison(rows, algorithm_label)

        if overflow_at is not None:
            pieces.append(badge(panel_x + 22, panel_y + 42, f"Recursive overflow at {input_label(overflow_at)}", "#fff7ed", text_fill="#9a3412", stroke="#fdba74"))
        else:
            pieces.append(badge(panel_x + 22, panel_y + 42, f"Recursive safe through {input_label(INPUT_SIZES[-1])}", "#ecfdf5", text_fill="#065f46", stroke="#86efac"))

        if ratio is not None and compared_size is not None:
            pieces.append(
                f'<text x="{panel_x + panel_width - 22}" y="{panel_y + 60}" text-anchor="end" font-size="13" fill="#475569">'
                f'At {input_label(compared_size)}: recursion is {html.escape(ratio_label(ratio))}</text>'
            )

        algorithm_rows = rows_for_algorithm(rows, algorithm_label)
        positive_values = [row["avg_time_ns"] for row in algorithm_rows if row["avg_time_ns"] > 0]
        if not positive_values:
            continue

        min_log = min(safe_log10(value) for value in positive_values)
        max_log = max(safe_log10(value) for value in positive_values)
        if math.isclose(min_log, max_log):
            min_log -= 0.5
            max_log += 0.5
        else:
            padding = (max_log - min_log) * 0.12
            min_log -= padding
            max_log += padding

        def x_pos(input_size: int) -> float:
            idx = INPUT_SIZES.index(input_size)
            if len(INPUT_SIZES) == 1:
                return plot_x + plot_width / 2
            return plot_x + idx * plot_width / (len(INPUT_SIZES) - 1)

        def y_pos(value: int) -> float:
            normalized = (safe_log10(value) - min_log) / (max_log - min_log)
            return plot_y + plot_height - normalized * plot_height

        tick_min = math.floor(min_log)
        tick_max = math.ceil(max_log)
        for exponent in range(tick_min, tick_max + 1):
            tick_value = 10 ** exponent
            if exponent < -1:
                continue
            y = y_pos(tick_value)
            pieces.append(f'<line x1="{plot_x}" y1="{y}" x2="{plot_x + plot_width}" y2="{y}" stroke="#e2e8f0" stroke-width="1"/>')
            pieces.append(f'<text x="{plot_x - 14}" y="{y + 5}" text-anchor="end" font-size="12" fill="#64748b">{value_label(tick_value)}</text>')

        for size in INPUT_SIZES:
            x = x_pos(size)
            pieces.append(f'<line x1="{x}" y1="{plot_y}" x2="{x}" y2="{plot_y + plot_height}" stroke="#f1f5f9" stroke-width="1"/>')
            pieces.append(f'<text x="{x}" y="{plot_y + plot_height + 26}" text-anchor="middle" font-size="12" fill="#64748b">{input_label(size)}</text>')

        pieces.append(f'<line x1="{plot_x}" y1="{plot_y + plot_height}" x2="{plot_x + plot_width}" y2="{plot_y + plot_height}" stroke="#334155" stroke-width="1.6"/>')
        pieces.append(f'<line x1="{plot_x}" y1="{plot_y}" x2="{plot_x}" y2="{plot_y + plot_height}" stroke="#334155" stroke-width="1.6"/>')

        if overflow_at is not None:
            overflow_x = x_pos(overflow_at)
            pieces.append(
                f'<line x1="{overflow_x}" y1="{plot_y}" x2="{overflow_x}" y2="{plot_y + plot_height}" '
                f'stroke="#fb923c" stroke-width="2" stroke-dasharray="7 7" opacity="0.9"/>'
            )
            pieces.append(
                f'<text x="{overflow_x + 10}" y="{plot_y + 18}" font-size="12" font-weight="700" fill="#9a3412">'
                f'Overflow starts at {input_label(overflow_at)}</text>'
            )

        pieces.append(f'<text x="{plot_x + plot_width / 2}" y="{plot_y + plot_height + 50}" text-anchor="middle" font-size="13" fill="#334155">Input Size</text>')
        pieces.append(
            f'<text x="{plot_x - 58}" y="{plot_y + plot_height / 2}" text-anchor="middle" font-size="13" fill="#334155" '
            f'transform="rotate(-90 {plot_x - 58} {plot_y + plot_height / 2})">Average Runtime (ns, log scale)</text>'
        )

        for method in METHODS:
            method_rows = [row for row in algorithm_rows if row["method"] == method]
            ok_rows = [row for row in method_rows if row["avg_time_ns"] > 0]
            color = COLORS[method]
            points = [(x_pos(row["input_size"]), y_pos(row["avg_time_ns"])) for row in ok_rows]

            for start, end in pairwise(points):
                pieces.append(
                    f'<line x1="{start[0]}" y1="{start[1]}" x2="{end[0]}" y2="{end[1]}" '
                    f'stroke="{color}" stroke-width="4" stroke-linecap="round"/>'
                )

            for point_x, point_y in points:
                pieces.append(f'<circle cx="{point_x}" cy="{point_y}" r="5" fill="{color}" stroke="#ffffff" stroke-width="2"/>')

            if method == "Recursive":
                overflow_rows = [row for row in method_rows if row["avg_time_ns"] < 0]
                for overflow_row in overflow_rows:
                    pieces.append(draw_overflow_x(x_pos(overflow_row["input_size"]), plot_y + 26, "#c2410c"))

    pieces.append(
        f'<text x="{outer_margin_x}" y="{height - 28}" font-size="13" fill="#475569">'
        f'10-run averages. Java 17. Recursive Fibonacci and recursive Factorial both fail by {input_label(50000)} because of stack depth, while Binary Search and Fast Exponentiation remain stable through {input_label(100000)}.</text>'
    )
    pieces.append("</svg>")
    return write_svg(CHART_DIR / "poster_main_runtime.svg", "\n".join(pieces))


def make_poster_recursion_cliff_svg(rows: list[dict]) -> Path:
    width = 1500
    height = 760
    margin_left = 250
    margin_right = 90
    margin_top = 140
    margin_bottom = 100
    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom
    row_height = plot_height / len(ALGORITHMS)

    pieces = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#fffdf8"/>',
        chart_title_block(
            "Where Recursion Stops Scaling",
            "Poster figure for the recursion cliff. Each row tracks the recursive version only: solid line = completed safely, X = first stack overflow.",
            x=70,
            y=58,
        ),
        badge(width - 344, 48, "safe recursive range", "#ffedd5", text_fill="#9a3412", stroke="#fdba74"),
        badge(width - 182, 48, "X = first overflow", "#ffffff", text_fill="#991b1b", stroke="#fca5a5"),
    ]

    plot_x = margin_left
    plot_y = margin_top
    pieces.append(f'<line x1="{plot_x}" y1="{plot_y + plot_height}" x2="{plot_x + plot_width}" y2="{plot_y + plot_height}" stroke="#334155" stroke-width="1.6"/>')

    for size in INPUT_SIZES:
        x = plot_x + (size / INPUT_SIZES[-1]) * plot_width
        pieces.append(f'<line x1="{x}" y1="{plot_y - 8}" x2="{x}" y2="{plot_y + plot_height}" stroke="#e5e7eb" stroke-width="1"/>')
        pieces.append(f'<text x="{x}" y="{plot_y + plot_height + 30}" text-anchor="middle" font-size="13" fill="#64748b">{input_label(size)}</text>')

    for index, (_, algorithm_label) in enumerate(ALGORITHMS):
        y_center = plot_y + row_height * index + row_height / 2
        track_y = y_center + 2
        pieces.append(f'<text x="{plot_x - 22}" y="{y_center + 5}" text-anchor="end" font-size="19" font-weight="700" fill="#0f172a">{html.escape(algorithm_label)}</text>')
        pieces.append(f'<line x1="{plot_x}" y1="{track_y}" x2="{plot_x + plot_width}" y2="{track_y}" stroke="#e2e8f0" stroke-width="8" stroke-linecap="round"/>')

        safe_through = largest_safe_size(rows, algorithm_label) or 0
        overflow_at = first_overflow_size(rows, algorithm_label)
        safe_x_end = plot_x + (safe_through / INPUT_SIZES[-1]) * plot_width if safe_through else plot_x
        pieces.append(f'<line x1="{plot_x}" y1="{track_y}" x2="{safe_x_end}" y2="{track_y}" stroke="#ea580c" stroke-width="14" stroke-linecap="round"/>')

        if overflow_at is not None:
            overflow_x = plot_x + (overflow_at / INPUT_SIZES[-1]) * plot_width
            pieces.append(draw_overflow_x(overflow_x, track_y, "#b91c1c", size=10))
            pieces.append(
                f'<text x="{overflow_x + 16}" y="{track_y - 8}" font-size="14" font-weight="700" fill="#9a3412">'
                f'overflow at {input_label(overflow_at)}</text>'
            )
            pieces.append(
                f'<text x="{overflow_x + 16}" y="{track_y + 16}" font-size="13" fill="#64748b">'
                f'largest safe input: {input_label(safe_through)}</text>'
            )
        else:
            pieces.append(f'<circle cx="{safe_x_end}" cy="{track_y}" r="8" fill="#059669" stroke="#ffffff" stroke-width="2"/>')
            pieces.append(
                f'<text x="{safe_x_end + 16}" y="{track_y + 5}" font-size="14" font-weight="700" fill="#065f46">'
                f'no overflow observed through {input_label(INPUT_SIZES[-1])}</text>'
            )

    pieces.append(f'<text x="{plot_x + plot_width / 2}" y="{height - 36}" text-anchor="middle" font-size="14" fill="#334155">Tested Input Size</text>')
    pieces.append("</svg>")
    return write_svg(CHART_DIR / "poster_recursion_cliff.svg", "\n".join(pieces))


def make_poster_speedup_svg(rows: list[dict]) -> Path:
    width = 1500
    height = 780
    margin_left = 260
    margin_right = 180
    margin_top = 150
    margin_bottom = 90
    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom

    comparisons = []
    for _, algorithm_label in ALGORITHMS:
        compared_size, ratio = largest_shared_comparison(rows, algorithm_label)
        if compared_size is not None and ratio is not None:
            comparisons.append((algorithm_label, compared_size, ratio))

    x_min = 0.0
    x_max = max(3.2, max((ratio for _, _, ratio in comparisons), default=1.0) + 0.4)
    baseline_x = margin_left + ((1 - x_min) / (x_max - x_min)) * plot_width
    row_height = plot_height / len(comparisons) if comparisons else plot_height

    def x_pos(value: float) -> float:
        return margin_left + ((value - x_min) / (x_max - x_min)) * plot_width

    pieces = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f8fafc"/>',
        chart_title_block(
            "How Much Slower or Faster Was Recursion?",
            "Summary chart. Values are recursive time divided by iterative time at the largest input where both methods completed.",
            x=70,
            y=58,
        ),
        badge(width - 368, 48, "right of 1.0 = recursion slower", "#eff6ff", text_fill="#1d4ed8", stroke="#93c5fd"),
        badge(width - 176, 48, "left of 1.0 = recursion faster", "#ecfdf5", text_fill="#047857", stroke="#86efac"),
    ]

    tick_values = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    for tick in tick_values:
        if tick > x_max:
            continue
        x = x_pos(tick)
        stroke = "#94a3b8" if math.isclose(tick, 1.0) else "#e2e8f0"
        stroke_width = 2.5 if math.isclose(tick, 1.0) else 1
        pieces.append(f'<line x1="{x}" y1="{margin_top - 8}" x2="{x}" y2="{margin_top + plot_height}" stroke="{stroke}" stroke-width="{stroke_width}"/>')
        label = "1.0x" if math.isclose(tick, 1.0) else f"{tick:.1f}x"
        pieces.append(f'<text x="{x}" y="{margin_top + plot_height + 30}" text-anchor="middle" font-size="13" fill="#64748b">{label}</text>')

    for index, (algorithm_label, compared_size, ratio) in enumerate(comparisons):
        y_center = margin_top + row_height * index + row_height / 2
        bar_height = min(50, row_height * 0.42)
        start_x = min(baseline_x, x_pos(ratio))
        bar_width = abs(x_pos(ratio) - baseline_x)
        bar_fill = "#ea580c" if ratio >= 1 else "#0f766e"
        value_x = x_pos(ratio)

        pieces.append(f'<text x="{margin_left - 22}" y="{y_center + 5}" text-anchor="end" font-size="20" font-weight="700" fill="#0f172a">{html.escape(algorithm_label)}</text>')
        pieces.append(f'<rect x="{start_x}" y="{y_center - bar_height / 2}" width="{max(bar_width, 6)}" height="{bar_height}" rx="16" fill="{bar_fill}"/>')
        pieces.append(f'<circle cx="{value_x}" cy="{y_center}" r="8" fill="{bar_fill}" stroke="#ffffff" stroke-width="2"/>')

        if ratio >= 1:
            summary = f"{ratio:.2f}x slower"
            details = f"iteration wins at {input_label(compared_size)}"
            label_x = min(value_x + 16, width - margin_right + 30)
            anchor = "start"
        else:
            summary = f"{(1 / ratio):.2f}x faster"
            details = f"recursion edges out iteration at {input_label(compared_size)}"
            label_x = max(value_x - 16, 110)
            anchor = "end"

        pieces.append(f'<text x="{label_x}" y="{y_center - 6}" text-anchor="{anchor}" font-size="15" font-weight="700" fill="#111827">{html.escape(summary)}</text>')
        pieces.append(f'<text x="{label_x}" y="{y_center + 14}" text-anchor="{anchor}" font-size="13" fill="#64748b">{html.escape(details)}</text>')

    pieces.append(f'<line x1="{baseline_x}" y1="{margin_top - 10}" x2="{baseline_x}" y2="{margin_top + plot_height}" stroke="#475569" stroke-width="2.5"/>')
    pieces.append(f'<text x="{baseline_x}" y="{margin_top - 20}" text-anchor="middle" font-size="13" font-weight="700" fill="#334155">1.0x parity</text>')
    pieces.append(f'<text x="{margin_left + plot_width / 2}" y="{height - 34}" text-anchor="middle" font-size="14" fill="#334155">Recursive Runtime / Iterative Runtime</text>')
    pieces.append("</svg>")
    return write_svg(CHART_DIR / "poster_speedup_summary.svg", "\n".join(pieces))


def generate_charts(rows: list[dict]) -> list[Path]:
    return [
        make_poster_runtime_svg(rows),
        make_poster_recursion_cliff_svg(rows),
        make_poster_speedup_svg(rows),
    ]


def run_pipeline(num_runs: int = 10, timeout_seconds: int = 600) -> dict:
    rows = run_all_benchmarks(num_runs=num_runs, timeout_seconds=timeout_seconds)
    chart_paths = generate_charts(rows)
    return {
        "rows": rows,
        "csv_path": CSV_PATH,
        "chart_paths": chart_paths,
    }


def main(argv: list[str]) -> int:
    num_runs = int(argv[1]) if len(argv) > 1 else 10
    timeout_seconds = int(argv[2]) if len(argv) > 2 else 600
    result = run_pipeline(num_runs=num_runs, timeout_seconds=timeout_seconds)
    print(f"Saved benchmark CSV to {result['csv_path']}")
    for chart_path in result["chart_paths"]:
        print(f"Generated chart: {chart_path}")
    print()
    print(summary_markdown(result["rows"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
