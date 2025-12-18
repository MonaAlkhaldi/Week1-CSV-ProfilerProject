def basic_profile(rows: list[dict[str, str]]) -> dict:
    cols = get_columns(rows)
    report = {
        "summary": {
            "rows": len(rows),
            "columns": len(cols),
            "column_names": cols,
        },
        "columns": {},
    }

    for col in cols:
        values = column_values(rows, col)
        typ = infer_type(values)

        if typ == "number":
            stats = numeric_stats(values)
        else:
            stats = text_stats(values)

        report["columns"][col] = {"type": typ, **stats}

    return report

def get_columns(rows: list[dict[str, str]]) -> list[str]:
    if not rows:
        return []
    return list(rows[0].keys())

Mess=["" , "na" , "n/a", "null", "none", "nan"] #These are the things that i consider empty null --> false
def is_missing(value : str | None)-> bool:
    if value is None: #if its none it mean that it is not empty 
        return True
    return value.strip().casefold() in Mess #It is importent to clean the string si we can make sure if it is empty or not EX: " na " =! "na" 


def try_float(value: str) -> float | None: #We expect the value to be a string and we wnat to convert this value into float in not posible then it becoume None
    #First we want to convert to float
    try:
        return float(value)
    except ValueError:
        return None

def infer_type(values: list[str]) -> str:
    usable = [v for v in values if not is_missing(v)]
    if not usable:
        return "text"
    for v in usable:
        if try_float(v) is None:
            return "text"
    return "number"

def column_values(rows: list[dict[str, str]], col: str) -> list[str]:
    return [row.get(col, "") for row in rows]

def numeric_stats(values: list[str]) -> dict:
    use = []
    missing = 0

    for v in values:
        if is_missing(v):
            missing += 1
        else:
            use.append(v)

    num = []
    for v in use:
        x = try_float(v)
        if x is not None:
            num.append(x)

    count = len(num)
    unique = len(set(num))

    if count == 0:
        min_val = None
        max_val = None
        mean_val = None
    else:
        min_val = min(num)
        max_val = max(num)
        mean_val = sum(num) / count

    return {
        "count": count,
        "missing": missing,
        "unique": unique,
        "min": min_val,
        "max": max_val,
        "mean": mean_val,
    }


def text_stats(values: list[str], top_k: int = 5) -> dict:
    usable = [v for v in values if not is_missing(v)]
    missing = len(values) - len(usable)

    counts: dict[str, int] = {}
    for v in usable:
        counts[v] = counts.get(v, 0) + 1

    top_items = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:top_k]
    top = [{"value": v, "count": c} for v, c in top_items]

    return {
        "count": len(usable),
        "missing": missing,
        "unique": len(counts),
        "top": top,
    }










    










            
        
     

  


 