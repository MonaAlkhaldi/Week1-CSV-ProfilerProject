from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime


def write_json(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def md_header(source: str) -> list[str]:
    ts = datetime.now().isoformat(timespec="seconds")
    return [
        "# CSV Profiling Report",
        "",
        f"- **Source:** `{source}`",
        f"- **Generated:** `{ts}`",
        "",
    ]

def md_table_header() -> list[str]:
    return [
        "| Column | Type | Missing | Unique |",
        "|---|---:|---:|---:|",
    ]

def md_col_row(name: str, typ: str, missing: int, missing_pct: float, unique: int) -> str:
    return f"| `{name}` | {typ} | {missing} ({missing_pct:.1%}) | {unique} |"


def write_markdown(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    rows = report["summary"]["rows"]

    lines: list[str] = []
    lines.extend(md_header("data/sample.csv"))

    lines.append("## Summary")
    lines.append(f"- Rows: {rows:,}")
    lines.append(f"- Columns: {report['summary']['columns']:,}")
    lines.append("")

    lines.append("## Columns (table)")
    lines.extend(md_table_header())

    for name, col in report["columns"].items():
        missing_pct = (col["missing"] / rows) if rows else 0.0
        lines.append(md_col_row(name, col["type"], col["missing"], missing_pct, col["unique"]))

    lines.append("")
    lines.append("## Column details")

    for name, col in report["columns"].items():
        lines.append(f"### `{name}` ({col['type']})")

        if col["type"] == "number":
            lines.append(f"- min: {col['min']}")
            lines.append(f"- max: {col['max']}")
            lines.append(f"- mean: {col['mean']}")
        else:
            top = col.get("top", [])
            if not top:
                lines.append("- (no non-missing values)")
            else:
                lines.append("- top values:")
                for item in top:
                    lines.append(f"  - `{item['value']}`: {item['count']}")

        lines.append("")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")





def render_markdown(report: dict) -> str:
    lines: list[str] = []

    lines.append("# CSV Profiling Report\n")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}\n")

    summary = report.get("summary", {})
    n_rows = summary.get("rows", 0)
    n_cols = summary.get("columns", 0)

    lines.append("## Summary\n")
    lines.append(f"- Rows: **{n_rows}**")
    lines.append(f"- Columns: **{n_cols}**\n")

    lines.append("## Columns\n")

    cols = report.get("columns", {})

    if isinstance(cols, dict):
        for name, info in cols.items():
            lines.append(f"### {name}")
            lines.append(f"- {info}\n")
    else:
        lines.append("| name | type | missing | missing_pct | unique |")
        lines.append("|---|---:|---:|---:|---:|")
        for c in cols:
            lines.append(
                f"| {c.get('name','')} | {c.get('type','')} | {c.get('missing',0)} | "
                f"{float(c.get('missing_pct',0)):.1f}% | {c.get('unique',0)} |"
            )

    
    lines.append("\n## Notes\n")
    lines.append("- Missing values are: `''`, `na`, `n/a`, `null`, `none`, `nan` (case-insensitive)")

    return "\n".join(lines)
