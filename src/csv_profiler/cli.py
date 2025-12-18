import json
import typer
from pathlib import Path

from csv_profiler.io import read_csv_rows
from csv_profiler.profile import basic_profile
from csv_profiler.render import write_markdown

app = typer.Typer()

@app.command(help="Profile a CSV file and write JSON + Markdown")
def profiler(
    input_path: Path = typer.Argument(..., help="Input CSV file"),
    out_dir: Path = typer.Option(Path("outputs"), "--out-dir", help="Output folder"),
    report_name: str = typer.Option("report", "--report-name", help="Base name for outputs"),
    preview: bool = typer.Option(False, "--preview", help="Print a short summary"),
):
    # 1️⃣ Read CSV
    rows = read_csv_rows(input_path)

    # 2️⃣ Profile
    report = basic_profile(rows)

    # 3️⃣ Ensure output directory exists
    out_dir.mkdir(parents=True, exist_ok=True)

    # 4️⃣ Write JSON
    json_path = out_dir / f"{report_name}.json"
    json_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    # 5️⃣ Write Markdown
    md_path = out_dir / f"{report_name}.md"
    write_markdown(report, md_path)

    
    if preview:
        summary = report["summary"]
        typer.echo(f"Rows: {summary['rows']} | Cols: {summary['columns']}")

if __name__ == "__main__":
    app()




   