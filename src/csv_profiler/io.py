from pathlib import Path
import csv

def read_csv_rows(path: str | Path) -> list[dict[str, str]]:
    path = Path(path)  

    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        raise ValueError("CSV has no data rows")

    return rows
    







            
