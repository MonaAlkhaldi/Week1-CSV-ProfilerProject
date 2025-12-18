import csv
import json
from io import StringIO
from pathlib import Path

import streamlit as st

from csv_profiler.profile import basic_profile
from csv_profiler.render import render_markdown


st.set_page_config(page_title="CSV Profiler", layout="wide")
st.title("CSV Profiler")
st.caption("Upload CSV → profile → export JSON + Markdown")


st.sidebar.header("Inputs")
show_preview = st.sidebar.checkbox("Show preview", value=True)
report_name = st.sidebar.text_input("Report name", value="report")


uploaded = st.file_uploader("Upload a CSV", type=["csv"])
rows = None

if uploaded is not None:
    text = uploaded.getvalue().decode("utf-8-sig")
    rows = list(csv.DictReader(StringIO(text)))

    if not rows:
        st.error("CSV has no data rows.")
        st.stop()

    if show_preview:
        st.subheader("Preview")
        st.write(rows[:5])
else:
    st.info("Upload a CSV to begin.")


generate_disabled = rows is None
if st.button("Generate report", disabled=generate_disabled):
    st.session_state["report"] = basic_profile(rows)


report = st.session_state.get("report")

if report is not None:
    summary = report.get("summary", {}) or {}
    n_rows = int(summary.get("rows", 0) or 0)
    n_cols = int(summary.get("columns", 0) or 0)

    c1, c2 = st.columns(2)
    c1.metric("Rows", n_rows)
    c2.metric("Columns", n_cols)

    st.subheader("Columns")

    cols_dict = report.get("columns", {}) or {}
    table_rows = []

    if isinstance(cols_dict, dict):
        for col_name, info in cols_dict.items():
            info = info or {}
            missing = int(info.get("missing", 0) or 0)
            unique = int(info.get("unique", 0) or 0)
            typ = info.get("type", "")

            missing_pct = (missing / n_rows * 100) if n_rows else 0.0

            row = {
                "column": col_name,
                "type": typ,
                "count": int(info.get("count", 0) or 0),
                "missing": missing,
                "missing_pct": round(missing_pct, 1),
                "unique": unique,
            }

            if typ == "number":
                row["min"] = info.get("min", None)
                row["max"] = info.get("max", None)
                row["mean"] = info.get("mean", None)

            table_rows.append(row)

    if table_rows:
        st.dataframe(table_rows, use_container_width=True)
    else:
        st.warning("No column statistics found in report['columns'].")

    with st.expander("Markdown preview"):
        st.markdown(render_markdown(report))

    json_text = json.dumps(report, indent=2, ensure_ascii=False)
    md_text = render_markdown(report)

    col1, col2 = st.columns(2)
    col1.download_button(
        "Download JSON",
        data=json_text,
        file_name=f"{report_name}.json",
        mime="application/json",
    )
    col2.download_button(
        "Download Markdown",
        data=md_text,
        file_name=f"{report_name}.md",
        mime="text/markdown",
    )

    
    if st.button("Save to outputs/"):
        out_dir = Path("outputs")
        out_dir.mkdir(exist_ok=True)

        (out_dir / f"{report_name}.json").write_text(json_text, encoding="utf-8")
        (out_dir / f"{report_name}.md").write_text(md_text, encoding="utf-8")

        st.success("Saved to outputs/")




    
