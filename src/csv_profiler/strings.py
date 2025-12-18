def slugify(text: str) -> str:
    """Turn 'Report Name' → 'report-name'."""
    cleaned = ""
    for ch in text:
        if not ch.isdigit():
            cleaned += ch

    return cleaned.strip().lower().replace(" ", "-") 

    

    